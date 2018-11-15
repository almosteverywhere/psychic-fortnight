# Data Challenge
Book Packer

## Goal
Build an application that can extract relevant data and sort.

## Purpose
This exercise is designed to test your ability to use object-oriented design
principles, data structures, and standard algorithms to craft a small
application.  We will be looking at the correctness of your solution, however
just as important at the style of your code, its modularity, its extensibility,
documentation/commenting/instruction, and what kinds/how well the project is
tested.  As a small team we believe these principles are a key element of our
continued success.

The problem itself is not arbitrary but meant to simulate the type of work
Datafiniti performs. The transformation of unstructured data into structured
data involves parsing, computationally intensive algorithmic techniques and
ultimately some method of presenting that data in a human and machine digestible
format to our customers.

Have fun, be creative, and don't hesitate ask questions!

## Problem Description

### Part 1 - Data Extraction
In this repository you have been provided with the HTML source for twenty
randomly chosen Amazon book pages.  You will need to design and implement a
fully functioning application that can take these pages and extract meaningful
information from the raw source.

The extracted data must contain at least the following fields.  However,
additional fields are welcomed (feel free to review the
[Datafiniti schema](https://developer.datafiniti.co/docs/get-started)
for ideas):

* Title
* Author
* Price
* Shipping Weight
* ISBN-10

### Part 2 - Data Sorting and Storage
After extracting the above information you will need to divide these twenty
books into N boxes for shipping with each box having no more than ten pounds of
books.

Your application should output its results in a valid and well structured JSON
document like the example below:

```json
[
    {
        "id": 1,
        "totalWeight": "1.1 pounds",
        "contents": [
            {
                "title": "The Great Big Beautiful Tomorrow",
                "author": "Cory Doctorow",
                "price": "$9.82 USD",
                "shipping_weight": "0.8 pounds",
                "isbn-10": 1604864044
            },
            . . .
        ]
    },
    . . .
]
```

Once your solution is completed please add an EXTENSIONS.md file to your
solution.  In this give us feedback on ways your application could be modified
to handle more challenging problems.  Some examples include:

    1. Extracting data from websites other than Amazon
    2. Extract data other than books (for example, other verticals Datafiniti
    currently offers to its customers)
    3. Parsing and packing 2 million books in a computationally efficient manner
    4. Extracting information intelligently i.e. without the need for someone
    to review where field's data is located on a web page
    5. Data storage in manner other than JSON, such as a datastore

Do not feel the need to address each of these or limit yourself to only those
additional problems.  Also, if you feel some of these examples are in fact
handled within your solution feel free to describe.

### Restrictions and Scope
The following details any restrictions on style or scope (or lack there of):

- Any programming language is fine (we mostly utilize Java, JavaScript, and
some Python)
- You may use any third party libraries you wish. Any dependencies must be
fully managed by a standard build tool for the language used.
- Instructions on how to setup and operate should be clear (as we expect with
any project we develop internally)
- Deployment to any cloud provider is not necessary, but if local deployment of
any tools, environments, or similar is desired feel free (please provide
instruction for us to duplicate)

## What We'll Be Reviewing
The main points we will be reviewing:

- Does the application function as expected and outlined in the purpose?
- Code readability and reusability (how "productized" your code is)?
- Does the project contain testing (unit, integration, etc)?
- Are all design considerations/decisions explained and the project documented?

## Submission Instructions
Setup and submit a personal GitHub repository with the project's code base.
Email us a link with the finished code.
