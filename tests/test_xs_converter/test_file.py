import unittest

from xs_converter.converter import PythonToXsConverter
from xs_converter.exceptions import XsConversionError
from tests.test_xs_converter.helpers import convert_file, module_from_source

import tests.test_xs_converter.fixtures.imports_only as imports_only
import tests.test_xs_converter.fixtures.imports_and_function as imports_and_function
import tests.test_xs_converter.fixtures.variables as variables
import tests.test_xs_converter.fixtures.variable_assignment as variable_assignment
import tests.test_xs_converter.fixtures.multiple_functions as multiple_functions
import tests.test_xs_converter.fixtures.mixed as mixed
import tests.test_xs_converter.fixtures.with_xs_ignore as with_xs_ignore


class FileConversionTest(unittest.TestCase):
    def test_imports_are_ignored(self):
        expected = "void foo() {\n}\n"
        self.assertEqual(expected, convert_file(imports_and_function))

    def test_top_level_variable_declaration(self):
        expected = (
            "int count = 5;\n"
            "float total = 0.0;\n"
        )
        self.assertEqual(expected, convert_file(variables))

    def test_top_level_variable_assignment(self):
        expected = (
            "int count = 5;\n"
            "count = 10;\n"
        )
        self.assertEqual(expected, convert_file(variable_assignment))

    def test_multiple_functions(self):
        expected = (
            "void first() {\n"
            "    int x = 1;\n"
            "}\n"
            "\n"
            "int second() {\n"
            "    return (42);\n"
            "}\n"
        )
        self.assertEqual(expected, convert_file(multiple_functions))

    def test_mixed_functions_and_variables(self):
        expected = (
            "int g = 99;\n"
            "\n"
            "void foo(int x = 0) {\n"
            "    int y = x + g;\n"
            "}\n"
        )
        self.assertEqual(expected, convert_file(mixed))

    def test_unsupported_top_level_if_raises(self):
        mod = module_from_source("if True:\n    pass\n")
        with self.assertRaises(XsConversionError) as cm:
            PythonToXsConverter.to_xs_file(mod, indent=True)
        message = str(cm.exception)
        self.assertIn("If", message)
        self.assertIn("Location:", message)
        self.assertIn("if True:", message)
        self.assertIn("^", message)

    def test_unsupported_top_level_for_raises(self):
        mod = module_from_source("for i in range(10):\n    pass\n")
        with self.assertRaises(XsConversionError) as cm:
            PythonToXsConverter.to_xs_file(mod, indent=True)
        self.assertIn("For", str(cm.exception))

    def test_unsupported_top_level_while_raises(self):
        mod = module_from_source("while True:\n    pass\n")
        with self.assertRaises(XsConversionError) as cm:
            PythonToXsConverter.to_xs_file(mod, indent=True)
        self.assertIn("While", str(cm.exception))

    def test_unsupported_top_level_expression_raises(self):
        mod = module_from_source("print('hello')\n")
        with self.assertRaises(XsConversionError) as cm:
            PythonToXsConverter.to_xs_file(mod, indent=True)
        self.assertIn("Expr", str(cm.exception))

    def test_top_level_main_guard_is_converted_to_main_function(self):
        mod = module_from_source(
            "count: int = 1\n"
            "if __name__ == \"__main__\":\n"
            "    count = count + 1\n"
        )
        expected = (
            "int count = 1;\n"
            "\n"
            "void main() {\n"
            "    count = count + 1;\n"
            "}\n"
        )
        self.assertEqual(expected, convert_file(mod))

    def test_xs_ignore_skips_function(self):
        expected = (
            "void converted() {\n"
            "    int x = 1;\n"
            "}\n"
            "\n"
            "int alsoConverted() {\n"
            "    return (42);\n"
            "}\n"
        )
        self.assertEqual(expected, convert_file(with_xs_ignore))

    def test_empty_file_with_only_imports(self):
        self.assertEqual("", convert_file(imports_only))

    def test_top_level_list_literal_is_lowered_with_temp_statements(self):
        mod = module_from_source("arr: list[int] = [1, 2, 3]\n")
        expected = (
            "int arr = xsArrayCreateInt(3);\n"
            "xsArraySetInt(arr, 0, 1);\n"
            "xsArraySetInt(arr, 1, 2);\n"
            "xsArraySetInt(arr, 2, 3);\n"
        )
        self.assertEqual(expected, convert_file(mod))

    def test_rule_after_top_level_variables_is_converted(self):
        mod = module_from_source(
            "x: int = 1\n"
            "@xs_rule()\n"
            "def tick() -> None:\n"
            "    pass\n"
        )
        expected = (
            "int x = 1;\n"
            "\n"
            "rule tick inactive {\n"
            "}\n"
        )
        self.assertEqual(expected, convert_file(mod))


if __name__ == "__main__":
    unittest.main()
