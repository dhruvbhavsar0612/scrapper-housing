from flask import Flask, request, jsonify
import psycopg2
from Constants.constants import DB_PARAMS

# init flask app
app = Flask(__name__)


# Function to fetch data from the database based on partial text search
def get_data_by_name(search_text):
    '''
    input-
        search_text(string): search text for querying into database table
    returns-
        data(JSON): entire record from database as a json object
    '''
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cursor = conn.cursor()
        
        # Use ILIKE to perform case-insensitive partial text search on buyer's name, seller's name, and other information
        query = (
            "SELECT * FROM tbl_andheri_housing WHERE "
            "buyer_history ILIKE %s OR seller_history ILIKE %s"
        )
        cursor.execute(query, ('%' + search_text + '%', '%' + search_text + '%'))
        
        data = cursor.fetchall()
        conn.close()
        
        return data
    except Exception as e:
        return str(e)

# function to get data using partial text search on address present in other_info
def get_data_by_address(search_text):
    '''
    input-
        search_text(string): search text for querying into database table
    returns-
        data(JSON): entire record from database as a json object
    '''
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cursor = conn.cursor()
        
        # Use ILIKE to perform case-insensitive partial text search on other_info
        query = (
            "SELECT * FROM tbl_andheri_housing WHERE "
            "other_info ILIKE %s"
        )
        cursor.execute(query, ('%' + search_text + '%',))

        
        data = cursor.fetchall()
        conn.close()
        
        return data
    except Exception as e:
        return str(e)

# function to fetch data from database based on doc_no
def get_data_by_doc_no(doc_no):
    '''
    input-
        doc_no(int): query doc_no to select from database table
    returns-
        data(JSON): entire record from database as a json object
    '''
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cursor = conn.cursor()

        query = f"SELECT * FROM tbl_andheri_housing WHERE doc_no = '{doc_no}'"
        cursor.execute(query)

        data = cursor.fetchall()

        conn.close()
        return data
    except Exception as e:
        return str(e)
    
# function to fetch data from database based on doc_date of type date containing specific year

def get_data_by_doc_date(year):
    '''
    input-
        year(string): search year for querying into database table
    returns-
        data(JSON): entire record from database as a json object
    '''
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cursor = conn.cursor()

        query = f"SELECT * FROM tbl_andheri_housing WHERE EXTRACT(YEAR FROM doc_date) = {year}"
        cursor.execute(query)

        data = cursor.fetchall()

        conn.close()
        return data
    except Exception as e:
        return str(e)
    
@app.route("/doc_no", methods=['GET'])
def fetch_data_by_doc_no_endpoint():
    doc_no = request.args.get('search')
    if not doc_no:
        return jsonify({'error': 'Please provide a Document No.'}), 400
    
    data = get_data_by_doc_no(doc_no)
    return jsonify(data)

@app.route("/year/<string:year>", methods=['GET'])
def fetch_data_by_year_endpoint(year):
    data = get_data_by_doc_date(year)
    return jsonify(data)

@app.route("/name", methods=['GET'])
def fetch_data_by_name_endpoint():
    search_text = request.args.get('search')
    if not search_text:
        return jsonify({'error': 'Please provide a Name'}), 400
    
    data = get_data_by_name(search_text)
    return jsonify(data)

@app.route("/address", methods=['GET'])
def fetch_data_by_address_endpoint():
    search_text = request.args.get('search')
    if not search_text:
        return jsonify({'error': 'Please provide a search term'}), 400
    
    data = get_data_by_address(search_text)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)