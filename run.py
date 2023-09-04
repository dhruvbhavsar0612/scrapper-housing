from Extracter.extracter import InputFields
import pandas as pd
import time
from table import inputTableToPostgres

# all the methods called one by one for extracting the data
def extract_pages(count):
    with InputFields() as bot:
        bot.landing_page()
        bot.select_year(year='2023')
        bot.select_district(name='मुंबई उपनगर')
        bot.select_taluka(name='अंधेरी')
        bot.select_village(name='बांद्रा')
        bot.type_doc_year(year="2023")
        bot.submit()
        bot.select_rows(rows='50')
        i=0 
        while i<count:
            bot.save_table(name='data_with_link',count=i)
            input_table= inputTableToPostgres()
            input_table.input_table(count=i)
            bot.next_page()
            i=i+1

extract_pages(1)