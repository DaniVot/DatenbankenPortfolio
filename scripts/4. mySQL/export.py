import mysql.connector
from pymongo import MongoClient
from datetime import datetime

# MongoDB Connection
mongo_client = MongoClient("mongodb://localhost:27017/")
mongo_db = mongo_client["PortfolioPruefung"]
inspection_collection = mongo_db["fake_inspection_results"]
yelp_collection = mongo_db["fake_yelp_business"]

# MySQL Connection
try:
    mysql_conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="my-secret-pw",
        port=3306,
    )
    mysql_cursor = mysql_conn.cursor()

    # Create Database and Tables
    mysql_cursor.execute("CREATE DATABASE IF NOT EXISTS PortfolioPruefung")
    mysql_cursor.execute("USE PortfolioPruefung")

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
        reviews INT
    );
    """
    mysql_cursor.execute(yelp_table_query)
    print("yelp_business table created")

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
        cuisine_description VARCHAR(255),
        FOREIGN KEY (business_id) REFERENCES yelp_business(business_id) ON DELETE CASCADE
    );
    """
    mysql_cursor.execute(inspection_table_query)
    print("inspection_results table created")

    # Extract data from MongoDB and insert into MySQL
    batch_size = 100  # Adjust batch size as needed

    # Define the Yelp insert query
    yelp_insert_query = """
    INSERT INTO yelp_business (
        business_id, name, address, postal_code, borough, latitude, longitude, stars, reviews
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

# Extract data from MongoDB and insert into MySQL
    print("Transferring data from MongoDB to MySQL...")
    yelp_data = yelp_collection.find()
    yelp_values_list = []
    for yelp in yelp_data:
        yelp_values = (
            yelp.get("business_id"),
            yelp.get("name"),
            yelp.get("address"),
            yelp.get("postal_code"),
            yelp.get("city"),
            yelp.get("latitude"),
            yelp.get("longitude"),
            yelp.get("stars"),
            yelp.get("review_count")
        )
        yelp_values_list.append(yelp_values)
        if len(yelp_values_list) >= batch_size:
            mysql_cursor.executemany(yelp_insert_query, yelp_values_list)
            mysql_conn.commit()
            yelp_values_list = []
    if yelp_values_list:
        mysql_cursor.executemany(yelp_insert_query, yelp_values_list)
        mysql_conn.commit()
    print(f"Inserted Yelp business records")


    # Define the inspection insert query
    inspection_insert_query = """
    INSERT INTO inspection_results (
        business_id, inspection_date, action, violation_code, violation_description, 
        critical_flag, score, grade, inspection_type, cuisine_description
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    # Collect inspection values
    inspection_values_list = []
    inspection_data = inspection_collection.find()
    for inspection in inspection_data:
        # Convert date format from MM/DD/YYYY to YYYY-MM-DD
        inspection_date = datetime.strptime(inspection.get("INSPECTION DATE"), '%m/%d/%Y').strftime('%Y-%m-%d')
        
        inspection_values = (
            inspection.get("CAMIS"),
            inspection_date,
            inspection.get("ACTION"),
            inspection.get("VIOLATION CODE"),
            inspection.get("VIOLATION DESCRIPTION"),
            inspection.get("CRITICAL FLAG"),
            inspection.get("SCORE"),
            inspection.get("GRADE"),
            inspection.get("INSPECTION TYPE"),
            inspection.get("CUISINE DESCRIPTION")
        )
        inspection_values_list.append(inspection_values)
        if len(inspection_values_list) >= batch_size:
            mysql_cursor.executemany(inspection_insert_query, inspection_values_list)
            mysql_conn.commit()
            inspection_values_list = []
    if inspection_values_list:
        mysql_cursor.executemany(inspection_insert_query, inspection_values_list)
        mysql_conn.commit()
    print(f"Inserted inspection result records")

    print("Data transfer complete")

except mysql.connector.Error as err:
    print(f"Error: {err}")
finally:
    if mysql_conn.is_connected():
        mysql_cursor.close()
        mysql_conn.close()
        print("MySQL connection closed")