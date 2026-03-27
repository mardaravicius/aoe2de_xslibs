import ast
import textwrap
import types
import unittest
from unittest.mock import patch

from xs_converter.context import XsContext
from xs_converter.converter import PythonToXsConverter
from xs_converter.exceptions import XsConversionError
from tests.test_xs_converter.helpers import module_from_source


def expr_from_source(source: str) -> ast.expr:
    return ast.parse(source, mode="eval").body


def stmt_from_source(source: str) -> ast.stmt:
    return ast.parse(textwrap.dedent(source)).body[0]


def function_from_source(source: str) -> ast.FunctionDef:
    node = stmt_from_source(source)
    assert isinstance(node, ast.FunctionDef)
    return node


def make_converter(source: str = "x = 1\n", **bindings: object) -> PythonToXsConverter:
    converter = PythonToXsConverter(indent=True, bindings=dict(bindings))
    normalized_source = textwrap.dedent(source)
    converter._set_source_context(
        normalized_source,
        source_name="<test>",
        display_source_lines=normalized_source.splitlines(),
    )
    return converter


class ConverterExceptionInfrastructureTest(unittest.TestCase):
    def assert_error(self, fn, expected_text: str) -> XsConversionError:
        with self.assertRaises(XsConversionError) as cm:
            fn()
        self.assertIn(expected_text, str(cm.exception))
        return cm.exception

    def test_to_xs_file_reports_syntax_errors(self):
        mod = module_from_source("def broken(:\n    pass\n")

        error = self.assert_error(
            lambda: PythonToXsConverter.to_xs_file(mod, indent=True),
            "Location:",
        )
        message = str(error)
        self.assertIn("def broken(", message)
        self.assertIn("^", message)

    def test_to_xs_file_falls_back_to_getsource_when_getsourcelines_fails(self):
        mod = types.ModuleType("_fake")
        mod.__file__ = "/tmp/fallback_module.py"

        with patch("xs_converter.converter.inspect.getsourcefile", return_value=mod.__file__), \
                patch("xs_converter.converter.inspect.getsourcelines", side_effect=OSError("boom")), \
                patch("xs_converter.converter.inspect.getsource", return_value="def broken(:\n    pass\n"):
            error = self.assert_error(
                lambda: PythonToXsConverter.to_xs_file(mod, indent=True),
                "Location: /tmp/fallback_module.py:1",
            )
        self.assertIn("def broken(", str(error))

    def test_to_xs_function_falls_back_to_getsource_and_reports_syntax_errors(self):
        def dummy() -> None:
            pass

        converter = PythonToXsConverter(indent=True, bindings={})
        with patch("xs_converter.converter.inspect.getsourcefile", return_value="/tmp/fallback_function.py"), \
                patch("xs_converter.converter.inspect.getsourcelines", side_effect=OSError("boom")), \
                patch("xs_converter.converter.inspect.getsource", return_value="def broken(:\n    pass\n"):
            error = self.assert_error(
                lambda: converter._to_xs_function(dummy),
                "Location: /tmp/fallback_function.py:1",
            )
        self.assertIn("def broken(", str(error))

    def test_to_xs_file_wraps_source_lookup_failures(self):
        mod = types.ModuleType("_fake")
        mod.__file__ = "/tmp/missing_module.py"

        with patch("xs_converter.converter.inspect.getsourcefile", return_value=mod.__file__), \
                patch("xs_converter.converter.inspect.getsourcelines", side_effect=OSError("no lines")), \
                patch("xs_converter.converter.inspect.getsource", side_effect=OSError("no source")):
            error = self.assert_error(
                lambda: PythonToXsConverter.to_xs_file(mod, indent=True),
                "Could not read Python source",
            )
        self.assertIn("/tmp/missing_module.py", str(error))

    def test_to_xs_function_wraps_source_lookup_failures(self):
        def dummy() -> None:
            pass

        converter = PythonToXsConverter(indent=True, bindings={})
        with patch("xs_converter.converter.inspect.getsourcefile", return_value="/tmp/missing_function.py"), \
                patch("xs_converter.converter.inspect.getsourcelines", side_effect=OSError("no lines")), \
                patch("xs_converter.converter.inspect.getsource", side_effect=OSError("no source")):
            error = self.assert_error(
                lambda: converter._to_xs_function(dummy),
                "Could not read Python source",
            )
        self.assertIn("/tmp/missing_function.py", str(error))

    def test_direct_helper_exception_includes_precise_node_location(self):
        source = "x: bytes = 1\n"
        converter = make_converter(source)
        stmt = stmt_from_source(source)
        assert isinstance(stmt, ast.AnnAssign)

        error = self.assert_error(
            lambda: converter._to_xs_variable_definition(stmt, XsContext()),
            "Location: <test>:1:4",
        )
        self.assertIn("x: bytes = 1", str(error))

    def test_to_xs_function_requires_source_to_be_a_single_function(self):
        def dummy() -> None:
            pass

        converter = PythonToXsConverter(indent=True, bindings={})
        with patch("xs_converter.converter.inspect.getsourcefile", return_value="/tmp/not_function.py"), \
                patch("xs_converter.converter.inspect.getsourcelines", side_effect=OSError("boom")), \
                patch("xs_converter.converter.inspect.getsource", return_value="x = 1\n"):
            error = self.assert_error(
                lambda: converter._to_xs_function(dummy),
                "single function definition",
            )
        message = str(error)
        self.assertIn("Location: /tmp/not_function.py:1:1", message)
        self.assertIn("x = 1", message)
        self.assertIn("^", message)

    def test_error_and_enrich_conversion_errors_without_ast_nodes(self):
        converter = make_converter()

        error = converter._error("boom")
        self.assertEqual("boom", error.message)
        self.assertEqual("<test>", error.source_name)
        self.assertIsNone(error.line)

        enriched = converter._enrich_conversion_error(XsConversionError("later"), None)
        self.assertEqual("<test>", enriched.source_name)
        self.assertEqual("later", enriched.message)

        existing = XsConversionError("explicit", source_name="custom.py")
        self.assertIs(existing, converter._enrich_conversion_error(existing, None))

    def test_raise_as_conversion_error_wraps_non_converter_exceptions(self):
        converter = make_converter("x = 1\n")
        node = stmt_from_source("x = 1")

        error = self.assert_error(
            lambda: converter._raise_as_conversion_error(RuntimeError("boom"), node),
            "boom",
        )
        self.assertIn("Location: <test>:1:1", str(error))

    def test_top_level_annotated_list_requires_simple_name_target(self):
        mod = module_from_source("obj.x: list[int] = [1]\n")
        self.assert_error(
            lambda: PythonToXsConverter.to_xs_file(mod, indent=True),
            "simple variable name",
        )

    def test_to_xs_file_uses_1_based_locations_for_module_errors(self):
        mod = module_from_source("if True:\n    pass\n")

        error = self.assert_error(
            lambda: PythonToXsConverter.to_xs_file(mod, indent=True),
            "Unsupported top-level statement",
        )
        message = str(error)
        self.assertIn(":1:1", message)
        self.assertNotIn(":0:", message)
        self.assertIn("if True:", message)


