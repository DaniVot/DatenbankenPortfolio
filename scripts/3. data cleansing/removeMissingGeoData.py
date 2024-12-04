from pymongo import MongoClient

# Verbindung zur MongoDB herstellen
client = MongoClient("mongodb://localhost:27017/")  # Passe die Verbindung bei Bedarf an
db = client["PortfolioPruefung"]  # Ersetze "deine_datenbank" durch den Namen deiner Datenbank

# Collections auswählen
fake_yelp_business = db["fake_yelp_business"]
fake_inspection_results = db["fake_inspection_results"]

# Finde alle business_ids in fake_yelp_business ohne Geodaten
business_ids_without_geo = fake_yelp_business.find(
    {"$or": [{"latitude": None}, {"longitude": None}]},
    {"business_id": 1, "_id": 0}
)

# Extrahiere die business_ids aus dem Cursor
business_ids_without_geo = [doc["business_id"] for doc in business_ids_without_geo]

# Lösche die betroffenen Datensätze aus fake_yelp_business
result_yelp = fake_yelp_business.delete_many({"business_id": {"$in": business_ids_without_geo}})
print(f"Gelöschte Datensätze aus fake_yelp_business: {result_yelp.deleted_count}")

# Lösche die entsprechenden Datensätze aus fake_inspection_results
result_inspection = fake_inspection_results.delete_many({"CAMIS": {"$in": business_ids_without_geo}})
print(f"Gelöschte Datensätze aus fake_inspection_results: {result_inspection.deleted_count}")
