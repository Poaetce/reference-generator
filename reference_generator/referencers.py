import ast

CONNECTOR: str = "\n\n'''\n\n"


def get_type(expression: ast.expr) -> str:
    match type(expression):
        case ast.Name:
            return expression.id
        case ast.Constant:
            return expression.value
        case ast.Tuple:
            elements: list[str] = [get_type(element) for element in expression.elts]
            return ', '.join(elements)
        case ast.Subscript:
            value: str = get_type(expression.value)
            slice: str = get_type(expression.slice)
            return f'{value}[{slice}]'
        

class _BaseReferencer:
    def __init__(self, node: ast.stmt, reference: str) -> None:
        self.identifier: str = node.name

        docstring: str = ast.get_docstring(node) or None
        self.docstring: str = docstring.strip() if docstring else None
        self.description: str = docstring.strip().splitlines()[0] if docstring else None

        self.reference: str = reference
        

class _BaseFunctionReferencer(_BaseReferencer):
    def __init__(self, function_node: ast.FunctionDef, reference: str) -> None:
        _BaseReferencer.__init__(self, function_node, reference)

        arguments: ast.arguments = function_node.args
        self.parameters: list[str] = [argument.arg for argument in arguments.args]
        self.parameter_types: list[str] = [get_type(argument.annotation) for argument in arguments.args]
        self.parameter_optional: list[bool] = [False] * (len(arguments.args) - len(arguments.defaults)) + [True] * len(arguments.defaults)

        self.return_type: str = get_type(function_node.returns)

    def table_item(self) -> str:
        main: str = "|`*{identifier}*`\n|{description}".format(
            identifier = self.identifier,
            description = self.description or '',
        )
        
        if self.return_type:
            main = "|`_{return_type}_`\n".format(
                return_type = self.return_type,
            ) + main
        
        return main
    
    def shape(self) -> str:
        parameters: str = '_' + '_, _'.join(self.parameters) + '_' if self.parameters else ''

        return f"`{self.reference}.*{self.identifier}*({parameters})`"
    
    def details(self) -> str:
        return f"== `{self.identifier}`\n\n{self.shape()}\n\n{self.docstring}"


class TopLevelFunctionReferencer(_BaseFunctionReferencer):
    def __init__(self, function_node: ast.FunctionDef, import_path: str) -> None:
        _BaseFunctionReferencer.__init__(self, function_node, import_path)

    def docstring_template(self) -> str:
        main: str = "<DESCRIPTION>\n\n<EXPLANATION>"

        if self.parameters:
            parameter_list: str = "=== parameters"
            for index in range(len(self.parameters)):
                item: str = "\n* _{parameter_type}_ *{parameter}*{optional} - <PARAMETER DESCRIPTION>".format(
                    parameter_type = self.parameter_types[index],
                    parameter = self.parameters[index],
                    optional = " (optional)" if self.parameter_optional[index] else '',
                )
                parameter_list += item
            
            main += '\n\n' + parameter_list
        
        if self.return_type:
            returns: str = "=== returns\n_{return_type}_ - <RETURN DESCRIPTION>".format(
                return_type = self.return_type,
            )

            main += '\n\n' + returns

        return main


class MethodReferencer(_BaseFunctionReferencer):
    def __init__(self, function_node: ast.FunctionDef, class_reference: str) -> None:
        _BaseFunctionReferencer.__init__(self, function_node, class_reference)
        
        self.static: bool = True if 'cls' in self.parameters else False

        for parameter in self.parameters:
            if parameter in [
                'self',
                'cls',
            ]:
                index: int = self.parameters.index(parameter)
                self.parameters.pop(index)
                self.parameter_types.pop(index)
                self.parameter_optional.pop(index)


    def docstring_template(self) -> str:
        main: str = "<DESCRIPTION>\n\n<EXPLANATION>"

        if self.parameters:
            parameter_list: str = "==== parameters"
            for index in range(len(self.parameters)):
                item: str = "\n* _{parameter_type}_ *{parameter}*{optional} - <PARAMETER DESCRIPTION>".format(
                    parameter_type = self.parameter_types[index],
                    parameter = self.parameters[index],
                    optional = " (optional)" if self.parameter_optional[index] else '',
                )
                parameter_list += item
            
            main += '\n\n' + parameter_list
        
        if self.return_type:
            returns: str = "==== returns\n_{return_type}_ - <RETURN DESCRIPTION>".format(
                return_type = self.return_type,
            )

            main += '\n\n' + returns

        return main
    

class ConstructorReferencer(MethodReferencer):
    def __init__(self, function_node: ast.FunctionDef, import_path: str, identifier: str) -> None:
        MethodReferencer.__init__(self, function_node, import_path)

        self.identifier = identifier

    def docstring_template(self) -> str:
        main: str = ''

        if self.parameters:
            parameter_list: str = "==== parameters"
            for index in range(len(self.parameters)):
                item: str = "\n* _{parameter_type}_ *{parameter}*{optional} - <PARAMETER DESCRIPTION>".format(
                    parameter_type = self.parameter_types[index],
                    parameter = self.parameters[index],
                    optional = " (optional)" if self.parameter_optional[index] else '',
                )
                parameter_list += item
            
            main = parameter_list

        return main


class ClassReferencer(_BaseReferencer):
    def __init__(self, class_node: ast.ClassDef, import_path: str) -> None:
        _BaseReferencer.__init__(self, class_node, import_path)
        
        self.constructor: ConstructorReferencer

        self.methods: list[MethodReferencer] = []
        for node in ast.iter_child_nodes(class_node):
            if type(node) == ast.FunctionDef:
                if node.name == '__init__':
                    self.constructor = ConstructorReferencer(node, import_path, self.identifier)
                else:
                    self.methods.append(MethodReferencer(node, self.identifier))

    def docstring_template(self) -> str:
        return "<DESCRIPTION>\n\n<EXPLANATION>\n\n=== attributes\n* _<ATTRIBUTE TYPE>_ *<ATTRIBUTE>* - <ATTRIBUTE_DESCRIPTION>"

    def shape(self) -> str:
        return f"`{self.reference}.*{self.identifier}*`"
    
    def method_tables(self) -> str:
        main: str = '=== methods\n\n'

        if self.methods:
            non_typed_table: str = ''
            typed_table: str = ''

            for method in self.methods:
                if method.return_type:
                    typed_table += method.table_item() + '\n\n'
                else:
                    non_typed_table += method.table_item() + '\n\n'

            non_typed_table = (f"[cols='1,5']\n|===\n\n{non_typed_table}|===") if non_typed_table else ''
            typed_table = (f"[cols='1,1,5']\n|===\n\n{typed_table}|===") if typed_table else ''

            main += '\n\n'.join([non_typed_table, typed_table])

        return main

    def details(self) -> str:
        main: str = f"== `{self.identifier}`\n\n{self.shape()}\n\n{self.docstring}{CONNECTOR}{self.method_tables()}{CONNECTOR}"

        main += (self.constructor.details() if self.constructor else '') + CONNECTOR

        if self.methods:
            main += CONNECTOR.join(method.details() for method in self.methods)
        
        return main


    
