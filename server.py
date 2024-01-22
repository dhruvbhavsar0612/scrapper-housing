from flask import Flask, request, jsonify
import psycopg2
from Constants.constants import DB_PARAMS

# init flask app
app = Flask(__name__)


# post methods
def insert_data(data):
    '''
    input-
        data(list): data to be inserted into the database for a single row
    returns-
        message(str): success or error message
    '''
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cursor = conn.cursor()

        print("printingggg - ------------ ",data)


        query_template = (
            "INSERT INTO public.tbl_andheri_housing "
            "(sr_no, doc_no, doc_type, dn_office, doc_date, buyer_history, "
            "seller_history, other_info, list_no_2, latest_buyer_name, latest_seller_name) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        )

        cursor.execute(query_template, (
            data[0], data[1], data[2], data[3], data[4], data[5],
            data[6], data[7], data[8], data[9], data[10]
        ))

        conn.commit()
        conn.close()

        return 'Data inserted successfully'
    except Exception as e:
        return f'Error inserting data: {str(e)}'


def update_data(doc_no, updated_data):
    '''
    input-
        doc_no(int): doc_no to identify the record to be updated
        updated_data(dict): updated data
    returns-
        message(str): success or error message
    '''
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cursor = conn.cursor()

        # Assuming updated_data is a dictionary containing the fields to be updated
        # Adjust the query and parameters based on your database schema
        query = (
            "UPDATE tbl_andheri_housing "
            "SET field1 = %s, field2 = %s, field3 = %s "
            "WHERE doc_no = %s"
        )
        cursor.execute(query, (updated_data['field1'], updated_data['field2'], updated_data['field3'], doc_no))

        conn.commit()
        conn.close()

        return 'Data updated successfully'
    except Exception as e:
        return str(e)




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
        search_text = search_text.replace(' ', '%')
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
        search_text = search_text.replace(' ', '%')
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

@app.route("/<string:year>", methods=['GET'])
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



@app.route("/insert", methods=['POST'])
def insert_data_endpoint():
    data = request.json
    if not data:
        return jsonify({'error': 'Please provide data for insertion'}), 400
    
    message = insert_data(data)
    return jsonify({'message': message})


@app.route("/update/<int:doc_no>", methods=['PUT'])
def update_data_endpoint(doc_no):
    updated_data = request.json
    if not updated_data:
        return jsonify({'error': 'Please provide updated data'}), 400

    message = update_data(doc_no, updated_data)
    return jsonify({'message': message})




if __name__ == '__main__':
    app.run(debug=True)