import mysql.connector

mysql_conn = None

try:
    mysql_conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="my-secret-pw",
        port=3306,
        database="PortfolioPruefung"
    )

    cursor = mysql_conn.cursor()

    # Add new column to yelp_business
    cursor.execute("ALTER TABLE yelp_business ADD COLUMN cuisine_description VARCHAR(255)")

    # Select business_id and cuisine_description from inspection_results
    cursor.execute("SELECT business_id, cuisine_description FROM inspection_results")
    inspection_results = cursor.fetchall()

    # Update yelp_business with cuisine_description in batches
    batch_size = 100  # Adjust batch size as needed
    update_values_list = []
    for business_id, cuisine_description in inspection_results:
        update_values_list.append((cuisine_description, business_id))
        if len(update_values_list) >= batch_size:
            cursor.executemany("""
                UPDATE yelp_business
                SET cuisine_description = %s
                WHERE business_id = %s
            """, update_values_list)
            mysql_conn.commit()
            update_values_list = []

    # Commit any remaining updates
    if update_values_list:
        cursor.executemany("""
            UPDATE yelp_business
            SET cuisine_description = %s
            WHERE business_id = %s
        """, update_values_list)
        mysql_conn.commit()

    # Delete cuisine_description column from inspection_results
    cursor.execute("ALTER TABLE inspection_results DROP COLUMN cuisine_description")

    # Commit the changes
    mysql_conn.commit()

except mysql.connector.Error as err:
    print(f"Error: {err}")
finally:
    if mysql_conn is not None and mysql_conn.is_connected():
        cursor.close()
        mysql_conn.close()