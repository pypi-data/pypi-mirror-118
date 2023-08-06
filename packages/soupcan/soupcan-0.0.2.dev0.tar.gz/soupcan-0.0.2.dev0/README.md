# **SoupCan** : Your BeautifulSoup in a Can

*SoupCan* aims to simplify the process of designing a Python tool for extracting and displaying webpage content.

It builds on the wonderful library, Beautiful Soup,  allowing you to leverage this library's powerful features in your tool.

All you need to do to design your tool with SoupCan is to define the kinds of content that you wish to extract, select which parts of the content you wish to display, and SoupCan will do the rest.

SoupCan is ideal for designing a tool that works in a Jupyter notebook, as SoupCan, out of the box, supports HTML rendering of content in notebook cells.

## Prerequisites

To get started with SoupCan, you'll need to have:

* some familiarity with HTML generally, and particularly with the HTML of the webpage that you wish to extract and display content from.

* knowledge of the Beautiful Soup library, and especially its search method, `find()`.

* an understanding of object-oriented programming concepts, and how you apply them in Python.

## Software Requirements

To use SoupCan in your tool, you'll need to have:

* Python 3.6+; and 
* the Beautiful Soup library

For information on the various ways you can install the Beautiful Soup library, see this library's own [documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup).

## Installation

To install SoupCan, execute the following in your local or virtual Python environment:

```bash
pip install soupcan
```

If you don't already have the Beautiful Soup library installed in your environment, this command will install this library (from the PyPI repository) too. 

Under the hood, the Beautiful Soup library, by default, uses the [HTML parser](https://docs.python.org/3/library/html.parser.html#module-html.parser) that comes with the standard libray, [html](https://docs.python.org/3/library/html.html). If you wish to use a third-party parser, like [lxml](https://lxml.de/) or [html5lib](https://github.com/html5lib/), instead, you'll have to install them yourself, which you can do by adding `lxml html5lub` to the above command. 

It is also up to you how you get the HTML content from a webpage. SoupCan is not a webscraper package, and so you'll have to implement those procedures yourself when designing your tool.

Finally, SoupCan does not include any Jupyter software as a dependency.  You or your tool users will need to have Jupyter, if you wish to make the most of SoupCan's display features.

## Basic example

Let's design a simple package with SoupCan, and apply it to a basic html document:

```Python
import soupcan as sc

class Paragraph(sc.Content):
    """Return a Content-typed object for <p></p> element"""
    _KIND = {"name": "p"}
    
    text = sc.Property(lambda self: self.text, doc="Return text of paragraph")
    
class Paragraphs(sc.Contents):
    """Return a Contents-typed object with Paragraph-typed object"""
    _CONTENT = Paragraph
    
class Body(sc.Content):
    """Return a Content-typed object for a <body></body> element"""
    _KIND = {"name": "body"}  

    from_string = sc.AltConstructor() 
    
    paragraphs = sc.Property(Paragraphs, doc="Return paragraphs")    

## example html document (originally used in the BeautifulSoup documentation)
    
html= """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>
<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""

body = Body.from_string(html,'html.parser')

print(body.paragraphs[0].text)  # print The Dormouse's story as text
```

You could instead create a `Body`-typed object by initialising it with a BeautifulSoup object, like follows:

```Python
from bs4 import BeautifulSoup
soup = BeautifulSoup(html, features='html.parser')
body2  = Body(soup)
```                     

However, the `from_string()` alternative-constructor method, implemented using SoupCan's `AltConstructor` class, does all of this for you, under the hood. 

You can extend this example package:

* by adding other Content-types, say for a Hyperlink class 

```Python
class Hyerlink(sc.Content):  
    """Return a Content-type object for an <a></a> element"""    
    _KIND = {"name": "a"}

 ```
  
* by creating separate a Content-type for more specific piece of content, say for a `class=title` paragraph:

```Python
class TitlePargraph(sc.Content):        
    """Return a Content-type object for a <p class='title'></p> element"""    
    _KIND = {"name": "p", 'class_':"title"}

```

Extend an existing Content type, by subclassing it and then adding  
(say using the Property class):

```Python
class Link(Hyerlink):
    """Return a extented Content-type object for an <a></a> element."""
    
    href = sc.Property(lambda self: self.href, doc = "Return hyperlink reference")    
    text = sc.Property(lambda self: self.text, doc= "Return hyperlink text")
```

The `Propery` class is a (non-data) descriptor class. It works much like a property method:

```Python
class ExtendedTitlePargraph(TitlePargraph):
    
    @property
    def text(self):
        "Return text string"
        return self._element.text
```
In the above, the `self._element` is the underlying BeautifulSoup object at the `<p>`element (with the "class=title" attribute).



    
## License
[BSD 3](LICENSE)

