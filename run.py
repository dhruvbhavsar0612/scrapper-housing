from Extracter.extracter import InputFields
import pandas as pd
import time
<<<<<<< HEAD
=======
from TableNew.table import inputTableToPostgres
>>>>>>> bdc53be12ff0768043ffdab7dbb740668f72183c

# all the methods called one by one for extracting the data
def extract_pages(count, year, district, taluka, village , doc_year, rows):
    '''
    input-
        count(int): specify the number of pages to be extracted
    function-
        executes every step required to input on the webpage
        uses webdriver object 
    '''
    with InputFields() as bot:
        bot.landing_page()
        bot.select_year(year=year)
        bot.select_district(name=district)
        bot.select_taluka(name=taluka)
        bot.select_village(name=village)
        bot.type_doc_year(year=year)
        bot.submit()
        bot.select_rows(sleep_time=30,rows=rows)
        i=0 
        # using while loop to extract the data for the number of pages specified
        while i<count:
            bot.save_table(count=i)
            bot.next_page()
            i=i+1

<<<<<<< HEAD
with InputFields() as bot:
    bot.landing_page()
    bot.select_year(year='2023')
    bot.select_district(name='मुंबई उपनगर')
    bot.select_taluka(name='अंधेरी')
    bot.select_village(name='बांद्रा')
    bot.type_doc_year(year="2023")
    bot.submit()
    bot.select_rows(rows='50')
    df = bot.save_table(name='data_with_link_2')
    bot.clean_table(df=df, name='data_with_link_cleaned')
=======
# enter the number of pages required to be extracted
# here the number of pages is 1
extract_pages(count=1, year='2023', district='मुंबई उपनगर', taluka='अंधेरी', village='बांद्रा', doc_year='2023' ,rows='50')
>>>>>>> bdc53be12ff0768043ffdab7dbb740668f72183c
