from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import time
import datetime
import json

###get all content on home_page
import getApiSpotify
import pika

if __name__ == '__main__':
  sp = getApiSpotify.authen()
  time = datetime.datetime(2017, 1, 1)
  # init rabbitmq and queue
  connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672))
  channel = connection.channel()
  channel.queue_declare(queue='theMusketeer')
  # execute program
  while (1):
    timestr = time.strftime("%Y-%m-%d")
    print(timestr)
    home_page = 'https://spotifycharts.com/regional/global/daily/' + timestr
    print(home_page)
    driver = webdriver.Chrome('./chromedriver')
    driver.get(home_page)
    hresponse = driver.page_source
    soup = BeautifulSoup(hresponse)
    driver.close()
    ###parse through the home_page to get all the region names and their codes
    region_fullname = []
    # td = soup.find_all('td', {'class': 'chart-table-image'})
    # print(td)
    tracksTop50 = []
    tracksTop100 = []
    tracksTop150 = []
    tracksTop200 = []
    count = 0
    for td in soup.find_all('td', {'class': 'chart-table-image'}):  # run alone no probs
      link = td.a['href']
      idTrack = link[link.rfind('/')+1:]
      if (count < 50):
        tracksTop50 = tracksTop50 + [idTrack]
      elif (count < 100):
        tracksTop100 = tracksTop100 + [idTrack]
      elif (count < 150):
        tracksTop150 = tracksTop150 + [idTrack]
      else:
        tracksTop200 = tracksTop200 + [idTrack]
      count += 1
    print(count)
    results = []
    if tracksTop50:
      results = results + getApiSpotify.getListAudioFeature(sp, tracksTop50, timestr, channel)
    if tracksTop100:
      results = results + getApiSpotify.getListAudioFeature(sp, tracksTop100, timestr, channel)
    if tracksTop150:
      results = results + getApiSpotify.getListAudioFeature(sp, tracksTop150, timestr, channel)
    if tracksTop200:
      results = results + getApiSpotify.getListAudioFeature(sp, tracksTop200, timestr, channel)
    with open('./newdata/data-'+ timestr +'.json', 'w+', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)
    dataPublish = {
      'time': timestr,
      'data': results
    }
    channel.basic_publish(exchange='', routing_key='theMusketeer', body=json.dumps(dataPublish))
    time += datetime.timedelta(days=1)
  # create a list of URLS for the landing page of each region collected earlier