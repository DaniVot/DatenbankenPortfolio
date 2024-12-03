from pymongo import MongoClient

# MongoDB-Verbindung aufbauen
client = MongoClient('mongodb://localhost:27017/')
db = client['PortfolioPruefung']

# Collections
fake_inspection_results = db.fake_inspection_results
fake_yelp_business = db.fake_yelp_business

# 1. Alle Dokumente mit INSPECTION DATE = "01/01/1900" finden
documents_to_delete = fake_inspection_results.find({'INSPECTION DATE': "01/01/1900"})

# 2. business_id/CAMIS-Werte sammeln
business_ids_to_delete = [doc['CAMIS'] for doc in documents_to_delete]

# 3. Zugehörige Einträge in fake_yelp_business löschen
result_yelp = fake_yelp_business.delete_many({'business_id': {'$in': business_ids_to_delete}})
print(f"{result_yelp.deleted_count} Einträge aus fake_yelp_business gelöscht.")

# 4. Einträge in fake_inspection_results löschen
result_inspection = fake_inspection_results.delete_many({'INSPECTION DATE': "01/01/1900"})
print(f"{result_inspection.deleted_count} Einträge aus fake_inspection_results gelöscht.")
