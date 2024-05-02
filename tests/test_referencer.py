import unittest
import ast
from reference_generator.referencer import FunctionRef, ClassRef
from reference_generator.documenter import flatten


def open_read_parse(file_path: str, depth: int) -> ast.stmt:
    with open(file_path, 'r') as file:
        module: ast.Module = ast.parse(file.read())
        for level in range(depth):
            node: ast.stmt = module.body[0]
        return node


class TestFunctionRef(unittest.TestCase):

    def test_attributes(self):
        full_function: FunctionRef = FunctionRef(open_read_parse('tests/test_files/functions/full_function.py', 1), 'functions')
        self.assertEqual(full_function.identifier, 'hello')
        self.assertEqual(full_function.parameters, ['name'])
        self.assertEqual(full_function.return_type, 'str')
        self.assertEqual(full_function.description, "greets the user")
        self.assertEqual(full_function.reference, 'functions')


    def test_docstring_template(self):
        base_function: FunctionRef = FunctionRef(open_read_parse('tests/test_files/functions/base_function.py', 1), 'functions')
        expected_base_function_docstring: str = '\n'.join([
            "<DESCRIPTION>",
            '',
            "<EXPLANATION>",
        ])
        self.assertEqual(base_function.docstring_template(), expected_base_function_docstring)

        return_function: FunctionRef = FunctionRef(open_read_parse('tests/test_files/functions/return_function.py', 1), 'functions')
        expected_return_function_docstring: str = '\n'.join([
            "<DESCRIPTION>",
            '',
            "<EXPLANATION>",
            '',
            "=== returns",
            '',
            "_str_ - <RETURN DESCRIPTION>",
        ])
        self.assertEqual(return_function.docstring_template(), expected_return_function_docstring)

        parameter_function: FunctionRef = FunctionRef(open_read_parse('tests/test_files/functions/parameter_function.py', 1), 'functions')
        expected_parameter_function_docstring: str = '\n'.join([
            "<DESCRIPTION>",
            '',
            "<EXPLANATION>",
            '',
            "=== parameters",
            '',
            "* _str_ *name* - <PARAMETER DESCRIPTION>",
        ])
        self.assertEqual(parameter_function.docstring_template(), expected_parameter_function_docstring)

        multiple_parameter_function: FunctionRef = FunctionRef(open_read_parse('tests/test_files/functions/multiple_parameter_function.py', 1), 'functions')
        expected_multiple_parameter_function_docstring: str = '\n'.join([
            "<DESCRIPTION>",
            '',
            "<EXPLANATION>",
            '',
            "=== parameters",
            '',
            "* _str_ *name* - <PARAMETER DESCRIPTION>",
            "* _bool_ *shout* (optional) - <PARAMETER DESCRIPTION>",
        ])
        self.assertEqual(multiple_parameter_function.docstring_template(), expected_multiple_parameter_function_docstring)

        full_function: FunctionRef = FunctionRef(open_read_parse('tests/test_files/functions/full_function.py', 1), 'functions')
        expected_full_function_docstring: str = '\n'.join([
            "<DESCRIPTION>",
            '',
            "<EXPLANATION>",
            '',
            "=== parameters",
            '',
            "* _str_ *name* - <PARAMETER DESCRIPTION>",
            '',
            "=== returns",
            '',
            "_str_ - <RETURN DESCRIPTION>",
        ])
        self.assertEqual(full_function.docstring_template(), expected_full_function_docstring)

    def test_table_item(self):
        base_function: FunctionRef = FunctionRef(open_read_parse('tests/test_files/functions/base_function.py', 1), 'functions')
        expected_base_function_item: list[str] = [
            "`*hello*`",
            "greets the user",
        ]
        self.assertEqual(base_function.table_item(), expected_base_function_item)

        return_function: FunctionRef = FunctionRef(open_read_parse('tests/test_files/functions/return_function.py', 1), 'functions')
        expected_return_function_item: list[str] = [
            "`_str_`",
            "`*hello*`",
            "greets the user",
        ]
        self.assertEqual(return_function.table_item(), expected_return_function_item)

    def test_shape(self):
        base_function: FunctionRef = FunctionRef(open_read_parse('tests/test_files/functions/base_function.py', 1), 'functions')
        expected_base_function_shape: str = "`functions.*hello*()`"
        self.assertEqual(base_function.shape().generate()[0], expected_base_function_shape)

        parameter_function: FunctionRef = FunctionRef(open_read_parse('tests/test_files/functions/parameter_function.py', 1), 'functions')
        expected_parameter_function_shape: str = "`functions.*hello*(_name_)`"
        self.assertEqual(parameter_function.shape().generate()[0], expected_parameter_function_shape)

        multiple_parameter_function: FunctionRef = FunctionRef(open_read_parse('tests/test_files/functions/multiple_parameter_function.py', 1), 'functions')
        expected_multiple_parameter_function_shape: str = "`functions.*hello*(_name_, _shout_)`"
        self.assertEqual(multiple_parameter_function.shape().generate()[0], expected_multiple_parameter_function_shape)

    def test_details(self):
        base_function: FunctionRef = FunctionRef(open_read_parse('tests/test_files/functions/base_function.py', 1), 'functions')
        expected_base_function_details: str = f"== `hello`\n\n{base_function.shape().generate()[0]}\n\n{base_function.docstring}"
        self.assertEqual(flatten(base_function.details()), expected_base_function_details)

        return_function: FunctionRef = FunctionRef(open_read_parse('tests/test_files/functions/return_function.py', 1), 'functions')
        expected_return_function_details: str = f"== `hello`\n\n{return_function.shape().generate()[0]}\n\n{return_function.docstring}"
        self.assertEqual(flatten(return_function.details()), expected_return_function_details)

        parameter_function: FunctionRef = FunctionRef(open_read_parse('tests/test_files/functions/parameter_function.py', 1), 'functions')
        expected_parameter_function_details: str = f"== `hello`\n\n{parameter_function.shape().generate()[0]}\n\n{parameter_function.docstring}"
        self.assertEqual(flatten(parameter_function.details()), expected_parameter_function_details)

        multiple_parameter_function: FunctionRef = FunctionRef(open_read_parse('tests/test_files/functions/multiple_parameter_function.py', 1), 'functions')
        expected_multiple_parameter_function_details: str = f"== `hello`\n\n{multiple_parameter_function.shape().generate()[0]}\n\n{multiple_parameter_function.docstring}"
        self.assertEqual(flatten(multiple_parameter_function.details()), expected_multiple_parameter_function_details)

        full_function: FunctionRef = FunctionRef(open_read_parse('tests/test_files/functions/full_function.py', 1), 'functions')
        expected_full_function_details: str = f"== `hello`\n\n{full_function.shape().generate()[0]}\n\n{full_function.docstring}"
        self.assertEqual(flatten(full_function.details()), expected_full_function_details)


