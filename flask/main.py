import os
from flask import Flask, render_template, request, url_for, flash, redirect, make_response
# import operator
# import re
# import requests
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# import time
# from selenium.webdriver import ActionChains
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.common.by import By
# from bs4 import BeautifulSoup
# import html2text
# from selenium.common.exceptions import TimeoutException
# from selenium.webdriver.chrome.options import Options
# import json
from fpdf import FPDF

import sys

sys.path.insert(0, r'C:\Users\akasy\python\scraper\jobs.atos.net')

import scraper, pdf_lib

# def call(text, region):
#     sk = ['NodeJS', 'Angular', 'TypeScript', 'Robot Framework',
#           'Linux', 'Unix', 'Cloud', 'Cybersecurity', 'Devops',
#           'Java', 'C', 'C++', 'C#', 'React', 'Oracle', 'Shell', 'Perl',
#           'Go', 'Golang', 'Python', 'Rust', 'Javascript',
#           'SQL', 'Git', 'Angular', 'Vue', 'Docker', 'Kubernetes']
#     dict_of_key_skills = {}
#     dict_of_key_skills['strSearch'] = text
#     dict_of_key_skills['strArea'] = region
#     dict_of_key_skills['strUrl'] = []
#     dict_of_key_skills['strJobTitle'] = []
#     dict_of_key_skills['strArrKeySkills'] = []
#     next_page = 0
#     repeat = True
#     options = Options()
#     options.add_argument("--headless")
#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
#     while repeat:
#         url = 'https://jobs.atos.net/search/?q=' + text + '&locationsearch=' + region + '&startrow=' + str(next_page)
#         driver.get(url)
#         content = driver.page_source
#         soup = BeautifulSoup(content, "html.parser")
#         try:
#             count_jobs_str = soup.find('span', {'class': 'paginationLabel'})
#             count_jobs_split = re.findall(r'\d+', count_jobs_str.text)
#             for a in soup.findAll('a', {'class': 'jobTitle-link'}):
#                 link = a['href']
#                 link = 'https://jobs.atos.net' + link
#                 if link not in dict_of_key_skills['strUrl']:
#                     dict_of_key_skills['strUrl'].append(link)
#                     link_text = requests.get(link).text
#                     soup_l = BeautifulSoup(link_text, 'html.parser')
#                     title = soup_l.find(attrs={
#                         'itemprop': 'title'})
#                     if title:
#                         dict_of_key_skills['strJobTitle'].append(title.text)
#                     span = soup_l.find('span', attrs={
#                         'class': 'jobdescription'})
#                     d = html2text.HTML2Text()
#                     d.ignore_links = True
#                     skills = d.handle(span.text)
#                     array = re.split(r'/|,| |\n|;|(?!.* ).', skills, flags=re.DOTALL)
#                     list = frozenset(array)
#                     for skill in list:
#                         for s in sk:
#                             if skill.upper() == s.upper():
#                                 if s.upper() not in dict_of_key_skills['strArrKeySkills']:
#                                     dict_of_key_skills['strArrKeySkills'].append(s)
#             repeat = count_jobs_split[1] < count_jobs_split[2]
#             dict_of_key_skills['amountvac'] = count_jobs_split[2]
#             if repeat:
#                 next_page = count_jobs_split[1]
#         except:
#             repeat = False
#     driver.quit()
#     return dict_of_key_skills
#
#
# def analisys(dict, dict_of_key_skills):
#     for key_skill in dict_of_key_skills['strArrKeySkills']:
#         if dict.setdefault(key_skill) == None:
#             dict[key_skill] = 1
#         else:
#             dict[key_skill] += 1
# def json_create(dict_json):
#     with open("skills.json", "w") as outfile:
#         json.dump(dict_json, outfile)
# def prepare_data(text, region):
#     dict_of_key_skills = call(text, region)
#     dict_json = {}
#     dict_json['strSearch'] = dict_of_key_skills['strSearch']
#     dict_json['strArea'] = dict_of_key_skills['strArea']
#     dict_json['strUrl'] = dict_of_key_skills['strUrl']
#     dict_json['strJobTitle'] = dict_of_key_skills['strJobTitle']
#     dict_json['amountvac'] = dict_of_key_skills['amountvac']
#     dicti = {}
#     analisys(dicti, dict_of_key_skills)
#     sorted_d = dict(sorted(dicti.items(), key=operator.itemgetter(1), reverse=True))
#     dict_json['skills'] = sorted_d
#     json_create(dict_json)
#     dict_json['amountvacstr'] = f"{(len(sorted_d))} skills are found"
#     return dict_json

app = Flask(__name__)
port = int(os.environ.get('PORT', 3000))

djson = {}

@app.route('/', methods=('GET', 'POST'))
def load():
    global djson
    if request.method != 'POST':
        str_text = ""
        str_area = ""
        dict_json = {}
        dict_json['skills'] = {}
        dict_json['amountvacstr'] = ""
        pdf_display = False
    if request.method == 'POST':
        str_text = request.form['strText']
        str_area = request.form['strArea']

        text = str_text
        region = str_area
        djson = dict_json = scraper.prepare_data(text, region)
        pdf_display = True
    return render_template('index.html', strText=str_text, strArea=str_area, skill_list=dict_json['skills'],
                           strItemsNum=dict_json['amountvacstr'], pdf_display=pdf_display, )

@app.route('/pdf')
def pdf_gen():
    global djson
    pdf = pdf_lib.print(djson)

    response = make_response(pdf.output(dest='S').encode('latin-1'))
    response.headers['Content-Type'] = 'application/pdf;'
    response.headers['Content-Disposition'] = 'inline; filename=test.pdf'
    # response.headers.set('Content-Disposition', 'attachment', filename= 'test.pdf')
    # response.headers.set('Content-Type', 'application/pdf')
    return response

if __name__ == '__main__':
    app.run(host='localhost', port=port)
