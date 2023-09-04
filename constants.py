TYPE_MAPPING = {
    'in the development agreement': 'development agreement',
    'section 66 - notice of lie pendency': 'notice of pendency',
    '65-error correction letter': 'error correction letter',
    'deed of transfer': 'transfer deed',
    'agreement': 'general agreement',
}

VALID_TYPES = [
    'lease',
    'development agreement',
    'sale deed',
    'notice of pendency',
    'error correction letter',
    'transfer deed',
    'affidavit',
    'lease deed',
    'prize certificate',
    'declaration',
    'live ad licenses',
    'general agreement',
    'bill of sale',
]
from sqlalchemy import types
POSTGRES_DTYPES = {
    'sr_no': types.INTEGER,
    'doc_no': types.INTEGER,
    'doc_type': types.TEXT,
    'doc_date': types.DATE,
    'latest_buyer_name': types.TEXT,
    'latest_seller_name': types.TEXT,
    'other_info': types.TEXT,
    'list_no_2': types.TEXT,
    'buyer_history':types.TEXT,
    'seller_history':types.TEXT,
}

DB_PARAMS = {
    'user':'postgres',
    'password':'admin',
    'host':'localhost',
    'port':'5433',
    'database':'postgres'
}