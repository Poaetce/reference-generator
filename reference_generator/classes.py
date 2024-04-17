import ast

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
            return '{value}[{slice}]'.format(
                value = value,
                slice = slice,
            )


class Function:
    def __init__(self, function: ast.FunctionDef) -> None:
        self.identifier: str = function.name

        arguments = function.args
        self.parameters: list[str] = [argument.arg for argument in arguments.args]
        self.parameter_types: list[str] = [get_type(argument.annotation) for argument in arguments.args]
        self.parameter_optional: list[bool] = [False] * (len(arguments.args) - len(arguments.defaults)) + [True] * len(arguments.defaults)

        self.return_type: str = get_type(function.returns)

        self.docstring: str = ast.get_docstring(function)
        self.description: str = ast.get_docstring(function).splitlines()[0] if self.docstring else None

    def docstring_template(self) -> str:
        main: str = "<DESCRIPTION>\n\n<EXPLANATION>"

        if self.parameters:
            parameter_list: str = "=== parameters"
            for index in range(len(self.parameters)):
                item: str = "\n* _{parameter_type}_ *{parameter}* {optional} - <PARAMETER DESCRIPTION>".format(
                    parameter_type = self.parameter_types[index],
                    parameter = self.parameters[index],
                    optional = '(optional)' if self.parameter_optional[index] else '',
                )
                parameter_list += item
            
            main += '\n\n' + parameter_list
        
        if self.return_type:
            returns: str = "=== returns\n_{return_type}_- <RETURN DESCRIPTION>".format(
                return_type = self.return_type,
            )

            main += '\n\n' + returns

        return main

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