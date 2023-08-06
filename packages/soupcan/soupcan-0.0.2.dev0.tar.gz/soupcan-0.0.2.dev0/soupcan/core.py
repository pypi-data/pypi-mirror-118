"""Module to help you define a Content or Contents type."""

import types
from typing import (
    Union,
    Optional,
    Dict,
    Tuple,
    Callable,
    TypeVar,
    Type,
    Any,
    ClassVar,
    NoReturn,
)
import functools

from bs4 import (
    SoupStrainer,
    BeautifulSoup,
    Tag,
    CData,
    Comment,
    NavigableString,
    PageElement,
)

element_types = (BeautifulSoup, Tag, CData, Comment, NavigableString)
"""BeautifulSoup object types"""

# for typing
SoupType = TypeVar(
    "SoupType", BeautifulSoup, Tag, CData, Comment, NavigableString
)
"""A generic type for BeautifulSoup object types"""


class ContentNotFound(Exception):
    """Raise if HTML content does not exist."""
    pass

    
def raise_content_error() -> NoReturn:
    """Raise ContentNotFound."""
    raise ContentNotFound


def get(self, call: Callable, default_value=None, *args, **kwargs):
    """Get content object.
    
    Parameters
    ----------
    call :
        a callable whose first argument is a Beatiful Soup-typed object.
    default_value:
        a value that the function defaults to if the callable raises an 
        ContentNotFound.
    
    """
    try:
        return call(self._element, *args, **kwargs)
    except ContentNotFound:
        return default_value


class Content:
    """
    Base class for defining a Content type.
    
    A Content type let you represent a piece of HTML content as an object. 
    You can then use this object to extract and display the content,
    and parts of that content.
       
    To create a Content type, subclass this base class, and set the class 
    attribute, ``_KIND``. Add methods to your Content type to let users 
    extract the content, and any sub-part of the content.  
    
    Attributes
    ----------
    _KIND: dict
    
        define the *kind* of HTML content with the keyword arguments of BeautifulSoup 
        `.find`  method. See BeautifulSoup documentation for
        `details <https://www.crummy.com/software/BeautifulSoup/bs4/doc/#find>`_.
        
    Raises
    ------
    NotImplementedError
        if you fail to set the _KIND attribute. 
    
    TypeError
        if you don't set to _KIND attribute a Python dictionary object.
        
    """

    _KIND: ClassVar[
        Dict[Optional[str], Union[str, int, bool, Callable[..., Any]]]
    ]

    @classmethod
    def __init_subclass__(cls, **kwargs):

        if not hasattr(cls, "_KIND"):
            raise NotImplementedError("You must define _KIND attribute.")

        if not isinstance(cls._KIND, dict):
            raise TypeError("You must set _KIND to a dictionary.")

        if not hasattr(cls, "__slots___"):
            setattr(cls, "__slots__", ("_element",))

        super().__init_subclass__(**kwargs)

    def __init__(self, element: SoupType):
        if not isinstance(element, element_types):
            raise TypeError(
                """An error has occurred with the design of this tool."""
                )

        self._element =  (
            self._get_current(element, self._KIND)
            or self._get_nearest_parent(element, self._KIND)
            or self._get_nearest_child(element, self._KIND)
            or raise_content_error()
        )

    @staticmethod
    def _get_current(element, kind) -> Optional[SoupType]:
        """Return current soup element object iff the object matches the keyword arguments."""
        return SoupStrainer(**kind).search(element)
    
    @staticmethod
    def _get_nearest_parent(element, kind) -> Optional[SoupType]:
        """Return a parent soup element object iff the parent object matches the keyword
        arguments."""
        if kind.get("text") != None:
            return None
        return element.find_parent(**kind)

    @staticmethod
    def _get_nearest_child(element, kind) -> Optional[SoupType]:
        """Return a soup element object iff the child object matches the keyword arguments."""
        if not element.name:
            return None
        return element.find(**kind)
            

    def __eq__(self, other) -> bool:
        """Return True iff ``other`` has the same element object."""
        if not isinstance(other, self.__class__):
            return False
        return self._element == other._element

    def __hash__(self):
        """Return the element object's own hash"""
        return self._element.__hash__()

    def __str__(self):
        """Return a plain-text representation of the soup element object."""
        return f"{self._element.text if self._element.name else self._element}"

    def _repr_html_(self):
        """Render a html representation of the soup element object (Jupyer notebook only)."""
        return str(self._element)
    
    
