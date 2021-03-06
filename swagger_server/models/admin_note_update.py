# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class AdminNoteUpdate(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, note: str=None):  # noqa: E501
        """AdminNoteUpdate - a model defined in Swagger

        :param note: The note of this AdminNoteUpdate.  # noqa: E501
        :type note: str
        """
        self.swagger_types = {
            'note': str
        }

        self.attribute_map = {
            'note': 'note'
        }

        self._note = note

    @classmethod
    def from_dict(cls, dikt) -> 'AdminNoteUpdate':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The admin_note_update of this AdminNoteUpdate.  # noqa: E501
        :rtype: AdminNoteUpdate
        """
        return util.deserialize_model(dikt, cls)

    @property
    def note(self) -> str:
        """Gets the note of this AdminNoteUpdate.


        :return: The note of this AdminNoteUpdate.
        :rtype: str
        """
        return self._note

    @note.setter
    def note(self, note: str):
        """Sets the note of this AdminNoteUpdate.


        :param note: The note of this AdminNoteUpdate.
        :type note: str
        """

        self._note = note
