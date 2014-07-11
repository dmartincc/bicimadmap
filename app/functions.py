
def get_db(db_name):
    from pymongo import MongoClient
    uri = 'mongodb://user:passw0rd@kahana.mongohq.com:10070/bicimadmap'
    client = MongoClient(uri)
    db = client[db_name]
    return db  