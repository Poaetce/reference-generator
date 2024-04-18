import unittest
import ast
from reference_generator.referencers import TopLevelFunctionReferencer


def open_read_parse(file: str) -> ast.FunctionDef:
    with open(file, 'r') as opened:
        return ast.parse(opened.read()).body[0]


class TestTopLevelFunctionReferencer(unittest.TestCase):

    def test_docstring_template(self):
        base_function: TopLevelFunctionReferencer = TopLevelFunctionReferencer(open_read_parse('tests/test_files/functions/base_function.py'), 'functions')
        expected_base_function_docstring: str = '\n'.join([
            "<DESCRIPTION>",
            '',
            "<EXPLANATION>",
        ])
        self.assertEqual(base_function.docstring_template(), expected_base_function_docstring)

        return_function: TopLevelFunctionReferencer = TopLevelFunctionReferencer(open_read_parse('tests/test_files/functions/return_function.py'), 'functions')
        expected_return_function_docstring: str = '\n'.join([
            "<DESCRIPTION>",
            '',
            "<EXPLANATION>",
            '',
            "=== returns",
            "_str_ - <RETURN DESCRIPTION>",
        ])
        self.assertEqual(return_function.docstring_template(), expected_return_function_docstring)

        parameter_function: TopLevelFunctionReferencer = TopLevelFunctionReferencer(open_read_parse('tests/test_files/functions/parameter_function.py'), 'functions')
        expected_parameter_function_docstring: str = '\n'.join([
            "<DESCRIPTION>",
            '',
            "<EXPLANATION>",
            '',
            "=== parameters",
            "* _str_ *name* - <PARAMETER DESCRIPTION>",
        ])
        self.assertEqual(parameter_function.docstring_template(), expected_parameter_function_docstring)

        multiple_parameter_function: TopLevelFunctionReferencer = TopLevelFunctionReferencer(open_read_parse('tests/test_files/functions/multiple_parameter_function.py'), 'functions')
        expected_multiple_parameter_function_docstring: str = '\n'.join([
            "<DESCRIPTION>",
            '',
            "<EXPLANATION>",
            '',
            "=== parameters",
            "* _str_ *name* - <PARAMETER DESCRIPTION>",
            "* _bool_ *shout* (optional) - <PARAMETER DESCRIPTION>",
        ])
        self.assertEqual(multiple_parameter_function.docstring_template(), expected_multiple_parameter_function_docstring)

        full_function: TopLevelFunctionReferencer = TopLevelFunctionReferencer(open_read_parse('tests/test_files/functions/full_function.py'), 'functions')
        expected_full_function_docstring: str = '\n'.join([
            "<DESCRIPTION>",
            '',
            "<EXPLANATION>",
            '',
            "=== parameters",
            "* _str_ *name* - <PARAMETER DESCRIPTION>",
            '',
            "=== returns",
            "_str_ - <RETURN DESCRIPTION>",
        ])
        self.assertEqual(full_function.docstring_template(), expected_full_function_docstring)

    def test_table_item(self):
        base_function: TopLevelFunctionReferencer = TopLevelFunctionReferencer(open_read_parse('tests/test_files/functions/base_function.py'), 'functions')
        expected_base_function_item: str = '\n'.join([
            "|`*hello*`",
            "|greets the user",
        ])
        self.assertEqual(base_function.table_item(), expected_base_function_item)

        return_function: TopLevelFunctionReferencer = TopLevelFunctionReferencer(open_read_parse('tests/test_files/functions/return_function.py'), 'functions')
        expected_return_function_item: str = '\n'.join([
            "|`_str_`",
            "|`*hello*`",
            "|greets the user",
        ])
        self.assertEqual(return_function.table_item(), expected_return_function_item)

    def test_shape(self):
        base_function: TopLevelFunctionReferencer = TopLevelFunctionReferencer(open_read_parse('tests/test_files/functions/base_function.py'), 'functions')
        expected_base_function_shape: str = "`functions.*hello*()`"
        self.assertEqual(base_function.shape(), expected_base_function_shape)

        parameter_function: TopLevelFunctionReferencer = TopLevelFunctionReferencer(open_read_parse('tests/test_files/functions/parameter_function.py'), 'functions')
        expected_parameter_function_shape: str = "`functions.*hello*(_name_)`"
        self.assertEqual(parameter_function.shape(), expected_parameter_function_shape)

        multiple_parameter_function: TopLevelFunctionReferencer = TopLevelFunctionReferencer(open_read_parse('tests/test_files/functions/multiple_parameter_function.py'), 'functions')
        expected_multiple_parameter_function_shape: str = "`functions.*hello*(_name_, _shout_)`"
        self.assertEqual(multiple_parameter_function.shape(), expected_multiple_parameter_function_shape)

    def test_details(self):
        base_function: TopLevelFunctionReferencer = TopLevelFunctionReferencer(open_read_parse('tests/test_files/functions/base_function.py'), 'functions')
        expected_base_function_details: str = f"== `hello`\n\n{base_function.shape()}\n\n{base_function.docstring}"
        self.assertEqual(base_function.details(), expected_base_function_details)

        return_function: TopLevelFunctionReferencer = TopLevelFunctionReferencer(open_read_parse('tests/test_files/functions/return_function.py'), 'functions')
        expected_return_function_details: str = f"== `hello`\n\n{return_function.shape()}\n\n{return_function.docstring}"
        self.assertEqual(return_function.details(), expected_return_function_details)

        parameter_function: TopLevelFunctionReferencer = TopLevelFunctionReferencer(open_read_parse('tests/test_files/functions/parameter_function.py'), 'functions')
        expected_parameter_function_details: str = f"== `hello`\n\n{parameter_function.shape()}\n\n{parameter_function.docstring}"
        self.assertEqual(parameter_function.details(), expected_parameter_function_details)

        multiple_parameter_function: TopLevelFunctionReferencer = TopLevelFunctionReferencer(open_read_parse('tests/test_files/functions/multiple_parameter_function.py'), 'functions')
        expected_multiple_parameter_function_details: str = f"== `hello`\n\n{multiple_parameter_function.shape()}\n\n{multiple_parameter_function.docstring}"
        self.assertEqual(multiple_parameter_function.details(), expected_multiple_parameter_function_details)

        full_function: TopLevelFunctionReferencer = TopLevelFunctionReferencer(open_read_parse('tests/test_files/functions/full_function.py'), 'functions')
        expected_full_function_details: str = f"== `hello`\n\n{full_function.shape()}\n\n{full_function.docstring}"
        self.assertEqual(full_function.details(), expected_full_function_details)


if __name__ == '__main__':
    unittest.main()