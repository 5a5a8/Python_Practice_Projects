payload = '''
{
    "Origin": null,
    "Destination": {
        "Name": "DestinationName",
        "Address": {
            "BuildingName": "",
            "StreetAddress": "DestinationStreetAddress",
            "Suburb": "Avonside",
            "City": "Christchurch",
            "PostCode": "8061",
            "CountryCode": "NZ"
        },
        "Email": "destinationemail@email.com",
        "ContactPerson": "DestinationContact",
        "PhoneNumber": "123456789",
        "IsRural": false,
        "DeliveryInstructions": "Desinationdeliveryinstructions",
        "SendTrackingEmail": false,
        "ExplicitNotRural": false
    },
    "Packages": [
        {
            "Name": "NZC E25B",
            "Length": 1,
            "Width": 10,
            "Height": 1,
            "Kg": 0.1,
        }
    ],
    "Commodities": null,
    "IsSaturdayDelivery": false,
    "IsSignatureRequired": false,
    "IsUrgentCouriers": false,
    "DutiesAndTaxesByReceiver": false,
    "RuralOverride": false,
    "DeliveryReference": "11000000090",
    "PrintToPrinter": "false",
    "Carrier": "NZ Couriers"
}
'''

import requests
import base64
import json

#create label
key = '0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f'
url = 'http://api.gosweetspot.com/api/shipments?outputs=label_pdf'
headers = {'access_key': key, 'Content-Type': 'application/json; charset=utf-8'}

response = requests.post(url, data=payload, headers=headers)

print('First call response: ' , response)

#get label pdf
jsonResponse = json.loads(response.text)
connote = ((jsonResponse["Consignments"])[0])["Connote"]

print('Got shipping number: ' + connote)
url2 = 'http://api.gosweetspot.com/api/labels?format=label_pdf&connote=' + connote

response2 = requests.get(url2, headers=headers)
print('Second call response: ' , response2)
pdfBytes = base64.b64decode(response2.content[2:-2], validate=True)

with open('label.pdf', 'wb') as f2:
	f2.write(pdfBytes)
	print('Wrote PDF to file label.pdf')
