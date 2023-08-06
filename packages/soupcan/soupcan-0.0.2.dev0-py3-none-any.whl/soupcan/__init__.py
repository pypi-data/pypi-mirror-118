from .core import (
    Content,
    Contents,
    Property,
    AltConstructor,
    ContentNotFound,
    get,
)

__doc__ = """

:mod:`soupcan` is the top-level module for the **SoupCan** package. This 
module principally offers four classes: two base classes and two (non-data) 
descriptor classes. 

The two base classes, :class:`soupcan.Content` and :class:`soupcan.Contents`, 
are the foundation blocks from which you can design your HTML-parser package. 

The two descriptor classes, :class:`soupcan.Property` and :class:`soupcan.AltConstructor`, 
help to you add features to your Content or Contents types. 

"""

__all__ = (
    "Content",
    "Contents",
    "Property",
    "AltConstructor",
    "ContentNotFound",
    "get",
    "__doc__",
)
