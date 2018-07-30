import requests
from lxml.html import etree
import json
import time        # 导入模块
import os
import xlsxwriter as xlw
import csv
city_name=str(input("请输入需要查询天气的城市名称："))
path = os.getcwd()
class MoJiWeather():
    # def city_name(*other):  # 定义一个输入城市名称的函数
    #     # cityname = str(input("输入城市名称："))
    #     cityname = str("武汉")
    #     return cityname
    def search_city(city_name):    # 搜索这个城市
        index_url = "http://tianqi.moji.com/api/citysearch/%s"%city_name   #  构造查询相应城市天气的url   
        response = requests.get(index_url)
        response.encoding = "utf-8"
        try:    # 异常捕获
            city_id = json.loads(response.text).get('city_list')[0].get('cityId')# 通过上面的url获取城市的id
            city_url = "http://tianqi.moji.com/api/redirect/%s"%str(city_id)  # 通过城市id获取城市天气
            return city_url
        except:
            print('城市名输入错误')
            exit()
    def parse(city_url):    # 解析函数
        response = requests.get(city_url)
        response.encoding = 'utf-8'
        html = etree.HTML(response.text)
        current_city = html.xpath("//div[@class='search_default']/em/text()")[0]#    下面都是利用xpath解析的
        print('当前城市：'+current_city)
        current_kongqi = html.xpath("//div[@class='left']/div[@class='wea_alert clearfix']/ul/li/a/em/text()")[0]
        print('空气质量：'+current_kongqi)
        current_wendu = html.xpath("//div[@class='left']/div[@class='wea_weather clearfix']/em/text()")[0]
        print('当前温度：'+current_wendu+'℃')
        current_weather = html.xpath("//div[@class='wea_weather clearfix']/b/text()")[0]
        print('天气状况：' + current_weather)
        current_shidu = html.xpath("//div[@class='left']/div[@class='wea_about clearfix']/span/text()")[0]
        print('当前湿度：'+current_shidu)
        current_fengji = html.xpath("//div[@class='left']/div[@class='wea_about clearfix']/em/text()")[0]
        print('当前风速：'+current_fengji)
        jingdian = html.xpath("//div[@class='right']/div[@class='near'][2]/div[@class='item clearfix']/ul/li/a/text()")
        print('附近景点：')
        for j in jingdian:
            print('\t\t'+j)
    #     return current_city,current_kongqi,current_wendu,current_weather,current_shidu,current_fengji

    # def rewrite(city,kongqi,wendu,weather,shidu,fengji):
    #     # if not os.path.exists(weather.csv):     #判断当前路径是否存在，没有则创建new文件夹
           
    #     # else:
        # with open('te8578978888888888st.txt', 'w') as f:
        #     f.write('hello, python')
        #     print("数据写入完成")
        with open(path+"\\"+city_name+'weather.csv','a') as f:
            # f.write(current_city ,current_shidu)
            data1 = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            time1 = time.strftime('%H:%M:%S',time.localtime(time.time()))
            writer = csv.writer(f)
            #先写入columns_name
            #writer.writerow(["index","csv_1","csv_2"])
        #写入多行用writerows
            try:
                #f.write('hello, python')
                writer.writerows([[data1,current_city[:3],current_wendu,current_shidu,current_weather,current_fengji]])
                print("csv数据写入完成\n{},{}{}{}{}{}{}".format(data1,time1,current_city[:3],current_wendu,current_shidu,current_weather,current_fengji))
                print('等待正在运行....')
            except:
                print('数据保存错误')
                #writer.writerows([[data1,time1,current_city[:3],current_wendu,current_shidu,current_weather,current_fengji]])
            f.close()
while True:
    try:
        #schedule.every(10).seconds.do()
        print("欢迎在{}使用EPC天气查询系统".format(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))))
        # city_name = MoJiWeather.city_name()
        print(path+city_name+'weather.csv')
        cityurl = MoJiWeather.search_city(city_name)
        MoJiWeather.parse(cityurl)
   # MoJiWeather.rewrite(current_city,current_kongqi,current_wendu,current_weather,current_shidu,current_fengji)
        time.sleep(6)
    except:
        print('error')
        continue    