import pymongo
import mysql.connector
from mysql.connector import Error

# MongoDB connection
mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
mongo_db = mongo_client["PortfolioPruefung"]

# MySQL connection
try:
    mysql_conn = mysql.connector.connect(
        host='localhost',
        database='PortfolioPruefung',
        user='root',
        password='my-secret-pw'
    )
    if mysql_conn.is_connected():
        cursor = mysql_conn.cursor()

        # Create yelp_data table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS yelp_data (
                object_id INT AUTO_INCREMENT PRIMARY KEY,
                business_id VARCHAR(255) UNIQUE NOT NULL,
                name VARCHAR(255),
                address VARCHAR(255),
                postal_code VARCHAR(10),
                borough VARCHAR(50),
                latitude DECIMAL(10, 8),
                longitude DECIMAL(11, 8),
                phone VARCHAR(15),
                stars DECIMAL(2, 1),
                reviews INT,
                cuisine_description TEXT
            )
        """)

        # Create inspection_results table if it doesn't exist
        cursor.execute("""
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
                community_board INT,
                council_district INT,
                census_tract INT,
                bin VARCHAR(20),
                bbl VARCHAR(20),
                nta VARCHAR(50),
                FOREIGN KEY (business_id) REFERENCES yelp_data(business_id)
                    ON DELETE CASCADE
            )
        """)

        # Fetch data from MongoDB
        yelp_businesses = mongo_db["fake_yelp_business"].find()
        inspection_results = mongo_db["fake_inspection_results"].find()

        # Create a dictionary to map business_id to cuisine_description
        cuisine_map = {inspection['CAMIS']: inspection.get('CUISINE DESCRIPTION', '') for inspection in inspection_results}

        # Insert data into yelp_data table
        for business in yelp_businesses:
            business_id = business.get('business_id')
            cuisine_description = cuisine_map.get(business_id, '')

            print(f"Inserting business: {business_id}, cuisine_description length: {len(cuisine_description)}")
            print(f"Inserting business: {business_id}, cuisine_description: {cuisine_description}")
            cursor.execute("""
                INSERT INTO yelp_data (business_id, name, address, postal_code, borough, latitude, longitude, phone, stars, reviews, cuisine_description)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                name=VALUES(name), address=VALUES(address), postal_code=VALUES(postal_code), borough=VALUES(borough),
                latitude=VALUES(latitude), longitude=VALUES(longitude), phone=VALUES(phone), stars=VALUES(stars),
                reviews=VALUES(reviews), cuisine_description=VALUES(cuisine_description)
            """, (
                business_id,
                business.get('name'),
                business.get('address'),
                business.get('postal_code'),
                business.get('city'),
                business.get('latitude'),
                business.get('longitude'),
                business.get('phone'),
                business.get('stars'),
                business.get('review_count'),
                cuisine_description
            ))

        # Insert data into inspection_results table
        for inspection in inspection_results:
            cursor.execute("""
                INSERT INTO inspection_results (business_id, inspection_date, action, violation_code, violation_description, critical_flag, score, grade, inspection_type, community_board, council_district, census_tract, bin, bbl, nta)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                inspection.get('CAMIS'),
                inspection.get('INSPECTION DATE'),
                inspection.get('ACTION'),
                inspection.get('VIOLATION CODE'),
                inspection.get('VIOLATION DESCRIPTION'),
                inspection.get('CRITICAL FLAG'),
                inspection.get('SCORE'),
                inspection.get('GRADE'),
                inspection.get('INSPECTION TYPE'),
                inspection.get('Community Board'),
                inspection.get('Council District'),
                inspection.get('Census Tract'),
                inspection.get('BIN'),
                inspection.get('BBL'),
                inspection.get('NTA')
            ))

        # Commit the transaction
        mysql_conn.commit()

except Error as e:
    print(f"Error: {e}")
finally:
    if mysql_conn.is_connected():
        cursor.close()
        mysql_conn.close()
    mongo_client.close()