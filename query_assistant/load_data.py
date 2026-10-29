import pandas as pd
import psycopg2
import sys
from pathlib import Path

def load_zomato_data():
    try:
        csv_file = "Zomato-data.csv"
        if not Path(csv_file).exists():
            print(f"Error: {csv_file} not found in current directory")
            return False
        
        df = pd.read_csv(csv_file)
        print(f"Found {len(df)} restaurants in CSV")
        
        print("Connecting to PostgreSQL database...")
        conn = psycopg2.connect(
            host="localhost", 
            database="restaurants",
            user="admin", 
            password="pass123",
            port="5432"
        )
        cursor = conn.cursor()
        print("Database connection successful")
        
        print("Clearing existing restaurant data...")
        cursor.execute("DELETE FROM restaurants WHERE id > 0")
        deleted_count = cursor.rowcount
        print(f"Cleared {deleted_count} existing records")
        
        print("Inserting restaurant data...")
        success_count = 0
        
        for index, row in df.iterrows():
            try:
                cursor.execute("""
                    INSERT INTO restaurants (name, online_order, book_table, rate, votes, approx_cost, listed_in_type)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (
                    str(row['name']),
                    str(row['online_order']),
                    str(row['book_table']),
                    str(row['rate']),
                    int(row['votes']) if pd.notna(row['votes']) else 0,
                    int(row['approx_cost(for two people)']) if pd.notna(row['approx_cost(for two people)']) else 0,
                    str(row['listed_in(type)'])
                ))
                success_count += 1
                
                if success_count % 50 == 0:
                    print(f"Inserted {success_count} records...")
                    
            except Exception as row_error:
                print(f"Error inserting row {index}: {row_error}")
                continue
        
        conn.commit()
        
        cursor.execute("SELECT COUNT(*) FROM restaurants")
        result = cursor.fetchone()
        final_count = result[0] if result else 0
        
        cursor.close()
        conn.close()
        
        print(f"Successfully loaded {success_count} restaurants!")
        print(f"Total in database: {final_count} restaurants")
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    load_zomato_data()