class TestClassRef(unittest.TestCase):

    def test_attributes(self):
        base_class: ClassRef = ClassRef(open_read_parse('tests/test_files/classes/base_class.py', 1), 'classes')
        self.assertEqual(base_class.identifier, 'Cat')
        self.assertEqual(base_class.description, "cat class")
        self.assertEqual(base_class.reference, 'classes')
    
    def test_docstring_template(self):
        base_class: ClassRef = ClassRef(open_read_parse('tests/test_files/classes/base_class.py', 1), 'classes')
        expected_base_class_docstring: str = '\n'.join([
            "<DESCRIPTION>",
            '',
            "<EXPLANATION>",
            '',
            "=== attributes",
            '',
            "* _<ATTRIBUTE TYPE>_ *<ATTRIBUTE>* - <ATTRIBUTE_DESCRIPTION>",
            "* _<ATTRIBUTE TYPE>_ *<ATTRIBUTE>* - <ATTRIBUTE_DESCRIPTION>",
        ])
        self.assertEqual(base_class.docstring_template(), expected_base_class_docstring)

    def test_method_tables(self):
        base_class: ClassRef = ClassRef(open_read_parse('tests/test_files/classes/base_class.py', 1), 'classes')
        expected_base_class_tables: str = '\n'.join([
            "=== methods",
            '',
            "[cols='1,5']",
            "|===",
            '',
            "|`*rename*`",
            "|renames the cat",
            '',
            "|`*introduce*`",
            "|introduces the cat",
            '',
            "|`*call*`",
            "|meows",
            '',
            "|===",
            '',
            "[cols='1,1,5']",
            "|===",
            '',
            "|`_int_`",
            "|`*age_human_years*`",
            "|age of cat in human years",
            '',
            "|===",
        ])
        self.assertEqual(flatten(base_class.method_tables()), expected_base_class_tables)

    def test_shape(self):
        base_class: ClassRef = ClassRef(open_read_parse('tests/test_files/classes/base_class.py', 1), 'classes')
        expected_base_class_shape: str = "`classes.*Cat*`"
        self.assertEqual(base_class.shape().generate()[0], expected_base_class_shape)

    def test_details(self):
        pass


if __name__ == '__main__':
    unittest.main()