from lxml import etree
from pyramid.view import view_config
from spyne.application import Application
from spyne.decorator import srpc
from spyne.model.complex import ComplexModel
from spyne.model.complex import Iterable
from spyne.model.enum import Enum
from spyne.model.fault import Fault
from spyne.error import ResourceNotFoundError
from spyne.model.primitive import AnyDict
from spyne.model.primitive import Boolean
from spyne.model.primitive import Date
from spyne.model.primitive import Integer
from spyne.model.primitive import Unicode
from spyne.protocol.soap import Soap11
from spyne.service import ServiceBase

import datetime

import logging

log = logging.getLogger(__name__)

STA = {
    '123456': {
        'Name': 'Max Mustermann',
        'Born': datetime.date(year=1900, month=1, day=1),
        'ID_No': '1234567890',
    },
    '234567': {
        'Name': 'Maria Mustermann',
        'Born': datetime.date(year=1970, month=6, day=15),
        'ID_No': '1234567890',
    }
}

CardTypeEnum = Enum(
    'STA',
    'StaffID',
    'StudentID',
    'AffiliationID',
    type_name='CardType',
    __namespace__='http://webcardmanagement.ana-u.com/'
)


class Person(ComplexModel):
    __namespace__ = 'http://webcardmanagement.ana-u.com/'
    _type_info = {
        'Identifier': Unicode,
        'Name': Unicode,
        'Born': Date,
        'ID_No': Unicode,
        'CardType': CardTypeEnum,
    }
    type_name = 'Person'

    Identifier = Unicode
    Name = Unicode
    Born = Date
    ID_No = Unicode
    CardType = CardTypeEnum

    def __init__(self, id, type, name, born, id_no):
        self.Identifier = id
        self.Name = name
        if isinstance(born, datetime.date):
            self.Born = born
        else:
            self.Born = datetime.date(born)
        self.ID_No = id_no
        self.CardType = type


class Card(ComplexModel):
    __namespace__ = 'http://webcardmanagement.ana-u.com/'
    _type_info = {
        'Validity': Date,
        'Function': Unicode,
        'SemesterTicket': Unicode,
    }
    Validity = Date
    Function = Unicode
    SemesterTicket = Unicode

    def __init__(self, date, function, semester_ticket):
        if isinstance(date, datetime.date):
            self.Validity = date
        else:
            self.Validity = datetime.date.today()
        self.Function = function
        if semester_ticket:
            self.SemesterTicket = 'MVV'
        else:
            self.SemesterTicket = None


class Picture(Unicode):
    #__namespace__ = 'http://webcardmanagement.ana-u.com/'
    pass


class AnaUSOAPWebService(ServiceBase):

    @srpc(Unicode, Integer, _returns=Iterable(Unicode))
    def say_hello(name, times):
        for i in range(times):
            yield 'Hello, %s' % name

    @srpc(Unicode, CardTypeEnum, _returns=Iterable(Person))
    def GetPersonData(SearchValue, CardType):
        log.info('GetPersonData for SearchValue: "%s"; CardType: "%s"', SearchValue, CardType)
        if CardType == CardTypeEnum.STA:
            result = []
            for person_id, person in STA.items():
                person_obj = Person(id=person_id,
                                    type=CardTypeEnum.STA,
                                    name=person.get('Name', ''),
                                    born=person.get('Born', datetime.date(year=1900, month=1, day=1)),
                                    id_no=person.get('ID_No', '00000000'),
                                    )
                log.info('Person data: "%s"', person_obj)
                result.append(person_obj)
            log.info('Results: "%s"', result)
            return result
        elif CardType == CardTypeEnum.StudentID:
            pass
        elif CardType == CardTypeEnum.StaffID:
            pass
        elif CardType == CardTypeEnum.AffilitationID:
            pass
        else:
            raise Fault('401', 'Unknown CardType')
        return []

    @srpc(Unicode, CardTypeEnum, _returns=Picture)
    def GetPersonPhoto(PersonIdentifier, CardType):
        log.info('Lookup Photo for Person Identifier: "%s" on Card Type: "%s"', PersonIdentifier, CardType)
        if CardType == CardTypeEnum.STA:
            if PersonIdentifier in STA.keys() and 'Photo' in STA[PersonIdentifier].keys():
                log.info('PhotoData: "%s"', STA[PersonIdentifier]['Photo'])
                return STA[PersonIdentifier]['Photo']
            raise Fault('No Picture avalible')
        elif CardType == CardTypeEnum.StudentID:
            pass
        elif CardType == CardTypeEnum.StaffID:
            pass
        elif CardType == CardTypeEnum.AffilitationID:
            pass
        else:
            raise Fault('401', 'Unknown CardType')
        return Picture('Test')

    @srpc(Unicode, CardTypeEnum, Unicode, _returns=Boolean)
    def SetPersonPhoto(SearchValue, CardType, Base64Photo):
        log.info('Lookup "%s" on Card Type: "%s"', SearchValue, CardType)
        if CardType == CardTypeEnum.STA:
            log.info('CardType is STA "%s"', CardType)
            if SearchValue in STA.keys():
                STA[SearchValue]['Photo'] = Base64Photo
                return True
            else:
                log.warn('SearchValue %s not found.', SearchValue)
                #raise ResourceNotFoundError(fault_string='User / Card not known')
                raise Fault('404', 'User / Card not known')
        elif CardType == CardTypeEnum.StudentID:
            pass
        elif CardType == CardTypeEnum.StaffID:
            pass
        elif CardType == CardTypeEnum.AffilitationID:
            pass
        return False

    @srpc(Unicode, CardTypeEnum, AnyDict, _returns=Boolean)
    def SetCardData(PersonIdentifier, CardType, CardData):
        if CardType == CardTypeEnum.STA:
            if PersonIdentifier in STA:
                STA[PersonIdentifier]['CardType'] = CardType
            else:
                STA[PersonIdentifier] = {
                    'CardType': CardType,
                }
            for key in CardData.keys():
                STA[PersonIdentifier][key] = CardData[key]
            return True
        elif CardType == CardTypeEnum.StudentID:
            pass
        elif CardType == CardTypeEnum.StaffID:
            pass
        elif CardType == CardTypeEnum.AffilitationID:
            pass
        return False

    @srpc(Unicode, _returns=Iterable(Card))
    def GetValidationData(CardIdentifier):
        date = datetime.date.today() + datetime.timedelta(days=365)
        function = 'DEMO-Card'
        return [Card(date=date, function=function, semester_ticket=False)]


anau_soap_webservice_application = Application(
    [AnaUSOAPWebService],
    tns='http://webcardmanagement.ana-u.com/',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11(validator='lxml', pretty_print=True)
)
