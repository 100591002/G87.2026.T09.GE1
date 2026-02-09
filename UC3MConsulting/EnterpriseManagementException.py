"""
Custom exceptions for enterprise management operations.
"""


class EnterpriseManagementException(Exception):
    """
    Exception raised for errors related to enterprise management.

    Attributes:
    message (str): Human-readable error message describing the failure.
    """
    def __init__(self, message):
        self.__message = message
        super().__init__(self.message)

    @property
    def message(self):
        return self.__message

    @message.setter
    def message(self,value):
        self.__message = value
