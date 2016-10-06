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
management.ana-u.com/IDatabaseService/SetCardData</Action>
  </s:Header>
  <s:Body>
    <SetCardData xmlns="http://webcardmanagement.ana-u.com/">
      <PersonIdentifier>12345</PersonIdentifier>
      <CardType>STA</CardType>
      <CardData>
        <Card>
          <Uid>aabbccddeeff</Uid>
          <Iep>112233445566</Iep>
        </Card>
      </CardData>
    </SetCardData>
  </s:Body>
</s:Envelope>
"""

soap_response = """\
<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
  <s:Header />
  <s:Body>
    <SetCardDataResponse xmlns="http://webcardmanagement.ana-u.com/">
      <SetCardDataResult>
        <Result>TRUE</Result>
        <Error></Error>
      </SetCardDataResult>
    </SetCardDataResponse>
  </s:Body>
</s:Envelope>
"""


def test_SetCardData():
    #r = requests.post(url, data=soap_request)
    #assert r.status_code == 200
    #assert r.text == soap_response
    pass
