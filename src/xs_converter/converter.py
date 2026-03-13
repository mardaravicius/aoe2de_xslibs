import ast
import inspect
import re
from ast import FunctionDef, Constant, Name, expr, arg, Expr, AnnAssign, Call, Assign, BinOp, Add, Sub, Mod, Mult, Div, \
    operator, If, Compare, Eq, Gt, GtE, Lt, LtE, NotEq, cmpop, For, While, AugAssign, Match, MatchValue, MatchAs, \
    Return, Pass, Subscript, stmt, Attribute, keyword, With, Tuple, UnaryOp, USub, JoinedStr, FormattedValue, Global, \
    BoolOp, Or, And, Not, FloorDiv
from dataclasses import dataclass, field
from typing import Iterable, Optional

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
    macro_functions = {
        macro_pass_value.__name__,
    }
    macro_repeat_functions = {
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

    @staticmethod
    def to_xs_script(*functions, indent: bool, **kwargs) -> str:
        xs = ""
        for i, f in enumerate(functions):
            root_f = i == 0
            converter = PythonToXsConverter(indent, kwargs)
            xs += converter.to_xs_function(f, root_f)
            if i < len(functions) - 1:
                xs += converter.nl
        return xs

    def __init__(self, indent: bool, vars: dict[str, any]):
        if indent:
            self.sp = " "
            self.nl = "\n"
            self.indent = " " * 4
        else:
            self.sp = ""
            self.nl = ""
            self.indent = ""
        self.vars = vars
        self.doc_strings = set()

    def _wrap_parens(self, xs: str, enclosed: bool) -> str:
        if enclosed:
            return xs
        return f"({xs})"

    def _stmt(self, depth: int, content: str) -> str:
        return f"{depth * self.indent}{content};{self.nl}"

    def _block(self, depth: int, header: str, body: str) -> str:
        return f"{depth * self.indent}{header}{self.sp}{{{self.nl}{body}{depth * self.indent}}}{self.nl}"

    def to_camel_case(self, s: str) -> str:
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

    def to_xs_type(self, python_type: str) -> str:
        xs_type = self._TYPE_MAP.get(python_type)
        if xs_type is None:
            raise ValueError(f"not convertable type: {python_type}")
        return xs_type

    def to_xs_modifier(self, python_type: str) -> str:
        xs_mod = self._MODIFIER_MAP.get(python_type)
        if xs_mod is None:
            raise ValueError(f"not convertable modifier: {python_type}")
        return xs_mod

    def to_xs_function_type(self, expression: expr) -> str:
        if isinstance(expression, Constant) and expression.value is None:
            return "void"
        if isinstance(expression, Name):
            return self.to_xs_type(expression.id)
        raise ValueError(f"unexpected token {expression}")

    def to_xs_arg(self, a: arg, default, ctx: XsContext) -> str:
        name = self.to_camel_case(a.arg)
        type = self.to_xs_type(a.annotation.id)
        xs = f"{type} {name}"
        if default is not None:
            xs += f"{self.sp}={self.sp}{self.to_xs_expression(default, ctx)}"
        return xs

    def to_xs_variable_definition(self, a: AnnAssign, ctx: XsContext) -> str:
        if isinstance(a.annotation, Name):
            modifier = ""
            type = self.to_xs_type(a.annotation.id)
        elif isinstance(a.annotation, Subscript):
            if isinstance(a.annotation.value, Name):
                modifier = self.to_xs_modifier(a.annotation.value.id) + " "
            else:
                raise ValueError("assignment with xs modifier type must have the modifier type")
            if isinstance(a.annotation.slice, Name):
                type = self.to_xs_type(a.annotation.slice.id)
            else:
                raise ValueError("assignment must have a variable type")
        else:
            raise ValueError("assignment must have a variable type")

        if isinstance(a.target, Name):
            name = self.to_camel_case(a.target.id)
        else:
            raise ValueError("assignment must have a variable name")
        value_xs = self.to_xs_expression(a.value, ctx, enclosed=True)
        return self._stmt(ctx.depth, f"{modifier}{type} {name}{self.sp}={self.sp}{value_xs}")

    def to_xs_variable_assignment(self, a: Assign, ctx: XsContext) -> str:
        if len(a.targets) != 1:
            raise ValueError("only one target assignment is supported")
        target = a.targets[0]
        if isinstance(target, Name):
            name = self.to_camel_case(target.id)
        else:
            raise ValueError("assignment needs to be a variable")
        value_xs = self.to_xs_expression(a.value, ctx, enclosed=True)
        return self._stmt(ctx.depth, f"{name}{self.sp}={self.sp}{value_xs}")

    def to_xs_variable_aug_assignment(self, a: AugAssign, ctx: XsContext) -> str:
        if isinstance(a.target, Name):
            name = self.to_camel_case(a.target.id)
        else:
            raise ValueError("assignment needs to be a variable")
        op = self.to_xs_binary_op(a.op)
        if isinstance(a.value, Constant) and a.value.value == 1 and op == "+":
            return self._stmt(ctx.depth, f"{name}++")
        if isinstance(a.value, Constant) and a.value.value == 1 and op == "-":
            return self._stmt(ctx.depth, f"{name}--")
        return self._stmt(ctx.depth, f"{name}{self.sp}={self.sp}{name}{self.sp}{op}{self.sp}{self.to_xs_expression(a.value, ctx)}")

    def to_xs_expression_top(self, e: Expr, ctx: XsContext) -> str:
        if (isinstance(e.value, Constant) and isinstance(e.value.value, str)
                and e.value.value.strip().replace("\n", "").replace(" ", "") in self.doc_strings):
            return ""
        return self._stmt(ctx.depth, self.to_xs_expression(e.value, ctx))

    def to_xs_binary_op(self, op) -> str:
        xs_op = self._OPERATOR_MAP.get(type(op))
        if xs_op is None:
            raise ValueError(f"unknown binary operator: {op}")
        return xs_op

    def to_xs_expression(self, e: expr, ctx: XsContext, enclosed=False) -> str:
        if isinstance(e, Constant):
            return self.to_xs_constant(e.value, enclosed)
        if isinstance(e, Name):
            if e.id in ctx.replacements:
                return ctx.replacements[e.id]
            return self.to_camel_case(e.id)
        if isinstance(e, Call):
            if e.func.id in self.macro_functions:
                return self.to_xs_constant(self.eval_macro_function(e), enclosed)
            return self.to_xs_call(e, ctx, enclosed)
        if isinstance(e, BinOp):
            left_xs = self.to_xs_expression(e.left, ctx)
            op_xs = self.to_xs_binary_op(e.op)
            right_xs = self.to_xs_expression(e.right, ctx)
            return self._wrap_parens(f"{left_xs}{self.sp}{op_xs}{self.sp}{right_xs}", enclosed)
        if isinstance(e, UnaryOp):
            if isinstance(e.op, USub) and isinstance(e.operand, Constant):
                return self.to_xs_constant(e.operand.value * -1, enclosed)
            if isinstance(e.op, Not):
                return self._wrap_parens(
                    f"{self.to_xs_expression(e.operand, ctx)}{self.sp}=={self.sp}false", enclosed)
            raise ValueError(f"unsupported unary operator: {e}")
        if isinstance(e, Compare):
            if len(e.comparators) != 1 or len(e.ops) != 1:
                raise ValueError("comparison must have exactly 1 operator and 1 comparator")
            left_xs = self.to_xs_expression(e.left, ctx)
            op = self.to_xs_binary_op(e.ops[0])
            right_xs = self.to_xs_expression(e.comparators[0], ctx)
            return self._wrap_parens(f"{left_xs}{self.sp}{op}{self.sp}{right_xs}", enclosed)
        if isinstance(e, Attribute) and isinstance(e.value, Name) and e.value.id == "XsConstants":
            return self.to_camel_case(e.attr)
        if isinstance(e, JoinedStr):
            parts = [self.to_xs_expression(val, ctx) for val in e.values]
            return f"({f'{self.sp}+{self.sp}'.join(parts)})"
        if isinstance(e, FormattedValue):
            return self.to_xs_expression(e.value, ctx)
        if isinstance(e, BoolOp):
            op_xs = self.to_xs_binary_op(e.op)
            left_xs = self.to_xs_expression(e.values[0], ctx)
            right_xs = self.to_xs_expression(e.values[1], ctx)
            return self._wrap_parens(f"{left_xs}{self.sp}{op_xs}{self.sp}{right_xs}", enclosed)
        raise ValueError(f"Unsupported expression: {expr}")

    def to_xs_constant(self, value, enclosed: bool = False):
        if isinstance(value, str):
            return '"' + value.replace('"', '\\"') + '"'
        if isinstance(value, bool):
            return str(value).lower()
        if isinstance(value, int):
            if value > 999_999_999:
                if value > 2_147_483_647:
                    raise ValueError(f"xs int can't hold such big value: {value}")
                base = int(value / 10)
                remainder = int(value % 10)
                return self._wrap_parens(f"{base}{self.sp}*{self.sp}10{self.sp}+{self.sp}{remainder}", enclosed)
            if value < -999_999_999:
                if value < -2_147_483_648:
                    raise ValueError(f"xs int can't hold such small value: {value}")
                value = value * -1
                base = int(value / 10)
                remainder = int(value % 10)
                return self._wrap_parens(f"-{base}{self.sp}*{self.sp}10{self.sp}-{self.sp}{remainder}", enclosed)
            return f"{value}"
        if isinstance(value, float):
            return f"{value}"
        raise ValueError(f"Unsupported variable type: {value}")

    def _is_literal_constant(self, node) -> bool:
        return ((isinstance(node, UnaryOp) and isinstance(node.op, USub)
                 and isinstance(node.operand, Constant))
                or isinstance(node, Constant))

    def _to_xs_numeric_cast(self, zero: str, arg, ctx: XsContext, enclosed: bool) -> str:
        if self._is_literal_constant(arg):
            if isinstance(arg, UnaryOp):
                return self.to_xs_expression(arg, ctx, enclosed=enclosed)
            return self.to_xs_constant(arg.value, enclosed)
        xs = f"{zero}{self.sp}+{self.sp}{self.to_xs_expression(arg, ctx)}"
        return self._wrap_parens(xs, enclosed)

    def to_xs_call(self, e: Call, ctx: XsContext, enclosed=False) -> str:
        if not isinstance(e.func, Name):
            raise ValueError(f"Function call must be referenced by name not: {e.func}")
        function_name = self.to_camel_case(e.func.id)
        if function_name == "str":
            xs = f'""{self.sp}+{self.sp}' + self.to_xs_expression(e.args[0], ctx)
            return self._wrap_parens(xs, enclosed)
        zero = self._NUMERIC_CAST_ZEROS.get(function_name)
        if zero is not None:
            return self._to_xs_numeric_cast(zero, e.args[0], ctx, enclosed)
        args_xs = f",{self.sp}".join(
            [self.to_xs_expression(a, ctx, enclosed=True) for a in e.args])
        return f"{function_name}({args_xs})"

    def to_xs_if(self, e: If, ctx: XsContext, els: bool = False) -> str:
        xs = ""
        cond_xs = self.to_xs_expression(e.test, ctx, enclosed=True)
        if e.test is not None and not els:
            xs += f"{ctx.depth * self.indent}if{self.sp}({cond_xs}){self.sp}{{{self.nl}"
        elif e.test is not None and els:
            xs += f"{ctx.depth * self.indent}}}{self.sp}else if{self.sp}({cond_xs}){self.sp}{{{self.nl}"
        else:
            raise ValueError("else with a test statement")
        xs += self.to_xs_body(e.body, ctx)

        if len(e.orelse) == 1 and isinstance(e.orelse[0], If):
            xs += self.to_xs_if(e.orelse[0], ctx, True)
        elif len(e.orelse) > 0:
            xs += f"{ctx.depth * self.indent}}}{self.sp}else{self.sp}{{{self.nl}"
            xs += self.to_xs_body(e.orelse, ctx)
            xs += f"{ctx.depth * self.indent}}}{self.nl}"
        else:
            xs += f"{ctx.depth * self.indent}}}{self.nl}"
        return xs

    def to_xs_for(self, e: For, ctx: XsContext) -> str:
        if not (isinstance(e.iter, Call) and isinstance(e.iter.func, Name) and e.iter.func.id in {"range", "i32range"}):
            raise ValueError("for loops are only supported over range expressions")
        if not isinstance(e.target, Name):
            raise ValueError("loop target must be a new variable")

        xs_loop_var = self.to_camel_case(e.target.id)
        args = e.iter.args

        if 2 >= len(args) > 0 or (len(args) == 3 and self._unpack_int_constant(args[2]) in {1, -1}):
            if len(args) == 1:
                from_xs = "0"
                to_xs = self._to_xs_for_bound(args[0], ctx, True, True)
            else:
                from_xs = self.to_xs_expression(args[0], ctx, enclosed=True)
                positive = self._unpack_int_constant(args[2]) != -1 if len(args) == 3 else True
                to_xs = self._to_xs_for_bound(args[1], ctx, positive, True)
            header = f"for{self.sp}({xs_loop_var}{self.sp}={self.sp}{from_xs};{self.sp}{to_xs})"
            return self._block(ctx.depth, header, self.to_xs_body(e.body, ctx))

        if len(args) != 3:
            raise ValueError("for loops are only supported over range expressions")

        xs = self._stmt(ctx.depth, f"int {xs_loop_var}{self.sp}={self.sp}{self.to_xs_expression(args[0], ctx, enclosed=True)}")
        increment_val = self._unpack_int_constant(args[2])
        if increment_val is None or isinstance(increment_val, float):
            raise ValueError("loop increment value must be a constant")
        if increment_val == 0:
            raise ValueError("last range arg can't be 0")
        if increment_val > 0:
            increment_xs = f"{self.sp}={self.sp}{xs_loop_var}{self.sp}+{self.sp}{self.to_xs_constant(increment_val)}"
        else:
            increment_xs = f"{self.sp}={self.sp}{xs_loop_var}{self.sp}-{self.sp}{self.to_xs_constant(abs(increment_val))}"

        to_xs = self._to_xs_for_bound(args[1], ctx, increment_val >= 0, False)
        body_xs = self.to_xs_body(e.body, ctx)
        body_xs += self._stmt(ctx.depth + 1, f"{xs_loop_var}{increment_xs}")
        xs += self._block(ctx.depth, f"while{self.sp}({xs_loop_var}{self.sp}{to_xs})", body_xs)
        return xs

    def _unpack_int_constant(self, expr) -> Optional[int]:
        if isinstance(expr, UnaryOp) and isinstance(expr.op, USub) and isinstance(
            expr.operand, Constant) and isinstance(expr.operand.value, int):
            return expr.operand.value * -1
        if isinstance(expr, Constant) and isinstance(expr.value, int):
            return expr.value
        return None

    def to_xs_while(self, e: While, ctx: XsContext) -> str:
        header = f"while{self.sp}({self.to_xs_expression(e.test, ctx, enclosed=True)})"
        return self._block(ctx.depth, header, self.to_xs_body(e.body, ctx))

    def to_xs_match(self, e: Match, ctx: XsContext) -> str:
        inner = ctx.indented()
        cases_xs = ""
        for case in e.cases:
            if isinstance(case.pattern, MatchValue):
                xs_case = self.to_xs_expression(case.pattern.value, ctx)
                cases_xs += self._block(inner.depth, f"case {xs_case}:", self.to_xs_body(case.body, inner))
            elif isinstance(case.pattern, MatchAs) and case.pattern.name is None:
                cases_xs += self._block(inner.depth, "default:", self.to_xs_body(case.body, inner))
            else:
                raise ValueError(f"unsupported complex case pattern: {case.pattern}")
        header = f"switch{self.sp}({self.to_xs_expression(e.subject, ctx, enclosed=True)})"
        return self._block(ctx.depth, header, cases_xs)

    def to_xs_function_definition(self, function: FunctionDef, ctx: XsContext, root_function: bool = True) -> str:
        type = self.to_xs_function_type(function.returns)
        name = self.to_camel_case(function.name)

        if len(function.args.args) != len(function.args.defaults):
            raise ValueError("all functions arguments must have default value")

        parameters_xs = self._to_xs_parameters(function, ctx)
        has_parameters = len(parameters_xs) > 0

        rule_modifier_xs = self._to_xs_rule_modifiers(function, root_function, has_parameters, type)
        has_rules = len(rule_modifier_xs) > 0
        xs = ""
        doc = ast.get_docstring(function)
        if doc is not None:
            self.doc_strings.add(doc.replace("\n", "").replace(" ", ""))
        if doc is not None and len(self.indent) > 0:
            doc = re.sub(r'`([a-zA-Z_][a-zA-Z0-9_]*)`',
                         lambda m: '`' + self.to_camel_case(m.group(1)) + '`', doc)
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
        xs += self._block(ctx.depth, header, self.to_xs_body(function.body, ctx))
        return xs

    def _to_xs_parameters(self, function: FunctionDef, ctx: XsContext) -> str:
        parameters = [self.to_xs_arg(a, default, ctx) for a, default in zip(function.args.args, function.args.defaults)]
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
            if isinstance(kw, keyword) and (kw.value, Constant):
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
            if "min_interval" in rule_settings or "max_interval" in rule_settings:
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

    def to_xs_function(self, function, root_function: bool = True):
        source = inspect.getsource(function)
        module_ast = ast.parse(source)
        if len(module_ast.body) != 1 or not isinstance(module_ast.body[0], FunctionDef):
            raise ValueError("top level must contain a single function")
        return self.to_xs_function_definition(module_ast.body[0], XsContext(), root_function)

    def to_xs_body(self, body: list[expr | stmt], ctx: XsContext) -> str:
        xs = ""
        inner = ctx.indented()
        for e in body:
            if isinstance(e, AnnAssign):
                xs += self.to_xs_variable_definition(e, inner)
            elif isinstance(e, Assign):
                xs += self.to_xs_variable_assignment(e, inner)
            elif isinstance(e, AugAssign):
                xs += self.to_xs_variable_aug_assignment(e, inner)
            elif isinstance(e, Expr):
                xs += self.to_xs_expression_top(e, inner)
            elif isinstance(e, If):
                xs += self.to_xs_if(e, inner)
            elif isinstance(e, For):
                xs += self.to_xs_for(e, inner)
            elif isinstance(e, While):
                xs += self.to_xs_while(e, inner)
            elif isinstance(e, Match):
                xs += self.to_xs_match(e, inner)
            elif isinstance(e, With):
                xs += self.to_xs_macro_with(e, ctx)
            elif isinstance(e, Return):
                xs += self.to_xs_return(e, inner)
            elif isinstance(e, (Pass, Global)):
                pass
            else:
                raise ValueError(e)
        return xs

    def to_xs_return(self, e: Return, ctx: XsContext) -> str:
        if e.value is None:
            return self._stmt(ctx.depth, "return")
        return self._stmt(ctx.depth, f"return{self.sp}({self.to_xs_expression(e.value, ctx, enclosed=True)})")

    def eval_macro_function(self, call: Call) -> any:
        if not isinstance(call.func, Name):
            raise ValueError("Macro should be a name token")
        return self._eval_macro_var(call)

    def _eval_macro_var(self, call: Call) -> any:
        if 1 <= len(call.args) <= 2 and isinstance(call.args[0], Constant) and isinstance(
                call.args[0].value, str):
            return eval(call.args[0].value, self.vars)
        raise ValueError("macro should have 1 string constant argument")

    def to_xs_macro_with(self, e: With, ctx: XsContext) -> str:
        if not (len(e.items) == 1 and isinstance(e.items[0].context_expr, Call)):
            raise ValueError("incorrect repeated macro usage")

        if isinstance(e.items[0].optional_vars, Name):
            names = [e.items[0].optional_vars.id]
        elif isinstance(e.items[0].optional_vars, Tuple):
            names = [n.id for n in e.items[0].optional_vars.dims if isinstance(n, Name)]
        else:
            raise ValueError("only unpacked single or deconstructer tuple are allowed")
        iterable_value = self.eval_macro_function(e.items[0].context_expr)
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
                new_replacements[name] = self.to_xs_constant(val)
            xs += self.to_xs_body(e.body, ctx.with_replacements(new_replacements))
        return xs

    def _to_xs_for_bound(self, param: expr, ctx: XsContext, positive: bool, enclosed: bool) -> str:
        expected_op = Add if positive else Sub
        inclusive_sign = "<=" if positive else ">="
        if isinstance(param, BinOp) and isinstance(param.op, expected_op):
            for main, other in [(param.left, param.right), (param.right, param.left)]:
                if isinstance(other, Constant) and other.value == 1:
                    return f"{inclusive_sign}{self.sp}{self.to_xs_expression(main, ctx, enclosed=enclosed)}"
        exclusive_sign = "<" if positive else ">"
        return f"{exclusive_sign}{self.sp}{self.to_xs_expression(param, ctx, enclosed=enclosed)}"
