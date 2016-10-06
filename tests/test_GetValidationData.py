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
    <Action s:mustUnderstand="1" xmlns="http://schemas.microsoft.com/ws/2005/05/addressing/none">http://webcardmanagement.ana-u.com/IDatabaseService/GetValidationData</Action>
  </s:Header>
  <s:Body>
    <GetValidationData xmlns="http://webcardmanagement.ana-u.com/">
      <CardIdentifier>1a2b3c4d5e</CardIdentifier>
    </GetValidationData>
  </s:Body>
</s:Envelope>
"""

soap_response = """\
<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
  <s:Header />
  <s:Body>
    <GetValidationDataResponse xmlns="http://webcardmanagement.ana-u.com/">
      <GetValidationDataResult>
        <Card>
          <Gueltigkeit>20.12.2019<Gueltigkeit>
        </Card>
        <Error></Error>
      </GetValidationDataResult>
    </GetValidationDataResponse>
  </s:Body>
</s:Envelope>
"""


def test_GetValidationData_native():
    #r = requests.post(url, data=soap_request)
    #assert r.status_code == 200
    #assert r.text == soap_response
    pass


def test_GetValidationData_suds():
    client = Client(url)
    client.service.GetValidationData('1234567890')
    import pdb; pdb.set_trace()
