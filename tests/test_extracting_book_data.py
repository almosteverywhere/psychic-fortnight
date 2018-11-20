from extracting_book_data import get_book_data_from_file, sort_books_by_weight, \
    sort_books_into_boxes, Book, Box
import unittest


class TestGetBookDataFromFile(unittest.TestCase):
    def test_get_book_data_from_file(self):

        # ideally we'd mock up a test file here, but in the interest of time
        # let's use an existing one with known values 
        book = get_book_data_from_file("book9.html")
        self.assertEqual(book.author, u"Stephen Wolfram")
        self.assertEqual(book.title, u"A New Kind of Science [Hardcover]")
        self.assertEqual(book.price, u"$35.25")
        self.assertEqual(book.isbn_10, u"1579550088")
        self.assertEqual(book.weight, 5.6)


class TestSortBooksByWeight(unittest.TestCase):

    def test_sort_books_by_weight(self):

        book1 = Book(author="Foo", weight=10)
        book2 = Book(author="Bar", weight=1)
        book3 = Book(author="Baz", weight=5)
        books = [book1,book2,book3]
        self.assertEqual(sort_books_by_weight(books), [book1, book3, book2])

    def test_sort_empty_list_returns_empty_list(self):
        self.assertEqual(sort_books_by_weight([]), [])

class TestSortBooksIntoBoxes(unittest.TestCase):

    def test_sort_books_into_boxes(self):
        book1 = Book(author="Foo", weight=10)
        book2 = Book(author="Bar", weight=1)
        book3 = Book(author="Baz", weight=5)
        
        books = [book1,book2,book3]
        
        box1 = Box(id=1)
        box1.append(book1)
        box2 = Box(id=2)
        box2.append(book3)
        box2.append(book2)

        # getting object deep comparisons related issues here, just look to make sure
        # boxes have the requisite weight
        list_of_boxes = sort_books_into_boxes(books)
        self.assertEqual(list_of_boxes[0].totalWeight, box1.totalWeight)
        self.assertEqual(list_of_boxes[1].totalWeight, box2.totalWeight)


# that it initializes book object properly, that it sorts books into boxes properly


if __name__ == '__main__':
    unittest.main()