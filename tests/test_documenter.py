import unittest
from reference_generator.documenter import LineDoc, TextDoc, HeadingDoc, ListDoc, TableDoc
from reference_generator.documenter import flatten, document_list

class TestLineDoc(unittest.TestCase):

    def test_generate(self) -> None:
        line: LineDoc = LineDoc()
        expected_line: list[str] = ["'''"]
        self.assertEqual(line.generate(), expected_line)


class TestTextDoc(unittest.TestCase):

    def test_generate(self) -> None:
        text: TextDoc = TextDoc("this is a text")
        expected_text: list[str] = ["this is a text"]
        self.assertEqual(text.generate(), expected_text)


class TestHeadingDoc(unittest.TestCase):

    def test_generate(self) -> None:
        large_heading: HeadingDoc = HeadingDoc("this is a heading", 1)
        expected_large_heading: list[str] = ["= this is a heading"]
        self.assertEqual(large_heading.generate(), expected_large_heading)

        small_heading: HeadingDoc = HeadingDoc("this is a heading", 6)
        expected_small_heading: list[str] = ["====== this is a heading"]
        self.assertEqual(small_heading.generate(), expected_small_heading)

class TestListDoc(unittest.TestCase):

    def test_generate(self) -> None:
        full_list: ListDoc = ListDoc()
        full_list.add_item("this is an item")
        full_list.add_item("this is another item")
        full_list.add_item("this is a nested item", 2)
        full_list.add_item("this is a even more nested item", 3)
        expected_full_list: list[str] = [
            "* this is an item",
            "* this is another item",
            "** this is a nested item",
            "*** this is a even more nested item",
        ]
        self.assertEqual(full_list.generate(), expected_full_list)


class TestTableDoc(unittest.TestCase):

    def test_generate(self) -> None:
        single_table: TableDoc = TableDoc([1])
        single_table.add_item(["item 1"])
        single_table.add_item(["item 2"])
        single_table.add_item(["item 3"])
        expected_single_table: list[str] = [
            "[cols='1']",
            "|===",
            '',
            "|item 1",
            '',
            "|item 2",
            '',
            "|item 3",
            '',
            "|===",
        ]
        self.assertEqual(single_table.generate(), expected_single_table)

        triple_table: TableDoc = TableDoc([1, 1, 1])
        triple_table.add_item(["1", "0001", "one"])
        triple_table.add_item(["2", "0010", "two"])
        triple_table.add_item(["3", "0011", "three"])
        expected_triple_table: list[str] = [
            "[cols='1,1,1']",
            "|===",
            '',
            "|1",
            "|0001",
            "|one",
            '',
            "|2",
            "|0010",
            "|two",
            '',
            "|3",
            "|0011",
            "|three",
            '',
            "|===",
        ]
        self.assertEqual(triple_table.generate(), expected_triple_table)


if __name__ == '__main__':
    unittest.main()