import psycopg2
import subprocess
from psycopg2 import sql


DB_USER = 'postgres'
DB_PASSWORD = 'Testing123'
DB_HOST = 'database-1.cla4wo0qc30y.eu-north-1.rds.amazonaws.com'
DB_PORT = '5432'
#create_assets_table, insert_asset_data, get_asset_ip_addresses, scan_network_devices, compare_results_with_database

def create_assets_table(conn):
    """
    Create the "assets" table in the PostgreSQL database.
    """
    with conn.cursor() as cursor:
        # Define the SQL statement to create the "assets" table
        create_table_query = sql.SQL("""
            CREATE TABLE IF NOT EXISTS assets (
                id SERIAL PRIMARY KEY,
                mac_address VARCHAR(17) NOT NULL,
                ip_address VARCHAR(15) NOT NULL,
                vendor VARCHAR(255) NOT NULL
            )
        """)

        # Execute the SQL statement
        cursor.execute(create_table_query)

        # Commit the changes
        conn.commit()


def insert_asset_data(conn, mac_address, ip_address, vendor):
    """
    Insert sample data into the "assets" table.
    """
    with conn.cursor() as cursor:
        # Define the SQL statement to insert sample data into the "assets" table
        insert_data_query = sql.SQL("""
            INSERT INTO assets (mac_address, ip_address, vendor)
            VALUES 
                ('00:11:22:33:44:55', '192.168.1.1', 'VendorA'),
                ('0a:a6:1d:9b:7c:2c', '13.48.148.117', 'aws')
        """)

        # Execute the SQL statement
        cursor.execute(insert_data_query)

        # Commit the changes
        conn.commit()


def get_asset_ip_addresses(conn):
    """
    Retrieve the asset IP addresses from the "assets" table.
    """
    with conn.cursor() as cursor:
        # Define the SQL statement to retrieve IP addresses
        select_ip_query = "SELECT ip_address FROM assets"

        # Execute the SQL statement
        cursor.execute(select_ip_query)

        # Fetch all rows and extract IP addresses
        ip_addresses = [row[0] for row in cursor.fetchall()]

        return ip_addresses


def scan_network_devices(ip_addresses):
    """
    Scan network devices using nmap based on the provided IP addresses.
    """
    results = {}
    for ip_address in ip_addresses:
        try:
            # Run nmap command to scan the device
            nmap_command = f"nmap -p 1-65535 {ip_address}"
            scan_result = subprocess.check_output(nmap_command, shell=True, text=True)

            # Store the scan result in the dictionary
            results[ip_address] = scan_result

        except subprocess.CalledProcessError as e:
            print(f"Error scanning {ip_address}: {e}")

    return results


def compare_results_with_database(results, conn):
    """
    Compare the nmap scan results with the data stored in the "assets" table.
    """
    with conn.cursor() as cursor:
        for ip_address, scan_result in results.items():
            # Retrieve data from the "assets" table for the current IP address
            select_asset_query = "SELECT * FROM assets WHERE ip_address = %s"
            cursor.execute(select_asset_query, (ip_address,))
            asset_data = cursor.fetchone()

            if asset_data:
                # Compare the scan result with the data stored in the database
                print(f"Comparison for IP address {ip_address}:")
                print("Data from assets table:", asset_data)
                print("Scan result from nmap:", scan_result)
                print("-------------------------")
            else:
                print(f"No data found in the assets table for IP address {ip_address}")


if __name__ == "__main__":
    try:
        # Establish a connection to the PostgreSQL database
        connection = psycopg2.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )

        #create table
        create_assets_table(connection)

        #insret data
        insert_sample_data(connection)

        # Extract asset IP addresses from the "assets" table
        asset_ip_addresses = get_asset_ip_addresses(connection)

        # Scan network devices using nmap based on the retrieved IP addresses
        nmap_results = scan_network_devices(asset_ip_addresses)

        # Compare nmap results with data stored in the "assets" table
        compare_results_with_database(nmap_results, connection)

        # Close the database connection
        connection.close()

    except Exception as e:
        print(f"Error: {e}")

