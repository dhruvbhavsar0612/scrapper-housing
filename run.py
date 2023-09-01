from Extracter.extracter import InputFields

with InputFields() as bot:
    bot.landing_page()
    bot.select_year(year='2023')
    bot.select_district(name='मुंबई उपनगर')
    bot.select_taluka(name='अंधेरी')
    bot.select_village(name='बांद्रा')
    bot.type_doc_year(year="2023")
    bot.submit()