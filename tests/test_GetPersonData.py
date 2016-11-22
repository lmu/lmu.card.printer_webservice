# -*- coding: utf-8 -*-

from pyramid import testing
from suds.client import Client

import pytest
import requests
import suds

url = 'http://127.0.0.1:6543/soap/?wsdl'

soap_request = """\
<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
  <s:Header>
    <Action s:mustUnderstand="1"
xmlns="http://schemas.microsoft.com/ws/2005/05/addressing/none">http://webcard
management.ana-u.com/IDatabaseService/GetPersonData</Action>
  </s:Header>
  <s:Body>
    <GetPersonData xmlns="http://webcardmanagement.ana-u.com/">
      <SearchValue>Mustermann</SearchValue>
      <CardType>STA</CardType>
    </GetPersonData>
  </s:Body>
</s:Envelope>
"""

soap_response = """\
<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
  <s:Header />
  <s:Body>
    <GetPersonDataResponse xmlns="http://webcardmanagement.ana-u.com/">
      <GetPersonDataResult>
        <Record>
          <Person>
            <Name>Max</Name>
            <Familienname>Mustermann</Familienname>
            <Geburtsdatum>01.01.1900</Geburtsdatum>
            <CardType>student</CardType>
          </Person>
          <Person>
            <Name>Maria</Name>
            <Familienname>Muster</Familienname>
            <Geburtsdatum>22.40.1956</Geburtsdatum>
            <CardType>student</CardType>
          </Person>
        </Record>
        <Error></Error>
      </GetPersonDataResult>
    </GetPersonDataResponse>
  </s:Body>
</s:Envelope>
"""

headers = {
    'Content-Type': 'application/soap+xml; charset=utf-8',
    'SOAPAction': 'http://www.w3.org/2003/05/soap-envelope'
}


def setup_module():
    pass


@pytest.fixture
def pyramid_req():
    return testing.DummyRequest()


def test_GetPersonData(pyramid_req):
    #from lmu.card.printer_webservice.views import ana_u_webservice
    #response = ana_u_webservice(pyramid_req)
    #assert response == 'Hello World!'
    #req = requests.post(url, data=soap_request, headers=headers)
    #import pdb; pdb.set_trace()
    #assert req.status_code == 200
    #assert req.text == soap_response
    pass
