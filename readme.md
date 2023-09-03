## Scrapper for igrmaharashtra.gov.in website

- Implemented an automated scrapping tool for the website 'https://pay2igr.igrmaharashtra.gov.in/eDisplay/propertydetails'

To use the scrapper, 
``` bash 
python run.py
```
(execute the 'run.py' file)

Steps to follow: 
1. As site opens, let the script enter details until doc year = 2023
2. Enter captcha manually (will implement auto ocr in future iterations)
3. Wait for it to search and enter rows
4. Use google translate extension to translate the whole page NOTE: A window of 25 seconds is added to scroll down to bottom so that the extension translates the data fully.
5. If there is more than one page, let the script click on NEXT button, and scroll the page again for translated data.
(Auto Scrolling to be added in furthur iterations)

This process also implements data cleaning pipeline with a batchsize of 50 rows/ 1 page.

Subsequently, also adds the data to the POSTGRES table active on the local server.

## API Endpoints 