## Scrapper for igrmaharashtra.gov.in website

Implemented an automated scrapping tool for the website 'https://pay2igr.igrmaharashtra.gov.in/eDisplay/propertydetails'

NOTE : This script may not follow the _industry standards_, but I am willing to learn and in no time, will grasp all that is required for the furthur processes.

Navigate to root directory and

Install required libraries,
```bash
pip install -r requirements.txt
```

Use the scrapper, (execute the 'run.py' file)
``` bash 
python run.py
```

Steps to follow: 
1. As site opens, let the script enter details until doc year = 2023
2. Enter captcha manually (will implement auto ocr in future iterations)
3. Wait for it to search and enter rows
4. Use google translate extension to translate the whole page

   NOTE: A window of 25 seconds is added to scroll down to bottom so that the extension translates the data fully.
5. If there is more than one page, let the script click on NEXT button, and scroll the page again for translated data.
(Auto Scrolling to be added in furthur iterations)

This process also implements data cleaning pipeline with a batchsize of 50 rows/ 1 page.

Subsequently, also adds the data to the POSTGRES table active on the local server.

## API Endpoints 

### Retrieve Scraped Data

- **Endpoint**: `/column_name`
- **Method**: GET
- **Description**: Retrieve all scraped data from the database. 
- **Returns**: all records in JSON 

Steps: 
1. Go to Server Folder
2. Run command 
   ```
   python server.py
   ```
3. Wait for development server to start.
4. Copy the link and paste in API testing tool (Ex. POSTMAN API)
5. Follow example search strings as below

_These are just the examples of API endpoints that can be created. SQL queries can be used to search with the database to a good extent_

_These are the basic examples implemented to demonstrate the working ot api endpoints with postgres table_


**Example Request**:
- Request a specific `year` data
```bash
localhost/2023
```
- Request address using partial text search
```bash
localhost/address?search=mumbai
```
- Request name using partial text search
```bash
localhost/name?search=advocate
```
- Request name using partial text search
```bash
localhost/doc_no?search=2449
```

## Data Cleaning Pipeline Walkthrough

**Libraries used**: pandas, sklearn.base, numpy

**Loc**: custom_transformers.py

**Steps**
1. Dropped any of Nan values
2. Dropped undesired column list no. 2 ( already scraped link in another)
3. Renamed columns to database conventions separated with an underscore (ex. buyer_name)
4. Changed date dtypes from string object to datetime object
5. Changed float dtypes to int dtypes
6. Separated the latest buyers and sellers from buyer and seller list columns, created new columns with latest_buyer_name and latest_seller_name
7. Renamed old buyer and seller columns to buyer_history and seller_history
8. Removed anomalies from doc_type column

All these steps have been performed using sklearn.pipeline and sklearn.base libraries using Pipeline, TransformerMixin and BaseEstimator class. 

No real use of BaseEstimator in this case, helpful for imputing estimated values for numerical data

## Inputs in database

**Libraries** : pandas, sqlalchemy, psycopg2

**Loc**: Table/table.py

**Steps**
1. Connect to database using DB_PARAMS constants
2. Create sqlalchemy engine and entering database
3. Read cleaned_0.csv to pandas
4. Used to_sql method of postgres with sqlalchemy engine to input values in database
5. If table exists, options selected is to append values, we the inputs can keep coming from webdriver
6. Defined POSTGRES_DTYPES constant in Constants/constants.py and used it to define datatypes of database
7. Done for now, all inputs added

# Conclusion

This package demonstrates my abilities to scraping a website and clean the data in transition so that it is ready to be stored in the database. 

Most of my learnings while doing this project includes: 
   1. BS4 makes inputing structured data scraping easier.
   2. Automating every step of data ingestion can be challenging.
   3. Was weak using SQL queries but, with this I have learnt the capabilities of SQL
   4. There is always a scope of improvement.

## Plan for Furthur Iterations

I was suggested to use Docker Image to input data in PostGres. I am unfamilier with the use cases of docker. So will be exploring docker now, to ensure that the ETL flow is able to meet industry standards.

The captcha can be automated using OCR to convert image to text

For now, extension can only be enabled by webdriver, but user need to manually translate page using the extension and scroll

_Using JS injection in webpages may help with scrolling and libraries like autogui in python, we can direct the mouse cursor the translate the page for itself_

Will keep on exploring for furthur possibilities in automation of scrapping.