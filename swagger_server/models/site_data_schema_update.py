# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class SiteDataSchemaUpdate(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, schema: object=None):  # noqa: E501
        """SiteDataSchemaUpdate - a model defined in Swagger

        :param schema: The schema of this SiteDataSchemaUpdate.  # noqa: E501
        :type schema: object
        """
        self.swagger_types = {
            'schema': object
        }

        self.attribute_map = {
            'schema': 'schema'
        }

        self._schema = schema

    @classmethod
    def from_dict(cls, dikt) -> 'SiteDataSchemaUpdate':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The site_data_schema_update of this SiteDataSchemaUpdate.  # noqa: E501
        :rtype: SiteDataSchemaUpdate
        """
        return util.deserialize_model(dikt, cls)

    @property
    def schema(self) -> object:
        """Gets the schema of this SiteDataSchemaUpdate.


        :return: The schema of this SiteDataSchemaUpdate.
        :rtype: object
        """
        return self._schema

    @schema.setter
    def schema(self, schema: object):
        """Sets the schema of this SiteDataSchemaUpdate.


        :param schema: The schema of this SiteDataSchemaUpdate.
        :type schema: object
        """

        self._schema = schema
