import ast
from . import documenter

def get_type(expression: ast.expr) -> str:
    if isinstance(expression, ast.Name):
        return expression.id
    
    elif isinstance(expression, ast.Constant):
        return expression.value
        
    elif isinstance(expression, ast.Tuple):
        elements: list[str] = [get_type(element) for element in expression.elts]
        return ", ".join(elements)
        
    elif isinstance(expression, ast.Subscript):
        value: str = get_type(expression.value)
        slice: str = get_type(expression.slice)
        return f"{value}[{slice}]"
        
    elif isinstance(expression, ast.BinOp):
        shape: str
        match expression.op:
            case ast.BitOr: shape = '|'
            case _ : shape = ''
        left: str = get_type(expression.left)
        right: str = get_type(expression.right)
        return f"{left} {shape} {right}"

    else:
        return ''


class _BaseRef:
    def __init__(self, node: ast.FunctionDef | ast.ClassDef, reference: str) -> None:
        self.identifier: str = node.name

        docstring: str = ast.get_docstring(node) or ''
        self.docstring: str = docstring.strip()
        self.description: str = docstring.strip().splitlines()[0] if docstring else ''

        self.reference: str = reference
        

class _BaseFunctionRef(_BaseRef):
    def __init__(self, node: ast.FunctionDef, reference: str) -> None:
        super().__init__(node, reference)

        arguments: ast.arguments = node.args
        self.parameters: list[str] = [argument.arg for argument in arguments.args]
        self.parameter_types: list[str] = [get_type(argument.annotation) if argument.annotation else '' for argument in arguments.args]
        self.parameter_optional: list[bool] = [False] * (len(arguments.args) - len(arguments.defaults)) + [True] * len(arguments.defaults)

        self.return_type: str = get_type(node.returns) if node.returns else ''

        self.level: int

    def docstring_template(self) -> str:
        content: documenter.document_list = []

        content.append(documenter.TextDoc("<DESCRIPTION>"))
        content.append(documenter.TextDoc("<EXPLANATION>"))

        if self.parameters:
            content.append(documenter.HeadingDoc("parameters", self.level + 2))
            parameter_list: documenter.ListDoc = documenter.ListDoc()
            for index in range(len(self.parameters)):
                parameter: str = self.parameters[index]
                parameter_type: str = self.parameter_types[index]
                optional: str = " (optional)" if self.parameter_optional[index] else ''
                parameter_list.add_item(f"_{parameter_type}_ *{parameter}*{optional} - <PARAMETER DESCRIPTION>")
            content.append(parameter_list)

        if self.return_type:
            content.append(documenter.HeadingDoc("returns", self.level + 2))
            content.append(documenter.TextDoc(f"_{self.return_type}_ - <RETURN DESCRIPTION>"))

        return documenter.flatten(content)

    def table_item(self) -> list[str]:
        content: list[str] = []

        if self.return_type:
            content.append(f"`_{self.return_type}_`")

        content.append(f"`*{self.identifier}*`")
        content.append(self.description)

        return content
    
    def shape(self) -> documenter.TextDoc:
        parameter_string: str = ''
        if self.parameters:
            parameter_string = ", ".join(f"_{parameter}_" for parameter in self.parameters)
        
        return documenter.TextDoc(f"`{self.reference}.*{self.identifier}*({parameter_string})`")
    
    def details(self) -> documenter.document_list:
        content: documenter.document_list = []

        content.append(documenter.HeadingDoc(f"`{self.identifier}`", self.level + 1))
        content.append(self.shape())
        content.append(documenter.TextDoc(self.docstring))

        return content


class FunctionRef(_BaseFunctionRef):
    def __init__(self, node: ast.FunctionDef, import_path: str) -> None:
        super().__init__(node, import_path)

        self.level: int = 1


class MethodRef(_BaseFunctionRef):
    def __init__(self, node: ast.FunctionDef, class_reference: str) -> None:
        super().__init__(node, class_reference)
        self.level: int = 2
        
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
    

class ConstructorRef(MethodRef):
    def __init__(self, node: ast.FunctionDef, import_path: str, identifier: str) -> None:
        super().__init__(node, import_path)

        self.identifier = identifier


class ClassRef(_BaseRef):
    def __init__(self, node: ast.ClassDef, import_path: str) -> None:
        super().__init__(node, import_path)
        
        self.constructor: ConstructorRef

        self.methods: list[MethodRef] = []
        for child in ast.iter_child_nodes(node):
            if type(child) == ast.FunctionDef:
                if child.name.startswith('_'):
                    if child.name == '__init__':
                        self.constructor = ConstructorRef(child, import_path, self.identifier)
                    else:
                        continue
                else:
                    self.methods.append(MethodRef(child, self.identifier))

    def docstring_template(self) -> str:
        content: documenter.document_list = []

        content.append(documenter.TextDoc("<DESCRIPTION>"))
        content.append(documenter.TextDoc("<EXPLANATION>"))

        content.append(documenter.HeadingDoc("attributes", 3))
        attribute_list: documenter.ListDoc = documenter.ListDoc()
        attribute_list.add_item("_<ATTRIBUTE TYPE>_ *<ATTRIBUTE>* - <ATTRIBUTE_DESCRIPTION>")
        attribute_list.add_item("_<ATTRIBUTE TYPE>_ *<ATTRIBUTE>* - <ATTRIBUTE_DESCRIPTION>")
        content.append(attribute_list)

        return documenter.flatten(content)

    def shape(self) -> documenter.TextDoc:
        return documenter.TextDoc(f"`{self.reference}.*{self.identifier}*`")
    
    def method_tables(self) -> documenter.document_list:
        content: documenter.document_list = []

        non_typed_table: documenter.TableDoc = documenter.TableDoc([1, 5])
        typed_table: documenter.TableDoc = documenter.TableDoc([1, 1, 5])

        for method in self.methods:
            if method.return_type:
                typed_table.add_item(method.table_item())
            else:
                non_typed_table.add_item(method.table_item())

        if non_typed_table.contents or typed_table.contents:
            content.append(documenter.HeadingDoc("methods", 3))
            if non_typed_table.contents:
                content.append(non_typed_table)
            if typed_table.contents:
                content.append(typed_table)

        return content

    def details(self) -> documenter.document_list:
        content: documenter.document_list = []

        content.append(documenter.HeadingDoc(f"`{self.identifier}`", 2))
        content.append(self.shape())
        content.append(documenter.TextDoc(self.docstring))
        content.append(documenter.LineDoc())
        content += self.method_tables()
        content.append(documenter.LineDoc())

        if self.constructor: content += self.constructor.details()
        for method in self.methods: content += method.details()

        return content

    
