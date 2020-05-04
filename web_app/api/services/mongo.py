import ssl
from pymongo import MongoClient

url = "mongodb+srv://AltAllergenDBAdmin:allergenadmin@altallergendbcluster-kkirt.mongodb.net"

def get_collection(name):
    client = MongoClient(url, ssl_cert_reqs=ssl.CERT_NONE)
    db = client['altAllergen']
    return db[name]
