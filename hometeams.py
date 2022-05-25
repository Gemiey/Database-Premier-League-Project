from operator import itemgetter
from pickle import FALSE, TRUE
import pip
from bs4 import BeautifulSoup
import urllib.request
import csv
from itertools import zip_longest
import requests
import os
import random
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
import time

url = "https://www.premierleague.com/clubs"

players = requests.get(url)
src = players.content
soup = BeautifulSoup(src,"lxml")


name = soup.find_all("a",{"class":"playerName"})
nametd= soup.find_all("td")
temp=[]
td = " "	
pllinks =[]
clubnames = []
links = []
squad =[]
squadlinks = []
player = []
clubsquad =['','','','','','','','','','','','','','','','','','','','']

name = soup.find_all("h4",{"class":"clubName"})
div = soup.find_all("div",{"class":"stadiumName u-show-mob"})

tr = soup.find_all("tr")


playernames = []
links = []
hometeam=[]
first=[]
second=[]
third=[]
fourth=[]



# filling list for clubnames  
for i in range(len(name)):
    clubnames.append(name[i].text)


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

  # finding links for squads 
  lk = soup.find_all('a',class_="active btn-tab")
  for ele in lk:
    squadlinks.append(ele.get('href'))
  sitediv = soup.find_all("div",{"class":"website"})
for b in q:
  test = b.split('overview')[0]
  squad.append(test)


# finding links to squad page by appending the word squad to the url of the club
for ll in range(len(squad)):
    squad[ll] = squad[ll] + 'squad'
z=0
count=0
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
         if  count+1 != len(player) +1:
          clubsquad[z]+= ', '
         count+=1
  z+=1
  count=0
  player=[]
    
  lkp = soup.find_all('a',class_="playerOverviewCard active")  
# finding all links with href attribute
  for ele in lkp:
    pllinks.append(ele.get('href'))
i =0
z=0
count=0
ht=[]
seasons=[]
zz=0
bl = 0
f=''
ff=''
fff=''
ffff=''
countcommas = 0
# filling ht list to avoid exception
for i in range(700):
  ht.append('')

for k in clubsquad:
    x = k.split(', ')
    for i in x:
        y = i.split(', ') 
        if y[0] != '':
         playernames.append(y[0])

# player links
for i in range(len(pllinks)):    
  playerpath = ("https://www.premierleague.com" + pllinks[i])
  players = requests.get(playerpath)
  pls = playerpath
  src = players.content
  soup = BeautifulSoup(src,"lxml")
  team = soup.find_all("td",{"class":"team"})

  # home teams for the past 4 seasons
  for i in team:
    aa = i.find_all("a")
    for j in aa:
     spn = j.find_all("span",{"class":"long"})
     for k in range(len(spn)):
      hometeam.append(spn[k].text)
  for xx in hometeam: 
       ht[z] += xx
       if  count+1 != len(hometeam) and count <3:
         ht[z]+= ', '
       count+=1
       if count ==4:
         break
  # finding home clubs for each season      
  for k in ht[z]:   
         if k != ',' and bl==0 and countcommas == 0:
            f+= k
         else:
           bl = 1
           if k == ',':
             countcommas+=1
           if countcommas == 3:
             if k!= ',' and k is not None:
               ffff+=k  
           if countcommas == 2:  
             if k!=',' and k is not None:
               fff+=k  
           if k!=',' and k is not None and countcommas == 1:
             ff+=k
  fourth.append(ffff)
  third.append(fff)
  second.append(ff)
  first.append(f)
  f=''
  ff=''
  fff=''
  ffff=''
  countcommas=0    
  bl=0
  z+=1
  count=0
  hometeam=[]


# csv
file_list = [playernames,first,second,third,fourth]
exported = zip_longest(*file_list)
with open(r"C:\Users\lenovo\Documents\databaseproj\hometeams.csv","w") as clubfile:
    wr = csv.writer(clubfile)
    wr.writerow(["Player","2021/2022","2020/2021","2019/2020","2018/2019"])
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
      for i in range(len(pllinks)):
        sql= "INSERT INTO `player_club_history` (`player`,`2021/2022`,`2020/2021`,`2019/2020`,`2018/2019`) VALUES (%s,%s,%s,%s,%s)"     
        cursor.execute(sql, (playernames[i],first[i],second[i],third[i],fourth[i]))           
    connection.commit()
except Exception as e:
         print(e)
finally:
    connection.close()