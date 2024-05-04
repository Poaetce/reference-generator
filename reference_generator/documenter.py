class LineDoc:
    def generate(self) -> list[str]:
        # returns a horizontal rule as a list
        return ["'''"]


class TextDoc:
    def __init__(self, content: str) -> None:
        self.content: str = content # content of the text

    def generate(self) -> list[str]:
        # returns content as a list
        return [self.content]


class HeadingDoc:
    def __init__(self, content: str, level: int) -> None:
        self.content: str = content # content of the heading
        self.level: int = level # heading level
    
    def generate(self) -> list[str]:
        # returns the heading as a list
        return [f"{'=' * self.level} {self.content}"]


class ListDoc:
    def __init__(self) -> None:
        self.contents: list[str] = [] # items in the list
        self.levels: list[int] = [] # indent level corresponding to the item

    def add_item(self, content: str, level: int = 1) -> None:
        # appends item content and level
        self.contents.append(content)
        self.levels.append(level)
    
    def generate(self) -> list[str]:
        # returns each list content in its respective level in a list
        return [f"{'*' * self.levels[index]} {self.contents[index]}" for index in range(len(self.contents))]


class TableDoc:
    def __init__(self, shape: list[int]) -> None:
        self.shape: list[int] = shape # column shape of the table
        self.contents: list[list[str]] = [] # list of items in rows

    def add_item(self, content: list[str]) -> None:
        # appends new item to content
        self.contents.append(content)
    
    def generate(self) -> list[str]:
        table: list[str] = [] #empty list for table
        
        # creates table shape and opening
        table.append(f"[cols='{','.join(str(value) for value in self.shape)}']")
        table.append("|===")
        table.append('')

        # appends each item to the table separated by an empty string
        for item in self.contents:
            for column in item:
                table.append(f"|{column}")
            table.append('')

        # closes table
        table.append("|===")

        #returns table
        return table


document_list = list[LineDoc | TextDoc | HeadingDoc | ListDoc | TableDoc]


def flatten(document: document_list) -> str:
    elements: list[str] = [] #empty list for elements to flatten

    # appends each element followed by an empty string
    for element in document:
        elements += element.generate()
        elements.append('')

    # flattens the elements list to a line separated string
    return '\n'.join(elements).strip()