class ConverterDirectExceptionPathTest(unittest.TestCase):
    def assert_error(self, fn, expected_text: str) -> None:
        with self.assertRaises(XsConversionError) as cm:
            fn()
        self.assertIn(expected_text, str(cm.exception))

    def test_basic_helper_exception_paths(self):
        converter = make_converter()
        ctx = XsContext()
        cases = [
            ("invalid_type", lambda: converter._to_xs_type(expr_from_source("bytes")), "cannot be converted"),
            ("invalid_modifier", lambda: converter._to_xs_modifier("Readonly"), "cannot be converted"),
            ("invalid_return_type", lambda: converter._to_xs_function_type(expr_from_source("list[int]")), "Function return annotations"),
            ("invalid_array_create_type", lambda: converter._to_xs_array_create("dict", expr_from_source("0"), expr_from_source("1"), ctx), "Array creation does not support"),
            ("invalid_binary_operator", lambda: converter._to_xs_binary_op(ast.Pow()), "Unsupported binary operator"),
            ("invalid_literal", lambda: converter._to_xs_constant(object()), "Unsupported literal value"),
        ]
        for name, fn, message in cases:
            with self.subTest(name=name):
                self.assert_error(fn, message)

    def test_array_literal_exception_paths(self):
        converter = make_converter()
        cases = [
            ("plain_list", lambda: converter._parse_array_literal(expr_from_source("[1, 2]")), "use [default] * size"),
            ("not_repeat_syntax", lambda: converter._parse_array_literal(expr_from_source("value")), "[default_value] * size"),
            ("multi_default", lambda: converter._parse_array_literal(expr_from_source("[1, 2] * 3")), "single-element list"),
        ]
        for name, fn, message in cases:
            with self.subTest(name=name):
                self.assert_error(fn, message)

    def test_variable_and_array_target_exception_paths(self):
        converter = make_converter()
        ctx = XsContext()
        invalid_ann_slice = stmt_from_source("x: XsConst[list[int]] = 1")
        invalid_ann_root = stmt_from_source("x: 1 = 1")
        invalid_ann_target = stmt_from_source("obj.x: int = 1")
        multi_assign = stmt_from_source("a = b = 1")
        attr_assign = stmt_from_source("obj.x = 1")
        attr_aug_assign = stmt_from_source("obj.x += 1")
        invalid_subscript = expr_from_source("(a + b)[0]")
        valid_subscript = expr_from_source("arr[0]")

        cases = [
            ("variable_definition_invalid_slice", lambda: converter._to_xs_variable_definition(invalid_ann_slice, ctx), "supported type annotation"),
            ("variable_definition_invalid_root", lambda: converter._to_xs_variable_definition(invalid_ann_root, ctx), "supported type annotation"),
            ("variable_definition_invalid_target", lambda: converter._to_xs_variable_definition(invalid_ann_target, ctx), "simple variable name"),
            ("array_get_invalid_type", lambda: converter._to_xs_array_get(valid_subscript, "dict", ctx), "Array reads do not support"),
            ("array_get_invalid_target", lambda: converter._to_xs_array_get(invalid_subscript, "int", ctx), "Array read targets"),
            ("variable_assignment_multiple_targets", lambda: converter._to_xs_variable_assignment(multi_assign, ctx), "single-target assignments"),
            ("variable_assignment_invalid_target", lambda: converter._to_xs_variable_assignment(attr_assign, ctx), "variable name"),
            ("aug_assignment_invalid_target", lambda: converter._to_xs_variable_aug_assignment(attr_aug_assign, ctx), "variable name"),
            ("array_set_invalid_target", lambda: converter._to_xs_array_set(invalid_subscript, expr_from_source("1"), ctx), "Array assignment target"),
        ]
        for name, fn, message in cases:
            with self.subTest(name=name):
                self.assert_error(fn, message)

        with patch.object(converter, "_infer_array_element_type", return_value="custom"):
            self.assert_error(
                lambda: converter._to_xs_array_set(valid_subscript, expr_from_source("1"), ctx),
                "Array assignment does not support",
            )

    def test_expression_exception_paths(self):
        converter = make_converter("value = 1\n")
        ctx = XsContext()
        cases = [
            ("unsupported_unary", lambda: converter._to_xs_expression(expr_from_source("~x"), ctx), "Unsupported unary operator"),
            ("comparison_chain", lambda: converter._to_xs_expression(expr_from_source("1 < x < 3"), ctx), "exactly one operator"),
            ("unsupported_expression", lambda: converter._to_xs_expression(expr_from_source("lambda x: x"), ctx), "Unsupported expression type"),
            ("call_target_not_name", lambda: converter._to_xs_call(expr_from_source("(foo.bar)()"), ctx), "must reference a name"),
            ("cast_wrong_arity", lambda: converter._to_xs_call(expr_from_source("cast(int)"), ctx), "exactly 2 arguments"),
        ]
        for name, fn, message in cases:
            with self.subTest(name=name):
                self.assert_error(fn, message)

    def test_control_flow_exception_paths(self):
        converter = make_converter()
        ctx = XsContext()
        invalid_iter = stmt_from_source(
            """
            for x in values:
                pass
            """
        )
        invalid_target = stmt_from_source(
            """
            for x, y in range(3):
                pass
            """
        )
        invalid_match = stmt_from_source(
            """
            match x:
                case 1 | 2:
                    pass
            """
        )
        cases = [
            ("for_invalid_iter", lambda: converter._to_xs_for(invalid_iter, ctx), "range(...) or i32range"),
            ("for_invalid_target", lambda: converter._to_xs_for(invalid_target, ctx), "simple variable names"),
            ("range_zero_step", lambda: converter._parse_range_args([expr_from_source("0"), expr_from_source("3"), expr_from_source("0")]), "cannot be 0"),
            ("range_wrong_arity", lambda: converter._parse_range_args([expr_from_source("0"), expr_from_source("1"), expr_from_source("2"), expr_from_source("3")]), "1 to 3 arguments"),
            ("invalid_match_pattern", lambda: converter._to_xs_match(invalid_match, ctx), "only support literal cases"),
        ]
        for name, fn, message in cases:
            with self.subTest(name=name):
                self.assert_error(fn, message)

        self.assert_error(
            lambda: converter._to_xs_body([stmt_from_source("del x")], XsContext()),
            "Unsupported statement in function body",
        )
        self.assert_error(
            lambda: converter._to_xs_body([stmt_from_source("obj.x: list[int] = [1]")], XsContext()),
            "simple variable name",
        )

    def test_function_and_rule_exception_paths(self):
        converter = make_converter()
        no_defaults = function_from_source(
            """
            def f(x: int, y: int = 1) -> None:
                pass
            """
        )
        invalid_rule_keyword = function_from_source(
            """
            @xs_rule(active=flag)
            def f() -> None:
                pass
            """
        )
        conflicting_rule = function_from_source(
            """
            @xs_rule(high_frequency=True, min_interval=1)
            def f() -> None:
                pass
            """
        )

        self.assert_error(
            lambda: converter.to_xs_function_definition(no_defaults, XsContext(), root_function=False),
            "default value",
        )
        self.assert_error(
            lambda: converter._to_xs_rule_modifiers(invalid_rule_keyword, root_function=False, has_parameters=False, xs_type="void"),
            "constant keyword arguments",
        )
        self.assert_error(
            lambda: converter._to_xs_rule_modifiers(conflicting_rule, root_function=False, has_parameters=False, xs_type="void"),
            "cannot combine high_frequency",
        )

    def test_macro_exception_paths(self):
        converter = make_converter()
        ctx = XsContext()
        invalid_repeat_shape = stmt_from_source(
            """
            with foo(), bar():
                pass
            """
        )
        invalid_repeat_target = stmt_from_source(
            """
            with macro_repeat_with_iterable("[]", int) as obj.x:
                pass
            """
        )
        non_iterable_repeat = stmt_from_source(
            """
            with macro_repeat_with_iterable("1", int) as value:
                pass
            """
        )

        cases = [
            ("macro_function_requires_name", lambda: converter._eval_macro_function(expr_from_source("(lambda: 1)()")), "function name"),
            ("macro_var_requires_string", lambda: converter._eval_macro_var(expr_from_source("macro_pass_value(1)")), "string constant"),
            ("macro_var_eval_failure", lambda: converter._eval_macro_var(expr_from_source("macro_pass_value(\"missing_name\", int)")), "Failed to evaluate macro expression"),
            ("macro_with_invalid_shape", lambda: converter._to_xs_macro_with(invalid_repeat_shape, ctx), "single call in the with-statement"),
            ("macro_with_invalid_target", lambda: converter._to_xs_macro_with(invalid_repeat_target, ctx), "single name or a destructured tuple"),
            ("macro_with_non_iterable", lambda: converter._to_xs_macro_with(non_iterable_repeat, ctx), "evaluate to an iterable"),
        ]
        for name, fn, message in cases:
            with self.subTest(name=name):
                self.assert_error(fn, message)


if __name__ == "__main__":
    unittest.main()
