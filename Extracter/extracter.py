# webdriver imports and os import for setting driver path variable
from selenium import webdriver
import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import Extracter.constants as const
# from selenium.webdriver.support.wait import WebDriverWait

# table extraction imports
from bs4 import BeautifulSoup
import pandas as pd

<<<<<<< HEAD
=======
from custom_transformers import NanDropper, ColDropper, ReplaceNames, DateFormat, FloatInt, NameSeparator, HistoryColumns, RemoveAnomalies
from sklearn.pipeline import Pipeline
>>>>>>> bdc53be12ff0768043ffdab7dbb740668f72183c

class InputFields(webdriver.Chrome):

    def __init__(self, driver_path="G:/SeleniumDrivers" ,teardown=False):
        '''
        input-
            driver_path(PATH): specifies path to chromedriver.exe
            teardown(boolean): if true, browser will not close after opening the landing page
        function -
            initializes the driver and sets the driver path in os environment
            sets the teardown variable to prevent browser from closing immediately
        '''
        self.driver_path = driver_path
        self.teardown = teardown #prevents webpage from closing immediately
        os.environ['PATH'] += self.driver_path #sets driver path in os environments
        options = webdriver.ChromeOptions()
        options.add_extension('C:/Users/Admin/AppData/Local/Google/Chrome/User Data/Default/Extensions/aapbdbdomjkkjkaonfhkkikfgjllcleb/2.0.13_0.crx')
        super(InputFields,self).__init__(options=options)
        self.maximize_window()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        '''
        function- 
            prevents browser from closing
        '''
        if self.teardown:
            self.quit()
        # else:
        #     while(True): #browser keeps on closing after opening, hence I thought of this idea, if i keep loop running, then it won't close the browser
        #         pass

    def landing_page(self):
        '''
        function -
            driver launches the landing page
        '''
        self.get(const.BASE_URL)
    
    def select_year(self, year):
        '''
        input-
            year(string:number): year of document
        function -
            enters keys in the required input fields
        '''
        select_element = self.find_element(By.NAME,'years')
        select = Select(select_element)
        select.select_by_visible_text(year)
        time.sleep(2)
    
    def select_district(self, name):
        '''
        input-
            name(string): name of district
        function -
            selects the district from the drop down menu
        '''
        select_element = self.find_element(By.NAME, 'district_id')
        select = Select(select_element)
        select.select_by_visible_text(name)
        time.sleep(2)
    
    def select_taluka(self, name):
        '''
        input-
            name(string): name of taluka
        function -
            selects the taluka from the drop down menu
        '''
        select_element = self.find_element(By.NAME, 'taluka_id')
        select = Select(select_element)
        select.select_by_visible_text(name)
        time.sleep(2)
    
    def select_village(self,name):
        '''
        input-
            name(string): name of village
        function -
            selects the village from the drop down menu
        '''
        select_element = self.find_element(By.NAME, 'village_id')
        select = Select(select_element)
        select.select_by_visible_text(name)
        time.sleep(2)

    def type_doc_year(self, year):
        '''
        input- 
            year(string:number): year of document
        function -
            enters keys in the required input fields
        '''
        select_element = self.find_element(By.ID,'free_text')
        select_element.send_keys(year)
        time.sleep(7) #meanwhile i enter the captcha manually (as of now)
    
    def submit(self):
        '''
            click on submit button
        '''
        select_element = self.find_element(By.ID, 'submit')
        select_element.click()

    def select_rows(self, rows='50', sleep_time=20):
        '''
        input-
            rows(string:number): number of rows to display in webp table
        '''
        self.implicitly_wait(10)
        select_element= self.find_element(By.NAME, 'tableparty_length')
        select = Select(select_element)
        select.select_by_value(rows)

        # wait for extension to translate the data
        time.sleep(sleep_time)

    def save_table(self,count=1):
        '''
        input args-  
            count(int) : count of number of webpages to be scrapped
        output- 
            saves tables of 50 rows as csv 
        function workflow- 
            creates datapipeline using Pipeline object of sklearn
            extracts table using BS4 and column names
            extracts all the data in the table
            passes the created dataframe into Pipeline object
            saves cleaned_numbered.csv
        '''
        from TableNew.table import inputTableToPostgres

        table = self.find_element(By.ID,'tableparty')
        
        # INITIALIZING data cleaning pipeline
        data_cleaning_pipeline = Pipeline([
            ('nan_dropper', NanDropper()),  # Drop rows with NaN values
            ('col_dropper', ColDropper()),  # Drop a specific column
            ('replace_names', ReplaceNames()),  # Replace column names
            ('date_format', DateFormat()),  # Format date column
            ('float_int', FloatInt()), # Convert float values to int
            ("name_sep", NameSeparator()), #separate latest buyers from the data 
            ("add_history_columns", HistoryColumns()), # add older columns as history of buyers and sellers
            ("remove_anomalies", RemoveAnomalies()) 
        ])

        # using beautiful to parse the html table, helps extracting the data easily
        soup = BeautifulSoup(table.get_attribute('outerHTML'),"html.parser")
        print('soup initialized')
        # initialize a list of headers 
        table_headers=[]
        for th in soup.find_all('th'):
            table_headers.append(th.text)
        print('Headers denoted')
        table_headers.append('List No. 2')
        
        for row in soup.find_all('tr')[1:]:
            table_rows=[]

            columns= row.find_all('td')
            output_data=[]

            for col in columns:
                output_data.append(col.text)
            
            for a in row.find_all('a',href=True):
                output_data.append(const.BASE_URL+''+a['href'])
                
            table_rows.append(output_data)
