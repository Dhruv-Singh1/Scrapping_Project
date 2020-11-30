import requests
from bs4 import BeautifulSoup
import urllib.request
import csv
csvf= open('profile_info.csv','w')
csw = csv.writer(csvf)
csw.writerow(['Name ','Degree ','Carrer Level ', 'Membership','Skills','Goal','Certification' ])
ind =1
cnt=1
while cnt < 100 :
 url= "https://www.myvisajobs.com/CV/Candidates.aspx?P={ab}".format(ab=ind)
 home = requests.get(url).content
 pgH =BeautifulSoup(home,'html.parser')

 mem= goal=skil=carel=deg=name= "N/A"

 for links in pgH.find_all('td',  align="left" ,style="line-height:20px;width:100%;" ,valign="top"):

    c= requests.get("https://www.myvisajobs.com{p}".format(p =links.a['href'])).content
    cand= BeautifulSoup(c,'html.parser')
    name=  cand.find('span',itemprop='name')
    name=name.text
    print(name)
    img = cand.find('img',itemprop ='photo')['src']
    print(img)
    img ="https://www.myvisajobs.com{a}".format(a=img)
    iname = name+str(cnt)+".jpg"
    urllib.request.urlretrieve(img,iname)
    ex = cand.find_all('table', style="border:solid  #ADD8E6 1px;" )[1]
    for row in ex.find_all('tr'):
        cell=row.find_all('td')
        if ( cell[0].text== 'Degree: '):
            deg= cell[1].text
        elif(cell[0].text== 'Career Level: '):
            carel=cell[1].text
        elif(cell[0].text== 'Skills: '):
            skil=cell[1].text
        elif(cell[0].text== 'Goal: '):
            goal=cell[1].text
        elif(cell[0].text== 'Membership: '):
            mem=cell[1].text
        elif(cell[0].text== 'Certification: '):
            certi=cell[1].text
    csw.writerow([name,deg,carel,mem,goal,skil,certi])
    cnt = cnt + 1
 ind=ind+1

csvf.close()