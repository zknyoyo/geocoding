#!/usr/bin/env python
#coding=utf-8

import urllib2
import json
import random

class MapConfig:
    def __init__(self, city, key, map_proxy, input, output, error, thread_num):
        self.city = city
        self.key = key
        self.map_proxy = map_proxy
        self.input = input
        self.output = output
        self.error = error
        self.thread_num = thread_num
class AMapHelper:     #高德地图Geocoding
    def __init__(self, config):
        self._config = config
    def geocoding(self):
        input = open(self._config.input, 'r')
        output = open(self._config.output, 'w')
        error = open(self._config.error, 'w')
        address_list = list(input)
        input.close()
        for count in range(0, address_list.__len__(), 1):
            if self._geo(address_list[count], self._config.city, self._config.key, output):
                print '--- %d records imported ---' % (count + 1)
            else:
                error.write(address_list[count])
                print "*** The %dth record can't be decoded ***" % (count + 1)
            if (count % 100) == 0 and count != 0:
                output.close()
                print '%d records committed' % count
                output = open(self._config.output, 'a')

    def _geo(self, address, city, key, output):
        address = address.rstrip()
        request = 'http://restapi.amap.com/v3/geocode/geo?address=' + address + '&output=json&key=' + key + '&city=' + city
        result = self._get_response(request)
        # import_text = ''
        if result:
            json_result = json.loads(result)
            if json_result['status'] == '1':
                if json_result['geocodes']:
                    import_text = '[%s],' % json_result['geocodes'][0]['location']
                    output.write(import_text+'\n')
                    return True
                # print json_result['location']
            else:
                return False
        return False

    def _get_response(self, request):
        try:
            response = urllib2.urlopen(request)
            return response.read()
        except urllib2.URLError:
            return None

# def b_map_geo(address, city, ak, output_file): #百度地图Geocoding
#     address = address.rstrip()
#     request = 'http://api.map.baidu.com/geocoder/v2/?address=' + address + '&city=' + city + '&output=json&ak=' + ak + '&callback=showLocation'
#     result = get_response(request)
#     json_result = json.loads(result[27:-1])
#     if json_result['status'] == 0:
#         import_text = '[%s,%s]' % (json_result['result']['location']['lng'], json_result['result']['location']['lat'])
#     else:
#         import_text = '\n'
#     output_file.write(import_text+',\n')


if __name__ == '__main__':
    map_config = MapConfig('宁波',                               #City
                           '79cb4998af3566585868b629bacd696b',  #Key
                           'amap',                              #type of map proxy
                           'bill_address.txt',                  #input file
                           'lng&lat.txt',                       #output file
                           'log.txt',                 #error file
                           5) #thread number
    amap_helper = AMapHelper(map_config)
    amap_helper.geocoding()
    # address_file = open('address_6w.txt', 'r')
    # addresses = list(address_file)
    # random.shuffle(addresses)
    # result = open('result.txt', 'w')
    # for i in range(0, 10000, 1):
    #     result.write(addresses[i])
    #     print '-- %d records imported. --' % i
    # result.close()
    # address_file.close()
