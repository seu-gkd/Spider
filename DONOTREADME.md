        # loupans = self.get_loupan_info(city_name)
        # db = pymysql.connect("localhost", "root", "admin", "GKD")
        # cursor = db.cursor()
        # for loupan in loupans:
        #     insert_sql = "INSERT INTO {0} values ({1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},{13},{14},{15},{16},{17},{18},{19},{20},{21},{22},{23})" \
        #         .format('su', loupan.xiaoqu, loupan.price, loupan.total, loupan.url, loupan.propertyType,
        #                 loupan.referencePrice, loupan.projectFeatures, loupan.regionallocation,
        #                 loupan.propertyaddress, loupan.salesOfficeAddress, loupan.developer, loupan.buildingType,
        #                 loupan.siteArea, loupan.floorAreaRatio, loupan.buildingArea,
        #                 loupan.yearofpropertyRights, loupan.propertyCompany, loupan.parkingRatio, loupan.propertycosts,
        #                 loupan.heatingMethod, loupan.waterSupplyMethod,
        #                 loupan.powerSupply, loupan.parkingSpace)
        #     cursor.execute(insert_sql)
        # db.close()