#-*-coding:utf-8-*-

from weather import Weather
import cPickle as pickle

weather = Weather()

# get city id
def getcityid(city):
    return pickle.load(file('./cityid', 'r'))[city]

# get weather of city
def getweather(city):
    return weather.weather(getcityid(city.decode('utf8')))

if __name__ == '__main__':
    print getweather("天津")

