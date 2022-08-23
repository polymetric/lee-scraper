#!/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import WebDriverException, NoSuchElementException, TimeoutException
import time
from pyvirtualdisplay import Display
from tqdm import tqdm
import arrow
from arrow import Arrow
import re
import json
import os

headless = False

os.system('killall chromium')

#display = Display(backend="xvfb", visible=1, size=(800, 800))
#display.start()
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
chrome_options.add_experimental_option("prefs",prefs)
chrome_options.add_argument("user-data-dir=selenium")
#chrome_options.add_argument('headless')
chrome_options.add_argument('--disable-gpu')

#specify the path to chromedriver.exe (download and save on your computer)
driver = webdriver.Chrome('chromedriver', options=chrome_options)



#driver.get("https://leefilters.com/lighting/colour-effect-lighting-filters/")

#    driver.find_element(By.XPATH, "//a[@id='CybotCookiebotDialogBodyButtonAccept']").click()
#    driver.find_element(By.XPATH, "//button[@id='buttonGlobal']").click()

#try:
#    WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//a[@id='CybotCookiebotDialogBodyButtonAccept']"))).click()
#except TimeoutException:
#    pass
#try:
#    WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//button[@id='buttonGlobal']"))).click()
#except TimeoutException:
#    pass
#
#w_color_list = driver.find_element(By.XPATH, "//ul[@class='colours-list list colours-list--colour']")
#w_color_items = w_color_list.find_elements(By.XPATH, "./li[@class='colours-list__colour']")
#color_links = []
#print('scraping main list page')
#for item in tqdm(w_color_items):
#    #code = item.find_element(By.XPATH, "./div[@class='colours-list__colour-code']/span").text
#    link = item.find_element(By.XPATH, "./div[@class='colours-list__tooltip-wrapper']/a").get_attribute('href')
#    color_links.append(link)
#

colors = {}
if os.path.exists('colors.json'):
    f=open('colors.json', 'r')
    colors = json.loads(f.read())
    f.close()
print(f'loaded {len(colors)} existing colors')
before_len = len(colors)

color_links = [1]
print('scraping individual color pages')
for link in color_links:
#    driver.get(link)
    driver.get("https://leefilters.com/colour/002-rose-pink/")
    name_and_code = driver.find_element(By.XPATH, "//div[@class='page-header__text']").text
    name_and_code = re.search(r'(\d*) (.*)', name_and_code)
    code = name_and_code.group(1)
    name = name_and_code.group(2)
    desc = driver.find_element(By.XPATH, "//div[@class='page-header__colour-desc']").text
    rgb_raw = driver.find_element(By.XPATH, "//div[@class='page-header__colour']").get_attribute('style')
    rgb = re.search(r'(#[\d|\w]*)', rgb_raw).group(1)
    color_graph = driver.find_element(By.XPATH, "//div[@class='colour__graph-wrapper init']/*[local-name()='svg']")
    graph_tooltips = color_graph.find_elements(By.XPATH, ".//*[local-name()='circle']")
    graph = {}
    for i in graph_tooltips:
        text = i.get_attribute('title')
        re_result = re.search('<span>(\d*)<\/span>Colour:\xa0<b>(\d*\.\d*)<\/b>', text)
        wavelength = re_result.group(1)
        percentage = re_result.group(2)
        graph[wavelength] = percentage
    trans_specs = driver.find_element(By.XPATH, "//ul[@class='colour__transmissions']")
    tungsten_specs = trans_specs.find_element(By.XPATH, "./li/h2[text()='Tungsten']/..")
    daylight_specs = trans_specs.find_element(By.XPATH, "./li/h2[text()='Daylight (Source C)']/..")
    def get_specs(parent):
        trans = parent.find_element(By.XPATH, ".//span[text()='Transmission Y']/../span[@class='spec-list__value']").text
        x = parent.find_element(By.XPATH, ".//span[text()='x']/../span[@class='spec-list__value']").text
        y = parent.find_element(By.XPATH, ".//span[text()='y']/../span[@class='spec-list__value']").text
        absorption = parent.find_element(By.XPATH, ".//span[text()='Absorption']/../span[@class='spec-list__value']").text
        return(trans, x, y, absorption)
    (daylight_trans, daylight_x, daylight_y, daylight_absorption) = get_specs(daylight_specs)
    driver.find_element(By.XPATH, "//select[@class='colour__transmission-switcher']").click()
    driver.find_element(By.XPATH, "//option[text()='Tungsten']").click()
    (tungsten_trans, tungsten_x, tungsten_y, tungsten_absorption) = get_specs(tungsten_specs)

    # insert values into dictionary
    colors[code] = {}
    colors[code]['name'] = name
    colors[code]['desc'] = desc 
    colors[code]['rgb'] = rgb
    colors[code]['spect_graph'] = graph
    colors[code]['tungsten_specs'] = {}
    colors[code]['tungsten_specs']['trans'] = tungsten_trans
    colors[code]['tungsten_specs']['x'] = tungsten_x
    colors[code]['tungsten_specs']['y'] = tungsten_y
    colors[code]['tungsten_specs']['absorption'] = tungsten_absorption
    colors[code]['daylight_specs'] = {}
    colors[code]['daylight_specs']['trans'] = daylight_trans
    colors[code]['daylight_specs']['x'] = daylight_x
    colors[code]['daylight_specs']['y'] = daylight_y
    colors[code]['daylight_specs']['absorption'] = daylight_absorption

print(f'found {len(colors)-before_len} new colors')
f=open('colors.json', 'w')
f.write(json.dumps(colors, indent=4))
f.close()

