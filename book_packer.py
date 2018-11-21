import codecs
import os
import re
import json
from bs4 import BeautifulSoup
from operator import attrgetter

OUTPUT_FILE = "data.json"
DATA_DIR = "data"


class Book(object):
    """
    Represents a book, it has an author, title, price, shipping weight and ISBN 10 number.
    The packed field exists to make sorting it into boxes easier. 
    """
    def __init__(self, author="", title="", price=0, weight=0.0, isbn_10=""):
        self.author = author
        self.title = title
        self.price = price
        self.weight = weight
        self.isbn_10 = isbn_10
        # This is to make sorting the book into boxes easier. 
        self.packed = False
        
    def __str__(self):
        return "%s %s %s %s %s" % (self.author, self.title, self.price, 
                self.weight, self.isbn_10)


class Box(object):
    """
    Represents a box, it has an id, a total weight of all the books inside, and
    a list of books
    """

    def __init__(self, id=None):
        """
        Id is mostly to give the box number for json
        Total weight is the total weight of all books
        Contents is a list of all books contained in the box. 
        """
        self.id = id 
        self.totalWeight = 0 
        self.contents = []
        
        
    def __str__(self):
        return "%s %s %s" % (self.id, self.totalWeight, self.contents)

    def append(self, book):
        """
        Adds a book to the contents of the box and add the weight of the book to the 
        total box weight. 
        """
        self.contents.append(book)
        # This occasionally gets strange floating point errors, which can be solved
        # by using Decimal, however Decimal is not JSON serializable, so we're leaving
        # as is for now. This should be solved in a production application.
        self.totalWeight = self.totalWeight + book.weight


def get_book_data_from_file(filename):
    """
    Extract the relevant fields from one html page
    and returns a Book object
    :param filename to extract the data from 
    :return Book object 
    """

    f = codecs.open("data/" + filename)
    f = f.read()
    soup = BeautifulSoup(f, features="html.parser")

    # Title, author and price are straightforward because they're well marked in divs
    title = soup.select("#btAsinTitle")[0].text
    author = soup.select(".buying span a")[0].text
    
    # Sometimes it can have a rental price but in most cases it has this price
    price_div_list = soup.select("#actualPriceValue")
    if price_div_list:
        price = price_div_list[0].text
    else: 
        # this is complicated, for items where you can rent, the 
        # first price will be a sale price, the next
        # a true rental price but they are both marked up as rentPrice in the html
        price_div_list = soup.select(".buyNewOffers .rentPrice")
        if price_div_list:
            price = price_div_list = price_div_list[0].text
        else:
            # Should probably check this doesn't cause problems, for small data it's fine
            # but for production should check this more. 
            price = "0"
    
    # These don't have consistent locations in the list and they also don't
    # have markup around them, so we have to look at strings surrounding value we want.
    product_details_ul = soup.select("td.bucket ul li")
    
    for li in product_details_ul:
        # weight looks like this: 
        # Shipping Weight: 1.2 pounds (View shipping rates and policies)
        if re.match("Shipping Weight:", li.text):
            weight = li.text
            weight = weight.split("(")[0]
            weight = weight.split(":")[1]
            weight = weight.split("pounds")[0]
            weight = weight.strip()
            weight = float(weight)
            
        if re.match("ISBN-10", li.text):
            isbn_10 = li.text
            isbn_10 = isbn_10.split(":")[1]
            isbn_10 = isbn_10.strip()
            
    book = Book(title=title, author=author, price=price, weight=weight, isbn_10=isbn_10)
    return book 


def sort_books_by_weight(books):
    """
    Take a list of Book objects and return a list of Book objects sorted by weight. 
    :param books list of Book objects
    :return a list of Book objects sorted by weight  
    """
    sorted_books = sorted(books, key=attrgetter('weight'), reverse=True) 
    
    return sorted_books


def sort_books_into_boxes(sorted_books):
    """
    Given a sorted list of book objects, return a list of boxes containing a reasonable
    packing of the books into boxes, with each box containing not more than 10 pounds of books.
    Sorting like this is related to knapsack problem, which is NP-complete, 
    in the interest of time we implemented a simple solution since our list of books is not long. 
    :param List of Book objects sorted by weight
    :return List of Box objects each box containing not more than 10 pounds of books.
    """
    
    all_boxes = []
    total_boxes = 1
    current_box = Box(id=total_boxes)
    books_not_packed = len(sorted_books)
    
    # Books are sorted from the highest to lowest weight. Find the highest weight book
    # that will fit into the current box. When we can't find any more books to fit in,
    # start a new box.

    # We set a boolean in the Box object called "packed" to make sure we only pack each book
    # once, this avoids having to deal with a parallel list of packed bits, or having to remove
    # packed books from the list of existing books

    # While there's still books to be packed
    while(books_not_packed) > 0:
        # go over the list of all books and see if any can fit in the current box
        for i in range(0,len(sorted_books)):
            book = sorted_books[i]
            # 0 means not packed yet
            # If this book is unpacked and can fit in the current box, put it in the box
            if not book.packed and (book.weight + current_box.totalWeight) <= 10:
                # add this book to the box
                # the box object handles updating its total weight
                current_box.append(book)
                
                # set this book to packed
                book.packed = True 

                # One less book to pack 
                books_not_packed = books_not_packed - 1
 
        # start a new box
        all_boxes.append(current_box)
        # we keep track of total_boxes so far so we can assign an id to each box 
        # for the JSON output
        total_boxes = total_boxes + 1
        current_box = Box(id=total_boxes)

    return all_boxes 
            
 
def export_boxes_to_json(all_boxes, output_file=OUTPUT_FILE):
    """
    Given a list of Box objects, export contents to json format
    We don't return anything because it's easier to dump the json directly to a file.  
    :param A list of Box objects
    :param a file to output the json to
    """

    f = open(output_file, "w")
    # We need this default because Python objects are not directly serializable by json
    json.dump(all_boxes, f, indent=4, default=lambda x: x.__dict__)


def extract_book_data(directory="data"):
    """
    Given a set of sample book files, extract the book data, pack the 20 books into
    N boxes with a weight of no more than 10 pounds each, and output the box data to
    a JSON file. 
    :param directory where the data files are 
    """

    books = []

    # extract book data from files 
    for filename in os.listdir(directory):
        book = get_book_data_from_file(filename)
        books.append(book)

    # sort the list of books by weight:
    sorted_books = sort_books_by_weight(books)

    # put the books into different boxes
    all_boxes = sort_books_into_boxes(books)

    # boxes to json format
    export_boxes_to_json(all_boxes)

    
if __name__ == "__main__":

    extract_book_data(DATA_DIR)
    
   