# Embedding Route
# Routes related to creatiung text embeddings

import sys


from flask import (
    Blueprint, flash, g, redirect, request, session, url_for, jsonify, current_app as app
)
from werkzeug.exceptions import abort


#################################################
# Initialize the models
#################################################
# get the database configuration object
from ..config import config_db



from ..library.documentRetrieval import tfidf_score_str
from ..library.documentRetrieval import change_dict_structure
from ..library.postgresql import PostgresQL


# a dam tuki argumente ker mamo default ones, za funkcije to ni treba?

#tokens = app.config['TOKENS']
#texts = app.config['TEXTS']
#tfidf_function = app.config['TFIDF_FUNCTION']
#m = app.config['M']

## initialize text embedding model
model = PostgresQL()

#################################################
# Setup the embeddings blueprint
#################################################


bp = Blueprint('docRetrieval', __name__, url_prefix='/api/v1/docRetrieval')


@bp.route('/', methods=['GET'])
def index():
    # TODO: provide an appropriate output
    return abort(501)

@bp.route('/retrieval', methods=['GET', 'POST'])
def retrieval():
    # a je treba tukaj kje locit a pride stvar od userja al od drugega microservica

    tokens = None
    #tfidf_function = None
    m = None
    if request.method == 'GET':
        
        query=request.args.get('query', default='', type=str)
        tokens= query.split()
       # tfidf_function= request.args.get('tfidf_function', default='', type=str)
        m= request.args.get('m', default='', type=int)
    elif request.method == 'POST':
        
        tokens = request.json['tokens']
       # tfidf_function = request.json['tfidf_function']
        m = request.json['m']
    else:
        # TODO: log exception
        return abort(405)

    try:
        # TO OBVEZNO POPRAVI!!!
        db = config_db.get_db()
        #model.connect('envirolens', 'dbpass', user="postgres")
        docs = db.db_query(tokens)
        texts = change_dict_structure(docs) 
        tfidf_score = tfidf_score_str(tokens,texts,'tfidf_sum',m) 
        metadata = db.db_return_docs_metadata(tfidf_score)
        #config_db.close_db()
    except Exception as e:
        # TODO: log exception
        # something went wrong with the request
        return abort(400, str(e))
    else:
        # TODO: return the response
        return jsonify({
            "docs_metadata": metadata
        })

