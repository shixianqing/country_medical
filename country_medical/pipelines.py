# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import country_medical.dbtool as db
from country_medical.util.fileUtil import writeFile

class CountryMedicalInsurancePipeline(object):

    pool = db.MysqlPool()

    def process_item(self, item, spider):

        print("{}-----》》》{}".format(item["url"],item))

        info = item["info"]
        if info is None or len(info) == 0:
            spider.log("--------------------------采集数据为空，url写入文件，跳过插入数据库-----------------{}".format(item["url"]))
            writeFile(url=item["url"], fileName="E:\spilder\country_medical\country_medical\exception-file\exception.txt")
            return item

        sql = "insert into country_medicine(allow_no,medicine_name,en_name,trade_name,form,medicine_size,prod_unit,prod_addr," \
              "prod_type,allow_date,origin_allow_no,medicine_ben_code,code_remark) " \
              "values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        try:
            # self.pool.insert(sql, param=tuple(info))
            # self.pool.end("commit")
            spider.log(item["url"]+"-----------插入成功")
            print("{}-----》》插入成功".format(item["url"]))
        except BaseException as e:
            spider.log("{异常信息-----------》》{}".format(e))
            spider.log("{}------数据插入失败！".format(item["url"]))
            print("{}-----》》数据插入失败".format(item["url"]))
            writeFile(url=item["url"], fileName="E:\spilder\country_medical\country_medical\exception-file\exception.txt")
        return item

class ForeigeMedicinePipeline(object):

    def process_item(self, item, spider):

        print("item----------->>>>{}".format(item["medicine_info"]))
        return item

