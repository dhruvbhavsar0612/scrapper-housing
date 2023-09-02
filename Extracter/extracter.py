# webdriver imports and os import for setting driver path variable
from selenium import webdriver
import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import Extracter.constants as const
# from selenium.webdriver.support.wait import WebDriverWait

# importing google translator api
from googletrans import Translator

# table extraction imports
from bs4 import BeautifulSoup
import pandas as pd

class InputFields(webdriver.Chrome):
    def __init__(self, driver_path="G:/SeleniumDrivers" ,teardown=False):
        self.driver_path = driver_path
        self.teardown = teardown #prevents webpage from closing immediately
        os.environ['PATH'] += self.driver_path #sets driver path in os environments
        super(InputFields,self).__init__()
        self.maximize_window()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()
        else:
            while(True): #browser keeps on closing after opening, hence I thought of this idea, if i keep loop running, then it won't close the browser
                pass

    def landing_page(self):
        self.get(const.BASE_URL)
    
    def select_year(self, year):
        select_element = self.find_element(By.NAME,'years')
        select = Select(select_element)
        select.select_by_visible_text(year)
        time.sleep(2)
    
    def select_district(self, name):
        select_element = self.find_element(By.NAME, 'district_id')
        select = Select(select_element)
        select.select_by_visible_text(name)
        time.sleep(2)
    
    def select_taluka(self, name):
        select_element = self.find_element(By.NAME, 'taluka_id')
        select = Select(select_element)
        select.select_by_visible_text(name)
        time.sleep(2)
    
    def select_village(self,name):
        select_element = self.find_element(By.NAME, 'village_id')
        select = Select(select_element)
        select.select_by_visible_text(name)
        time.sleep(2)

    def type_doc_year(self, year):
        select_element = self.find_element(By.ID,'free_text')
        select_element.send_keys(year)
        time.sleep(7) #meanwhile i enter the captcha manually (as of now)
    
    def submit(self):
        select_element = self.find_element(By.ID, 'submit')
        select_element.click()

    def select_rows(self, rows='50'):
        self.implicitly_wait(10)
        select_element= self.find_element(By.NAME, 'tableparty_length')
        select = Select(select_element)
        select.select_by_value(rows)

    def save_table(self, name='data'):
        table = self.find_element(By.ID,'tableparty')

        # using beautiful to parse the html table, helps extracting the data easily
        soup = BeautifulSoup(table.get_attribute('outerHTML'),"html.parser")

        # initialize a list of headers 
        table_headers=[]
        for th in soup.find_all('th'):
            table_headers.append(th.text)

        table_rows=[]
        for row in soup.find_all('tr'):
            columns= row.find_all('td')
            output_data=[]

            for col in columns:
                output_data.append(col.text)

            table_rows.append(output_data)
        
        df = pd.DataFrame(table_rows, columns=table_headers)
        df.to_csv(name+'.csv')
