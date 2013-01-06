#-*-coding:utf-8-*-
 
import requests
import json
import time
 
class Weather:
 
    def __init__(self):
        pass
 
    def weather(self, cityid):
        flag = 1
        while flag:
            try:
                r = requests.get('http://www.weather.com.cn/data/cityinfo/'+cityid+'.html')
                weatherinfo = json.loads(r.text)[u'weatherinfo']
                flag = 0
            except:
                 pass
        return weatherinfo[u'city'] + u', ' + weatherinfo[u'weather'] + u', ' +  weatherinfo[u'temp1'] + u' ~ ' +  weatherinfo[u'temp2']
 
if __name__ == '__main__':
    weather = Weather()
    #print time.strftime('今天是%Y年%m月%d日',time.localtime(time.time())) 
    print weather.weather('101010100')
