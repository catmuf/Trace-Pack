import http.client
import json
#from .models import Courier
import os
from dotenv import load_dotenv, dotenv_values, find_dotenv

load_dotenv(find_dotenv("config.env"))

conn = http.client.HTTPSConnection("api.ship24.com")

headers = {
    'Content-Type': "application/json",
    'Authorization': os.getenv("SHIP_24_API_KEY")
}
# Get all courier
def getAllCouriers():

    conn.request("GET", "/public/v1/couriers", headers=headers)

    res = conn.getresponse()
    data = res.read().decode("utf-8")
    #overrides
    f = open("base\couriers.json", "w", encoding="utf-8")
    f.write(data)
    f.close()
    return data
    # jsondata = json.loads(data)

    # # Extract the courier name and code for each courier
    # for courier in jsondata['data']['couriers']:
    #     courier_name = courier['courierName']
    #     courier_code = courier['courierCode']
    #     print(courier_name, courier_code)
    # # return data.decode("utf-8")

    # with open('base/couriers.json', 'r', encoding='utf-8') as f:
    #     listCouriers = json.load(f)

    # for courier in listCouriers['data']['couriers']:
    #     existing_courier = Courier.objects.filter(code=courier['courierCode']).first()
    #     if not existing_courier:
    #         Courier.objects.create(
    #             name = courier['courierName'],
    #             code = courier['courierCode'],
    #             website = courier['website'],
    #         )

# Automatically detects which courier and prints information
def getAutoTrackingResults(trackingNumber):
    payload = "{\n  \"trackingNumber\": \""+trackingNumber+"\"\n}"

    conn.request("POST", "/public/v1/tracking/search", payload, headers)

    res = conn.getresponse()
    data = res.read().decode("utf-8")

    # f = open("base\datatrackCainao.json", "w", encoding="utf-8")
    # f.write(data)
    # f.close()
    
    return data

# With tracking number even if courier code is not registered with it, automatically detects which courier belongs to
def getTrackingResultWithCourier(trackingNumber, courier_code):
    payload = "{\n  \"trackingNumber\": \"" + trackingNumber + "\",\n  \"courierCode\": [\n    \"" + courier_code + "\"\n  ]\n}"

    conn.request("POST", "/public/v1/tracking/search", payload, headers)

    res = conn.getresponse()
    data = res.read().decode("utf-8")
    
    return data

""" def import_couriers():
    with open('base\couriers.json') as file:
        data = json.load(file)
        couriers = data['data']['couriers']

        for courier in couriers:
            Courier.objects.create(
                name=courier['courierName'],
                code=courier['courierCode'],
                website=courier['website']
            ) """

# getAllCouriers()

# import_couriers()