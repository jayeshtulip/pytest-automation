import pytest
import psycopg2
from nmap_ip_validation import create_assets_table, insert_asset_data, get_asset_ip_addresses, scan_network_devices, compare_results_with_database

# Replace these values with your PostgreSQL database credentials
DB_USER = 'postgres'
DB_PASSWORD = 'Testing123'
DB_HOST = 'database-1.cla4wo0qc30y.eu-north-1.rds.amazonaws.com'
DB_PORT = '5432'


# Test fixtures
@pytest.fixture
def database_connection():
    connection = psycopg2.connect(
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    yield connection
    connection.close()

# Test cases
def test_create_assets_table(database_connection):
    create_assets_table(database_connection)

    # Check if the table exists in the database
    with database_connection.cursor() as cursor:
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_name = 'assets'")
        assert cursor.fetchone() is not None, "Table 'assets' not found in the database."

def test_insert_asset_data(database_connection):
    # Insert sample data into the "assets" table
    insert_asset_data(database_connection, "00:11:22:33:44:55", "192.168.1.1", "VendorA")

    # Check if the data is inserted correctly
    with database_connection.cursor() as cursor:
        cursor.execute("SELECT * FROM assets WHERE mac_address = '00:11:22:33:44:55'")
        assert cursor.fetchone() is not None, "Data not inserted into 'assets' table."

def test_get_asset_ip_addresses(database_connection):
    # Assuming you have some sample data in the "assets" table
    ip_addresses = get_asset_ip_addresses(database_connection)

    # Check if the retrieved IP addresses match expectations
    assert len(ip_addresses) > 0, "No IP addresses retrieved from 'assets' table."

def test_scan_network_devices(database_connection):
    # Assuming you have some sample data in the "assets" table
    ip_addresses = get_asset_ip_addresses(database_connection)
    results = scan_network_devices(ip_addresses)

    # Check if the results obtained from the network scanning are not empty
    assert len(results) > 0, "No results obtained from network scanning."

def test_compare_results_with_database(database_connection):
    # Assuming you have some sample data in the "assets" table
    ip_addresses = get_asset_ip_addresses(database_connection)
    results = scan_network_devices(ip_addresses)

    # Compare results and check if any differences are found
    compare_results_with_database(results, database_connection)
    # You can add more specific assertions based on your comparison logic

