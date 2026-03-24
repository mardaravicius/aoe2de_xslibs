import ast
import inspect
import re
import textwrap
from ast import FunctionDef, Constant, Name, expr, arg, Expr, AnnAssign, Call, Assign, BinOp, Add, Sub, Mod, Mult, Div, \
    operator, If, Compare, Eq, Gt, GtE, Lt, LtE, NotEq, cmpop, For, While, AugAssign, Match, MatchValue, MatchAs, \
    Return, Pass, Subscript, stmt, Attribute, keyword, With, Tuple, UnaryOp, USub, JoinedStr, FormattedValue, Global, \
    BoolOp, Or, And, Not, FloorDiv, List, Import, ImportFrom
from dataclasses import dataclass, field
from types import ModuleType
from typing import Any, Iterable, Optional

from xs_converter.macro import macro_pass_value, macro_repeat_with_iterable


@dataclass(frozen=True)
class XsContext:
    depth: int = 0
    replacements: dict[str, str] = field(default_factory=dict)

    def indented(self) -> 'XsContext':
        return XsContext(self.depth + 1, self.replacements)

    def with_replacements(self, replacements: dict[str, str]) -> 'XsContext':
        return XsContext(self.depth, replacements)


class PythonToXsConverter:
    _macro_functions = {
        macro_pass_value.__name__,
    }
    _macro_repeat_functions = {
        macro_repeat_with_iterable.__name__,
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

    @staticmethod
    def to_xs_script(*functions, indent: bool, root_flags=None, **kwargs) -> str:
        xs = ""
        for i, f in enumerate(functions):
            root_f = (i == 0) if root_flags is None else root_flags[i]
            converter = PythonToXsConverter(indent, kwargs)
            xs += converter._to_xs_function(f, root_f)
            if i < len(functions) - 1:
                xs += converter.nl
        return xs

    @staticmethod
    def to_xs_file(module: ModuleType, indent: bool, **kwargs) -> str:
        source = inspect.getsource(module)
        module_ast = ast.parse(source)
        converter = PythonToXsConverter(indent, kwargs)
        ctx = XsContext()
        parts = []
        for node in module_ast.body:
            if isinstance(node, (Import, ImportFrom)):
                continue
            if isinstance(node, FunctionDef):
                parts.append(converter.to_xs_function_definition(node, ctx, root_function=len(parts) == 0))
            elif isinstance(node, AnnAssign):
                parts.append(converter._to_xs_variable_definition(node, ctx))
            elif isinstance(node, Assign):
                parts.append(converter._to_xs_variable_assignment(node, ctx))
            else:
                raise ValueError(f"unsupported top-level statement: {type(node).__name__}")
        return converter.nl.join(parts)

    def __init__(self, indent: bool, vars: dict[str, any]):
        if indent:
            self.sp = " "
            self.nl = "\n"
            self.indent = " " * 4
        else:
            self.sp = ""
            self.nl = ""
            self.indent = ""
        self._vars = vars
        self._doc_strings = set()
        self._pending_stmts: list[str] = []
        self._temp_counter = 0

    def _wrap_parens(self, xs: str, enclosed: bool) -> str:
        if enclosed:
            return xs
        return f"({xs})"

    def _stmt(self, depth: int, content: str) -> str:
        return f"{depth * self.indent}{content};{self.nl}"

    def _block(self, depth: int, header: str, body: str) -> str:
        return f"{depth * self.indent}{header}{self.sp}{{{self.nl}{body}{depth * self.indent}}}{self.nl}"

    def _to_camel_case(self, s: str) -> str:
        i = s.find("_")
        prefix = ""
        while i > -1:
            if i == 0:
                prefix += s[0]
                s = s[1:]
            elif i == len(s) - 1:
                s = s[:-1]
            else:
                s = s[:i] + s[i + 1].upper() + s[i + 2:]
            i = s.find("_")
        return prefix + s

    def _to_xs_type(self, python_type: str) -> str:
        xs_type = self._TYPE_MAP.get(python_type)
        if xs_type is None:
            raise ValueError(f"not convertable type: {python_type}")
        return xs_type

    def _to_xs_modifier(self, python_type: str) -> str:
        xs_mod = self._MODIFIER_MAP.get(python_type)
        if xs_mod is None:
            raise ValueError(f"not convertable modifier: {python_type}")
        return xs_mod

    def _to_xs_function_type(self, expression: expr) -> str:
        if isinstance(expression, Constant) and expression.value is None:
            return "void"
        if isinstance(expression, Name):
            return self._to_xs_type(expression.id)
        raise ValueError(f"unexpected token {expression}")

    def _to_xs_arg(self, a: arg, default, ctx: XsContext) -> str:
        name = self._to_camel_case(a.arg)
        type = self._to_xs_type(a.annotation.id)
        xs = f"{type} {name}"
        if default is not None:
            xs += f"{self.sp}={self.sp}{self._to_xs_expression(default, ctx)}"
        return xs

    def _parse_cast_call(self, node) -> Optional[tuple[str, expr]]:
        if (isinstance(node, Call)
                and isinstance(node.func, Name)
                and node.func.id == "cast"
                and len(node.args) == 2
                and isinstance(node.args[0], Name)
                and node.args[0].id in self._ARRAY_CREATE_MAP):
            return node.args[0].id, node.args[1]
        return None

    def _infer_array_element_type(self, node) -> str:
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
        raise ValueError(f"cannot infer array element type from value")

    def _to_xs_array_create(self, element_type: str, default_node, size_node, ctx: XsContext) -> str:
        create_func = self._ARRAY_CREATE_MAP.get(element_type)
        if create_func is None:
            raise ValueError(f"unsupported array element type: {element_type}")

        size_xs = self._to_xs_expression(size_node, ctx, enclosed=True)
        default_xs = self._to_xs_expression(default_node, ctx, enclosed=True)

        zero_xs = self._ARRAY_ZERO_XS.get(element_type)
        if element_type == "XsVector":
            zero_xs = f"vector(0.0,{self.sp}0.0,{self.sp}0.0)"

        if zero_xs is not None and default_xs == zero_xs:
            return f"{create_func}({size_xs})"
        return f"{create_func}({size_xs},{self.sp}{default_xs})"

    def _parse_array_literal(self, value) -> tuple:
        if isinstance(value, List):
            raise ValueError("cannot create array from list literal - use [default] * size syntax")
        if not (isinstance(value, BinOp) and isinstance(value.op, Mult) and isinstance(value.left, List)):
            raise ValueError("array must be defined as [default_value] * size")

        list_node = value.left
        if len(list_node.elts) != 1:
            raise ValueError("array default must be a single-element list")

        default_node = list_node.elts[0]
        if self._unpack_constant(default_node) is None and not isinstance(default_node, Call):
            raise ValueError("array default value must be a literal")
        return default_node, value.right

    _ARRAY_LIST_NAMES = {"list", "List"}

    def _flush_pending(self) -> str:
        if not self._pending_stmts:
            return ""
        result = "".join(self._pending_stmts)
        self._pending_stmts.clear()
        return result

    def _next_temp_name(self) -> str:
        name = f"temp{self._temp_counter:08x}"
        self._temp_counter += 1
        return name

    def _annotation_element_type(self, annotation) -> Optional[str]:
        if (isinstance(annotation, Subscript)
                and isinstance(annotation.value, Name)
                and annotation.value.id in self._ARRAY_LIST_NAMES
                and isinstance(annotation.slice, Name)
                and annotation.slice.id in self._ARRAY_CREATE_MAP):
            return annotation.slice.id
        return None

    def _infer_list_literal_type(self, elements: list[expr]) -> str:
        inferred = set()
        for elt in elements:
            try:
                t = self._infer_array_element_type(elt)
                inferred.add(t)
            except ValueError:
                continue
        if not inferred:
            raise ValueError(
                "cannot infer array type from list literal: "
                "at least one element must be a constant or typed cast"
            )
        create_funcs = {self._ARRAY_CREATE_MAP[t] for t in inferred}
        if len(create_funcs) > 1:
            raise ValueError("mixed constant types in list literal are not supported")
        return sorted(inferred)[0]

    def _to_xs_list_literal_stmts(self, var_name: str, elements: list[expr],
                                   element_type: str, ctx: XsContext) -> str:
        create_func = self._ARRAY_CREATE_MAP[element_type]
        set_func = self._ARRAY_SET_MAP[element_type]
        saved_pending = self._pending_stmts
        self._pending_stmts = []
        xs = self._stmt(ctx.depth, f"int {var_name}{self.sp}={self.sp}{create_func}({len(elements)})")
        for i, elt in enumerate(elements):
            value_xs = self._to_xs_expression(elt, ctx, enclosed=True)
            xs += self._flush_pending()
            xs += self._stmt(ctx.depth, f"{set_func}({var_name},{self.sp}{i},{self.sp}{value_xs})")
        self._pending_stmts = saved_pending
        return xs

    def _to_xs_list_literal_expr(self, list_node: List, ctx: XsContext) -> str:
        elements = list_node.elts
        if not elements:
            raise ValueError("cannot create array from empty list literal")
        element_type = self._infer_list_literal_type(elements)
        temp_name = self._next_temp_name()
        self._pending_stmts.append(
            self._to_xs_list_literal_stmts(temp_name, elements, element_type, ctx)
        )
        return temp_name

    def _to_xs_variable_definition(self, a: AnnAssign, ctx: XsContext) -> str:
        if isinstance(a.annotation, Name):
            modifier = ""
            python_type = a.annotation.id
            type = self._to_xs_type(python_type)
        elif isinstance(a.annotation, Subscript) and isinstance(a.annotation.value, Name):
            python_type = None
            if a.annotation.value.id in self._ARRAY_LIST_NAMES:
                modifier = ""
                type = "int"
            else:
                modifier = self._to_xs_modifier(a.annotation.value.id) + " "
                if isinstance(a.annotation.slice, Name):
                    type = self._to_xs_type(a.annotation.slice.id)
                else:
                    raise ValueError("assignment must have a variable type")
        else:
            raise ValueError("assignment must have a variable type")

        if isinstance(a.target, Name):
            name = self._to_camel_case(a.target.id)
        else:
            raise ValueError("assignment must have a variable name")

        if isinstance(a.value, Subscript) and python_type is not None:
            value_xs = self._to_xs_array_get(a.value, python_type, ctx)
        elif isinstance(a.value, Subscript):
            value_xs = self._to_xs_array_get(a.value, "int", ctx)
        else:
            value_xs = self._to_xs_expression(a.value, ctx, enclosed=True)
        return self._stmt(ctx.depth, f"{modifier}{type} {name}{self.sp}={self.sp}{value_xs}")

    def _to_xs_array_get(self, subscript: Subscript, element_type: str, ctx: XsContext) -> str:
        get_func = self._ARRAY_GET_MAP.get(element_type)
        if get_func is None:
            raise ValueError(f"unsupported array element type for get: {element_type}")
        index_xs = self._to_xs_expression(subscript.slice, ctx, enclosed=True)
        if isinstance(subscript.value, Name):
            array_xs = self._to_camel_case(subscript.value.id)
        elif isinstance(subscript.value, Subscript):
            array_xs = self._to_xs_array_get(subscript.value, "int", ctx)
        else:
            raise ValueError("array get target must be a variable name or array access")
        return f"{get_func}({array_xs},{self.sp}{index_xs})"

    def _parse_nd_array_annotation(self, annotation) -> Optional[tuple[int, str]]:
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

    def _parse_nd_array_value(self, value, depth: int) -> Optional[tuple[list, Any]]:
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

    def _to_xs_nd_array_init_stmts(self, var_name: str, sizes: list, inner_element_type: str, inner_default_node, ctx: XsContext) -> str:
        outer_size_xs = self._to_xs_expression(sizes[0], ctx, enclosed=True)
        xs = self._stmt(ctx.depth, f"int {var_name}{self.sp}={self.sp}xsArrayCreateInt({outer_size_xs})")
        xs += self._to_xs_nd_array_fill_loop(var_name, sizes[0], sizes[1:], inner_element_type, inner_default_node, ctx)
        return xs

    def _to_xs_nd_array_fill_loop(self, parent_var: str, parent_size_node, sub_sizes: list, inner_element_type: str, inner_default_node, ctx: XsContext) -> str:
        loop_var = self._next_temp_name()
        parent_size_xs = self._to_xs_expression(parent_size_node, ctx, enclosed=True)
        header = f"for{self.sp}({loop_var}{self.sp}={self.sp}0;{self.sp}<{self.sp}{parent_size_xs})"
        if len(sub_sizes) == 1:
            create_xs = self._to_xs_array_create(inner_element_type, inner_default_node, sub_sizes[0], ctx)
            body_xs = self._stmt(ctx.depth + 1, f"xsArraySetInt({parent_var},{self.sp}{loop_var},{self.sp}{create_xs})")
        else:
            temp_var = self._next_temp_name()
            sub_size_xs = self._to_xs_expression(sub_sizes[0], ctx, enclosed=True)
            body_xs = self._stmt(ctx.depth + 1, f"int {temp_var}{self.sp}={self.sp}xsArrayCreateInt({sub_size_xs})")
            body_xs += self._stmt(ctx.depth + 1, f"xsArraySetInt({parent_var},{self.sp}{loop_var},{self.sp}{temp_var})")
            body_xs += self._to_xs_nd_array_fill_loop(temp_var, sub_sizes[0], sub_sizes[1:], inner_element_type, inner_default_node, ctx.indented())
        return self._block(ctx.depth, header, body_xs)

    def _to_xs_variable_assignment(self, a: Assign, ctx: XsContext) -> str:
        if len(a.targets) != 1:
            raise ValueError("only one target assignment is supported")
        target = a.targets[0]
        if isinstance(target, Name):
            name = self._to_camel_case(target.id)
        else:
            raise ValueError("assignment needs to be a variable")
        value_xs = self._to_xs_expression(a.value, ctx, enclosed=True)
        return self._stmt(ctx.depth, f"{name}{self.sp}={self.sp}{value_xs}")

    def _to_xs_array_set(self, target: Subscript, value, ctx: XsContext) -> str:
        index_xs = self._to_xs_expression(target.slice, ctx, enclosed=True)
        if isinstance(target.value, Name):
            array_xs = self._to_camel_case(target.value.id)
        elif isinstance(target.value, Subscript):
            array_xs = self._to_xs_array_get(target.value, "int", ctx)
        else:
            raise ValueError("array assignment target must be a variable name or array access")
        element_type = self._infer_array_element_type(value)
        set_func = self._ARRAY_SET_MAP.get(element_type)
        if set_func is None:
            raise ValueError(f"unsupported array element type for set: {element_type}")
        value_xs = self._to_xs_expression(value, ctx, enclosed=True)
        return self._stmt(ctx.depth, f"{set_func}({array_xs},{self.sp}{index_xs},{self.sp}{value_xs})")

    def _to_xs_variable_aug_assignment(self, a: AugAssign, ctx: XsContext) -> str:
        if isinstance(a.target, Name):
            name = self._to_camel_case(a.target.id)
        else:
            raise ValueError("assignment needs to be a variable")
        op = self._to_xs_binary_op(a.op)
        aug_value = self._unpack_constant(a.value)
        if aug_value == 1 and not isinstance(aug_value, bool) and op == "+":
            return self._stmt(ctx.depth, f"{name}++")
        if aug_value == 1 and not isinstance(aug_value, bool) and op == "-":
            return self._stmt(ctx.depth, f"{name}--")
        return self._stmt(ctx.depth, f"{name}{self.sp}={self.sp}{name}{self.sp}{op}{self.sp}{self._to_xs_expression(a.value, ctx)}")

    def _to_xs_expression_top(self, e: Expr, ctx: XsContext) -> str:
        if (isinstance(e.value, Constant) and isinstance(e.value.value, str)
                and e.value.value.strip().replace("\n", "").replace(" ", "") in self._doc_strings):
            return ""
        return self._stmt(ctx.depth, self._to_xs_expression(e.value, ctx))

    def _to_xs_binary_op(self, op) -> str:
        xs_op = self._OPERATOR_MAP.get(type(op))
        if xs_op is None:
            raise ValueError(f"unknown binary operator: {op}")
        return xs_op

    def _to_xs_expression(self, e: expr, ctx: XsContext, enclosed=False) -> str:
        if isinstance(e, Constant):
            return self._to_xs_constant(e.value, enclosed)
        if isinstance(e, Name):
            if e.id in ctx.replacements:
                return ctx.replacements[e.id]
            return self._to_camel_case(e.id)
        if isinstance(e, Call):
            if isinstance(e.func, Name) and e.func.id in self._macro_functions:
                return self._to_xs_constant(self._eval_macro_function(e), enclosed)
            return self._to_xs_call(e, ctx, enclosed)
        if isinstance(e, BinOp) and isinstance(e.op, Mult) and isinstance(e.left, List):
            default_node, size_node = self._parse_array_literal(e)
            element_type = self._infer_array_element_type(default_node)
            return self._to_xs_array_create(element_type, default_node, size_node, ctx)
        if isinstance(e, BinOp):
            left_xs = self._to_xs_expression(e.left, ctx)
            op_xs = self._to_xs_binary_op(e.op)
            right_xs = self._to_xs_expression(e.right, ctx)
            return self._wrap_parens(f"{left_xs}{self.sp}{op_xs}{self.sp}{right_xs}", enclosed)
        if isinstance(e, UnaryOp):
            value = self._unpack_constant(e)
            if value is not None:
                return self._to_xs_constant(value, enclosed)
            if isinstance(e.op, Not):
                return self._wrap_parens(
                    f"{self._to_xs_expression(e.operand, ctx)}{self.sp}=={self.sp}false", enclosed)
            raise ValueError(f"unsupported unary operator: {e}")
        if isinstance(e, Compare):
            if len(e.comparators) != 1 or len(e.ops) != 1:
                raise ValueError("comparison must have exactly 1 operator and 1 comparator")
            left_xs = self._to_xs_expression(e.left, ctx)
            op = self._to_xs_binary_op(e.ops[0])
            right_xs = self._to_xs_expression(e.comparators[0], ctx)
            return self._wrap_parens(f"{left_xs}{self.sp}{op}{self.sp}{right_xs}", enclosed)
        if isinstance(e, Attribute) and isinstance(e.value, Name) and e.value.id == "XsConstants":
            return self._to_camel_case(e.attr)
        if isinstance(e, JoinedStr):
            parts = [self._to_xs_expression(val, ctx) for val in e.values]
            return f"({f'{self.sp}+{self.sp}'.join(parts)})"
        if isinstance(e, FormattedValue):
            return self._to_xs_expression(e.value, ctx)
        if isinstance(e, BoolOp):
            op_xs = self._to_xs_binary_op(e.op)
            parts = [self._to_xs_expression(v, ctx) for v in e.values]
            return self._wrap_parens(f"{self.sp}{op_xs}{self.sp}".join(parts), enclosed)
        if isinstance(e, List):
            return self._to_xs_list_literal_expr(e, ctx)
        raise ValueError(f"Unsupported expression: {e}")

    def _to_xs_constant(self, value, enclosed: bool = False):
        if isinstance(value, str):
            return '"' + value.replace('"', '\\"') + '"'
        if isinstance(value, bool):
            return str(value).lower()
        if isinstance(value, int):
            if value > 999_999_999:
                if value > 2_147_483_647:
                    raise ValueError(f"xs int can't hold such big value: {value}")
                base = value // 10
                remainder = value % 10
                return self._wrap_parens(f"{base}{self.sp}*{self.sp}10{self.sp}+{self.sp}{remainder}", enclosed)
            if value < -999_999_999:
                if value < -2_147_483_648:
                    raise ValueError(f"xs int can't hold such small value: {value}")
                value = value * -1
                base = value // 10
                remainder = value % 10
                return self._wrap_parens(f"-{base}{self.sp}*{self.sp}10{self.sp}-{self.sp}{remainder}", enclosed)
            return f"{value}"
        if isinstance(value, float):
            return f"{value}"
        raise ValueError(f"Unsupported variable type: {value}")

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

    def _to_xs_numeric_cast(self, zero: str, arg, ctx: XsContext, enclosed: bool) -> str:
        value = self._unpack_constant(arg)
        if value is not None:
            return self._to_xs_constant(value, enclosed)
        xs = f"{zero}{self.sp}+{self.sp}{self._to_xs_expression(arg, ctx)}"
        return self._wrap_parens(xs, enclosed)

    def _to_xs_call(self, e: Call, ctx: XsContext, enclosed=False) -> str:
        if not isinstance(e.func, Name):
            raise ValueError(f"Function call must be referenced by name not: {e.func}")
        function_name = self._to_camel_case(e.func.id)
        if function_name == "str":
            xs = f'""{self.sp}+{self.sp}' + self._to_xs_expression(e.args[0], ctx)
            return self._wrap_parens(xs, enclosed)
        if function_name == "len":
            arg_xs = self._to_xs_expression(e.args[0], ctx, enclosed=True)
            return f"xsArrayGetSize({arg_xs})"
        if function_name == "cast":
            if len(e.args) != 2:
                raise ValueError("cast() requires exactly 2 arguments")
            inner = e.args[1]
            if isinstance(inner, Subscript):
                return self._to_xs_array_get(inner, e.args[0].id, ctx)
            return self._to_xs_expression(inner, ctx, enclosed=enclosed)
        zero = self._NUMERIC_CAST_ZEROS.get(function_name)
        if zero is not None:
            return self._to_xs_numeric_cast(zero, e.args[0], ctx, enclosed)
        args_xs = f",{self.sp}".join(
            [self._to_xs_expression(a, ctx, enclosed=True) for a in e.args])
        return f"{function_name}({args_xs})"

    def _to_xs_if(self, e: If, ctx: XsContext, els: bool = False) -> str:
        xs = ""
        cond_xs = self._to_xs_expression(e.test, ctx, enclosed=True)
        if e.test is not None and not els:
            xs += f"{ctx.depth * self.indent}if{self.sp}({cond_xs}){self.sp}{{{self.nl}"
        elif e.test is not None and els:
            xs += f"{ctx.depth * self.indent}}}{self.sp}else if{self.sp}({cond_xs}){self.sp}{{{self.nl}"
        else:
            raise ValueError("else with a test statement")
        xs += self._to_xs_body(e.body, ctx)

        if len(e.orelse) == 1 and isinstance(e.orelse[0], If):
            xs += self._to_xs_if(e.orelse[0], ctx, True)
        elif len(e.orelse) > 0:
            xs += f"{ctx.depth * self.indent}}}{self.sp}else{self.sp}{{{self.nl}"
            xs += self._to_xs_body(e.orelse, ctx)
            xs += f"{ctx.depth * self.indent}}}{self.nl}"
        else:
            xs += f"{ctx.depth * self.indent}}}{self.nl}"
        return xs

    def _to_xs_for(self, e: For, ctx: XsContext) -> str:
        if not (isinstance(e.iter, Call) and isinstance(e.iter.func, Name) and e.iter.func.id in {"range", "i32range"}):
            raise ValueError("for loops are only supported over range expressions")
        if not isinstance(e.target, Name):
            raise ValueError("loop target must be a new variable")

        loop_var = self._to_camel_case(e.target.id)
        start_node, end_node, step = self._parse_range_args(e.iter.args)

        if step == 1 or step == -1:
            positive = step > 0
            start_xs = "0" if start_node is None else self._to_xs_expression(start_node, ctx, enclosed=True)
            bound_xs = self._to_xs_for_bound(end_node, ctx, positive, True)
            header = f"for{self.sp}({loop_var}{self.sp}={self.sp}{start_xs};{self.sp}{bound_xs})"
            return self._block(ctx.depth, header, self._to_xs_body(e.body, ctx))

        xs = self._stmt(ctx.depth, f"int {loop_var}{self.sp}={self.sp}{self._to_xs_expression(start_node, ctx, enclosed=True)}")
        if isinstance(step, int):
            positive = step > 0
            op = "+" if positive else "-"
            step_xs = self._to_xs_constant(abs(step))
        else:
            positive = True
            op = "+"
            step_xs = self._to_xs_expression(step, ctx)
        bound_xs = self._to_xs_for_bound(end_node, ctx, positive, False)
        body_xs = self._to_xs_body(e.body, ctx)
        body_xs += self._stmt(ctx.depth + 1, f"{loop_var}{self.sp}={self.sp}{loop_var}{self.sp}{op}{self.sp}{step_xs}")
        xs += self._block(ctx.depth, f"while{self.sp}({loop_var}{self.sp}{bound_xs})", body_xs)
        return xs

    def _parse_range_args(self, args: list[expr]) -> tuple[Optional[expr], expr, int | expr]:
        if len(args) == 1:
            return None, args[0], 1
        if len(args) == 2:
            return args[0], args[1], 1
        if len(args) == 3:
            step = self._unpack_int_constant(args[2])
            if step is None:
                return args[0], args[1], args[2]
            if step == 0:
                raise ValueError("loop step cannot be 0")
            return args[0], args[1], step
        raise ValueError("range() takes 1 to 3 arguments")

    def _unpack_int_constant(self, expr: expr) -> Optional[int]:
        value = self._unpack_constant(expr)
        if not isinstance(value, int):
            return None
        return value

    def _to_xs_while(self, e: While, ctx: XsContext) -> str:
        header = f"while{self.sp}({self._to_xs_expression(e.test, ctx, enclosed=True)})"
        return self._block(ctx.depth, header, self._to_xs_body(e.body, ctx))

    def _to_xs_match(self, e: Match, ctx: XsContext) -> str:
        inner = ctx.indented()
        cases_xs = ""
        for case in e.cases:
            if isinstance(case.pattern, MatchValue):
                xs_case = self._to_xs_expression(case.pattern.value, ctx)
                cases_xs += self._block(inner.depth, f"case {xs_case}:", self._to_xs_body(case.body, inner))
            elif isinstance(case.pattern, MatchAs) and case.pattern.name is None:
                cases_xs += self._block(inner.depth, "default:", self._to_xs_body(case.body, inner))
            else:
                raise ValueError(f"unsupported complex case pattern: {case.pattern}")
        header = f"switch{self.sp}({self._to_xs_expression(e.subject, ctx, enclosed=True)})"
        return self._block(ctx.depth, header, cases_xs)

    def to_xs_function_definition(self, function: FunctionDef, ctx: XsContext, root_function: bool = True) -> str:
        type = self._to_xs_function_type(function.returns)
        name = self._to_camel_case(function.name)

        if len(function.args.args) != len(function.args.defaults):
            raise ValueError("all functions arguments must have default value")

        parameters_xs = self._to_xs_parameters(function, ctx)
        has_parameters = len(parameters_xs) > 0

        rule_modifier_xs = self._to_xs_rule_modifiers(function, root_function, has_parameters, type)
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
            header = f"{type} {name}({parameters_xs})"
        xs += self._block(ctx.depth, header, self._to_xs_body(function.body, ctx))
        return xs

    def _to_xs_parameters(self, function: FunctionDef, ctx: XsContext) -> str:
        parameters = [self._to_xs_arg(a, default, ctx) for a, default in zip(function.args.args, function.args.defaults)]
        return f",{self.sp}".join(parameters)

    def _to_xs_rule_modifiers(self, function: FunctionDef, root_function: bool, has_parameters: bool, type: str) -> str:
        rule_decorator = [d for d in function.decorator_list if
                          isinstance(d, Call) and isinstance(d.func, Name) and d.func.id == "xs_rule"]
        is_rule = len(rule_decorator) > 0
        if is_rule and (root_function or has_parameters or type != "void"):
            raise ValueError("can not have xs task with parameters or as a default root function")
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
                raise ValueError(f"not a keyword: {kw}")
        modifiers = []
        if rule_settings.get("group") is not None:
            modifiers.append(f"group {rule_settings['group']}")
        if rule_settings.get("active"):
            modifiers.append("active")
        else:
            modifiers.append("inactive")
        if rule_settings.get("high_frequency"):
            if rule_settings.get("min_interval") is not None or rule_settings.get("max_interval") is not None:
                raise ValueError("can not use both high_frequency and min/max_interval")
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

    def _to_xs_function(self, function, root_function: bool = True):
        source = textwrap.dedent(inspect.getsource(function))
        module_ast = ast.parse(source)
        if len(module_ast.body) != 1 or not isinstance(module_ast.body[0], FunctionDef):
            raise ValueError("top level must contain a single function")
        return self.to_xs_function_definition(module_ast.body[0], XsContext(), root_function)

    def _to_xs_body(self, body: list[expr | stmt], ctx: XsContext) -> str:
        xs = ""
        inner = ctx.indented()
        for e in body:
            if isinstance(e, AnnAssign) and isinstance(e.value, List):
                if not isinstance(e.target, Name):
                    raise ValueError("assignment must have a variable name")
                element_type = self._annotation_element_type(e.annotation)
                if element_type is None:
                    element_type = self._infer_list_literal_type(e.value.elts)
                stmt_xs = self._to_xs_list_literal_stmts(
                    self._to_camel_case(e.target.id), e.value.elts, element_type, inner)
            elif isinstance(e, AnnAssign):
                nd_result = self._try_to_xs_nd_array_init(e, inner)
                if nd_result is not None:
                    stmt_xs = nd_result
                else:
                    stmt_xs = self._to_xs_variable_definition(e, inner)
            elif isinstance(e, Assign) and len(e.targets) == 1 and isinstance(e.targets[0], Subscript):
                stmt_xs = self._to_xs_array_set(e.targets[0], e.value, inner)
            elif isinstance(e, Assign) and len(e.targets) == 1 and isinstance(e.targets[0], Name) and isinstance(e.value, List):
                element_type = self._infer_list_literal_type(e.value.elts)
                stmt_xs = self._to_xs_list_literal_stmts(
                    self._to_camel_case(e.targets[0].id), e.value.elts, element_type, inner)
            elif isinstance(e, Assign):
                stmt_xs = self._to_xs_variable_assignment(e, inner)
            elif isinstance(e, AugAssign):
                stmt_xs = self._to_xs_variable_aug_assignment(e, inner)
            elif isinstance(e, Expr):
                stmt_xs = self._to_xs_expression_top(e, inner)
            elif isinstance(e, If):
                stmt_xs = self._to_xs_if(e, inner)
            elif isinstance(e, For):
                stmt_xs = self._to_xs_for(e, inner)
            elif isinstance(e, While):
                stmt_xs = self._to_xs_while(e, inner)
            elif isinstance(e, Match):
                stmt_xs = self._to_xs_match(e, inner)
            elif isinstance(e, With):
                stmt_xs = self._to_xs_macro_with(e, ctx)
            elif isinstance(e, Return):
                stmt_xs = self._to_xs_return(e, inner)
            elif isinstance(e, (Pass, Global)):
                stmt_xs = ""
            else:
                raise ValueError(e)
            xs += self._flush_pending() + stmt_xs
        return xs

    def _to_xs_return(self, e: Return, ctx: XsContext) -> str:
        if e.value is None:
            return self._stmt(ctx.depth, "return")
        return self._stmt(ctx.depth, f"return{self.sp}({self._to_xs_expression(e.value, ctx, enclosed=True)})")

    def _eval_macro_function(self, call: Call) -> any:
        if not isinstance(call.func, Name):
            raise ValueError("Macro should be a name token")
        return self._eval_macro_var(call)

    def _eval_macro_var(self, call: Call) -> any:
        if 1 <= len(call.args) <= 2 and isinstance(call.args[0], Constant) and isinstance(
                call.args[0].value, str):
            return eval(call.args[0].value, self._vars)
        raise ValueError("macro should have 1 string constant argument")

    def _to_xs_macro_with(self, e: With, ctx: XsContext) -> str:
        if not (len(e.items) == 1 and isinstance(e.items[0].context_expr, Call)):
            raise ValueError("incorrect repeated macro usage")

        if isinstance(e.items[0].optional_vars, Name):
            names = [e.items[0].optional_vars.id]
        elif isinstance(e.items[0].optional_vars, Tuple):
            names = [n.id for n in e.items[0].optional_vars.elts if isinstance(n, Name)]
        else:
            raise ValueError("only unpacked single or deconstructer tuple are allowed")
        iterable_value = self._eval_macro_function(e.items[0].context_expr)
        if not isinstance(iterable_value, Iterable):
            raise ValueError("repeater macro needs a reference to an iterable")
        xs = ""
        for value in iterable_value:
            new_replacements = ctx.replacements.copy()
            if isinstance(value, tuple):
                value_batch = list(value)
            else:
                value_batch = [value]
            for name, val in zip(names, value_batch):
                new_replacements[name] = self._to_xs_constant(val)
            xs += self._to_xs_body(e.body, ctx.with_replacements(new_replacements))
        return xs

    def _to_xs_for_bound(self, param: expr, ctx: XsContext, positive: bool, enclosed: bool) -> str:
        expected_op = Add if positive else Sub
        inclusive_sign = "<=" if positive else ">="
        if isinstance(param, BinOp) and isinstance(param.op, expected_op):
            pairs = [(param.left, param.right), (param.right, param.left)] if positive else [(param.left, param.right)]
            for main, other in pairs:
                other_value = self._unpack_constant(other)
                if other_value == 1 and not isinstance(other_value, bool):
                    return f"{inclusive_sign}{self.sp}{self._to_xs_expression(main, ctx, enclosed=enclosed)}"
        exclusive_sign = "<" if positive else ">"
        return f"{exclusive_sign}{self.sp}{self._to_xs_expression(param, ctx, enclosed=enclosed)}"
