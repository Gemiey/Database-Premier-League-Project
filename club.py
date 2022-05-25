from bs4 import BeautifulSoup
import urllib.request
import csv
from itertools import zip_longest
import requests
import os
clubnames = []
stadium = []
links = []

website = []
squad =[]
squadlinks = []
player = []
id=[]
clubsquad =['','','','','','','','','','','','','','','','','','','','']

url = "https://www.premierleague.com/clubs"

players = requests.get(url)
src = players.content
soup = BeautifulSoup(src,"lxml")

name = soup.find_all("h4",{"class":"clubName"})
div = soup.find_all("div",{"class":"stadiumName u-show-mob"})

tr = soup.find_all("tr")
for i in range(20):
  id .append(i) 
for i in range(len(name)):
    clubnames.append(name[i].text)

for td in tr:
    td=soup.find_all("th",{"class":"team"})
    for a in td:
        a = soup.find_all("a")
    for divs in a:
        divs = soup.find_all("div",{"class":"nameContainer"})
    for std in divs:
        std = soup.find_all("div",{"class":"stadiumName"})
   
    for i in range(len(name)):     
      if(len(stadium) < 20):      
        stadium.append(std[i].text)

# finding links to all clubs
lk = soup.find_all('a',class_="indexItem")
for ele in lk:
    links.append(ele.get('href'))
    
q = []
for i in range(len(links)):    
  clubpath = ("https://www.premierleague.com" + links[i])
  q.append(clubpath)
  clubs = requests.get(clubpath)
  pls = clubpath
  src = clubs.content
  soup = BeautifulSoup(src,"lxml")
  sitediv = soup.find_all("div",{"class":"website"})
  # finding links for squads 
  lk = soup.find_all('a',class_="active btn-tab")
  for ele in lk:
    squadlinks.append(ele.get('href'))
    #club websites
  for k in sitediv: 	  
    l = k.find_all("a")
    for j in range(len(l)):
	    website.append(l[j].text)


for b in q:
  test = b.split('overview')[0]
  squad.append(test)
# finding links to squad page by appending the word squad to the url of the club
for ll in range(len(squad)):
    squad[ll] = squad[ll] + 'squad'
z=0
count =0
for i in range(len(clubnames)):
  squadpath = (squad[i])  
  sq = requests.get(squadpath)
  pls = squadpath
  src = sq.content
  soup = BeautifulSoup(src,"lxml")  
  header = soup.find_all("h4",{"class":"name"})
  for i in range(len(header)):
       player.append(header[i].text)
  for j in player: 
         clubsquad[z] += j
         if  count+1 != len(player):
          clubsquad[z]+= ', '
         count+=1
  z+=1
  count=0
  player=[]
        
# csv
file_list = [clubnames,id,stadium,website,clubsquad]
exported = zip_longest(*file_list)
with open(r"C:\Users\lenovo\Documents\databaseproj\clubs.csv","w") as clubfile:
    wr = csv.writer(clubfile)
    wr.writerow(["Club","ID","Stadium","Website","Squad"])
    wr.writerows(exported)

import pymysql.cursors

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='premier_league',
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)
i=0
try:
    with connection.cursor() as cursor:
      print('test')
      print(len(clubnames))
      print(len(website))
      for i in range(20):
        sql= "INSERT INTO `clubs` (`name`,`website`,`stadium`) VALUES (%s,%s,%s)"     
        cursor.execute(sql, (clubnames[i],website[i],stadium[i]))                        
    connection.commit()
except Exception as e:
         print(e)
finally:
    print('asdasd')
    connection.close()