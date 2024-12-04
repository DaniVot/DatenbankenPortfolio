import mysql.connector

# Database connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="my-secret-pw",
    port=3306,
    database="PortfolioPruefung"
)

cursor = conn.cursor()

# Drop views if they already exist
cursor.execute("DROP VIEW IF EXISTS bad_inspections")
cursor.execute("DROP VIEW IF EXISTS ok_inspections")
cursor.execute("DROP VIEW IF EXISTS good_inspections")

# Create views
cursor.execute("""
    CREATE VIEW bad_inspections AS
    SELECT ir.business_id, ir.inspection_date, yb.latitude, yb.longitude
    FROM inspection_results ir
    JOIN yelp_business yb ON ir.business_id = yb.business_id
    WHERE ir.score BETWEEN 0 AND 33
""")

cursor.execute("""
    CREATE VIEW ok_inspections AS
    SELECT ir.business_id, ir.inspection_date, yb.latitude, yb.longitude
    FROM inspection_results ir
    JOIN yelp_business yb ON ir.business_id = yb.business_id
    WHERE ir.score BETWEEN 34 AND 66
""")

cursor.execute("""
    CREATE VIEW good_inspections AS
    SELECT ir.business_id, ir.inspection_date, yb.latitude, yb.longitude
    FROM inspection_results ir
    JOIN yelp_business yb ON ir.business_id = yb.business_id
    WHERE ir.score BETWEEN 67 AND 100
""")

# Commit and close connection
conn.commit()
cursor.close()
conn.close()

print("Views created successfully.")