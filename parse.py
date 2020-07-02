from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import re
import requests
import os
import time


path_sc = r'/home/v-osipov/PycharmProjects/pars/venv/scripts_from_git/'


def auth():
    driver = webdriver.Firefox()
    # driver.get(f"https://github.com/search?l=Visual+Basic+.NET&q=vba&type=Code")
    # driver.get('https://github.com/search?l=Visual+Basic+.NET&o=desc&q=vba&s=indexed&type=Code')
    # driver.get('https://github.com/search?l=Visual+Basic+.NET&o=asc&q=vba&s=indexed&type=Code')
    driver.get('https://github.com/search?l=Visual+Basic+.NET&p=1&q=visual+basic&type=Code')
    login = driver.find_element_by_id("login_field")
    password = driver.find_element_by_id("password")
    login.send_keys('taytds10@gmail.com')
    password.send_keys('pass')
    inp = driver.find_element_by_name('commit')
    inp.click()
    return  driver



def get_page(driver):
    for n in range(1,100):
        driver.get(f'https://github.com/search?l=Visual+Basic+.NET&p={n}&q=visual+basic&type=Code')
        #driver.get(f'https://github.com/search?l=Visual+Basic+.NET&o=asc&p={n}&q=vba&s=indexed&type=Code')
        # driver.get(f'https://github.com/search?l=Visual+Basic+.NET&o=desc&p={n}&q=vba&s=indexed&type=Code')
        # driver.get(f"https://github.com/search?l=Visual+Basic+.NET&p={n}&q=vba&type=Code")
        get_write_code(driver.page_source)
        time.sleep(1.5)
    driver.close()


#
#
def get_write_code(page_html):
    soup = BeautifulSoup(page_html, 'html.parser')
    divs = soup.find_all(class_='f4 text-normal')

    for element in divs:
        string = element.a.attrs['data-hydro-click']
        url = re.search(r'(https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?', string)
        url = url.group(0)
        url = url.split('https://github.com/')[1]
        url = 'https://raw.githubusercontent.com/' + ''.join(url.split('/blob'))

        req=requests.get(url)

        file_name = url.split('/')[-1]
        try:
            with open(path_sc + file_name, 'w') as f:
                f.write(req.text)
        except IsADirectoryError:
            pass


#
get_page(auth())

