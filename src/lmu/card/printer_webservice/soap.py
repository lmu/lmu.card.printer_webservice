from lmu.card.printer_webservice.resources import root_factory
from lxml import etree
from pyramid.view import view_config
from spyne.application import Application
from spyne.decorator import srpc
from spyne.error import ResourceNotFoundError
from spyne.model.complex import ComplexModel
from spyne.model.complex import Iterable
from spyne.model.enum import Enum
from spyne.model.fault import Fault
from spyne.model.primitive import AnyDict
from spyne.model.primitive import Boolean
from spyne.model.primitive import Date
from spyne.model.primitive import Integer
from spyne.model.primitive import Unicode
from spyne.protocol.soap import Soap11
from spyne.service import ServiceBase

import base64
import datetime
import logging


log = logging.getLogger(__name__)

image = b'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'

STA = {
    '123456': {
        'Name': 'Max Mustermann',
        'Born': datetime.date(year=1900, month=1, day=1),
        'ID_No': '1234567890',
        'Photo': image,
    },
    '234567': {
        'Name': 'Maria Mustermann',
        'Born': datetime.date(year=1970, month=6, day=15),
        'ID_No': '1234567890',
        'Photo': image,
    },
    '10175648': {
        'Name': 'Dr. rer pol Anna-Sophie Müller-Schmidt Gräfin von Musterburg zu Hohensee',
        'Born': datetime.date(year=1987, month=9, day=23),
        'ID_No': '10175648',
        'Photo': image,
    }
}

CARDS = dict()

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
        'Gueltigkeit': Unicode,
        'ExtendedCardData': AnyDict,
    }
    Gueltigkeit = Unicode
    ExtendedCardData = AnyDict

    def __init__(self, date, data):
        if isinstance(date, datetime.date):
            self.Gueltigkeit = date.isoformat()
        else:
            self.Gueltigkeit = datetime.date.today().isoformat()
        self.ExtendedCardData = data


class Picture(Unicode):
    #__namespace__ = 'http://webcardmanagement.ana-u.com/'
    pass


class AnaUSOAPWebService(ServiceBase):

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

    @srpc(Unicode, CardTypeEnum, Unicode, Date, Unicode, _returns=Boolean)
    def SetPersonData(PersonIdentifier, CardType, Name, Born, ID_No):
        if CardType == CardTypeEnum.STA:
            if PersonIdentifier in STA:
                STA[PersonIdentifier]['CardType'] = CardType
            else:
                STA[PersonIdentifier] = {
                    'CardType': CardType,
                }
            STA[PersonIdentifier]['Name'] = Name
            STA[PersonIdentifier]['Born'] = Born
            STA[PersonIdentifier]['ID_No'] = ID_No
            return True
        elif CardType == CardTypeEnum.StudentID:
            pass
        elif CardType == CardTypeEnum.StaffID:
            pass
        elif CardType == CardTypeEnum.AffilitationID:
            pass
        return False

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
    def SetPersonPhoto(PersonIndentifier, CardType, Base64Photo):
        log.info('Lookup "%s" on Card Type: "%s"', PersonIndentifier, CardType)
        if CardType == CardTypeEnum.STA:
            log.info('CardType is STA "%s"', CardType)
            if PersonIndentifier in STA.keys():
                STA[PersonIndentifier]['Photo'] = Base64Photo
                return True
            else:
                log.warn('PersonIndentifier %s not found.', PersonIndentifier)
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
        log.info('Store Card Data Infos for: "%s" on "%s": "%s"', PersonIdentifier, CardType, CardData)
        if not PersonIdentifier:
            return False
        if CardType == CardTypeEnum.STA:
            if PersonIdentifier in CARDS:
                CARDS[PersonIdentifier]['CardType'] = CardType
            else:
                CARDS[PersonIdentifier] = {
                    'CardType': CardType,
                }
            if isinstance(CardData, dict):
                for key in CardData.keys():
                    CARDS[PersonIdentifier][key] = CardData[key]
            return True
        elif CardType == CardTypeEnum.StudentID:
            pass
        elif CardType == CardTypeEnum.StaffID:
            pass
        elif CardType == CardTypeEnum.AffilitationID:
            pass
        return False

    @srpc(Unicode, CardTypeEnum, _returns=AnyDict)
    def GetCardData(PersonIdentifier, CardType):
        log.info('Card Data Infos for: "%s" on "%s"', PersonIdentifier, CardType)
        return CARDS.get(PersonIdentifier, dict())

    @srpc(Unicode, _returns=Iterable(Card))
    def GetValidationData(CardIdentifier):
        date = datetime.date.today()
        data = {}
        if CardIdentifier == "000000791428":
            date = datetime.date.today() + datetime.timedelta(days=365)
            data = {
                'functions': 'TRUE',
                'function_title': 'Studiengang, Fach/FS (FKZ/ETCS) / Study, Topic, ETCS',
                'function1': 'LA Gymnasium (modul.) Deutsch / 13 (U105)',
                'function2': 'Englisch / 13 (U/105)',
                'function3': 'Erziehungswiss. Studium / 13 (P/36)',
                'function4': 'Sozialkunde / 9 (E)',
                'function5': '',
                'semesterticket_valid': 'TRUE',
                'semesterticket_code': 'WS2016/17',
                'TUM': 'False',
                'valid': 'TRUE',
            }
        elif CardIdentifier == "000000399262":
            date = datetime.date.today() + datetime.timedelta(days=365)
            data = {
                'functions': 'TRUE',
                'function_title': 'Funktion / Function',
                'function1': 'Referent IT-Projekte',
                'function2': 'Dezernat VI - Informations- und Kommunikationstechnik',
                'function3': 'Zentrale Universitätsverwaltung',
                'function4': 'Martiusstraße 4 - Raum 404',
                'function5': '+49 89 2180 9831',
                'semesterticket_valid': 'FALSE',
                'semesterticket_code': 'WS2016/17',
                'TUM': 'False',
                'valid': 'TRUE',
            }
        else:
            data = {
                'valid': 'FALSE',
            }

        log.info('Validation data for "%s": %s', CardIdentifier, data)
        return [Card(date=date, data=data)]
