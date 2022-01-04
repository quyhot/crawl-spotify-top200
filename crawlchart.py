from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import time
import datetime

###get all content on home_page
import getApiSpotify

if __name__ == '__main__':
  sp = getApiSpotify.authen()
  time = datetime.datetime(2018, 5, 9)
  while (1):
    timestr = time.strftime("%Y-%m-%d")
    print(timestr)
    home_page = 'https://spotifycharts.com/regional/vn/daily/' + timestr
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
    if tracksTop50:
      getApiSpotify.getListAudioFeature(sp, tracksTop50, timestr)
    if tracksTop100:
      getApiSpotify.getListAudioFeature(sp, tracksTop100, timestr)
    if tracksTop150:
      getApiSpotify.getListAudioFeature(sp, tracksTop150, timestr)
    if tracksTop200:
      getApiSpotify.getListAudioFeature(sp, tracksTop200, timestr)
    time += datetime.timedelta(days=1)
  # create a list of URLS for the landing page of each region collected earlier