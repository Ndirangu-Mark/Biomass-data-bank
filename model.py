import psycopg2
from psycopg2 import sql
import pandas as pd

# Database connection parameters
DB_NAME = "Biomassdb"
DB_USER = "postgres"  # Replace with your PostgreSQL username
DB_PASSWORD = "12345678"  # Replace with your PostgreSQL password
DB_HOST = "localhost"
DB_PORT = "5432"
CSV_FILE_PATH = r"D:\Project\modified_ground_data.csv"  # Replace with your CSV file path

# Data to be inserted
data = {
    "project_year": 2024,
    "accuracy": 83,
    "green_space": 0.4308,
    "total_biomass": 49219.26,
    "carbon_quantity": 23133.05
}

image_data = [
    {"image_name": "biomass_map", "image_link": "https://example.com/maps/biomass_map_1.png"},
    {"image_name": "carbon_map", "image_link": "https://example.com/maps/biomass_map_2.png"},
]

try:
    # Step 1: Connect to the 'postgres' database
    conn = psycopg2.connect(
        dbname="postgres",
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    conn.autocommit = True
    cursor = conn.cursor()

    # Step 2: Create the new database
    cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(DB_NAME)))
    print(f"Database {DB_NAME} created successfully.")
    cursor.close()
    conn.close()

    # Step 3: Connect to the new database
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    cursor = conn.cursor()

    # Step 4: Load CSV data into a pandas DataFrame
    df = pd.read_csv(CSV_FILE_PATH, encoding='ISO-8859-1')
    print(f"Loaded {len(df)} records from the CSV file.")

    # Preprocess column names to ensure they are valid for PostgreSQL
    # Replace invalid characters with underscores and convert to lowercase
    df.columns = [
        "".join(c if c.isalnum() or c == "_" else "_" for c in col).lower()
        for col in df.columns
    ]

    # Step 5: Create the field_data table based on the DataFrame columns
    column_definitions = ", ".join([
        f"{col} {('FLOAT' if df[col].dtype in ['float64', 'int64'] else 'VARCHAR(255)')}"
        for col in df.columns
    ])
    create_table_query = f"""
    CREATE TABLE field_data (
        id SERIAL PRIMARY KEY,
        {column_definitions}
    );
    """
    cursor.execute(create_table_query)
    print("Table 'field_data' created successfully.")

    # Step 6: Insert data from the DataFrame into the table
    for _, row in df.iterrows():
        columns = ", ".join(row.index)
        values = ", ".join([f"%s" for _ in row])
        insert_query = f"INSERT INTO field_data ({columns}) VALUES ({values})"
        cursor.execute(insert_query, tuple(row))
    print(f"Inserted {len(df)} records into the 'field_data' table.")

    # Create the table
    create_table_query = """
    CREATE TABLE IF NOT EXISTS project_data (
        id SERIAL PRIMARY KEY,
        project_year INT NOT NULL,
        accuracy FLOAT NOT NULL,
        green_space_km2 FLOAT NOT NULL,
        total_biomass_tonnes FLOAT NOT NULL,
        carbon_quantity_tonnes FLOAT NOT NULL
    );
    """
    cursor.execute(create_table_query)
    print("Table 'project_data' created successfully.")

    # Insert data into the table
    insert_query = """
    INSERT INTO project_data (year, accuracy, green_space, total_biomass, carbon_quantity)
    VALUES (%s, %s, %s, %s, %s);
    """
    cursor.execute(insert_query, (
        data["year"],
        data["accuracy"],
        data["green_space"],
        data["total_biomass"],
        data["carbon_quantity"]
    ))
    print("Data inserted successfully.")

    # Create the table
    create_table_query = """
    CREATE TABLE IF NOT EXISTS map_images (
        id SERIAL PRIMARY KEY,
        image_name VARCHAR(255) NOT NULL,
        image_link TEXT NOT NULL
    );
    """
    cursor.execute(create_table_query)
    print("Table 'map_images' created successfully.")

    # Insert example data into the table
    insert_query = """
    INSERT INTO map_images (image_name, image_link)
    VALUES (%s, %s);
    """
    for image in image_data:
        cursor.execute(insert_query, (image["image_name"], image["image_link"]))
    print(f"{len(image_data)} image records inserted successfully.")

    # Commit changes and close the connection
    conn.commit()
    cursor.close()
    conn.close()
    print("Database setup completed successfully.")

except psycopg2.Error as e:
    print("Error:", e)