import requests
from bs4 import BeautifulSoup
import urllib.request
import csv
import logging

def extract_candidate_info(candidate_url, csw, count):
    try:
        candidate = BeautifulSoup(candidate_url, 'html.parser')
        candidate_name = candidate.find('span',itemprop='name')
        candidate_name = candidate_name.text
        logging.info(candidate_name)
        candidate_image = candidate.find('img',itemprop ='photo')['src']
        logging.info(candidate_image)
        candidate_image = "https://www.myvisajobs.com{a}".format(a=candidate_image)
        candidate_image_name = candidate_name+str(count)+".jpg"
        urllib.request.urlretrieve(candidate_image, candidate_image_name)
        extra_info = candidate.find_all('table', style="border:solid  #ADD8E6 1px;" )[1]
        membership = goal = skills = carrer_level = degree = candidate_name = certification = "N/A"
        for row in extra_info.find_all('tr'):
            cell = row.find_all('td')
            if (cell[0].text == 'Degree: '):
                degree = cell[1].text
            elif(cell[0].text == 'Career Level: '):
                carrer_level = cell[1].text
            elif(cell[0].text == 'Skills: '):
                skills = cell[1].text
            elif(cell[0].text == 'Goal: '):
                goal = cell[1].text
            elif(cell[0].text == 'Membership: '):
                membership = cell[1].text
            elif(cell[0].text == 'Certification: '):
                certification = cell[1].text
        csw.writerow([candidate_name, degree, carrer_level ,membership, goal ,skills, certification])

    except Exception as e:
        print(f"Error: {e}")
        pass

def main():
    csv_file = open('profile_info.csv','w')
    csw = csv.writer(csv_file)
    csw.writerow(['Name ', 'Degree ', 'Carrer Level ', 'Membership', 'Skills', 'Goal',' Certification' ])
    page_number = 1
    count = 1
    while count < 2:
        url = "https://www.myvisajobs.com/CV/Candidates.aspx?P={ab}".format(ab=page_number)
        home = requests.get(url).content
        pgH = BeautifulSoup(home,'html.parser')

        for links in pgH.find_all('td',  align="left" ,style="line-height:20px;width:100%;" ,valign="top"):
            candidate_url = requests.get("https://www.myvisajobs.com{p}".format(p =links.a['href'])).content
            extract_candidate_info(candidate_url, csw, count)
            count += 1
        page_number += 1

    csv_file.close()

if __name__ == "__main__":
    main()
