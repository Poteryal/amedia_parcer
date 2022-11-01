from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import requests
import json


def selenium_scrap():
    options = webdriver.ChromeOptions()

    options.add_argument("--disable-blink-features=Automation")

    driver = webdriver.Chrome(
        options=options,
        service=Service('./chromedriver')
    )

    animes_list = {}
    driver.get('https://amedia.online')
    sleep(5)

    count = 0
    for i in range(4):
        sleep(.5)
        animes = driver.find_element(By.CLASS_NAME, 'section-content').find_elements(By.CLASS_NAME, 'newser')
        try:
            btn_more = driver.find_element(By.XPATH, '//a[text()="Вперед"]')
        except:
            btn_more = ''

        for j in animes:
            count += 1
            title = j.find_element(By.CLASS_NAME, 'animetitle1').text
            href = j.find_element(By.CSS_SELECTOR, 'div.animeposter>a').get_property('href')
            animes_list[count] = {'title': title, 'href': href}

        try:
            btn_more.click()
        except:
            pass

    with open('selenium_scrap.txt', 'w') as file:
        for i in animes_list:
            file.write(f"{i};{animes_list[i].get('title')};{animes_list[i].get('href')}\n")


def recycling_scrap():
    with open('selenium_scrap.txt', 'r') as file:
        s_scrap_file = file.read()

    new_scrap_file = s_scrap_file.split('\n')
    new_scrap_file.pop(-1)

    anime_info = {}
    for i in range(len(new_scrap_file)):
        g = new_scrap_file[i].split(';')
        num, title_name, url = g[0], g[1], g[2]

        req = requests.get(url)
        soup = BeautifulSoup(req.text, 'lxml')

        series_out = soup.find('div', class_='info').find('span').text
        series_total = soup.find('div', class_='info').find('span').find_next('span').text

        anime_info[num] = {
            'title_name': title_name,
            'series_out': series_out,
            'series_total': series_total
        }
        print('\r', f"Идет обработка данных: {int(i*100/len(new_scrap_file))}%", end='')
    print('\r', 'Данные получены и обработаны', end='')
    print('')

    with open('amedia_parcer.json', 'w') as file:
        json.dump(anime_info, file, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    selenium_scrap()
    recycling_scrap()
