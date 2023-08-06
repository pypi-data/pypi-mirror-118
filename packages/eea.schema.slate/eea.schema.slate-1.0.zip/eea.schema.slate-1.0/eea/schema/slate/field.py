""" Slate field
"""
import json
from zope.interface import implementer
from zope.schema.interfaces import IFromUnicode
from plone.schema.jsonfield import IJSONField, JSONField

DEFAULT_JSON_SCHEMA = json.dumps({"type": "array", "items": {}})


class ISlateJSONField(IJSONField):
    """A text field that stores A Slate JSON."""


@implementer(ISlateJSONField, IFromUnicode)
class SlateJSONField(JSONField):
    """ Slate JSON Field """
    def __init__(self, schema=DEFAULT_JSON_SCHEMA, widget=None, **kw):
        super(SlateJSONField, self).__init__(
            schema=schema, widget=widget, **kw
        )
