import unittest
import ast
from reference_generator.classes import Function

def open_read_parse(file: str) -> ast.FunctionDef:
    with open(file, 'r') as opened:
        return ast.parse(opened.read()).body[0]


class TestFunction(unittest.TestCase):

    def test_docstring_template(self):
        base_function: Function = Function(open_read_parse('tests/test_files/functions/base_function.py'))
        expected_base_function_docstring: str = "<DESCRIPTION>\n\n<EXPLANATION>"
        self.assertEqual(base_function.docstring_template(), expected_base_function_docstring)

        return_function: Function = Function(open_read_parse('tests/test_files/functions/return_function.py'))
        expected_return_function_docstring: str = "<DESCRIPTION>\n\n<EXPLANATION>\n\n=== returns\n_str_- <RETURN DESCRIPTION>"
        self.assertEqual(return_function.docstring_template(), expected_return_function_docstring)

        parameter_function: Function = Function(open_read_parse('tests/test_files/functions/parameter_function.py'))
        expected_parameter_function_docstring: str = "<DESCRIPTION>\n\n<EXPLANATION>\n\n=== parameters\n* _str_ *name*  - <PARAMETER DESCRIPTION>"
        self.assertEqual(parameter_function.docstring_template(), expected_parameter_function_docstring)

        multiple_parameter_function: Function = Function(open_read_parse('tests/test_files/functions/multiple_parameter_function.py'))
        expected_multiple_parameter_function_docstring: str = "<DESCRIPTION>\n\n<EXPLANATION>\n\n=== parameters\n* _str_ *name*  - <PARAMETER DESCRIPTION>\n* _bool_ *shout* (optional) - <PARAMETER DESCRIPTION>"
        self.assertEqual(multiple_parameter_function.docstring_template(), expected_multiple_parameter_function_docstring)

        full_function: Function = Function(open_read_parse('tests/test_files/functions/full_function.py'))
        expected_full_function_docstring: str = "<DESCRIPTION>\n\n<EXPLANATION>\n\n=== parameters\n* _str_ *name*  - <PARAMETER DESCRIPTION>\n\n=== returns\n_str_- <RETURN DESCRIPTION>"
        self.assertEqual(full_function.docstring_template(), expected_full_function_docstring)

    def test_table_item(self):
        base_function: Function = Function(open_read_parse('tests/test_files/functions/base_function.py'))
        expected_base_function_item: str = "|`*hello*`\n|"
        self.assertEqual(base_function.table_item(), expected_base_function_item)

        return_function: Function = Function(open_read_parse('tests/test_files/functions/return_function.py'))
        expected_return_function_item: str = "|`_str_`\n|`*hello*`\n|"
        self.assertEqual(return_function.table_item(), expected_return_function_item)


if __name__ == '__main__':
    unittest.main()