class Property:
    """Add a property method to a Content type.
    
    Parameters
    ----------
    call :
        a callable whose first argument is a element object.
    default_value:
        a value that the property defaults to if the callable raise an 
        ContentNotFound.
    doc :
        docstring for the result property method.
    kwargs :
       any keyword arguments that the callable can take.
       
    """

    def __init__(self, call: Callable, default_value=None, doc: str = None,**kwargs):
        self._call = call
        self._default_value = default_value
        self._kwargs = kwargs

        if doc is None:
            doc = call.__doc__
        self.__doc__ = doc

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return get(
            instance, 
            self._call, 
            default_value=self._default_value,
            **self._kwargs)

    def __set__(self, instance, call):
        raise AttributeError("can't set attribute")

    def __delete__(self, instance):
        raise AttributeError("can't delete attribute")


class AltConstructor(classmethod):
    """
    Add an alternative constructor method to a Content or Contents type.

    Parameters
    ----------
    name: str
        name of this constructor.
    doc: str
        docstring for this constructor.
    kwargs
        any keyword arguments to initialize the BeautifulSoup class. 
        
    """

    def __init__(
        self, doc: Optional[str] = None, name: Optional[str] = None, **kwargs
    ):
        self._doc = doc
        self._name = name
        self._kwargs = kwargs
        self.__doc__ = doc

    def __get__(self, instance, owner):
        def _alt(owner, markup="", features=None, **kwargs):
            self._kwargs.update(kwargs)
            if features:
                self._kwargs["features"] = features
            else:
                self._kwargs["features"] = 'html.parser'
            if markup != "":
                self._kwargs["markup"] = markup
            return owner(BeautifulSoup(**self._kwargs))

        if self._name:
            _alt.__name__ = self._name
        if self._doc:
            _alt.__doc__ = self._doc

        return types.MethodType(_alt, owner)

    def __set_name__(self, owner, name):
        self._name = name


class Contents:
    """
    Base class for defining a Contents type.

    A Contents type, when you initialize it, creates a container with objects of a specific Content type. 
    
    Use this class to define which Content-typed object you wish to be in the resultant container object.
    
    To use this base class, subclass it and set its class attribute, _CONTENT, to an existing Content type.

    Attributes
    ----------
    _CONTENT
        a class that is a subclass of the Content type.
        
    Raises
    ------
    NotImplementedError
        if you fail to set the _CONTENT attribute. 
        
    TypeError
        if you do not set the _CONTENT attribute to a valid Content type.
        
    """

    _CONTENT: Type[Content]

    @classmethod
    def __init_subclass__(cls, **kwargs):
        """This method ensures the class attribute `_CONTENT` is set to a
        class that is a subclass of the Content type."""

        if not hasattr(cls, "_CONTENT"):
            raise NotImplementedError("You must define _CONTENT attribute.")

        try:
            cls._CONTENT._KIND.keys()
        except (AttributeError, SyntaxError):
            raise TypeError(
                """You must set _CONTENT attribute to a Content type."""
            )

        super().__init_subclass__(**kwargs)

    def __init__(self, element: Union[BeautifulSoup, Tag]):
        if not isinstance(element, (BeautifulSoup, Tag)):
           raise TypeError(
                """An error has occurred with the design of this tool."""
                )
        self._element = element
        self._elements = self._get_elements(element, self._CONTENT._KIND)
        
    @staticmethod
    def _get_elements(element, kind):
        """Return a BeautifulSoup ResultSet of all soup elements that match the kind."""
        return element.find_all(**kind)
    
    def __contains__(self, content):
        """Return True if element in elements."""
        if not isinstance(content, self._CONTENT):
            return False
        return content._element in self._elements

    def __len__(self):
        """Return integer indicating the number of elements in this collection."""
        return len(self._elements)

    def __getitem__(self, index):
        """Return Content-typed object corresponding to index."""
        if isinstance(index, slice):
            return [self._CONTENT(element) for element in  self._elements]
        return self._CONTENT(self._elements[index])
        
    def __eq__(self, other) -> bool:
        """Return True iff ``other`` is the same soup element object."""
        if not isinstance(other, self.__class__):
            return False
        return self._elements == other._elements

    def __str__(self):
        """Return plain-text list of contents."""
        return "\n".join(
            str(c) + " " + str(content) for c, content in enumerate(self)
        )

    def _repr_pretty_(self, p, cycle):
        """Render a pretty print representation (Jupyter notebook only)."""
        p.text(str(self) if not cycle else "...")
