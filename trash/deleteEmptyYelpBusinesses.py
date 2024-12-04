from pymongo import MongoClient

# Replace the uri string with your MongoDB deployment's connection string.
client = MongoClient('mongodb://localhost:27017/')
db = client['NYAnalyse']

# Collections
inspection_collection = db['fake_inspection_results']
business_collection = db['fake_yelp_business']

# Retrieve all CAMIS values from fake_inspection_results
inspection_camis = inspection_collection.distinct('CAMIS')

# Find documents in fake_yelp_business where business_id is not in inspection_camis
query = {"business_id": {"$nin": inspection_camis}}

# Count the documents to be deleted
count = business_collection.count_documents(query)
print(f"There are {count} documents to be deleted.")

# Prompt user for confirmation
confirmation = input("Do you want to delete these documents? (y/n): ")

if confirmation.lower() == 'y':
    # Delete documents where business_id is not in inspection_camis
    result = business_collection.delete_many(query)
    print(f"Deleted {result.deleted_count} documents.")
else:
    print("Deletion aborted.")