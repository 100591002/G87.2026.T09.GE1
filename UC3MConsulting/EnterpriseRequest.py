"""Enterprise request data model used by the UC3MConsulting package."""

import json
from datetime import datetime


class EnterpriseRequest:
    """
    Represents an enterprise request containing
    CIF, phone, name, and a timestamp.
    """

    def __init__(self, cIf, phone, eName):
        self.enterpriseName = eName
        self.cIf = cIf
        self.phone = phone
        JUST_NOW = datetime.utcnow()
        self._timeStamp = datetime.timestamp(JUST_NOW)

    def __str__(self):
        return "Enterprise:" + json.dumps(self.__dict__)

    @property
    def enterpriseCIf(self):
        return self.cIf
    @enterpriseCIf.setter
    def enterpriseCIf(self, value):
        self.cIf = value

    @property
    def phoneNumber(self):
        return self.phone
    @phoneNumber.setter
    def phoneNumber(self, value):
        self.phone = value

    @property
    def enterpriseName(self):
        return self.enterpriseName
    @enterpriseName.setter
    def enterpriseName(self, value):
        self.enterpriseName = value