<<<<<<< HEAD

        df = pd.DataFrame(table_rows,columns=table_headers)
        df.to_csv(name,'.csv')
    
    def clean_table(self, name='data'):
        df = pd.read_csv('data_with_link.csv', index_col=[0])
        
        df.dropna(axis=1, inplace=True)

        # keeping the last column of links and rejecting the second last column of useless data

        # ['Sl no.', 'Diarrhea no.', 'diarrhea type', 'Du. Prohibit. Office','Year', 'Will write', 'Will write down', 'Other information','List no. 2']
        drop_col = df.columns[-2]
        df.drop(columns=drop_col, inplace=True)
        df.rename(columns={'link':drop_col}, inplace=True)

        # renaming the anomalies in the columns
        df.rename(columns={
            df.columns[0]:'sr_no',
            df.columns[1]:'doc_no',
            df.columns[2]:'doc_type',
            df.columns[3]:'dn_office',
            df.columns[4]:'doc_date',
            df.columns[5]:'buyer_name',
            df.columns[6]:'seller_name',
            df.columns[7]:'other_info',
            df.columns[8]:'list_two_link'
        }, inplace=True)

        """
        ['lease', 'In the development agreement', 'sale deed',
            'Section 66 - Notice of lie pendency',
            '65-error correction letter', 'Development Agreement',
            'Deed of Transfer', 'affidavit', 'leasedeed', '59-Transfer',
            'prize certificate', 'declaration', 'Live Ad Licenses',
            'transfer deed', 'Agreement', '36-A-Live Ad Licenses',
            'Bill of Sale', 'Amphideviate']
        Unique values need to be tweaked for better readability
        """
        df.replace(to_replace='Amphideviate', value='affidavit', inplace=True)
        df.replace(to_replace='Deed of Transfer', value='transfer deed', inplace=True)
        df.replace(to_replace='leasedeed',value='lease deed',inplace=True)
        df.replace(to_replace='Section 66 - Notice of lie pendency', value='Notice of lease pendency', inplace=True)

        # columns have datatypes of object and float64, need conventional form of dtypes
        for col in df.columns:
            if df[col].dtype == 'float64':
                df[col] = df[col].astype('int32')

        # converting doc_date from string object to datetime object
        try:
            df['doc_date'] = pd.to_datetime(df['Year'],format='mixed')
        except:
            ValueError('Not in correct format')
        
        df.to_csv(name,+'.csv')
=======
        
            df = pd.DataFrame(table_rows,columns=table_headers)
            print('data frame created')

            # handling any error in the pipeline
            try:
                cleaned_df = data_cleaning_pipeline.fit_transform(df)
                print('cleaning pipeline successful')
            except Exception as e:
                print(f"Pipeline error: {str(e)}")

            # initializing the input table object for database inputs
            input_table= inputTableToPostgres()
            input_table.input_table(df=cleaned_df)
    
    def next_page(self):
        '''
        function : clicks on the next page button of the website
        '''
        print('moving on to the next page')
        next_page = self.find_element(By.CSS_SELECTOR, 'a[data-dt-idx="8"]')
        next_page.click()    
        time.sleep(20)        
>>>>>>> bdc53be12ff0768043ffdab7dbb740668f72183c
