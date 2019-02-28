class LouPan(object):

    def __init__(self, xiaoqu, price, total):
        # 小区名
        self.xiaoqu = xiaoqu
        # 单价
        self.price = price
        # 总价
        self.total = total
        # url
        self.url = 0

        ## 基本信息
        # 物业类型
        self.propertyType = " "
        # 参考价格
        self.referencePrice = " "
        # 项目特色
        self.projectFeatures = " "
        # 区域位置
        self.regionallocation = " "
        # 楼盘地址
        self.propertyaddress = " "
        # 售楼处地址
        self.salesOfficeAddress = " "
        # 开发商
        self.developer = " "

        ## 规划信息
        # 建筑类型
        self.buildingType = " "
        # 绿化率
        self.landscapingRatio = " "
        # 占地面积
        self.siteArea = " "
        # 容积率
        self.floorAreaRatio = " "
        # 建筑面积
        self.buildingArea = " "
        # 产权年限
        self.yearofpropertyRights = " "
        # 规划户数
        self.numPlan = " "
        # 楼盘户型
        self.designType = " "

        ## 配套信息
        # 物业公司
        self.propertyCompany = " "
        # 车位配比
        self.parkingRatio = " "
        # 物业费
        self.propertycosts = " "
        # 供暖方式
        self.heatingMethod = " "
        # 供水方式
        self.waterSupplyMethod = " "
        # 供电方式
        self.powerSupply = " "
        # 车位
        self.parkingSpace = " "
        # 周边信息
        self.nearby = " "

        ## 其他
        self.area = " "

    def text(self):
        return str(self.xiaoqu) + "," + \
               str(self.price) + "," + \
               str(self.total) + "," + \
               str(self.url) + "," + \
            \
               str(self.propertyType) + "," + \
               str(self.referencePrice) + "," + \
               str(self.projectFeatures) + "," + \
               str(self.regionallocation) + "," + \
               str(self.propertyaddress) + "," + \
               str(self.salesOfficeAddress) + "," + \
               str(self.developer) + "," + \
            \
               str(self.buildingType) + "," + \
               str(self.landscapingRatio) + "," + \
               str(self.siteArea) + "," + \
               str(self.floorAreaRatio) + "," + \
               str(self.buildingArea) + "," + \
               str(self.yearofpropertyRights) + "," + \
               str(self.numPlan) + "," + \
               str(self.designType) + "," + \
            \
               str(self.propertyCompany) + "," + \
               str(self.parkingRatio) + "," + \
               str(self.propertycosts) + "," + \
               str(self.heatingMethod) + "," + \
               str(self.waterSupplyMethod) + "," + \
               str(self.powerSupply) + "," + \
               str(self.parkingSpace) + "," + \
               str(self.nearby) + "," + \
            \
               str(self.area)

    # def feature(self):
    #     return "xiaoqu,price,total,url,propertyType,referencePrice,projectFeatures,regionallocation," \
    #            "propertyaddress,salesOfficeAddress,developer,buildingType,landscapingRatio,siteArea,floorAreaRatio," \
    #            "buildingArea,yearofpropertyRights,numPlan,propertyCompany,parkingRatio,propertycosts,heatingMethod," \
    #            "waterSupplyMethod,powerSupply,parkingSpace"