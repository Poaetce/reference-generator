class LineDoc:
    def generate(self) -> list[str]:
        return ["'''"]


class TextDoc:
    def __init__(self, content: str) -> None:
        self.content: str = content

    def generate(self) -> list[str]:
        return [self.content]


class HeadingDoc:
    def __init__(self, content: str, level: int) -> None:
        self.content: str = content
        self.level: int = level
    
    def generate(self) -> list[str]:
        return [f"{'=' * self.level} {self.content}"]


class ListDoc:
    def __init__(self) -> None:
        self.contents: list[str] = []
        self.levels: list[int] = []

    def add_item(self, content: str, level: int = 1) -> None:
        self.contents.append(content)
        self.levels.append(level)
    
    def generate(self) -> list[str]:
        return [f"{'*' * self.levels[index]} {self.contents[index]}" for index in range(len(self.contents))]


class TableDoc:
    def __init__(self, shape: list[int]) -> None:
        self.shape: list[int] = shape
        self.contents: list[list[str]] = []

    def add_item(self, content: list[str]) -> None:
        self.contents.append(content)
    
    def generate(self) -> list[str]:
        table: list[str] = []
        
        table.append(f"[cols='{','.join(str(value) for value in self.shape)}']")
        table.append("|===")
        table.append('')

        for item in self.contents:
            for column in item:
                table.append(f"|{column}")
            table.append('')

        table.append("|===")

        return table


document_list = list[LineDoc | TextDoc | HeadingDoc | ListDoc | TableDoc]


def flatten(document: document_list) -> str:
    elements: list[str] = []
    for element in document:
        elements += element.generate()
        elements.append('')
    return '\n'.join(elements).strip()