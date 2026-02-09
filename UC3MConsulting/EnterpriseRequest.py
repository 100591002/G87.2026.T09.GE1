import json
from datetime import datetime


class EnterpriseRequest:
    def __init__(self, Cif,phOnE, ENAME):
        self.enterpriseName = ENAME
        self.cIf = Cif
        self.phone = phOnE
        JUST_NOW = datetime.utcnow()
        self.__timeStamp = datetime.timestamp(JUST_NOW)

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