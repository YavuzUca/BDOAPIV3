import requests
import fnmatch
from secret import *


def getPearlItems():
    """ Function that returns a list of pearl items, seven day volume ordered """
    response = requests.get("https://apiv2.bdolytics.com/en/EU/market/pearl-items?sort=seven_day_volume_asc",
                            data={},
                            headers={})
    data_json = response.json()
    return data_json['data']


class OutfitAPI:
    """ Class that has several functions to construct the class with a name parameter that returns buy order count. """

    def __init__(self, name):
        self.name = name
        self.count = self.findBuyCount()

    def getSearchList(self):
        """ Function that inputs the name from construct and returns a json list. """
        response = requests.post("https://eu-trade.naeu.playblackdesert.com/Home/GetWorldMarketSearchList",
                                 data={
                                     "__RequestVerificationToken": req_token,
                                     "searchText": self.name},
                                 headers={
                                     "User-Agent": me,
                                     "Cookie": cookie
                                 })
        data_json = response.json()
        return data_json['list']

    def getSubList(self):
        """ Function that inputs the result from getSearchList() and returns a json list. """
        data = self.getSearchList()
        response = requests.post("https://eu-trade.naeu.playblackdesert.com/Home/GetWorldMarketSubList",
                                 data={
                                     "__RequestVerificationToken": req_token,
                                     "mainKey": data[0]['mainKey']},
                                 headers={
                                     "User-Agent": me,
                                     "Cookie": cookie
                                 })
        data_json = response.json()
        return data_json['detailList']

    def getSellInfo(self):
        """ Function that inputs the result from getSubList() and returns a json list. """
        data = self.getSubList()
        response = requests.post("https://eu-trade.naeu.playblackdesert.com/Home/GetItemSellBuyInfo",
                                 data={
                                     "__RequestVerificationToken": req_token,
                                     "mainKey": data[0]['mainKey'],
                                     "subKey": data[0]['subKey'],
                                     "keyType": data[0]['keyType'],
                                     "isUp": "true"},
                                 headers={
                                     "User-Agent": me,
                                     "Cookie": cookie
                                 })
        data_json = response.json()
        return data_json['marketConditionList']

    def findHighestPrice(self, list):
        """ A function that inputs a json list from getSellInfo() and retuns the highest price possible at that
        moment in time. """
        highest = 0
        for item in list:
            if item['pricePerOne'] > highest:
                highest = item['pricePerOne']

        return highest

    def findBuyCount(self):
        """ A function that has a json list as data var and returns the buy count of a specific price. """
        data = self.getSellInfo()
        highest_price = self.findHighestPrice(data)

        for item in data:
            if item['pricePerOne'] == highest_price:
                return item['buyCount']

        return 0
