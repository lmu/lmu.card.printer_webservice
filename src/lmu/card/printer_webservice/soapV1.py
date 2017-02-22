from lmu.card.printer_webservice.resources import root_factory
from lmu.card.printer_webservice.test_data import CARDS
from lmu.card.printer_webservice.test_data import STA
from lmu.card.printer_webservice.test_data import validation_test_data
from lxml import etree
from pyramid.view import view_config
from spyne.application import Application
from spyne.decorator import srpc
from spyne.decorator import rpc
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
from spyne.server.pyramid import PyramidApplication
from spyne.service import ServiceBase
from spyne.util.simple import pyramid_soap11_application

import base64
import datetime
import logging


log = logging.getLogger(__name__)


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

    @rpc(Unicode, CardTypeEnum, _returns=Iterable(Person))
    def GetPersonData(context, SearchValue, CardType):
        log.info('APIv1 - GetPersonData: for SearchValue: "%s"; CardType: "%s"', SearchValue, CardType)
        #import pdb; pdb.set_trace()
        if CardType == CardTypeEnum.STA:
            result = []
            for person_id, person in STA.items():
                person_obj = Person(id=person_id,
                                    type=CardTypeEnum.STA,
                                    name=person.get('Name', ''),
                                    born=person.get('Born', datetime.date(year=1900, month=1, day=1)),
                                    id_no=person.get('ID_No', '00000000'),
                                    )
                log.info('APIv1 - Person data: "%s"', person_obj)
                result.append(person_obj)
            log.info('APIv1 - Results: "%s"', result)
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
        log.info('APIv1 - SetPersonData: PersonIdentifier: "%s" on Card Type: "%s"', PersonIdentifier, CardType)
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
        log.info('APIv1 - GetPersonPhoto: Lookup Photo for Person Identifier: "%s" on Card Type: "%s"', PersonIdentifier, CardType)
        if CardType == CardTypeEnum.STA:
            if PersonIdentifier in STA.keys() and 'Photo' in STA[PersonIdentifier].keys():
                #log.debug('APIv1 - PhotoData: "%s"', STA[PersonIdentifier]['Photo'])
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
        log.info('APIv1 - SetPersonPhoto: Lookup PersonIdentifier "%s" on Card Type: "%s"', PersonIndentifier, CardType)
        if CardType == CardTypeEnum.STA:
            if PersonIndentifier in STA.keys():
                STA[PersonIndentifier]['Photo'] = Base64Photo
                return True
            else:
                log.warn('APIv1 - PersonIndentifier %s not found.', PersonIndentifier)
                #raise ResourceNotFoundError(fault_string='User / Card not known')
                raise Fault('404', 'User / Card not known')
        elif CardType == CardTypeEnum.StudentID:
            pass
        elif CardType == CardTypeEnum.StaffID:
            pass
        elif CardType == CardTypeEnum.AffilitationID:
            pass
        return False

    @rpc(Unicode, CardTypeEnum, AnyDict, _returns=Boolean)
    def SetCardData(context, PersonIdentifier, CardType, CardData):
        log.info('APIv1 - SetCardData: Store Card Data Infos for: "%s" on "%s": "%s"', PersonIdentifier, CardType, CardData)
        #import pdb; pdb.set_trace()
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
        log.info('APIv1 - GetCardData: Card Data Infos for: "%s" on "%s"', PersonIdentifier, CardType)
        return CARDS.get(PersonIdentifier, dict())

    @srpc(Unicode, _returns=Iterable(Card))
    def GetValidationData(CardIdentifier):
        date = datetime.date.today()
        data = {}
        log.info('APIv1 - GetValidationData: Request Validation for "%s" (%s)', CardIdentifier, type(CardIdentifier))
        date, data = validation_test_data(CardIdentifier)
        if date is None and data is None:
            date = datetime.date(1970, 1, 1)
            data = {
                'valid': 'False',
            }
        log.info('Validation data for "%s": %s; Validation Date: %s', CardIdentifier, data, date)
        return [Card(date=date, data=data)]


anau_soap_webservice_application = pyramid_soap11_application(
    [AnaUSOAPWebService],
    tns='http://webcardmanagement.ana-u.com/'
)
