1. Extracting data from websites other than Amazon
2. Extract data other than books (for example, other verticals Datafiniti
currently offers to its customers)

It's easy to scrape data from any site that has a consistent template, so where a certain item of data is located within a consistent DOM element -- Amazon, Ebay, etc, it becomes complicated when you want to scrape a large number of sites, or when there
are issues like pages that need javascript to be rendered (needs to be pre-rendered in a headless browser or through a service online), or some types of sites that use react or another framework affecting when data is injected into the DOM, as well as servers that prevent web crawling. Of course there are many more possible issues. 

I gave a talk about analyzing rap lyrics using Python (which involved scraping to get lyrics data) that tackled a lot of issues that can occur: 
https://www.youtube.com/watch?v=FQuIqtx1Z24

3. Parsing and packing 2 million books in a computationally efficient manner

One idea is to store the parsing data in a database or other faster storage vs. JSON

4. Extracting information intelligently i.e. without the need for someone
to review where field's data is located on a web page

I gave a talk at PyCon 2018 about using machine learning to do this, it's a very complex issue: 

https://www.youtube.com/watch?v=BwC01zoSRBc

5. Data storage in manner other than JSON, such as a datastore

Not hard, just store the data in a database instead of outputting to JSON