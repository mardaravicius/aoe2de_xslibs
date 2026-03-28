import ast
import inspect
import re
import textwrap
from collections.abc import Iterable
from dataclasses import dataclass
from ast import FunctionDef, Constant, Name, expr, arg, Expr, AnnAssign, Call, Assign, BinOp, Add, Sub, Mod, Mult, Div, \
    If, Compare, Eq, Gt, GtE, Lt, LtE, NotEq, For, While, AugAssign, Match, MatchValue, MatchAs, Return, Pass, \
    Subscript, stmt, Attribute, keyword, With, Tuple, UnaryOp, USub, JoinedStr, FormattedValue, Global, BoolOp, Or, And, \
    Not, FloorDiv, List, Import, ImportFrom, operator, cmpop, boolop
from types import ModuleType
from typing import Any, Callable, Optional

from xs_converter.context import XsContext
from xs_converter.exceptions import XsConversionError
from xs_converter.macro import macro_pass_value, macro_repeat


@dataclass(frozen=True)
class RenderedStatement:
    text: str
    is_function: bool = False


@dataclass(frozen=True)
class RenderedExpression:
    value: str
    prelude: str = ""


class PythonToXsConverter:
    _macro_functions = {
        macro_pass_value.__name__,
    }
    _macro_repeat_functions = {
        macro_repeat.__name__,
    }

    _TYPE_MAP = {
        "int": "int",
        "int32": "int",
        "float": "float",
        "float32": "float",
        "bool": "bool",
        "str": "string",
        "XsVector": "vector",
    }

    _MODIFIER_MAP = {
        "XsStatic": "static",
        "XsConst": "const",
        "XsExtern": "extern",
        "XsExternConst": "extern const",
    }

    _OPERATOR_MAP = {
        Add: "+",
        Sub: "-",
        Mult: "*",
        Div: "/",
        FloorDiv: "/",
        Mod: "%",
        Eq: "==",
        NotEq: "!=",
        Gt: ">",
        GtE: ">=",
        Lt: "<",
        LtE: "<=",
        Or: "||",
        And: "&&",
    }

    _NUMERIC_CAST_ZEROS = {
        "float": "0.0",
        "float32": "0.0",
        "int": "0",
        "int32": "0",
    }

    _ARRAY_CREATE_MAP = {
        "int": "xsArrayCreateInt",
        "int32": "xsArrayCreateInt",
        "float": "xsArrayCreateFloat",
        "float32": "xsArrayCreateFloat",
        "bool": "xsArrayCreateBool",
        "str": "xsArrayCreateString",
        "XsVector": "xsArrayCreateVector",
    }

    _ARRAY_SET_MAP = {
        "int": "xsArraySetInt",
        "int32": "xsArraySetInt",
        "float": "xsArraySetFloat",
        "float32": "xsArraySetFloat",
        "bool": "xsArraySetBool",
        "str": "xsArraySetString",
        "XsVector": "xsArraySetVector",
    }

    _ARRAY_GET_MAP = {
        "int": "xsArrayGetInt",
        "int32": "xsArrayGetInt",
        "float": "xsArrayGetFloat",
        "float32": "xsArrayGetFloat",
        "bool": "xsArrayGetBool",
        "str": "xsArrayGetString",
        "XsVector": "xsArrayGetVector",
    }

    _ARRAY_ZERO_XS: dict[str, str] = {
        "int": "0",
        "int32": "0",
        "float": "0.0",
        "float32": "0.0",
        "bool": "false",
        "str": '""',
    }

    _ARRAY_LIST_NAMES = {"list", "List"}

    def __init__(self, indent: bool, bindings: dict[str, Any]):
        if indent:
            self.sp = " "
            self.nl = "\n"
            self.indent = " " * 4
        else:
            self.sp = ""
            self.nl = ""
            self.indent = ""
        self._vars = bindings
        self._doc_strings = set()
        self._temp_counter = 0
        self._source: Optional[str] = None
        self._source_name: Optional[str] = None
        self._source_line_offset = 0
        self._source_column_offset = 0
        self._display_source_lines: list[str] = []

    @staticmethod
    def to_xs_script(*functions: Callable[..., Any], indent: bool, **kwargs: Any) -> str:
        parts = []
        nl = "\n" if indent else ""
        for f in functions:
            converter = PythonToXsConverter(indent, kwargs)
            result = converter._to_xs_function(f)
            if result:
                parts.append(result)
        return nl.join(parts)

    @staticmethod
    def to_xs_file(module: ModuleType, indent: bool, **kwargs) -> str:
        converter = PythonToXsConverter(indent, kwargs)
        source_name = inspect.getsourcefile(module) or getattr(module, "__file__", None)
        source_lines, start_line = converter._read_source_lines(module, source_name)
        source = "".join(source_lines)
        module_ast = converter._parse_source(source, source_name)

        converter._set_source_context(
            source,
            source_name=source_name,
            line_offset=max(start_line - 1, 0),
            display_source_lines=source.splitlines(),
        )
        ctx = XsContext()
        parts: list[tuple[bool, str]] = []
        for node in module_ast.body:
            if isinstance(node, (Import, ImportFrom)):
                continue
            try:
                rendered = converter._render_module_statement(node, ctx)
            except Exception as exc:
                converter._raise_as_conversion_error(exc, node)
            if not rendered.text:
                continue
            parts.append((rendered.is_function, rendered.text))
        return converter._format_parts(parts)

    def to_xs_function_definition(self, function: FunctionDef, ctx: XsContext) -> str:
        try:
            if self._has_xs_ignore(function):
                return ""
            xs_type = self._to_xs_function_type(function.returns)
            name = self._to_camel_case(function.name)

            if len(function.args.args) != len(function.args.defaults):
                raise self._error("All function arguments must have a default value.", function.args)

            parameters_xs = self._to_xs_parameters(function, ctx)
            has_parameters = len(parameters_xs) > 0

            rule_modifier_xs = self._to_xs_rule_modifiers(function, has_parameters, xs_type)
            has_rules = len(rule_modifier_xs) > 0
            xs = ""
            doc = ast.get_docstring(function)
            if doc is not None:
                self._doc_strings.add(doc.replace("\n", "").replace(" ", ""))
            if doc is not None and len(self.indent) > 0:
                doc = re.sub(r'`([a-zA-Z_][a-zA-Z0-9_]*)`',
                             lambda m: '`' + self._to_camel_case(m.group(1)) + '`', doc)
                doc = doc.replace(":param", "@param")
                doc = doc.replace(":return:", "@return")
                doc = doc.replace(":", " -")
                doc = doc.replace("\n", f"\n{(ctx.depth + 1) * self.indent}")
                xs += f"{ctx.depth * self.indent}/*\n{(ctx.depth + 1) * self.indent}"
                xs += doc + "\n"
                xs += f"{ctx.depth * self.indent}*/\n"
            if has_rules:
                header = f"rule {name} {rule_modifier_xs}"
            else:
                header = f"{xs_type} {name}({parameters_xs})"
            xs += self._block(ctx.depth, header, self._to_xs_body(function.body, ctx))
            return xs
        except Exception as exc:
            self._raise_as_conversion_error(exc, function)

    @staticmethod
    def _syntax_error(exc: SyntaxError, source_name: Optional[str]) -> XsConversionError:
        return XsConversionError(
            exc.msg,
            source_name=exc.filename or source_name,
            line=exc.lineno,
            column=exc.offset,
            source_line=exc.text.rstrip("\n") if exc.text is not None else None,
            end_column=exc.end_offset,
        )

    @staticmethod
    def _source_access_error(exc: Exception, source_name: Optional[str]) -> XsConversionError:
        return XsConversionError(
            f"Could not read Python source: {exc}",
            source_name=source_name,
        )

    def _read_source_lines(self, source_object: Any, source_name: Optional[str]) -> tuple[list[str], int]:
        try:
            return inspect.getsourcelines(source_object)
        except (OSError, TypeError):
            try:
                source = inspect.getsource(source_object)
            except (OSError, TypeError) as exc:
                raise self._source_access_error(exc, source_name) from exc
            return source.splitlines(keepends=True), 1

    def _parse_source(self, source: str, source_name: Optional[str]) -> ast.Module:
        try:
            return ast.parse(source, filename=source_name or "<unknown>")
        except SyntaxError as exc:
            raise self._syntax_error(exc, source_name) from exc

    def _set_source_context(
            self,
            parsed_source: str,
            *,
            source_name: Optional[str],
            line_offset: int = 0,
            column_offset: int = 0,
            display_source_lines: Optional[list[str]] = None,
    ) -> None:
        self._source = parsed_source
        self._source_name = source_name
        self._source_line_offset = line_offset
        self._source_column_offset = column_offset
        self._display_source_lines = display_source_lines or parsed_source.splitlines()

    def _error(self, message: str, node: Optional[ast.AST] = None) -> XsConversionError:
        if node is None:
            return XsConversionError(message, source_name=self._source_name)

        lineno = getattr(node, "lineno", None)
        col_offset = getattr(node, "col_offset", None)
        end_col_offset = getattr(node, "end_col_offset", None)

        line = None
        column = None
        end_column = None
        source_line = None

        if lineno is not None:
            line = lineno + self._source_line_offset
            if 0 < lineno <= len(self._display_source_lines):
                source_line = self._display_source_lines[lineno - 1]
        if col_offset is not None:
            column = col_offset + 1 + self._source_column_offset
        if end_col_offset is not None:
            end_column = end_col_offset + 1 + self._source_column_offset

        return XsConversionError(
            message,
            source_name=self._source_name,
            line=line,
            column=column,
            source_line=source_line,
            end_column=end_column,
        )

    def _build_source_start_error(self, message: str) -> XsConversionError:
        source_line = self._display_source_lines[0] if self._display_source_lines else None
        line = self._source_line_offset + 1 if (self._source_name is not None or source_line is not None) else None
        column = 1 if source_line is not None else None
        end_column = 1 if source_line is not None else None
        return XsConversionError(
            message,
            source_name=self._source_name,
            line=line,
            column=column,
            source_line=source_line,
            end_column=end_column,
        )

    def _enrich_conversion_error(self, exc: XsConversionError, node: Optional[ast.AST]) -> XsConversionError:
        if node is None:
            if exc.source_name is None and self._source_name is not None:
                return XsConversionError(
                    exc.message,
                    source_name=self._source_name,
                    line=exc.line,
                    column=exc.column,
                    source_line=exc.source_line,
                    end_column=exc.end_column,
                )
            return exc

        enriched = self._error(exc.message, node)
        return XsConversionError(
            exc.message,
            source_name=exc.source_name or enriched.source_name,
            line=exc.line if exc.line is not None else enriched.line,
            column=exc.column if exc.column is not None else enriched.column,
            source_line=exc.source_line or enriched.source_line,
            end_column=exc.end_column if exc.end_column is not None else enriched.end_column,
        )

    def _raise_as_conversion_error(self, exc: Exception, node: Optional[ast.AST]) -> None:
        if isinstance(exc, XsConversionError):
            raise self._enrich_conversion_error(exc, node) from exc
        message = str(exc) or exc.__class__.__name__
        raise self._error(message, node) from exc

    def _format_parts(self, parts: list[tuple[bool, str]]) -> str:
        result = ""
        for i, (is_func, text) in enumerate(parts):
            if i > 0:
                prev_is_func = parts[i - 1][0]
                if is_func or prev_is_func:
                    result += self.nl
            result += text
        return result

    @staticmethod
    def _combine_prelude(*expressions: RenderedExpression) -> str:
        return "".join(expression.prelude for expression in expressions)

    @staticmethod
    def _common_indent(lines: list[str]) -> int:
        indents = [len(line) - len(line.lstrip()) for line in lines if line.strip()]
        return min(indents, default=0)

    def _wrap_parens(self, xs: str, enclosed: bool) -> str:
        if enclosed:
            return xs
        return f"({xs})"

    def _stmt(self, depth: int, content: str) -> str:
        return f"{depth * self.indent}{content};{self.nl}"

    def _block(self, depth: int, header: str, body: str) -> str:
        return f"{depth * self.indent}{header}{self.sp}{{{self.nl}{body}{depth * self.indent}}}{self.nl}"

    def _require_inline_expression(self, rendered: RenderedExpression, node: Optional[ast.AST] = None) -> str:
        if rendered.prelude:
            raise self._error("This expression form is not supported in this position.", node)
        return rendered.value

    def _to_camel_case(self, s: str) -> str:
        prefix = ""
        while s.startswith("_"):
            prefix += "_"
            s = s[1:]
        suffix = ""
        while s.endswith("_"):
            suffix += "_"
            s = s[:-1]
        s = re.sub(r'(?<!_)_(?!_)([a-zA-Z0-9])', lambda m: m.group(1).upper(), s)
        return prefix + s + suffix

    def _next_temp_name(self) -> str:
        name = f"temp{self._temp_counter:08x}"
        self._temp_counter += 1
        return name

    @staticmethod
    def _has_xs_ignore(node: FunctionDef) -> bool:
        return any(
            (isinstance(d, Name) and d.id == "xs_ignore")
            for d in node.decorator_list
        )

    def _to_xs_parameters(self, function: FunctionDef, ctx: XsContext) -> str:
        parameters = [self._to_xs_arg(a, default, ctx) for a, default in
                      zip(function.args.args, function.args.defaults)]
        return f",{self.sp}".join(parameters)

    def _to_xs_rule_modifiers(self, function: FunctionDef, has_parameters: bool, xs_type: str) -> str:
        rule_decorator = [d for d in function.decorator_list if
                          isinstance(d, Call) and isinstance(d.func, Name) and d.func.id == "xs_rule"]
        is_rule = len(rule_decorator) > 0
        if is_rule and (has_parameters or xs_type != "void"):
            raise self._error("xs_rule functions cannot have parameters or return values.", rule_decorator[0])
        if not is_rule:
            return ""

        rule_decorator = rule_decorator[0]
        rule_settings = {
            "group": None,
            "active": False,
            "high_frequency": False,
            "run_immediately": False,
            "min_interval": None,
            "max_interval": None,
            "priority": None,
        }
        for kw in rule_decorator.keywords:
            if isinstance(kw, keyword) and isinstance(kw.value, Constant):
                rule_settings[kw.arg] = kw.value.value
            else:
                raise self._error(f"xs_rule only supports constant keyword arguments; got {kw}.", kw)
        modifiers = []
        if rule_settings.get("group") is not None:
            modifiers.append(f"group {rule_settings['group']}")
        if rule_settings.get("active"):
            modifiers.append("active")
        else:
            modifiers.append("inactive")
        if rule_settings.get("high_frequency"):
            if rule_settings.get("min_interval") is not None or rule_settings.get("max_interval") is not None:
                raise self._error("xs_rule cannot combine high_frequency with min_interval or max_interval.",
                                  rule_decorator)
            modifiers.append("highFrequency")
        if rule_settings.get("run_immediately"):
            modifiers.append("runImmediately")
        if rule_settings.get("min_interval") is not None:
            modifiers.append(f"minInterval {rule_settings['min_interval']}")
        if rule_settings.get("max_interval") is not None:
            modifiers.append(f"maxInterval {rule_settings['max_interval']}")
        if rule_settings.get("priority") is not None:
            modifiers.append(f"priority {rule_settings['priority']}")
        return " ".join(modifiers)

    def _to_xs_function(self, function: Callable[..., Any]) -> str:
        source_name = inspect.getsourcefile(function)
        source_lines, start_line = self._read_source_lines(function, source_name)

        original_source = "".join(source_lines)
        source = textwrap.dedent(original_source)
        self._set_source_context(
            source,
            source_name=source_name,
            line_offset=max(start_line - 1, 0),
            column_offset=self._common_indent(original_source.splitlines()),
            display_source_lines=original_source.splitlines(),
        )
        module_ast = self._parse_source(source, source_name)

        if len(module_ast.body) != 1 or not isinstance(module_ast.body[0], FunctionDef):
            if module_ast.body:
                raise self._error("Top-level source must contain a single function definition.", module_ast.body[0])
            raise self._build_source_start_error("Top-level source must contain a single function definition.")
        return self.to_xs_function_definition(module_ast.body[0], XsContext())

    def _to_xs_body(self, body: list[expr | stmt], ctx: XsContext) -> str:
        xs = ""
        for statement in body:
            try:
                stmt_xs = self._render_body_statement(statement, ctx)
            except Exception as exc:
                self._raise_as_conversion_error(exc, statement)
            xs += stmt_xs
        return xs

    def _to_xs_return(self, return_stmt: Return, ctx: XsContext) -> str:
        if return_stmt.value is None:
            return self._stmt(ctx.depth, "return")
        value_expr = self._render_expression(return_stmt.value, ctx, enclosed=True)
        return value_expr.prelude + self._stmt(ctx.depth, f"return{self.sp}({value_expr.value})")

    def _to_xs_type(self, annotation: expr) -> str:
        if not isinstance(annotation, Name):
            raise self._error("Type annotations must be simple type names.", annotation)

        python_type = annotation.id
        xs_type = self._TYPE_MAP.get(python_type)
        if xs_type is None:
            raise self._error(f"Python type {python_type!r} cannot be converted to an XS type.", annotation)
        return xs_type

    def _to_xs_modifier(self, python_type: str, node: Optional[ast.AST] = None) -> str:
        xs_mod = self._MODIFIER_MAP.get(python_type)
        if xs_mod is None:
            raise self._error(f"Python modifier {python_type!r} cannot be converted to an XS modifier.", node)
        return xs_mod

    def _to_xs_function_type(self, expression: expr) -> str:
        if isinstance(expression, Constant) and expression.value is None:
            return "void"
        if isinstance(expression, Name):
            return self._to_xs_type(expression)
        raise self._error("Function return annotations must be a type name or None.", expression)

    def _to_xs_arg(self, a: arg, default: Optional[expr], ctx: XsContext) -> str:
        name = self._to_camel_case(a.arg)
        type = self._to_xs_type(a.annotation)
        xs = f"{type} {name}"
        if default is not None:
            default_xs = self._require_inline_expression(self._render_expression(default, ctx), default)
            xs += f"{self.sp}={self.sp}{default_xs}"
        return xs

    def _parse_cast_call(self, node: expr) -> Optional[tuple[str, expr]]:
        if (isinstance(node, Call)
                and isinstance(node.func, Name)
                and node.func.id == "cast"
                and len(node.args) == 2
                and isinstance(node.args[0], Name)
                and node.args[0].id in self._ARRAY_CREATE_MAP):
            return node.args[0].id, node.args[1]
        return None

    def _infer_array_element_type(self, node: expr) -> str:
        if isinstance(node, Call) and isinstance(node.func, Name):
            func_name = node.func.id
            if func_name in self._ARRAY_CREATE_MAP:
                return func_name
            if func_name == "vector":
                return "XsVector"
        cast_info = self._parse_cast_call(node)
        if cast_info is not None:
            return cast_info[0]
        value = self._unpack_constant(node)
        if value is not None:
            if isinstance(value, bool):
                return "bool"
            if isinstance(value, int):
                return "int"
            if isinstance(value, float):
                return "float"
            if isinstance(value, str):
                return "str"
        raise self._error("Could not infer the array element type from this value.", node)

    def _render_array_create(self, element_type: str, default_node: expr, size_node: expr,
                             ctx: XsContext) -> RenderedExpression:
        create_func = self._ARRAY_CREATE_MAP.get(element_type)
        if create_func is None:
            raise self._error(f"Array creation does not support element type {element_type!r}.", default_node)

        size_expr = self._render_expression(size_node, ctx, enclosed=True)
        default_expr = self._render_expression(default_node, ctx, enclosed=True)

        zero_xs = self._ARRAY_ZERO_XS.get(element_type)
        if element_type == "XsVector":
            zero_xs = f"vector(0.0,{self.sp}0.0,{self.sp}0.0)"

        prelude = self._combine_prelude(size_expr, default_expr)
        if zero_xs is not None and default_expr.value == zero_xs:
            return RenderedExpression(f"{create_func}({size_expr.value})", prelude)
        return RenderedExpression(f"{create_func}({size_expr.value},{self.sp}{default_expr.value})", prelude)

    def _to_xs_array_create(self, element_type: str, default_node: expr, size_node: expr, ctx: XsContext) -> str:
        return self._render_array_create(element_type, default_node, size_node, ctx).value

    def _parse_array_literal(self, value: expr) -> tuple[expr, expr]:
        if isinstance(value, List):
            raise self._error("Array creation from list literals is not supported here; use [default] * size instead.", value)
        if not (isinstance(value, BinOp) and isinstance(value.op, Mult) and isinstance(value.left, List)):
            raise self._error("Arrays must be defined with [default_value] * size syntax.", value)

        list_node = value.left
        if len(list_node.elts) != 1:
            raise self._error("Array defaults must be a single-element list.", list_node)

        default_node = list_node.elts[0]
        if self._unpack_constant(default_node) is None and not isinstance(default_node, Call):
            raise self._error("Array default values must be literals or constructor calls.", default_node)
        return default_node, value.right

    def _annotation_element_type(self, annotation: expr) -> Optional[str]:
        if (isinstance(annotation, Subscript)
                and isinstance(annotation.value, Name)
                and annotation.value.id in self._ARRAY_LIST_NAMES
                and isinstance(annotation.slice, Name)
                and annotation.slice.id in self._ARRAY_CREATE_MAP):
            return annotation.slice.id
        return None

    def _infer_list_literal_type(self, elements: list[expr], node: Optional[ast.AST] = None) -> str:
        inferred = set()
        for elt in elements:
            try:
                t = self._infer_array_element_type(elt)
                inferred.add(t)
            except XsConversionError:
                continue
        error_node = node if node is not None else (elements[0] if elements else None)
        if not inferred:
            raise self._error(
                "Could not infer the array type from this list literal: "
                "at least one element must be a constant or typed cast.",
                error_node,
            )
        create_funcs = {self._ARRAY_CREATE_MAP[t] for t in inferred}
        if len(create_funcs) > 1:
            raise self._error("Mixed constant types in a list literal are not supported.", error_node)
        return sorted(inferred)[0]

    def _to_xs_list_literal_stmts(self, var_name: str, elements: list[expr],
                                  element_type: str, ctx: XsContext) -> str:
        create_func = self._ARRAY_CREATE_MAP[element_type]
        set_func = self._ARRAY_SET_MAP[element_type]
        xs = self._stmt(ctx.depth, f"int {var_name}{self.sp}={self.sp}{create_func}({len(elements)})")
        for index, element in enumerate(elements):
            value_expr = self._render_expression(element, ctx, enclosed=True)
            xs += value_expr.prelude
            xs += self._stmt(ctx.depth, f"{set_func}({var_name},{self.sp}{index},{self.sp}{value_expr.value})")
        return xs

    def _render_list_literal_expr(self, list_node: List, ctx: XsContext) -> RenderedExpression:
        elements = list_node.elts
        if not elements:
            raise self._error("Cannot create an array from an empty list literal without a type annotation.", list_node)
        element_type = self._infer_list_literal_type(elements, list_node)
        temp_name = self._next_temp_name()
        prelude = self._to_xs_list_literal_stmts(temp_name, elements, element_type, ctx)
        return RenderedExpression(temp_name, prelude)

    def _to_xs_list_literal_target(self, target: Name, elements: list[expr], element_type: str, ctx: XsContext) -> str:
        return self._to_xs_list_literal_stmts(self._to_camel_case(target.id), elements, element_type, ctx)

    def _render_annotated_assignment(self, assign: AnnAssign, ctx: XsContext) -> str:
        if isinstance(assign.value, List):
            if not isinstance(assign.target, Name):
                raise self._error("Variable declaration must use a simple variable name.", assign.target)
            element_type = self._annotation_element_type(assign.annotation)
            if element_type is None:
                element_type = self._infer_list_literal_type(assign.value.elts, assign.value)
            return self._to_xs_list_literal_target(assign.target, assign.value.elts, element_type, ctx)

        nd_result = self._try_to_xs_nd_array_init(assign, ctx)
        if nd_result is not None:
            return nd_result
        return self._to_xs_variable_definition(assign, ctx)

    def _to_xs_variable_definition(self, a: AnnAssign, ctx: XsContext) -> str:
        if isinstance(a.annotation, Name):
            modifier = ""
            python_type = a.annotation.id
            xs_type = self._to_xs_type(a.annotation)
        elif isinstance(a.annotation, Subscript) and isinstance(a.annotation.value, Name):
            python_type = None
            if a.annotation.value.id in self._ARRAY_LIST_NAMES:
                modifier = ""
                xs_type = "int"
            else:
                modifier = self._to_xs_modifier(a.annotation.value.id, a.annotation.value) + " "
                if isinstance(a.annotation.slice, Name):
                    xs_type = self._to_xs_type(a.annotation.slice)
                else:
                    raise self._error("Variable declarations must include a supported type annotation.", a.annotation.slice)
        else:
            raise self._error("Variable declarations must include a supported type annotation.", a.annotation)

        if isinstance(a.target, Name):
            name = self._to_camel_case(a.target.id)
        else:
            raise self._error("Variable declarations must use a simple variable name.", a.target)

        if isinstance(a.value, Subscript) and python_type is not None:
            value_expr = self._render_array_get(a.value, python_type, ctx)
        elif isinstance(a.value, Subscript):
            value_expr = self._render_array_get(a.value, "int", ctx)
        else:
            value_expr = self._render_expression(a.value, ctx, enclosed=True)
        return value_expr.prelude + self._stmt(ctx.depth, f"{modifier}{xs_type} {name}{self.sp}={self.sp}{value_expr.value}")

    def _render_array_get(self, subscript: Subscript, element_type: str, ctx: XsContext) -> RenderedExpression:
        get_func = self._ARRAY_GET_MAP.get(element_type)
        if get_func is None:
            raise self._error(f"Array reads do not support element type {element_type!r}.", subscript)
        index_expr = self._render_expression(subscript.slice, ctx, enclosed=True)
        if isinstance(subscript.value, Name):
            array_expr = RenderedExpression(self._to_camel_case(subscript.value.id))
        elif isinstance(subscript.value, Subscript):
            array_expr = self._render_array_get(subscript.value, "int", ctx)
        else:
            raise self._error("Array read targets must be variable names or nested array accesses.", subscript.value)
        prelude = self._combine_prelude(array_expr, index_expr)
        return RenderedExpression(f"{get_func}({array_expr.value},{self.sp}{index_expr.value})", prelude)

    def _to_xs_array_get(self, subscript: Subscript, element_type: str, ctx: XsContext) -> str:
        return self._render_array_get(subscript, element_type, ctx).value

    def _parse_nd_array_annotation(self, annotation: expr) -> Optional[tuple[int, str]]:
        if not (isinstance(annotation, Subscript) and isinstance(annotation.value, Name)
                and annotation.value.id in self._ARRAY_LIST_NAMES):
            return None
        depth = 1
        current = annotation.slice
        while True:
            if isinstance(current, Name) and current.id in self._ARRAY_CREATE_MAP:
                return (depth, current.id)
            if (isinstance(current, Subscript) and isinstance(current.value, Name)
                    and current.value.id in self._ARRAY_LIST_NAMES):
                depth += 1
                current = current.slice
            else:
                return None

    def _parse_nd_array_value(self, value: expr, depth: int) -> Optional[tuple[list[expr], expr]]:
        sizes = []
        current = value
        for _ in range(depth):
            if not (isinstance(current, BinOp) and isinstance(current.op, Mult)
                    and isinstance(current.left, List) and len(current.left.elts) == 1):
                return None
            sizes.append(current.right)
            current = current.left.elts[0]
        if self._unpack_constant(current) is None and not isinstance(current, Call):
            return None
        return sizes, current

    def _try_to_xs_nd_array_init(self, e: AnnAssign, ctx: XsContext) -> Optional[str]:
        ann_result = self._parse_nd_array_annotation(e.annotation)
        if ann_result is None or ann_result[0] < 2:
            return None
        depth, inner_element_type = ann_result
        if not isinstance(e.target, Name):
            return None
        val_result = self._parse_nd_array_value(e.value, depth)
        if val_result is None:
            return None
        sizes, inner_default_node = val_result
        var_name = self._to_camel_case(e.target.id)
        return self._to_xs_nd_array_init_stmts(var_name, sizes, inner_element_type, inner_default_node, ctx)

    def _to_xs_nd_array_init_stmts(self, var_name: str, sizes: list[expr], inner_element_type: str,
                                   inner_default_node: expr, ctx: XsContext) -> str:
        outer_size_expr = self._render_expression(sizes[0], ctx, enclosed=True)
        xs = outer_size_expr.prelude
        xs += self._stmt(ctx.depth, f"int {var_name}{self.sp}={self.sp}xsArrayCreateInt({outer_size_expr.value})")
        xs += self._to_xs_nd_array_fill_loop(var_name, sizes[0], sizes[1:], inner_element_type, inner_default_node, ctx)
        return xs

    def _to_xs_nd_array_fill_loop(self, parent_var: str, parent_size_node: expr, sub_sizes: list[expr],
                                  inner_element_type: str, inner_default_node: expr, ctx: XsContext) -> str:
        loop_var = self._next_temp_name()
        parent_size_expr = self._render_expression(parent_size_node, ctx, enclosed=True)
        header = f"for{self.sp}({loop_var}{self.sp}={self.sp}0;{self.sp}<{self.sp}{parent_size_expr.value})"
        if len(sub_sizes) == 1:
            create_expr = self._render_array_create(inner_element_type, inner_default_node, sub_sizes[0], ctx)
            body_xs = create_expr.prelude
            body_xs += self._stmt(ctx.depth + 1, f"xsArraySetInt({parent_var},{self.sp}{loop_var},{self.sp}{create_expr.value})")
        else:
            temp_var = self._next_temp_name()
            sub_size_expr = self._render_expression(sub_sizes[0], ctx, enclosed=True)
            body_xs = sub_size_expr.prelude
            body_xs += self._stmt(ctx.depth + 1, f"int {temp_var}{self.sp}={self.sp}xsArrayCreateInt({sub_size_expr.value})")
            body_xs += self._stmt(ctx.depth + 1, f"xsArraySetInt({parent_var},{self.sp}{loop_var},{self.sp}{temp_var})")
            body_xs += self._to_xs_nd_array_fill_loop(temp_var, sub_sizes[0], sub_sizes[1:], inner_element_type,
                                                      inner_default_node, ctx.indented())
        return parent_size_expr.prelude + self._block(ctx.depth, header, body_xs)

    def _to_xs_variable_assignment(self, a: Assign, ctx: XsContext) -> str:
        if len(a.targets) != 1:
            raise self._error("Only single-target assignments are supported.", a)
        target = a.targets[0]
        if isinstance(target, Name):
            name = self._to_camel_case(target.id)
        else:
            raise self._error("Assignment target must be a variable name.", target)
        value_expr = self._render_expression(a.value, ctx, enclosed=True)
        return value_expr.prelude + self._stmt(ctx.depth, f"{name}{self.sp}={self.sp}{value_expr.value}")

    def _render_assignment(self, assign: Assign, ctx: XsContext) -> str:
        if len(assign.targets) == 1 and isinstance(assign.targets[0], Subscript):
            return self._to_xs_array_set(assign.targets[0], assign.value, ctx)
        if len(assign.targets) == 1 and isinstance(assign.targets[0], Name) and isinstance(assign.value, List):
            element_type = self._infer_list_literal_type(assign.value.elts, assign.value)
            return self._to_xs_list_literal_target(assign.targets[0], assign.value.elts, element_type, ctx)
        return self._to_xs_variable_assignment(assign, ctx)

    def _to_xs_array_set(self, target: Subscript, value: expr, ctx: XsContext) -> str:
        index_expr = self._render_expression(target.slice, ctx, enclosed=True)
        if isinstance(target.value, Name):
            array_expr = RenderedExpression(self._to_camel_case(target.value.id))
        elif isinstance(target.value, Subscript):
            array_expr = self._render_array_get(target.value, "int", ctx)
        else:
            raise self._error("Array assignment target must be a variable name or nested array access.", target.value)
        element_type = self._infer_array_element_type(value)
        set_func = self._ARRAY_SET_MAP.get(element_type)
        if set_func is None:
            raise self._error(f"Array assignment does not support element type {element_type!r}.", value)
        value_expr = self._render_expression(value, ctx, enclosed=True)
        prelude = self._combine_prelude(array_expr, index_expr, value_expr)
        return prelude + self._stmt(
            ctx.depth,
            f"{set_func}({array_expr.value},{self.sp}{index_expr.value},{self.sp}{value_expr.value})",
        )

    def _to_xs_variable_aug_assignment(self, a: AugAssign, ctx: XsContext) -> str:
        if isinstance(a.target, Name):
            name = self._to_camel_case(a.target.id)
        else:
            raise self._error("Assignment target must be a variable name.", a.target)
        op = self._to_xs_binary_op(a.op, a)
        aug_value = self._unpack_constant(a.value)
        if aug_value == 1 and not isinstance(aug_value, bool) and op == "+":
            return self._stmt(ctx.depth, f"{name}++")
        if aug_value == 1 and not isinstance(aug_value, bool) and op == "-":
            return self._stmt(ctx.depth, f"{name}--")
        value_expr = self._render_expression(a.value, ctx)
        return value_expr.prelude + self._stmt(
            ctx.depth,
            f"{name}{self.sp}={self.sp}{name}{self.sp}{op}{self.sp}{value_expr.value}",
        )

    def _render_module_statement(self, node: stmt, ctx: XsContext) -> RenderedStatement:
        if isinstance(node, FunctionDef):
            return RenderedStatement(
                self.to_xs_function_definition(node, ctx),
                is_function=True,
            )
        if isinstance(node, If) and self._is_main_guard(node):
            return RenderedStatement(
                self._to_xs_main_definition(node, ctx),
                is_function=True,
            )
        if isinstance(node, AnnAssign):
            return RenderedStatement(self._render_annotated_assignment(node, ctx))
        if isinstance(node, Assign):
            return RenderedStatement(self._render_assignment(node, ctx))
        raise self._error(f"Unsupported top-level statement: {type(node).__name__}.", node)

    def _render_body_statement(self, node: stmt, ctx: XsContext) -> str:
        inner = ctx.indented()
        if isinstance(node, AnnAssign):
            return self._render_annotated_assignment(node, inner)
        if isinstance(node, Assign):
            return self._render_assignment(node, inner)
        if isinstance(node, AugAssign):
            return self._to_xs_variable_aug_assignment(node, inner)
        if isinstance(node, Expr):
            return self._to_xs_expression_top(node, inner)
        if isinstance(node, If):
            return self._to_xs_if(node, inner)
        if isinstance(node, For):
            return self._to_xs_for(node, inner)
        if isinstance(node, While):
            return self._to_xs_while(node, inner)
        if isinstance(node, Match):
            return self._to_xs_match(node, inner)
        if isinstance(node, With):
            raise self._error(
                "With-statements are not supported. Use `for ... in macro_repeat(...)` for repeat macros.",
                node,
            )
        if isinstance(node, Return):
            return self._to_xs_return(node, inner)
        if isinstance(node, (Pass, Global)):
            return ""
        raise self._error(f"Unsupported statement in function body: {type(node).__name__}.", node)

    @staticmethod
    def _is_main_guard(node: If) -> bool:
        if not isinstance(node.test, Compare) or len(node.test.ops) != 1 or len(node.test.comparators) != 1:
            return False

        left = node.test.left
        right = node.test.comparators[0]

        def is_module_name(expr_node: expr) -> bool:
            return isinstance(expr_node, Name) and expr_node.id == "__name__"

        def is_main_name(expr_node: expr) -> bool:
            return isinstance(expr_node, Constant) and expr_node.value == "__main__"

        return (
            isinstance(node.test.ops[0], Eq)
            and ((is_module_name(left) and is_main_name(right)) or (is_main_name(left) and is_module_name(right)))
        )

    def _to_xs_main_definition(self, if_stmt: If, ctx: XsContext) -> str:
        if if_stmt.orelse:
            raise self._error("Top-level __name__ == '__main__' guard cannot have an else block.", if_stmt.orelse[0])
        return self._block(ctx.depth, "void main()", self._to_xs_body(if_stmt.body, ctx))

    def _to_xs_expression_top(self, e: Expr, ctx: XsContext) -> str:
        if (isinstance(e.value, Constant) and isinstance(e.value.value, str)
                and e.value.value.strip().replace("\n", "").replace(" ", "") in self._doc_strings):
            return ""
        value_expr = self._render_expression(e.value, ctx)
        return value_expr.prelude + self._stmt(ctx.depth, value_expr.value)

    def _to_xs_binary_op(self, op: operator | cmpop | boolop, node: Optional[ast.AST] = None) -> str:
        xs_op = self._OPERATOR_MAP.get(type(op))
        if xs_op is None:
            raise self._error(f"Unsupported binary operator: {op}.", node)
        return xs_op

    def _to_xs_name_expr(self, node: Name, ctx: XsContext) -> RenderedExpression:
        if node.id in ctx.replacements:
            return RenderedExpression(ctx.replacements[node.id])
        return RenderedExpression(self._to_camel_case(node.id))

    def _to_xs_bin_op_expr(self, node: BinOp, ctx: XsContext, enclosed: bool) -> RenderedExpression:
        if isinstance(node.op, Mult) and isinstance(node.left, List):
            default_node, size_node = self._parse_array_literal(node)
            element_type = self._infer_array_element_type(default_node)
            return self._render_array_create(element_type, default_node, size_node, ctx)

        left_expr = self._render_expression(node.left, ctx)
        op_xs = self._to_xs_binary_op(node.op, node)
        right_expr = self._render_expression(node.right, ctx)
        prelude = self._combine_prelude(left_expr, right_expr)
        value = self._wrap_parens(f"{left_expr.value}{self.sp}{op_xs}{self.sp}{right_expr.value}", enclosed)
        return RenderedExpression(value, prelude)

    def _to_xs_unary_expr(self, node: UnaryOp, ctx: XsContext, enclosed: bool) -> RenderedExpression:
        value = self._unpack_constant(node)
        if value is not None:
            return RenderedExpression(self._to_xs_constant(value, enclosed, node))
        if isinstance(node.op, Not):
            operand_expr = self._render_expression(node.operand, ctx)
            value = self._wrap_parens(
                f"{operand_expr.value}{self.sp}=={self.sp}false",
                enclosed,
            )
            return RenderedExpression(value, operand_expr.prelude)
        raise self._error(f"Unsupported unary operator: {node}.", node)

    def _to_xs_compare_expr(self, node: Compare, ctx: XsContext, enclosed: bool) -> RenderedExpression:
        if len(node.comparators) != 1 or len(node.ops) != 1:
            raise self._error("Comparisons must have exactly one operator and one comparator.", node)
        left_expr = self._render_expression(node.left, ctx)
        op_xs = self._to_xs_binary_op(node.ops[0], node)
        right_expr = self._render_expression(node.comparators[0], ctx)
        prelude = self._combine_prelude(left_expr, right_expr)
        value = self._wrap_parens(f"{left_expr.value}{self.sp}{op_xs}{self.sp}{right_expr.value}", enclosed)
        return RenderedExpression(value, prelude)

    def _to_xs_attribute_expr(self, node: Attribute) -> RenderedExpression:
        if isinstance(node.value, Name) and node.value.id == "XsConstants":
            return RenderedExpression(self._to_camel_case(node.attr))
        raise self._error(f"Unsupported expression type: {type(node).__name__}.", node)

    def _to_xs_joined_str_expr(self, node: JoinedStr, ctx: XsContext) -> RenderedExpression:
        parts = [self._render_expression(value, ctx) for value in node.values]
        prelude = self._combine_prelude(*parts)
        return RenderedExpression(f"({f'{self.sp}+{self.sp}'.join(part.value for part in parts)})", prelude)

    def _to_xs_formatted_value_expr(self, node: FormattedValue, ctx: XsContext) -> RenderedExpression:
        source_segment = ast.get_source_segment(self._source, node) if self._source is not None else None
        is_debug_expr = source_segment is not None and re.fullmatch(r"\{.+?=\s*\}", source_segment) is not None
        if is_debug_expr and node.conversion == ord("r") and node.format_spec is None:
            return self._render_expression(node.value, ctx)
        if node.conversion != -1:
            raise self._error("f-string conversion is not supported.", node)
        if node.format_spec is not None:
            raise self._error("f-string format spec is not supported.", node)
        return self._render_expression(node.value, ctx)

    def _to_xs_bool_op_expr(self, node: BoolOp, ctx: XsContext, enclosed: bool) -> RenderedExpression:
        op_xs = self._to_xs_binary_op(node.op, node)
        parts = [self._render_expression(value, ctx) for value in node.values]
        prelude = self._combine_prelude(*parts)
        value = self._wrap_parens(f"{self.sp}{op_xs}{self.sp}".join(part.value for part in parts), enclosed)
        return RenderedExpression(value, prelude)

    def _render_expression(self, e: expr, ctx: XsContext, enclosed: bool = False) -> RenderedExpression:
        try:
            if isinstance(e, Constant):
                return RenderedExpression(self._to_xs_constant(e.value, enclosed, e))
            if isinstance(e, Name):
                return self._to_xs_name_expr(e, ctx)
            if isinstance(e, Call):
                if isinstance(e.func, Name) and e.func.id in self._macro_functions:
                    return RenderedExpression(self._to_xs_constant(self._eval_macro_function(e), enclosed, e))
                return self._render_call(e, ctx, enclosed)
            if isinstance(e, BinOp):
                return self._to_xs_bin_op_expr(e, ctx, enclosed)
            if isinstance(e, UnaryOp):
                return self._to_xs_unary_expr(e, ctx, enclosed)
            if isinstance(e, Compare):
                return self._to_xs_compare_expr(e, ctx, enclosed)
            if isinstance(e, Attribute):
                return self._to_xs_attribute_expr(e)
            if isinstance(e, JoinedStr):
                return self._to_xs_joined_str_expr(e, ctx)
            if isinstance(e, FormattedValue):
                return self._to_xs_formatted_value_expr(e, ctx)
            if isinstance(e, BoolOp):
                return self._to_xs_bool_op_expr(e, ctx, enclosed)
            if isinstance(e, List):
                return self._render_list_literal_expr(e, ctx)
            raise self._error(f"Unsupported expression type: {type(e).__name__}.", e)
        except Exception as exc:
            self._raise_as_conversion_error(exc, e)

    def _to_xs_expression(self, e: expr, ctx: XsContext, enclosed: bool = False) -> str:
        return self._render_expression(e, ctx, enclosed).value

    def _to_xs_constant(self, value: str | bool | int | float, enclosed: bool = False,
                        node: Optional[ast.AST] = None) -> str:
        if isinstance(value, str):
            return '"' + value.replace('"', '\\"') + '"'
        if isinstance(value, bool):
            return str(value).lower()
        if isinstance(value, int):
            if value > 999_999_999:
                if value > 2_147_483_647:
                    raise self._error(f"XS ints cannot hold values larger than 2147483647: {value}.", node)
                base = value // 10
                remainder = value % 10
                return self._wrap_parens(f"{base}{self.sp}*{self.sp}10{self.sp}+{self.sp}{remainder}", enclosed)
            if value < -999_999_999:
                if value < -2_147_483_648:
                    raise self._error(f"XS ints cannot hold values smaller than -2147483648: {value}.", node)
                value = value * -1
                base = value // 10
                remainder = value % 10
                return self._wrap_parens(f"-{base}{self.sp}*{self.sp}10{self.sp}-{self.sp}{remainder}", enclosed)
            return f"{value}"
        if isinstance(value, float):
            return f"{value}"
        raise self._error(f"Unsupported literal value: {value!r}.", node)

    def _unpack_constant(self, node: expr) -> Optional[Any]:
        if isinstance(node, Constant):
            return node.value
        if isinstance(node, UnaryOp) and isinstance(node.op, USub):
            inner = self._unpack_constant(node.operand)
            if inner is not None:
                return -inner
        if (isinstance(node, Call) and isinstance(node.func, Name)
                and node.func.id in self._NUMERIC_CAST_ZEROS and len(node.args) == 1):
            return self._unpack_constant(node.args[0])
        cast_info = self._parse_cast_call(node)
        if cast_info is not None:
            return self._unpack_constant(cast_info[1])
        return None

    def _render_numeric_cast(self, zero: str, arg: expr, ctx: XsContext, enclosed: bool) -> RenderedExpression:
        value = self._unpack_constant(arg)
        if value is not None:
            return RenderedExpression(self._to_xs_constant(value, enclosed, arg))
        arg_expr = self._render_expression(arg, ctx)
        value_xs = self._wrap_parens(f"{zero}{self.sp}+{self.sp}{arg_expr.value}", enclosed)
        return RenderedExpression(value_xs, arg_expr.prelude)

    def _to_xs_numeric_cast(self, zero: str, arg: expr, ctx: XsContext, enclosed: bool) -> str:
        return self._render_numeric_cast(zero, arg, ctx, enclosed).value

    def _render_special_call(self, function_name: str, call: Call, ctx: XsContext,
                             enclosed: bool) -> Optional[RenderedExpression]:
        if function_name == "str":
            arg_expr = self._render_expression(call.args[0], ctx)
            value = self._wrap_parens(f'""{self.sp}+{self.sp}{arg_expr.value}', enclosed)
            return RenderedExpression(value, arg_expr.prelude)
        if function_name == "len":
            arg_expr = self._render_expression(call.args[0], ctx, enclosed=True)
            return RenderedExpression(f"xsArrayGetSize({arg_expr.value})", arg_expr.prelude)
        if function_name == "cast":
            if len(call.args) != 2:
                raise self._error("cast() requires exactly 2 arguments.", call)
            inner = call.args[1]
            if isinstance(inner, Subscript):
                return self._render_array_get(inner, call.args[0].id, ctx)
            return self._render_expression(inner, ctx, enclosed=enclosed)

        zero = self._NUMERIC_CAST_ZEROS.get(function_name)
        if zero is not None:
            return self._render_numeric_cast(zero, call.args[0], ctx, enclosed)
        return None

    def _render_call(self, call: Call, ctx: XsContext, enclosed: bool = False) -> RenderedExpression:
        if not isinstance(call.func, Name):
            raise self._error(f"Function calls must reference a name, not {call.func}.", call.func)
        if call.func.id in self._macro_repeat_functions:
            raise self._error("macro_repeat() is only supported as the iterable in a for-loop.", call)
        function_name = self._to_camel_case(call.func.id)
        special_expr = self._render_special_call(function_name, call, ctx, enclosed)
        if special_expr is not None:
            return special_expr
        args_expr = [self._render_expression(arg, ctx, enclosed=True) for arg in call.args]
        prelude = self._combine_prelude(*args_expr)
        args_xs = f",{self.sp}".join(arg.value for arg in args_expr)
        return RenderedExpression(f"{function_name}({args_xs})", prelude)

    def _to_xs_call(self, e: Call, ctx: XsContext, enclosed: bool = False) -> str:
        return self._render_call(e, ctx, enclosed).value

    def _to_xs_if(self, if_stmt: If, ctx: XsContext, els: bool = False) -> str:
        xs = ""
        cond_expr = self._render_expression(if_stmt.test, ctx, enclosed=True)
        if not els:
            xs += cond_expr.prelude
            xs += f"{ctx.depth * self.indent}if{self.sp}({cond_expr.value}){self.sp}{{{self.nl}"
        else:
            xs += f"{ctx.depth * self.indent}}}{self.sp}else if{self.sp}({cond_expr.value}){self.sp}{{{self.nl}"
        xs += self._to_xs_body(if_stmt.body, ctx)

        if len(if_stmt.orelse) == 1 and isinstance(if_stmt.orelse[0], If):
            xs += self._to_xs_if(if_stmt.orelse[0], ctx, True)
        elif len(if_stmt.orelse) > 0:
            xs += f"{ctx.depth * self.indent}}}{self.sp}else{self.sp}{{{self.nl}"
            xs += self._to_xs_body(if_stmt.orelse, ctx)
            xs += f"{ctx.depth * self.indent}}}{self.nl}"
        else:
            xs += f"{ctx.depth * self.indent}}}{self.nl}"
        return xs

    def _to_xs_for(self, for_stmt: For, ctx: XsContext) -> str:
        if (
                isinstance(for_stmt.iter, Call)
                and isinstance(for_stmt.iter.func, Name)
                and for_stmt.iter.func.id in self._macro_repeat_functions
        ):
            return self._to_xs_macro_repeat_for(for_stmt, ctx)
        if not (
                isinstance(for_stmt.iter, Call)
                and isinstance(for_stmt.iter.func, Name)
                and for_stmt.iter.func.id in {"range", "i32range"}
        ):
            raise self._error(
                "For-loops are only supported over range(...), i32range(...), or macro_repeat(...).",
                for_stmt.iter,
            )
        if not isinstance(for_stmt.target, Name):
            raise self._error("For-loop targets must be simple variable names.", for_stmt.target)

        loop_var = self._to_camel_case(for_stmt.target.id)
        start_node, end_node, step = self._parse_range_args(for_stmt.iter.args, for_stmt.iter)

        if step == 1 or step == -1:
            positive = step > 0
            start_expr = RenderedExpression("0") if start_node is None else self._render_expression(start_node, ctx, enclosed=True)
            bound_expr = self._render_for_bound(end_node, ctx, positive, True)
            header = f"for{self.sp}({loop_var}{self.sp}={self.sp}{start_expr.value};{self.sp}{bound_expr.value})"
            return self._combine_prelude(start_expr, bound_expr) + self._block(ctx.depth, header, self._to_xs_body(for_stmt.body, ctx))

        start_expr = self._render_expression(start_node, ctx, enclosed=True)
        xs = start_expr.prelude
        xs += self._stmt(ctx.depth, f"int {loop_var}{self.sp}={self.sp}{start_expr.value}")
        if isinstance(step, int):
            positive = step > 0
            op = "+" if positive else "-"
            step_xs = self._to_xs_constant(abs(step))
            bound_expr = self._render_for_bound(end_node, ctx, positive, False)
            body_xs = self._to_xs_body(for_stmt.body, ctx)
            body_xs += self._stmt(ctx.depth + 1,
                                  f"{loop_var}{self.sp}={self.sp}{loop_var}{self.sp}{op}{self.sp}{step_xs}")
            xs += bound_expr.prelude
            xs += self._block(ctx.depth, f"while{self.sp}({loop_var}{self.sp}{bound_expr.value})", body_xs)
            return xs

        step_expr = self._render_expression(step, ctx, enclosed=True)
        xs += step_expr.prelude
        if isinstance(step, Name):
            step_ref = step_expr.value
        else:
            step_ref = self._next_temp_name()
            xs += self._stmt(ctx.depth, f"int {step_ref}{self.sp}={self.sp}{step_expr.value}")

        positive_body_xs = self._to_xs_body(for_stmt.body, ctx.indented())
        positive_body_xs += self._stmt(ctx.depth + 2,
                                       f"{loop_var}{self.sp}={self.sp}{loop_var}{self.sp}+{self.sp}{step_ref}")
        positive_bound_expr = self._render_for_bound(end_node, ctx, True, False)
        positive_while_xs = self._block(
            ctx.depth + 1,
            f"while{self.sp}({loop_var}{self.sp}{positive_bound_expr.value})",
            positive_body_xs,
        )

        negative_body_xs = self._to_xs_body(for_stmt.body, ctx.indented())
        negative_body_xs += self._stmt(ctx.depth + 2,
                                       f"{loop_var}{self.sp}={self.sp}{loop_var}{self.sp}+{self.sp}{step_ref}")
        negative_bound_expr = self._render_for_bound(end_node, ctx, False, False)
        negative_while_xs = self._block(
            ctx.depth + 1,
            f"while{self.sp}({loop_var}{self.sp}{negative_bound_expr.value})",
            negative_body_xs,
        )

        xs += positive_bound_expr.prelude + negative_bound_expr.prelude
        xs += f"{ctx.depth * self.indent}if{self.sp}({step_ref}{self.sp}>{self.sp}0){self.sp}{{{self.nl}"
        xs += positive_while_xs
        xs += f"{ctx.depth * self.indent}}}{self.sp}else if{self.sp}({step_ref}{self.sp}<{self.sp}0){self.sp}{{{self.nl}"
        xs += negative_while_xs
        xs += f"{ctx.depth * self.indent}}}{self.nl}"
        return xs

    def _to_xs_macro_repeat_for(self, for_stmt: For, ctx: XsContext) -> str:
        if not isinstance(for_stmt.iter, Call):
            raise self._error("Macro repeat loops must iterate over a macro_repeat(...) call.", for_stmt.iter)

        names, destructured = self._parse_macro_repeat_target(for_stmt.target)
        iterable_value = self._eval_macro_repeat_iterable(for_stmt.iter)
        if not isinstance(iterable_value, Iterable):
            raise self._error(
                "Macro repeat loops require the iterable expression to evaluate to an iterable.",
                for_stmt.iter,
            )

        xs = ""
        for value in iterable_value:
            replacements = ctx.replacements.copy()
            values = self._macro_repeat_values_for_target(value, len(names), destructured, for_stmt.target)
            for name, val in zip(names, values):
                replacements[name] = self._to_xs_constant(val, node=for_stmt.iter)
            body_ctx = XsContext(ctx.depth - 1, replacements)
            xs += self._to_xs_body(for_stmt.body, body_ctx)
        return xs

    def _parse_macro_repeat_target(self, target: expr) -> tuple[list[str], bool]:
        if isinstance(target, Name):
            return [target.id], False
        if isinstance(target, Tuple):
            if not all(isinstance(node, Name) for node in target.elts):
                raise self._error(
                    "Macro repeat loop targets must be a simple variable name or a destructured tuple of names.",
                    target,
                )
            return [node.id for node in target.elts], True
        raise self._error(
            "Macro repeat loop targets must be a simple variable name or a destructured tuple of names.",
            target,
        )

    def _macro_repeat_values_for_target(self, value: Any, expected_count: int, destructured: bool,
                                        node: ast.AST) -> list[Any]:
        if not destructured:
            return [value]
        try:
            values = list(value)
        except TypeError as exc:
            raise self._error(
                "Macro repeat tuple targets require each iterated value to be iterable.",
                node,
            ) from exc
        if len(values) != expected_count:
            raise self._error(
                "Macro repeat tuple targets must match the number of values produced by the iterable.",
                node,
            )
        return values

    def _parse_range_args(self, args: list[expr], node: Optional[ast.AST] = None) -> tuple[Optional[expr], expr, int | expr]:
        if len(args) == 1:
            return None, args[0], 1
        if len(args) == 2:
            return args[0], args[1], 1
        if len(args) == 3:
            step = self._unpack_int_constant(args[2])
            if step is None:
                return args[0], args[1], args[2]
            if step == 0:
                raise self._error("For-loop steps cannot be 0.", args[2])
            return args[0], args[1], step
        raise self._error("range() accepts 1 to 3 arguments.", node or (args[0] if args else None))

    def _unpack_int_constant(self, expr: expr) -> Optional[int]:
        value = self._unpack_constant(expr)
        if not isinstance(value, int):
            return None
        return value

    def _render_for_bound(self, param: expr, ctx: XsContext, positive: bool, enclosed: bool) -> RenderedExpression:
        expected_op = Add if positive else Sub
        inclusive_sign = "<=" if positive else ">="
        if isinstance(param, BinOp) and isinstance(param.op, expected_op):
            pairs = [(param.left, param.right), (param.right, param.left)] if positive else [(param.left, param.right)]
            for main, other in pairs:
                other_value = self._unpack_constant(other)
                if other_value == 1 and not isinstance(other_value, bool):
                    main_expr = self._render_expression(main, ctx, enclosed=enclosed)
                    return RenderedExpression(f"{inclusive_sign}{self.sp}{main_expr.value}", main_expr.prelude)
        exclusive_sign = "<" if positive else ">"
        param_expr = self._render_expression(param, ctx, enclosed=enclosed)
        return RenderedExpression(f"{exclusive_sign}{self.sp}{param_expr.value}", param_expr.prelude)

    def _to_xs_for_bound(self, param: expr, ctx: XsContext, positive: bool, enclosed: bool) -> str:
        return self._render_for_bound(param, ctx, positive, enclosed).value

    def _to_xs_while(self, while_stmt: While, ctx: XsContext) -> str:
        condition_expr = self._render_expression(while_stmt.test, ctx, enclosed=True)
        header = f"while{self.sp}({condition_expr.value})"
        return condition_expr.prelude + self._block(ctx.depth, header, self._to_xs_body(while_stmt.body, ctx))

    def _to_xs_match(self, match_stmt: Match, ctx: XsContext) -> str:
        inner = ctx.indented()
        cases_xs = ""
        cases_prelude = ""
        for case in match_stmt.cases:
            if isinstance(case.pattern, MatchValue):
                case_expr = self._render_expression(case.pattern.value, ctx)
                cases_prelude += case_expr.prelude
                cases_xs += self._block(inner.depth, f"case {case_expr.value}:", self._to_xs_body(case.body, inner))
            elif isinstance(case.pattern, MatchAs) and case.pattern.name is None:
                cases_xs += self._block(inner.depth, "default:", self._to_xs_body(case.body, inner))
            else:
                raise self._error(f"Match statements only support literal cases and `case _`; got {case.pattern}.",
                                  case.pattern)
        subject_expr = self._render_expression(match_stmt.subject, ctx, enclosed=True)
        header = f"switch{self.sp}({subject_expr.value})"
        return subject_expr.prelude + cases_prelude + self._block(ctx.depth, header, cases_xs)

    def _eval_macro_function(self, call: Call) -> Any:
        if not isinstance(call.func, Name):
            raise self._error("Macro call must reference a function name.", call.func)
        return self._eval_macro_var(call)

    def _eval_macro_var(self, call: Call) -> Any:
        if len(call.args) == 1 and isinstance(call.args[0], Constant) and isinstance(call.args[0].value, str):
            reference = call.args[0].value
            if reference in self._vars:
                return self._vars[reference]
            raise self._error(f"Macro reference {reference!r} is not bound in converter bindings.", call.args[0])
        raise self._error("Macro calls must have a string constant as their first argument.", call)

    def _macro_reference_name(self, call: Call) -> str:
        if not (call.args and isinstance(call.args[0], Constant) and isinstance(call.args[0].value, str)):
            raise self._error("Macro calls must have a string constant as their first argument.", call)
        return call.args[0].value

    def _eval_macro_repeat_iterable(self, call: Call) -> Any:
        if len(call.args) != 1:
            raise self._error("macro_repeat() requires a string reference.", call)
        value = self._eval_macro_var(call)
        if not isinstance(value, Iterable):
            raise self._error(
                f"macro_repeat reference {self._macro_reference_name(call)!r} resolved to {value!r} "
                f"({type(value).__name__}), expected an iterable.",
                call,
            )
        return value
