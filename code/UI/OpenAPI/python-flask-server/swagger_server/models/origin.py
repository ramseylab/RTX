# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server.models.edge_attribute import EdgeAttribute  # noqa: F401,E501
from swagger_server import util


class Origin(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, id: str=None, type: str=None, name: str=None, attribute_list: List[EdgeAttribute]=None):  # noqa: E501
        """Origin - a model defined in Swagger

        :param id: The id of this Origin.  # noqa: E501
        :type id: str
        :param type: The type of this Origin.  # noqa: E501
        :type type: str
        :param name: The name of this Origin.  # noqa: E501
        :type name: str
        :param attribute_list: The attribute_list of this Origin.  # noqa: E501
        :type attribute_list: List[EdgeAttribute]
        """
        self.swagger_types = {
            'id': str,
            'type': str,
            'name': str,
            'attribute_list': List[EdgeAttribute]
        }

        self.attribute_map = {
            'id': 'id',
            'type': 'type',
            'name': 'name',
            'attribute_list': 'attribute_list'
        }

        self._id = id
        self._type = type
        self._name = name
        self._attribute_list = attribute_list

    @classmethod
    def from_dict(cls, dikt) -> 'Origin':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Origin of this Origin.  # noqa: E501
        :rtype: Origin
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id(self) -> str:
        """Gets the id of this Origin.

        URI for the origin of the edge  # noqa: E501

        :return: The id of this Origin.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id: str):
        """Sets the id of this Origin.

        URI for the origin of the edge  # noqa: E501

        :param id: The id of this Origin.
        :type id: str
        """

        self._id = id

    @property
    def type(self) -> str:
        """Gets the type of this Origin.

        Entity type of the origin  # noqa: E501

        :return: The type of this Origin.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type: str):
        """Sets the type of this Origin.

        Entity type of the origin  # noqa: E501

        :param type: The type of this Origin.
        :type type: str
        """

        self._type = type

    @property
    def name(self) -> str:
        """Gets the name of this Origin.

        Formal name of the piece evidence that yielded the edge  # noqa: E501

        :return: The name of this Origin.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name: str):
        """Sets the name of this Origin.

        Formal name of the piece evidence that yielded the edge  # noqa: E501

        :param name: The name of this Origin.
        :type name: str
        """

        self._name = name

    @property
    def attribute_list(self) -> List[EdgeAttribute]:
        """Gets the attribute_list of this Origin.

        A list of attributes for this edge from this origin (source)  # noqa: E501

        :return: The attribute_list of this Origin.
        :rtype: List[EdgeAttribute]
        """
        return self._attribute_list

    @attribute_list.setter
    def attribute_list(self, attribute_list: List[EdgeAttribute]):
        """Sets the attribute_list of this Origin.

        A list of attributes for this edge from this origin (source)  # noqa: E501

        :param attribute_list: The attribute_list of this Origin.
        :type attribute_list: List[EdgeAttribute]
        """

        self._attribute_list = attribute_list