#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of ReadBaseTransformer is responsible for reading a Dictionary object
"""
import io
import typing
from typing import Any, Optional, Union

from borb.io.read.read_base_transformer import ReadBaseTransformer, ReadTransformerState
from borb.io.read.types import AnyPDFType, Dictionary
from borb.pdf.canvas.event.event_listener import EventListener


class ReadDictionaryTransformer(ReadBaseTransformer):
    """
    This implementation of ReadBaseTransformer is responsible for reading a Dictionary object
    """

    def can_be_transformed(
        self, object: Union[io.BufferedIOBase, io.RawIOBase, io.BytesIO, AnyPDFType]
    ) -> bool:
        """
        This function returns True if the object to be transformed is a Dictionary object
        """
        return isinstance(object, Dictionary)

    def transform(
        self,
        object_to_transform: Union[io.BufferedIOBase, io.RawIOBase, AnyPDFType],
        parent_object: Any,
        context: Optional[ReadTransformerState] = None,
        event_listeners: typing.List[EventListener] = [],
    ) -> Any:
        """
        This function reads a Dictionary from a byte stream
        """

        # create root object
        assert isinstance(object_to_transform, Dictionary)
        object_to_transform.set_parent(parent_object)  # type: ignore [attr-defined]

        # add listener(s)
        for l in event_listeners:
            object_to_transform.add_event_listener(l)  # type: ignore [attr-defined]

        # transform key/value pair(s)
        for k, v in object_to_transform.items():
            v = self.get_root_transformer().transform(
                v, object_to_transform, context, []
            )
            if v is not None:
                object_to_transform[k] = v

        # return
        return object_to_transform
