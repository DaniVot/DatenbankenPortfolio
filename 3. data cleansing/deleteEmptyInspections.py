from pymongo import MongoClient

# Replace the uri string with your MongoDB deployment's connection string.
client = MongoClient('mongodb://localhost:27017/')
db = client['NYAnalyse']

# Replace 'your_collection' with the name of your collection
collection = db['fake_inspection_results']

# Count documents where INSPECTION DATE is "01.01.1900"
count = collection.count_documents({"INSPECTION DATE": "01/01/1900"})
print(f"There are {count} documents to be deleted.")

# Prompt user for confirmation
confirmation = input("Do you want to delete these documents? (y/n): ")

if confirmation.lower() == 'y':
    # Delete documents where INSPECTION DATE is "01.01.1900"
    result = collection.delete_many({"INSPECTION DATE": "01/01/1900"})
    print(f"Deleted {result.deleted_count} documents.")
else:
    print("Deletion aborted.")