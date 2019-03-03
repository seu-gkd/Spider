from util.headers import *
import requests
import time
import http.cookiejar
import urllib
from urllib.request import urlopen, Request
from lxml import etree

def get_region(city_name):
    regions = []
    regions_py = {}
    page = "https://{0}.fang.ke.com/loupan/".format(city_name)
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    headers = create_headers()
    opener.addheaders = headers

    req = Request(page)
    try:
        data = urlopen(req).read().decode('utf8')
    except:
        print("region open error")
        time.sleep(10)
    res = etree.HTML(data)

    try:
        count = 1
        while True:
            py = res.xpath("/html/body/div[4]/div[2]/ul/li[{0}]/@data-district-spell".format(count))[0]
            name = res.xpath("/html/body/div[4]/div[2]/ul/li[{0}]/text()".format(count))[0]
            regions.append(py)
            regions_py[py] = name
            count += 1
    except:
        print("共有{0}个区".format(count-1))

    return regions, regions_py



if __name__ == '__main__':
    a,b = get_region('gz')
    c = 1
