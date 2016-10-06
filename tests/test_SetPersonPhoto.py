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
management.ana-u.com/IDatabaseService/SetPersonPhoto</Action>
  </s:Header>
  <s:Body>
    <SetPersonPhoto xmlns="http://webcardmanagement.ana-u.com/">
      <PersonIdentifier>12345</PersonIdentifier>
      <CardType>STA</CardType>
        <Base64Photo>
/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAIBAQIBAQICAgICAgICAwUDAwMDAwYEBAMFBwYHBwcGBw
cICQsJCAgKCAcHCg0KCgsMDAwMBwkODw0MDgsMDAz/2wBDAQICAgMDAwYDAwYMCAcIDAwMDAwMDAwM
DAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAz/wAARCAAcABQDASIAAhEBAx
EB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQID
AAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRk
dISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2
t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQ
AAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEI
FEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2
hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU
1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD9gh8RV+NPjS/WfXPEmk+GZibDTb
DTB5Nxq7xXL212ZJAheKMvtSPbJDLiO6cZRI5Bk6jf2Mb2Nv8ADjV/Eun6ldy217p8VzqE9xY3kMr7
V3wSlpTG6rK4K42LbE5EayIY0kt/hto2o+DfEkfhnSb7T7+6v9N1bWLiIWF3aXl3cTOxWT5RJEJJEK
E5kQvsZd8witfE/wAXSfBawvtb1Lxlp8l5obQ3Y0i1nM9xOpECR+aI1DJGyxTO8oiYok7hQyxYlAPY
vgz8U7T40/DbS/Etjb3Fpb6nGXEM4xJEQSpU9sggj2PBwQQCsH9lT4eaz8MPgtpul655MN7uecWcRD
Lp6uc+Tuy25s5ZvmcB3ZQ7qAxKAPx+/wCC4X7VOsfF39tDUF8K3mtW/hv4KxR6DLq2mvLHDZapMxmn
JuI8eVIWhSIKzBi9jIVzgkeDftD+CfjJ+zX8W/hnqnivUNYk8UT6Xpni7wnNIrzmzllMcwiWIjaLiO
4UJMgGZHAZtwkUn9zP2iP2I/hv8R/2drr4ft4ds9F8M6x4m0/WL6DSoY7Zru5Op2800kh2nc0+GSRy
C7JIwDKcMOm/aO/ZP8G/tM6j4G1DxRYyS6j8PfEdp4j0W6gZUmhnhlR/KYlTuhkKJvj6NsQ8MisADB
/Y8/bc8N/tTfA7T/El08fhXxBbudO8QaFqbfZbrRtSjVDNAySYbb86ujEAtHIhIViVBXtmM0UAf//Z
      </Base64Photo>
    </SetPersonPhoto>
  </s:Body>
</s:Envelope>
"""

soap_response = """\
<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
  <s:Header />
  <s:Body>
    <SetPersonPhotoResponse xmlns="http://webcardmanagement.ana-u.com/">
      <SetPersonPhotoResult>
        <Result>TRUE</Result>
        <Error></Error>
      </SetPersonPhotoResult>
    </SetPersonPhotoResponse>
  </s:Body>
</s:Envelope>
"""


image_body = """\
/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAIBAQIBAQICAgICAgICAwUDAwMDAwYEBAMFBwYHBwcGBw
cICQsJCAgKCAcHCg0KCgsMDAwMBwkODw0MDgsMDAz/2wBDAQICAgMDAwYDAwYMCAcIDAwMDAwMDAwM
DAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAz/wAARCAAcABQDASIAAhEBAx
EB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQID
AAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRk
dISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2
t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQ
AAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEI
FEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2
hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU
1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD9gh8RV+NPjS/WfXPEmk+GZibDTb
DTB5Nxq7xXL212ZJAheKMvtSPbJDLiO6cZRI5Bk6jf2Mb2Nv8ADjV/Eun6ldy217p8VzqE9xY3kMr7
V3wSlpTG6rK4K42LbE5EayIY0kt/hto2o+DfEkfhnSb7T7+6v9N1bWLiIWF3aXl3cTOxWT5RJEJJEK
E5kQvsZd8witfE/wAXSfBawvtb1Lxlp8l5obQ3Y0i1nM9xOpECR+aI1DJGyxTO8oiYok7hQyxYlAPY
vgz8U7T40/DbS/Etjb3Fpb6nGXEM4xJEQSpU9sggj2PBwQQCsH9lT4eaz8MPgtpul655MN7uecWcRD
Lp6uc+Tuy25s5ZvmcB3ZQ7qAxKAPx+/wCC4X7VOsfF39tDUF8K3mtW/hv4KxR6DLq2mvLHDZapMxmn
JuI8eVIWhSIKzBi9jIVzgkeDftD+CfjJ+zX8W/hnqnivUNYk8UT6Xpni7wnNIrzmzllMcwiWIjaLiO
4UJMgGZHAZtwkUn9zP2iP2I/hv8R/2drr4ft4ds9F8M6x4m0/WL6DSoY7Zru5Op2800kh2nc0+GSRy
C7JIwDKcMOm/aO/ZP8G/tM6j4G1DxRYyS6j8PfEdp4j0W6gZUmhnhlR/KYlTuhkKJvj6NsQ8MisADB
/Y8/bc8N/tTfA7T/El08fhXxBbudO8QaFqbfZbrRtSjVDNAySYbb86ujEAtHIhIViVBXtmM0UAf//Z
"""


def test_SetPersonPhoto():
    #r = requests.post(url, data=soap_request)
    #assert r.status_code == 200
    #assert r.text == soap_response
    client = Client(url)
    result = client.service.SetPersonPhoto('1234567890', 'STA', image_body)
    assert result is False
