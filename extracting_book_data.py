from bs4 import BeautifulSoup
from operator import attrgetter
import codecs
import os
import re
import json

OUTPUT_FILE = "data.json"

# Class to represent a book
class Book(object):
    def __init__(self, author="", title="", price=0, weight=0.0, isbn_10=""):
        self.author = author
        self.title = title
        self.price = price
        self.weight = weight
        self.isbn_10 = isbn_10
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
        Adds a book to the contents of the box and updates the total box weight
        """
        self.contents.append(book)
        self.totalWeight = self.totalWeight + book.weight


def get_book_data_from_file(filename):
    """
    Takes a filename 
    Returns a book object with the relevant data
    """

    f = codecs.open("data/" + filename)
    f = f.read()
    soup = BeautifulSoup(f, features="html.parser")
    # title, author and price are straightforward because they're well marked in divs
    title = soup.select("#btAsinTitle")[0].text
    author = soup.select(".buying span a")[0].text
    
    # sometimes it can have a rental price but in most cases it has this price
    price_div_list = soup.select("#actualPriceValue")
    if price_div_list:
        price = price_div_list[0].text
    else: 
        # this is super sketchy, for items where you can rent, the 
        # first price will be a sale price, the next
        # a true rental price but they are both marked up as rentPrice in the html
        price_div_list = soup.select(".buyNewOffers .rentPrice")
        if price_div_list:
            price = price_div_list = price_div_list[0].text
        else:
            price = "N/A"
    
    # these don't have consistent locations in the list and they also don't
    #  have markup around them
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
    Takes a list of book objects, returns a list of books objects sorted by weight
    """
    sorted_books = sorted(books, key=attrgetter('weight'), reverse=True) 
    
    return sorted_books


def sort_books_into_boxes(sorted_books):
    # do it by books:
    all_boxes = []
    total_boxes = 1
    current_box = Box(id=total_boxes)
    books_not_packed = len(sorted_books)
    
    while(books_not_packed) > 0:
        for i in range(0,len(sorted_books)):
            book = sorted_books[i]
            # 0 means not sorted yet
            if not book.packed and (book.weight + current_box.totalWeight) <= 10:
                # add this book to the box
                current_box.append(book)
                
                # set this book to sorted
                book.packed = True 
                books_not_packed = books_not_packed - 1
 
        # start a new box
        all_boxes.append(current_box)
        total_boxes = total_boxes + 1
        current_box = Box(id=total_boxes)

    return all_boxes 
            
 
def export_boxes_to_json(all_boxes, output_file=OUTPUT_FILE):
    """
    get a list of Box objects and export contents to json format
    We don't return anything because it's easier to dump the json directly to a file.  
    """

    f = open(output_file, "w")
    json.dump(all_boxes, f, indent=4, default=lambda x: x.__dict__)
    

if __name__ == "__main__":

    books = []

    # extract book data from files 
    for filename in os.listdir("data"):
        book = get_book_data_from_file(filename)
        books.append(book)

    # sort the list of books by weight:
    sorted_books = sort_books_by_weight(books)

    # put the books into different boxes
    all_boxes = sort_books_into_boxes(books)

    # boxes to json format
    export_boxes_to_json(all_boxes)
