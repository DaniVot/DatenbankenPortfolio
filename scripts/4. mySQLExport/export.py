from pymongo import MongoClient
import mysql.connector
from mysql.connector import Error
from datetime import datetime

# MongoDB Connection
mongo_client = MongoClient("mongodb://localhost:27017/")
mongo_db = mongo_client["PortfolioPruefung"]
inspection_collection = mongo_db["fake_inspection_results"]
yelp_collection = mongo_db["fake_yelp_business"]
# Debug statement
print("Connected to MongoDB")

# MySQL Connection
try:
    mysql_conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="my-secret-pw",
        port=3306
    )
    print("Connected to MySQL")
    mysql_cursor = mysql_conn.cursor()
    mysql_cursor.execute("CREATE DATABASE IF NOT EXISTS PortfolioPruefung")
    mysql_cursor.execute("USE PortfolioPruefung")
except Error as e:
    print(f"Error connecting to MySQL: {e}")
    exit()

# Create Tables
yelp_table_query = """
CREATE TABLE IF NOT EXISTS yelp_business (
    object_id INT AUTO_INCREMENT PRIMARY KEY,
    business_id VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    address VARCHAR(255),
    postal_code VARCHAR(10),
    borough VARCHAR(50),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    stars DECIMAL(2, 1),
    reviews INT,
    cuisine_description VARCHAR(255)
);
"""
print("yelp_business created")

inspection_table_query = """
CREATE TABLE IF NOT EXISTS inspection_results (
    inspection_id INT AUTO_INCREMENT PRIMARY KEY,
    business_id VARCHAR(255) NOT NULL,
    inspection_date DATE NOT NULL,
    action VARCHAR(255),
    violation_code VARCHAR(10),
    violation_description TEXT,
    critical_flag VARCHAR(50),
    score INT,
    grade CHAR(1),
    inspection_type VARCHAR(255),
    FOREIGN KEY (business_id) REFERENCES yelp_business(business_id) ON DELETE CASCADE
);
"""
print("inspection_results created")

mysql_cursor.execute(yelp_table_query)
mysql_cursor.execute(inspection_table_query)

# Transfer Data from MongoDB to MySQL
def transfer_data():
    print("Transferring data...")
    yelp_docs = list(yelp_collection.find())
    inspection_docs = list(inspection_collection.find())

    # Insert Yelp data
    for doc in yelp_docs:
        business_id = doc["business_id"]
        cuisine_description = None  # Placeholder to be updated by inspection data
        insert_query = """
        INSERT INTO yelp_business (business_id, name, address, postal_code, latitude, longitude, stars, reviews, cuisine_description)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE cuisine_description = VALUES(cuisine_description);
        """
        values = (
            business_id,
            doc.get("name"),
            doc.get("address"),
            doc.get("postal_code"),
            float(doc.get("latitude") or 0.0),  # Handle None values
            float(doc.get("longitude") or 0.0),  # Handle None values
            float(doc.get("stars") or 0.0),  # Handle None values
            int(doc.get("review_count") or 0),  # Handle None values
            cuisine_description
        )
        mysql_cursor.execute(insert_query, values)

    # Insert Inspection data and update Yelp cuisine_description
    for doc in inspection_docs:
        business_id = doc["CAMIS"]
        cuisine_description = doc.get("CUISINE DESCRIPTION")
        inspection_date = datetime.strptime(doc["INSPECTION DATE"], "%m/%d/%Y").date()
        
        # Check if business_id exists in yelp_business
        mysql_cursor.execute("SELECT COUNT(*) FROM yelp_business WHERE business_id = %s", (business_id,))
        if mysql_cursor.fetchone()[0] == 0:
            print(f"Skipping inspection with business_id {business_id} as it does not exist in yelp_business")
            continue

        insert_inspection_query = """
        INSERT INTO inspection_results (
            business_id, inspection_date, action, violation_code, violation_description, critical_flag, score, grade,
            inspection_type
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        inspection_values = (
            business_id,
            inspection_date,
            doc.get("ACTION"),
            doc.get("VIOLATION CODE"),
            doc.get("VIOLATION DESCRIPTION"),
            doc.get("CRITICAL FLAG"),
            int(doc.get("SCORE", 0)),  # Convert to int
            doc.get("GRADE"),
            doc.get("INSPECTION TYPE"),
        )
        
        # Ensure all values are of the correct type
        inspection_values = tuple(
            int(value) if isinstance(value, (int, float)) else value
            for value in inspection_values
        )
        
        mysql_cursor.execute(insert_inspection_query, inspection_values)

    mysql_conn.commit()
    print("Data transfer complete.")

# Call the transfer_data function
transfer_data()

# Close connections
mysql_cursor.close()
mysql_conn.close()
mongo_client.close()