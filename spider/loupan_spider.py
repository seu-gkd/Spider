# coding=utf-8
# 爬取楼盘数据的爬虫派生类

import re
import math
import requests
from bs4 import BeautifulSoup

from util.path import *
from util.city import *
from util.date import *
from util.headers import *
from util.region import *
from item.loupan import *
from lxml import etree
import http.cookiejar
import urllib
from urllib.request import urlopen, Request
import codecs
import time
import threadpool


def getInfo1(i):
    return i[0].strip().replace(',','，').strip('\n')


def getInfo2(i):
    return i[0].split("\n")[1].strip().replace(',','，')

def getArea(url):
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    headers = create_headers()
    opener.addheaders = headers
    req = Request(url)
    data = urlopen(req).read().decode('utf8')
    res = etree.HTML(data)
    try:
        area = res.xpath("/html/body/div[2]/div[7]/div/div[2]/div[1]/ul/li[1]/ul/li[2]/p[2]/span[1]/text()")
        sum = 0
        for i in area:
            sum += float(i.split(' ')[1].split('m²')[0])
        return sum / len(area)
    except:
        print("except nimane")


class LouPanBaseSpider(object):
    def collect_city_loupan_data(self, city_name, fmt="csv"):
        """
        将指定城市的新房楼盘数据存储下来，默认存为csv文件
        :param city_name: 城市
        :param fmt: 保存文件格式
        :return: None
        """
        # 保存城市的信息
        # self.today_path = create_date_path("loupan", citiesname[city_name], get_date_string())
        csv_file = self.today_path + "/{0}.csv".format(city_name)
        # 总信息
        info_file = DATA_PATH + "/{0}".format("infodata.csv")

        with codecs.open(csv_file, "a+", 'utf-8') as f:
            # 开始获得需要的板块数据
            regions, regions_py = get_region(city_name)
            for region in regions:
                loupans = self.get_loupan_info(city_name, region)
                self.total_num = len(loupans)
                if fmt == "csv":
                    # f.write("date,city," + loupans[0].feature() + "\n")
                    for loupan in loupans:
                        f.write(self.date_string + "," + citiesname[city_name] + "," + regions_py[region] + "," + loupan.text() + "\n")
                print("{0}{1} done".format(citiesname[city_name],regions_py[region]))

        try:
            f1 = open(csv_file, 'rb')
            f2 = open(info_file , 'a+', encoding='utf-8')
            d = f1.read()
            da = d.decode('utf-8', 'replace')
            f2.write(da)
            f1.close()
        except:
            print("rewrite failed!")

        print("Finish crawl: " + city_name + ", save data to : " + csv_file)

    @staticmethod
    def get_loupan_info(city_name, region):
        """
        爬取页面获取城市新房楼盘信息def getInfo(self,):
        :param city_name: 城市
        :return: 新房楼盘信息列表
        """
        total_page = 1
        loupan_list = list()
        page = 'http://{0}.fang.ke.com/loupan/{1}'.format(city_name,region)
        headers = create_headers()
        try:
            response = requests.get(page, timeout=10, headers=headers)
        except:
            print("timed out")
            time.sleep("")
        html = response.content
        soup = BeautifulSoup(html, "lxml")

        # 获得总的页数
        try:
            page_box = soup.find_all('div', class_='page-box')[0]
            matches = re.search('.*data-total-count="(\d+)".*', str(page_box))
            total_page = int(math.ceil(int(matches.group(1)) / 10))
        except Exception as e:
            print("\tWarning: only find one page for {0}".format(city_name))
            print(e)

        print(total_page)

        # 从第一页开始,一直遍历到最后一页
        headers = create_headers()
        for i in range(1, total_page + 1):
            page = 'http://{0}.fang.ke.com/loupan/{1}/pg{2}'.format(city_name, region, i)
            print("page:" + page)
            time.sleep(random.randint(0, 16))
            response = 0
            try:
                response = requests.get(page, timeout=10, headers=headers, verify=False)
            except:
                print("timed out")
                time.sleep(random.randint(0, 6))
            html = response.content
            soup = BeautifulSoup(html, "lxml")

            # 获得有小区信息的panel
            house_elements = soup.find_all('li', class_="resblock-list")
            for house_elem in house_elements:
                price = house_elem.find('span', class_="number")
                unit = house_elem.find('span', class_="desc")
                total = house_elem.find('div', class_="second")
                loupan = house_elem.find('a', class_='name')
                url = house_elem.find('div', class_="resblock-name").a['href']

                # 继续清理数据
                try:
                    price = price.text.strip()
                except Exception as e:
                    price = '0'

                try:
                    unit = unit.text.strip()
                except:
                    unit = ''

                loupan = loupan.text.replace("\n", "")

                try:
                    total = total.text.strip()
                except Exception as e:
                    total = '0'

                print("{0} {1} {2} {3}".format(
                    loupan, str(price) + str(unit), total, url))

                # 作为对象保存
                loupan = LouPan(loupan, price, total)

                # 爬取详细信息
                cj = http.cookiejar.CookieJar()
                opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
                headers = create_headers()
                opener.addheaders = headers
                infourl = "https://sh.fang.ke.com" + url
                url = "https://sh.fang.ke.com" + url + "xiangqing"
                req = Request(url)
                try:
                    data = urlopen(req).read().decode('utf8')
                except:
                    print("open error")
                    time.sleep(10)
                res = etree.HTML(data)

                loupan.url = url
                print("---------------------")
                print(loupan.url)
                ## 基本信息
                # 物业类型
                try:
                    loupan.propertyType = getInfo1(res.xpath("/html/body/div[2]/div[1]/ul[1]/li[1]/span[2]/text()"))
                except:
                    print("loupan.propertyType Error")
                # 参考价格
                try:
                    loupan.referencePrice = getInfo1(
                        res.xpath("/html/body/div[2]/div[1]/ul[1]/li[2]/span[2]/span/text()")).split(' ')[1].split('元/平')[0]

                except:
                    print("loupan.referencePrice Error")

                if loupan.referencePrice.find('套') > 0:
                    try:
                        loupan.referencePrice = str(int(float(loupan.referencePrice.split(' ')[1].split('万/套')[0]) * 10000/getArea(infourl)))
                    except:
                        try:
                            loupan.referencePrice = str(int(float(loupan.referencePrice.split('万/套')[0]) * 10000 / getArea(infourl)))
                        except:
                            loupan.referencePrice = '暂无售价'

                # 项目特色
                try:
                    loupan.projectFeatures = getInfo1(res.xpath("/html/body/div[2]/div[1]/ul[1]/li[3]/span[2]/text()"))
                except:
                    print("loupan.projectFeatures Error")
                #  区域位置 todo
                try:
                    loupan.regionallocation = getInfo1(res.xpath("/html/body/div[2]/div[1]/ul[1]/li[4]/span[2]/text()")) + \
                                              getInfo1(res.xpath("/html/body/div[2]/div[1]/ul[1]/li[4]/span[2]/a/text()"))

                    if not loupan.regionallocation:
                        loupan.regionallocation = "暂无信息"
                except:
                    print("loupan.regionallocation Error")
                # 楼盘地址
                try:
                    loupan.propertyaddress = getInfo1(res.xpath("/html/body/div[2]/div[1]/ul[1]/li[5]/span[2]/text()"))
                except:
                    print("loupan.propertyaddress Error")
                # 售楼处地址
                try:
                    loupan.salesOfficeAddress = getInfo1(
                        res.xpath("/html/body/div[2]/div[1]/ul[1]/li[6]/span[2]/text()"))
                except:
                    print("loupan.salesOfficeAddress Error")
                # 开发商
                try:
                    loupan.developer = getInfo1(res.xpath("/html/body/div[2]/div[1]/ul[1]/li[7]/span[2]/text()"))
                except:
                    print("loupan.developer Error")

                ## 规划信息
                # 建筑类型
                try:
                    loupan.buildingType = getInfo1(res.xpath("/html/body/div[2]/div[1]/ul[3]/li[1]/span[2]/text()"))
                except:
                    print("loupan.buildingType Error")
                # 绿化率
                try:
                    loupan.landscapingRatio = getInfo1(res.xpath("/html/body/div[2]/div[1]/ul[3]/li[2]/span[2]/text()"))
                except:
                    print("loupan.landscapingRatio Error")
                # 占地面积
                try:
                    loupan.siteArea = getInfo2(res.xpath("/html/body/div[2]/div[1]/ul[3]/li[3]/span[2]/text()"))
                except:
                    print("loupan.siteArea Error")
                # 容积率
                try:
                    loupan.floorAreaRatio = getInfo2(res.xpath("/html/body/div[2]/div[1]/ul[3]/li[4]/span[2]/text()"))
                except:
                    print("loupan.floorAreaRatio Error")
                # 建筑面积
                try:
                    loupan.buildingArea = getInfo2(res.xpath("/html/body/div[2]/div[1]/ul[3]/li[5]/span[2]/text()"))
                except:
                    print("loupan.buildingArea Error")
                # 产权年限
                try:
                    loupan.yearofpropertyRights = getInfo1(res.xpath("/html/body/div[2]/div[1]/ul[3]/li[8]/span[2]/text()"))
                except:
                    print("loupan.yearofpropertyRights Error")
                # 规划户数
                try:
                    loupan.numPlan = getInfo1(res.xpath("/html/body/div[2]/div[1]/ul[3]/li[7]/span[2]/text()"))
                except:
                    print("loupan.numPlan Error")
                # 楼盘户型
                # loupan.designType = res.xpath("").extract()

                ## 配套信息
                # 物业公司
                try:
                    loupan.propertyCompany = getInfo1(res.xpath("/html/body/div[2]/div[1]/ul[4]/li[1]/span[2]/text()"))
                except:
                    print("loupan.propertyCompany Error")
                # 车位配比
                try:
                    loupan.parkingRatio = getInfo1(res.xpath("/html/body/div[2]/div[1]/ul[4]/li[2]/span[2]/text()"))
                except:
                    print("loupan.parkingRatio Error")
                # 物业费
                try:
                    loupan.propertycosts = getInfo1(res.xpath("/html/body/div[2]/div[1]/ul[4]/li[3]/span[2]/text()"))
                except:
                    print("loupan.propertycosts Error")
                # 供暖方式
                try:
                    loupan.heatingMethod = getInfo1(res.xpath("/html/body/div[2]/div[1]/ul[4]/li[4]/span[2]/text()"))
                except:
                    print("loupan.heatingMethod Error")
                # 供水方式
                try:
                    loupan.waterSupplyMethod = getInfo1(
                        res.xpath("/html/body/div[2]/div[1]/ul[4]/li[5]/span[2]/text()"))
                except:
                    print("loupan.waterSupplyMethod Error")
                # 供电方式
                try:
                    loupan.powerSupply = getInfo1(res.xpath("/html/body/div[2]/div[1]/ul[4]/li[6]/span[2]/text()"))
                except:
                    print("loupan.powerSupply Error")
                # 车位
                try:
                    loupan.parkingSpace = getInfo2(res.xpath("/html/body/div[2]/div[1]/ul[4]/li[7]/span[2]/text()"))
                except:
                    print("loupan.parkingSpace Error")

                loupan_list.append(loupan)
        return loupan_list

    def start(self):
        self.date_string = get_time_string()
        self.today_path = create_type_path("loupan", get_date_string())


        nones = [None for i in range(len(cities))]

        args = zip(zip(['sh']), nones)


        pool = threadpool.ThreadPool(50)
        my_requests = threadpool.makeRequests(self.collect_city_loupan_data, args)
        [pool.putRequest(req) for req in my_requests]
        pool.wait()
        pool.dismissWorkers(50, do_join=True)


        # for city in cities:
        #     print('Today date is: %s' % self.date_string)
        #     print('City is: %s' % city)
        #     self.today_path = create_date_path("/loupan", citiesname[city], get_date_string())
        #     t1 = time.time()  # 开始计时
        #     self.collect_city_loupan_data(city)
        #     t2 = time.time()  # 计时结束，统计结果
        #     print("Total crawl {0} loupan.".format(self.total_num))
        #     print("Total cost {0} second ".format(t2 - t1))


if __name__ == '__main__':
    pass
