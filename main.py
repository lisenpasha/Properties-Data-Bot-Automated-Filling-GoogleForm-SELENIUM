import time

form_url="https://forms.gle/M6ZLBuR13uXbnFc3A"
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

zillow_url="https://www.zillow.com/san-francisco-ca/rentals/?searchQueryState=%7B%22mapBounds%22%3A%7B%22north%22%3A37.84608530611633%2C%22east%22%3A-122.32758609179687%2C%22south%22%3A37.70443074814723%2C%22west%22%3A-122.53907290820312%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A20330%2C%22regionType%22%3A6%7D%5D%2C%22pagination%22%3A%7B%7D%7D"

parameters={
 "Accept-Language" : "en-GB,en-US;q=0.9,en;q=0.8",
  "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
}

response=requests.get(zillow_url,headers=parameters)
response=response.text

soup=BeautifulSoup(response,"lxml")
# print(soup.prettify())

adresses_list=[]
price_list=[]
links_list=[]

#GETTING properties data from Zillow Using BeautifulSoup.
adresses=soup.select(selector="address")
links=soup.select(selector="ul li article div a")
for adress in adresses:
    adresses_list.append(adress.text)

# print(adresses_list)
# print(len(adresses_list))
for link in links:
    link=link.get("href")
    if "https://www.zillow.com" in link:
        links_list.append(link)
    else:
        links_list.append("https://www.zillow.com" + link)


prices=soup.find_all(name="div",class_="StyledPropertyCardDataArea-c11n-8-73-8__sc-yipmu-0 hRqIYX")
for price in prices:
    only_the_price=price.getText().split("+")[0]
    if "mo" in only_the_price:
        only_the_price=only_the_price.split("/")[0]
    price_list.append(only_the_price)

#Initializing an AUTOMATED TEST SOFTWARE to fill in our form with the data we got from zillow's website.
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

chrome_driver_path="C:\Develpoment(Selenium)\chromedriver"
service = Service(f"{chrome_driver_path}.exe")

driver=webdriver.Chrome(service=service,options=chrome_options)
driver.get(form_url)

for i in range(len(adresses_list)):
    time.sleep(2)
    form_adress_input=driver.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    form_adress_input.send_keys(adresses_list[i])
    form_price_input=driver.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    form_price_input.send_keys(price_list[i])
    form_link_input=driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    form_link_input.send_keys(links_list[i])
    button=driver.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span')
    button.click()
    time.sleep(2)
    submit_another_response=driver.find_element(By.XPATH,'/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
    submit_another_response.click()