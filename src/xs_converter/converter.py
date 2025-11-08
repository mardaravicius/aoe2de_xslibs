import ast
import inspect
from ast import FunctionDef, Constant, Name, expr, arg, Expr, AnnAssign, Call, Assign, BinOp, Add, Sub, Mod, Mult, Div, \
    operator, If, Compare, Eq, Gt, GtE, Lt, LtE, NotEq, cmpop, For, While, AugAssign, Match, MatchValue, MatchAs, \
    Return, Pass, Subscript, stmt, Attribute, keyword, With, Tuple, UnaryOp, USub, JoinedStr, FormattedValue, Global, \
    BoolOp, Or, And, Not, FloorDiv
from typing import Iterable, Optional

from xs_converter.macro import macro_pass_value, macro_repeat_with_iterable


class PythonToXsConverter:
    macro_functions = {
        macro_pass_value.__name__,
    }
    macro_repeat_functions = {
        macro_repeat_with_iterable.__name__,
    }

    @staticmethod
    def to_xs_script(*functions, indent: bool, **kwargs) -> str:
        xs = ""
        for i, f in enumerate(functions):
            root_f = i == 0
            converter = PythonToXsConverter(indent, kwargs)
            xs += converter.to_xs_function(f, root_f)
            if i < len(functions) - 1:
                xs += converter.n
        return xs

    def __init__(self, indent: bool, vars: dict[str, any]):
        if indent:
            self.s = " "
            self.n = "\n"
            self.i = " " * 4
        else:
            self.s = ""
            self.n = ""
            self.i = ""
        self.vars = vars
        self.doc_strings = set()

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
        if python_type == 'int' or python_type == 'int32':
            return 'int'
        if python_type == 'float' or python_type == 'float32':
            return 'float'
        if python_type == 'bool':
            return 'bool'
        if python_type == 'str':
            return 'string'
        if python_type == 'XsVector':
            return 'vector'
        raise ValueError(f"not convertable type: {python_type}")

    def to_xs_modifier(self, python_type: str) -> str:
        if python_type == 'XsStatic':
            return 'static'
        if python_type == 'XsConst':
            return 'const'
        if python_type == 'XsExtern':
            return 'extern'
        if python_type == 'XsExternConst':
            return 'extern const'
        raise ValueError(f"not convertable modifier: {python_type}")

    def to_xs_function_type(self, expression: expr) -> str:
        if isinstance(expression, Constant) and expression.value is None:
            return "void"
        elif isinstance(expression, Name):
            return self.to_xs_type(expression.id)
        raise ValueError(f"unexpected token {expression}")

    def to_xs_arg(self, a: arg, default, vars_to_replace: dict[str, str]) -> str:
        name = self.to_camel_case(a.arg)
        type = self.to_xs_type(a.annotation.id)

        xs = f"{type} {name}"
        if default is not None:
            xs += f"{self.s}={self.s}{self.to_xs_expression(default, vars_to_replace)}"
        return xs

    def to_xs_variable_definition(self, a: AnnAssign, i: int, vars_to_replace: dict[str, str]) -> str:

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
        return f"{i * self.i}{modifier}{type} {name}{self.s}={self.s}{self.to_xs_expression(a.value, vars_to_replace, enclosed=True)};{self.n}"

    def to_xs_variable_assignment(self, a: Assign, i: int, vars_to_replace: dict[str, str]) -> str:
        if len(a.targets) != 1:
            raise ValueError("only one target assignment is supported")
        target = a.targets[0]
        if isinstance(target, Name):
            name = self.to_camel_case(target.id)
        else:
            raise ValueError("assignment needs to be a variable")
        return f"{i * self.i}{name}{self.s}={self.s}{self.to_xs_expression(a.value, vars_to_replace, enclosed=True)};{self.n}"

    def to_xs_variable_aug_assignment(self, a: AugAssign, i: int, vars_to_replace: dict[str, str]) -> str:
        if isinstance(a.target, Name):
            name = self.to_camel_case(a.target.id)
        else:
            raise ValueError("assignment needs to be a variable")
        operator = self.to_xs_binary_op(a.op)
        if isinstance(a.value, Constant) and a.value.value == 1 and operator == "+":
            return f"{i * self.i}{name}++;{self.n}"
        if isinstance(a.value, Constant) and a.value.value == 1 and operator == "-":
            return f"{i * self.i}{name}--;{self.n}"
        return f"{i * self.i}{name}{self.s}={self.s}{name}{self.s}{operator}{self.s}{self.to_xs_expression(a.value, vars_to_replace)};{self.n}"

    def to_xs_expression_top(self, e: Expr, i: int, vars_to_replace: dict[str, str]) -> str:
        if isinstance(e.value, Constant) and isinstance(e.value.value, str) and e.value.value.strip().replace("\n",
                                                                                                              "").replace(
            " ", "") in self.doc_strings:
            return ""
        return f"{i * self.i}{self.to_xs_expression(e.value, vars_to_replace)};{self.n}"

    def to_xs_binary_op(self, op: operator | cmpop):
        if isinstance(op, Add):
            return "+"
        if isinstance(op, Sub):
            return "-"
        if isinstance(op, Mult):
            return "*"
        if isinstance(op, Div):
            return "/"
        if isinstance(op, FloorDiv):
            return "/"
        if isinstance(op, Mod):
            return "%"
        if isinstance(op, Eq):
            return "=="
        if isinstance(op, NotEq):
            return "!="
        if isinstance(op, Gt):
            return ">"
        if isinstance(op, GtE):
            return ">="
        if isinstance(op, Lt):
            return "<"
        if isinstance(op, LtE):
            return "<="
        raise ValueError(f"unknown binary operator: {op}")

    def to_xs_expression(self, e: expr, vars_to_replace: dict[str, str], enclosed=False) -> str:
        if isinstance(e, Constant):
            return self.to_xs_constant(e.value, enclosed)
        if isinstance(e, Name):
            if e.id in vars_to_replace:
                return vars_to_replace[e.id]
            else:
                return self.to_camel_case(e.id)
        elif isinstance(e, Call):
            if e.func.id in self.macro_functions:
                return self.to_xs_constant(self.eval_macro_function(e), enclosed)
            else:
                return self.to_xs_call(e, vars_to_replace, enclosed)
        elif isinstance(e, BinOp):
            left_xs = self.to_xs_expression(e.left, vars_to_replace)
            op_xs = self.to_xs_binary_op(e.op)
            right_xs = self.to_xs_expression(e.right, vars_to_replace)
            xs = f"{left_xs}{self.s}{op_xs}{self.s}{right_xs}"
            if not enclosed:
                xs = f"({xs})"
            return xs
        elif isinstance(e, UnaryOp):
            if isinstance(e.op, USub) and isinstance(e.operand, Constant):
                return self.to_xs_constant(e.operand.value * -1, enclosed)
            if isinstance(e.op, Not):
                xs = f"{self.to_xs_expression(e.operand, vars_to_replace)}{self.s}=={self.s}false"
                if not enclosed:
                    xs = f"({xs})"
                return xs
            raise ValueError(f"unsupported unary operator: {e}")
        elif isinstance(e, Compare):
            left_xs = self.to_xs_expression(e.left, vars_to_replace)
            if len(e.comparators) > 1:
                raise ValueError(f"must have only 1 value to compare to, instead got: {len(e.comparators)}")
            if len(e.comparators) == 1:
                if len(e.ops) != 1:
                    raise ValueError(f"must have only 1 operator to compare to, instead got: {len(e.ops)}")
                operator = self.to_xs_binary_op(e.ops[0])
                right_xs = self.to_xs_expression(e.comparators[0], vars_to_replace)
                xs = f"{left_xs}{self.s}{operator}{self.s}{right_xs}"
                if not enclosed:
                    xs = f"({xs})"
                return xs
            else:
                return left_xs
        elif isinstance(e, Attribute) and isinstance(e.value, Name) and e.value.id == "XsConstants":
            return self.to_camel_case(e.attr)
        elif isinstance(e, JoinedStr):
            xs = "("
            xs += f"{self.s}+{self.s}".join([self.to_xs_expression(val, vars_to_replace) for val in e.values])
            xs += ")"
            return xs
        elif isinstance(e, FormattedValue):
            return self.to_xs_expression(e.value, vars_to_replace)
        elif isinstance(e, BoolOp):
            xs = self.to_xs_bool_op(e, vars_to_replace)
            if not enclosed:
                xs = f"({xs})"
            return xs
        else:
            raise ValueError(f"Unsupported expression: {expr}")

    def to_xs_bool_op(self, op, vars_to_replace: dict[str, str]) -> str:
        if isinstance(op.op, Or):
            return f"{self.to_xs_expression(op.values[0], vars_to_replace)}{self.s}||{self.s}{self.to_xs_expression(op.values[1], vars_to_replace)}"
        if isinstance(op.op, And):
            return f"{self.to_xs_expression(op.values[0], vars_to_replace)}{self.s}&&{self.s}{self.to_xs_expression(op.values[1], vars_to_replace)}"
        raise ValueError(f"Unsupported bool op: {op}")

    def to_xs_constant(self, value, enclosed: bool = False):
        if isinstance(value, str):
            return '"' + value.replace('"', '\\"') + '"'
        if isinstance(value, bool):
            return f'{str(value).lower()}'
        if isinstance(value, int):
            if value > 999_999_999:
                if value > 2_147_483_647:
                    raise ValueError(f"xs int can't hold such big value: {value}")
                base = int(value / 10)
                remainder = int(value % 10)
                xs = f"{base}{self.s}*{self.s}10{self.s}+{self.s}{remainder}"
                if not enclosed:
                    xs = f"({xs})"
                return xs
            if value < -999_999_999:
                if value < -2_147_483_648:
                    raise ValueError(f"xs int can't hold such small value: {value}")
                value = value * -1
                base = int(value / 10)
                remainder = int(value % 10)
                xs = f"-{base}{self.s}*{self.s}10{self.s}-{self.s}{remainder}"
                if not enclosed:
                    xs = f"({xs})"
                return xs
            return f"{value}"
        if isinstance(value, float):
            return f"{value}"
        else:
            raise ValueError(f"Unsupported variable type: {value}")

    def to_xs_call(self, e: Call, vars_to_replace: dict[str, str], enclosed=False) -> str:
        if isinstance(e.func, Name):
            function_name = self.to_camel_case(e.func.id)
            if function_name == "str":
                # assume no conversion is needed :(
                xs = f'""{self.s}+{self.s}' + self.to_xs_expression(e.args[0], vars_to_replace)
                if not enclosed:
                    xs = f"({xs})"
            elif function_name == "float" or function_name == "float32":
                if len(e.args) == 1 and ((isinstance(e.args[0], UnaryOp) and isinstance(e.args[0].op,
                                                                                        USub) and isinstance(
                        e.args[0].operand, Constant)) or (isinstance(e.args[0], Constant))):
                    if isinstance(e.args[0], UnaryOp):
                        xs = self.to_xs_expression(e.args[0], vars_to_replace, enclosed=enclosed)
                    else:
                        xs = self.to_xs_constant(e.args[0].value, enclosed)
                else:
                    xs = f'0.0{self.s}+{self.s}' + self.to_xs_expression(e.args[0], vars_to_replace)
                    if not enclosed:
                        xs = f"({xs})"
            elif function_name == "int" or function_name == "int32":
                if len(e.args) == 1 and ((isinstance(e.args[0], UnaryOp) and isinstance(e.args[0].op,
                                                                                        USub) and isinstance(
                        e.args[0].operand, Constant)) or (isinstance(e.args[0], Constant))):
                    if isinstance(e.args[0], UnaryOp):
                        xs = self.to_xs_expression(e.args[0], vars_to_replace, enclosed=enclosed)
                    else:
                        xs = self.to_xs_constant(e.args[0].value, enclosed)
                else:
                    xs = f'0{self.s}+{self.s}' + self.to_xs_expression(e.args[0], vars_to_replace)
                    if not enclosed:
                        xs = f"({xs})"
            else:
                xs = f"{function_name}("
                xs += f",{self.s}".join(
                    [self.to_xs_expression(a, vars_to_replace, enclosed=True) for a in e.args])
                xs += ")"
            return xs
        else:
            raise ValueError(f"Function call must be referenced by name not: {e.func}")

    def to_xs_if(self, e: If, i: int, vars_to_replace: dict[str, str], els: bool = False) -> str:
        xs = ""
        if e.test is not None and not els:
            xs += f"{i * self.i}if{self.s}("
            xs += self.to_xs_expression(e.test, vars_to_replace, enclosed=True)
            xs += f"){self.s}{{{self.n}"
        elif e.test is not None and els:
            xs += f"{i * self.i}}}{self.s}else if{self.s}("
            xs += self.to_xs_expression(e.test, vars_to_replace, enclosed=True)
            xs += f"){self.s}{{{self.n}"
        else:
            raise ValueError("else with a test statement")
        xs += self.to_xs_body(e.body, i, vars_to_replace)

        if len(e.orelse) == 1 and isinstance(e.orelse[0], If):
            xs += self.to_xs_if(e.orelse[0], i, vars_to_replace, True)
        elif len(e.orelse) > 0:
            xs += f"{i * self.i}}}{self.s}else{self.s}{{{self.n}"
            xs += self.to_xs_body(e.orelse, i, vars_to_replace)
            xs += f"{i * self.i}}}{self.n}"
        else:
            xs += f"{i * self.i}}}{self.n}"
        return xs

    def to_xs_for(self, e: For, i: int, vars_to_replace: dict[str, str]) -> str:
        xs = ""
        if isinstance(e.iter, Call) and isinstance(e.iter.func, Name) and e.iter.func.id in {"range", "i32range"}:
            args = e.iter.args
            if 2 >= len(args) > 0 or (len(args) == 3 and self.unpackIntConstant(args[2]) in {1, -1}):
                if isinstance(e.target, Name):
                    xs_loop_var = self.to_camel_case(e.target.id)
                else:
                    raise ValueError(f"loop target must be a new variable")

                if len(args) == 1:
                    from_xs = _xs = "0"
                    to_xs = self.to_xs_for_to(args[0], vars_to_replace, True, True)
                else:
                    from_xs = self.to_xs_expression(args[0], vars_to_replace, enclosed=True)
                    positive = not self.unpackIntConstant(args[2]) == -1 if len(args) == 3 else True
                    to_xs = self.to_xs_for_to(args[1], vars_to_replace, positive, True)

                xs += f"{i * self.i}for{self.s}({xs_loop_var}{self.s}={self.s}{from_xs};{self.s}{to_xs}){self.s}{{{self.n}"
                xs += self.to_xs_body(e.body, i, vars_to_replace)
                xs += f"{i * self.i}}}{self.n}"
                return xs
            if len(args) == 3:
                if isinstance(e.target, Name):
                    xs_loop_var = self.to_camel_case(e.target.id)
                    xs += f"{i * self.i}int {xs_loop_var}{self.s}={self.s}{self.to_xs_expression(args[0], vars_to_replace, enclosed=True)};{self.n}"
                else:
                    raise ValueError(f"loop target must be a new variable")
                increment_val = self.unpackIntConstant(args[2])
                if increment_val is None or isinstance(increment_val, float):
                    raise ValueError(f"loop increment value must be a constant")
                if increment_val == 1:
                    xs_loop_increment = "++;"
                elif increment_val == -1:
                    xs_loop_increment = "--;"
                elif increment_val < 0:
                    xs_loop_increment = f"{self.s}={self.s}{xs_loop_var}{self.s}-{self.s}{self.to_xs_constant(abs(increment_val))};"
                elif increment_val > 0:
                    xs_loop_increment = f"{self.s}={self.s}{xs_loop_var}{self.s}+{self.s}{self.to_xs_constant(increment_val)};"
                else:
                    raise ValueError("last range arg can't be 0")
                to_xs = self.to_xs_for_to(args[1], vars_to_replace, increment_val >= 0, False)
                xs += f"{i * self.i}while{self.s}({xs_loop_var}{self.s}{to_xs}){self.s}{{{self.n}"
                xs += self.to_xs_body(e.body, i, vars_to_replace)
                xs += f"{(i + 1) * self.i}{xs_loop_var}{xs_loop_increment}{self.n}"
                xs += f"{i * self.i}}}{self.n}"
                return xs
            else:
                raise ValueError("for loops are only supported over 1 argument range expressions")
        raise ValueError("for loops are only supported over 1 argument range expressions")


    def unpackIntConstant(self, expr) -> Optional[int]:
        if isinstance(expr, UnaryOp) and isinstance(expr.op, USub) and isinstance(
            expr.operand, Constant) and isinstance(expr.operand.value, int):
            return expr.operand.value * -1
        if isinstance(expr, Constant) and isinstance(expr.value, int):
            return expr.value
        return None

    def to_xs_while(self, e: While, i: int, vars_to_replace: dict[str, str]) -> str:
        xs = ""
        xs += f"{i * self.i}while{self.s}("
        xs += self.to_xs_expression(e.test, vars_to_replace, enclosed=True)
        xs += f"){self.s}{{{self.n}"
        xs += self.to_xs_body(e.body, i, vars_to_replace)
        xs += f"{i * self.i}}}{self.n}"
        return xs

    def to_xs_match(self, e: Match, i: int, vars_to_replace: dict[str, str]) -> str:
        xs = ""
        xs += f"{i * self.i}switch{self.s}("
        xs += self.to_xs_expression(e.subject, vars_to_replace, enclosed=True)
        xs += f"){self.s}{{{self.n}"
        i += 1
        for case in e.cases:
            if isinstance(case.pattern, MatchValue):
                xs_case = self.to_xs_expression(case.pattern.value, vars_to_replace)
                xs += f"{i * self.i}case {xs_case}:{self.s}{{{self.n}"
                xs += self.to_xs_body(case.body, i, vars_to_replace)
                xs += f"{i * self.i}}}{self.n}"
            elif isinstance(case.pattern, MatchAs) and case.pattern.name is None:
                xs += f"{i * self.i}default:{self.s}{{{self.n}"
                xs += self.to_xs_body(case.body, i, vars_to_replace)
                xs += f"{i * self.i}}}{self.n}"
            else:
                raise ValueError(f"unsupported complex case pattern: {case.pattern}")
        xs += f"{(i - 1) * self.i}}}{self.n}"
        return xs

    def to_xs_function_definition(self, function: FunctionDef, i: int, root_function: bool = True) -> str:
        type = self.to_xs_function_type(function.returns)
        name = self.to_camel_case(function.name)

        if len(function.args.args) != len(function.args.defaults):
            raise ValueError(f"all functions arguments must have default value")

        parameters_xs = self.to_xs_parameters(function, root_function, type)
        has_parameters = len(parameters_xs) > 0

        rule_modifier_xs = self.to_xs_rule_modifiers(function, root_function, has_parameters, type)
        has_rules = len(rule_modifier_xs) > 0
        xs = ""
        doc = ast.get_docstring(function)
        if doc is not None:
            self.doc_strings.add(doc.replace("\n", "").replace(" ", ""))
        if doc is not None and len(self.i) > 0:
            doc = doc.replace(":param", "@param")
            doc = doc.replace(":return:", "@return")
            doc = doc.replace(":", " -")
            doc = doc.replace("\n", f"\n{(i + 1) * self.i}")
            xs += f"{i * self.i}/*\n{(i + 1) * self.i}"
            xs += doc + "\n"
            xs += f"{i * self.i}*/\n"
        if has_rules > 0:
            xs += f"{i * self.i}rule {name} {rule_modifier_xs}{self.s}{{{self.n}"
        else:
            xs += f"{i * self.i}{type} {name}({parameters_xs}){self.s}{{{self.n}"

        xs += self.to_xs_body(function.body, i, {})
        xs += f"{i * self.i}}}{self.n}"
        return xs

    def to_xs_parameters(self, function: FunctionDef, root_function: bool, type: str) -> str:
        parameters = [self.to_xs_arg(a, default, {}) for a, default in zip(function.args.args, function.args.defaults)]
        # if root_function:
        #     if len(parameters) != 0 or type != "void":
        #         raise ValueError("root function must have None return type and have no parameters")
        parameters_xs = f",{self.s}".join(parameters)
        return parameters_xs

    def to_xs_rule_modifiers(self, function: FunctionDef, root_function: bool, has_parameters: bool, type: str) -> str:
        rule_decorator = [d for d in function.decorator_list if
                          isinstance(d, Call) and isinstance(d.func, Name) and d.func.id == "xs_rule"]
        is_rule = len(rule_decorator) > 0
        if is_rule and (root_function or has_parameters or type != "void"):
            raise ValueError("can not have xs task with parameters or as a default root function")
        if is_rule:
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
        return ""

    def to_xs_function(self, function, root_function: bool = True):
        source = inspect.getsource(function)
        module_ast = ast.parse(source)
        function_body = module_ast.body[0]
        if isinstance(module_ast.body, list) and len(module_ast.body) == 1 and isinstance(function_body, FunctionDef):
            return self.to_xs_function_definition(function_body, 0, root_function)

        else:
            raise ValueError("top level must contain a single function")

    def to_xs_body(self, body: list[expr | stmt], i: int, vars_to_replace: dict[str, str]) -> str:
        xs = ""
        i += 1
        for e in body:
            if isinstance(e, AnnAssign):
                xs += self.to_xs_variable_definition(e, i, vars_to_replace)
            elif isinstance(e, Assign):
                xs += self.to_xs_variable_assignment(e, i, vars_to_replace)
            elif isinstance(e, AugAssign):
                xs += self.to_xs_variable_aug_assignment(e, i, vars_to_replace)
            elif isinstance(e, Expr):
                xs += self.to_xs_expression_top(e, i, vars_to_replace)
            elif isinstance(e, If):
                xs += self.to_xs_if(e, i, vars_to_replace)
            elif isinstance(e, For):
                xs += self.to_xs_for(e, i, vars_to_replace)
            elif isinstance(e, While):
                xs += self.to_xs_while(e, i, vars_to_replace)
            elif isinstance(e, Match):
                xs += self.to_xs_match(e, i, vars_to_replace)
            elif isinstance(e, With):
                xs += self.to_xs_macro_with(e, i - 1, vars_to_replace)
            elif isinstance(e, Return):
                xs += self.to_xs_return(e, i, vars_to_replace)
            elif isinstance(e, Pass):
                pass
            elif isinstance(e, Global):
                pass
            else:
                raise ValueError(e)
        return xs

    def to_xs_return(self, e: Return, i: int, vars_to_replace: dict[str, str]) -> str:
        if e.value is None:
            return_xs = ""
        else:
            return_xs = f"{self.s}({self.to_xs_expression(e.value, vars_to_replace, enclosed=True)})"
        return f"{self.i * i}return{return_xs};{self.n}"

    def eval_macro_function(self, call: Call) -> any:
        if isinstance(call.func, Name):
            return self.eval_macro_var(call)
        else:
            raise ValueError("Macro should be a name token")

    def eval_macro_var(self, call: Call) -> any:
        if len(call.args) >= 1 and len(call.args) <= 2 and isinstance(call.args[0], Constant) and isinstance(
                call.args[0].value, str):
            macro_arg = call.args[0].value
            return eval(macro_arg, self.vars)
        else:
            raise ValueError("macro should have 1 string constant argument")

    def to_xs_macro_with(self, e: With, i: int, vars_to_replace: dict[str, str]) -> str:
        if (len(e.items) == 1 and
                isinstance(e.items[0].context_expr, Call)):
            xs = ""

            if isinstance(e.items[0].optional_vars, Name):
                names = [e.items[0].optional_vars.id]
            elif isinstance(e.items[0].optional_vars, Tuple):
                names = [n.id for n in e.items[0].optional_vars.dims if isinstance(n, Name)]
            else:
                raise ValueError("only unpacked single or deconstructer tuple are allowed")
            iterable_value = self.eval_macro_function(e.items[0].context_expr)
            if not isinstance(iterable_value, Iterable):
                raise ValueError("repeater macro needs a reference to an iterable")
            for value in iterable_value:
                new_dict = vars_to_replace.copy()
                if isinstance(value, tuple):
                    value_batch = list(value)
                else:
                    value_batch = [value]
                for name, val in zip(names, value_batch):
                    new_dict[name] = self.to_xs_constant(val)
                xs += self.to_xs_body(e.body, i, new_dict)
            return xs
        else:
            raise ValueError("incorrect repeated macro usage")

    def to_xs_for_to(self, param: expr, vars_to_replace: dict[str, str], positive: bool, enclosed: bool) -> str:
        if isinstance(param, BinOp) and isinstance(param.op, Add) and positive:
            sign = "<="
            if isinstance(param.right, Constant) and param.right.value == 1:
                return f"{sign}{self.s}{self.to_xs_expression(param.left, vars_to_replace, enclosed=enclosed)}"
            if isinstance(param.left, Constant) and param.left.value == 1:
                return f"{sign}{self.s}{self.to_xs_expression(param.right, vars_to_replace, enclosed=enclosed)}"
        if isinstance(param, BinOp) and isinstance(param.op, Sub) and not positive:
            sign = ">="
            if isinstance(param.right, Constant) and param.right.value == 1:
                return f"{sign}{self.s}{self.to_xs_expression(param.left, vars_to_replace, enclosed=enclosed)}"
            if isinstance(param.left, Constant) and param.left.value == 1:
                return f"{sign}{self.s}{self.to_xs_expression(param.right, vars_to_replace, enclosed=enclosed)}"
        sign = ">"
        if positive:
            sign = "<"
        return f"{sign}{self.s}{self.to_xs_expression(param, vars_to_replace, enclosed=enclosed)}"
