import psycopg2
import uuid

def get_db_connection():
    try:
        connection = psycopg2.connect(
            host="localhost",
            database="restaurants",
            user="admin", 
            password="pass123",
            port="5432",
            connect_timeout=10
        )
        return connection
    except psycopg2.OperationalError as e:
        print(f"Database connection error: {e}")
        raise

def generate_sql(query):
    q = query.lower()
    
    base_select = "SELECT id, name, online_order, book_table, rate, votes, approx_cost, listed_in_type FROM restaurants"
    
    
    if "cafe" in q or "coffee" in q:
        if "all" in q:
            return f"{base_select} WHERE listed_in_type = 'Cafes' ORDER BY CAST(SUBSTRING(rate, 1, 3) AS FLOAT) DESC"
        else:
            return f"{base_select} WHERE listed_in_type = 'Cafes' ORDER BY CAST(SUBSTRING(rate, 1, 3) AS FLOAT) DESC LIMIT 10"
            
    elif "buffet" in q:
        if "all" in q:
            return f"{base_select} WHERE listed_in_type = 'Buffet' ORDER BY CAST(SUBSTRING(rate, 1, 3) AS FLOAT) DESC"
        else:
            return f"{base_select} WHERE listed_in_type = 'Buffet' ORDER BY CAST(SUBSTRING(rate, 1, 3) AS FLOAT) DESC LIMIT 10"
            
    elif "dining" in q:
        if "all" in q:
            return f"{base_select} WHERE listed_in_type = 'Dining' ORDER BY CAST(SUBSTRING(rate, 1, 3) AS FLOAT) DESC"
        else:
            return f"{base_select} WHERE listed_in_type = 'Dining' ORDER BY CAST(SUBSTRING(rate, 1, 3) AS FLOAT) DESC LIMIT 10"
            
    elif "cheap" in q or "low cost" in q or "budget" in q:
        if "all" in q:
            return f"{base_select} WHERE approx_cost < 400 ORDER BY approx_cost"
        else:
            return f"{base_select} WHERE approx_cost < 400 ORDER BY approx_cost LIMIT 10"
            
    elif "expensive" in q or "costly" in q or "premium" in q:
        if "all" in q:
            return f"{base_select} WHERE approx_cost > 700 ORDER BY approx_cost DESC"
        else:
            return f"{base_select} WHERE approx_cost > 700 ORDER BY approx_cost DESC LIMIT 10"
            
    elif "best" in q or "rating" in q or "top" in q or "highest" in q:
        if "all" in q:
            return f"{base_select} ORDER BY CAST(SUBSTRING(rate, 1, 3) AS FLOAT) DESC"
        else:
            return f"{base_select} ORDER BY CAST(SUBSTRING(rate, 1, 3) AS FLOAT) DESC LIMIT 15"
            
    elif "online" in q or "delivery" in q:
        if "all" in q:
            return f"{base_select} WHERE online_order = 'Yes' ORDER BY CAST(SUBSTRING(rate, 1, 3) AS FLOAT) DESC"
        else:
            return f"{base_select} WHERE online_order = 'Yes' ORDER BY CAST(SUBSTRING(rate, 1, 3) AS FLOAT) DESC LIMIT 10"
            
    elif "booking" in q or "table" in q or "reservation" in q:
        if "all" in q:
            return f"{base_select} WHERE book_table = 'Yes' ORDER BY CAST(SUBSTRING(rate, 1, 3) AS FLOAT) DESC"
        else:
            return f"{base_select} WHERE book_table = 'Yes' ORDER BY CAST(SUBSTRING(rate, 1, 3) AS FLOAT) DESC LIMIT 10"
    
    elif "all" in q or "show" in q:
        return f"{base_select} ORDER BY CAST(SUBSTRING(rate, 1, 3) AS FLOAT) DESC"
    
    else:
        return "NOT_RESTAURANT"

def restaurant_query_function(user_query: str) -> str:
    sql = generate_sql(user_query)
    
    if sql == "NOT_RESTAURANT":
        return "I cannot answer this. Please ask something related to restaurants."
    
    conn = None
    cursor = None
    current_row = None
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        
        if not results:
            response = "No restaurants found matching your criteria."
        else:
            total_count = len(results)
            response = f"🍽️ Found {total_count} restaurants:\n\n"
            
            if total_count <= 20:
                display_results = results
                response += f"Showing all {total_count} results:\n\n"
            elif total_count <= 50:
                display_results = results[:30]
                response += f"Showing first 30 of {total_count} results:\n\n"
            else:
                display_results = results[:50] 
                response += f"Showing first 50 of {total_count} results:\n\n"
            
            for i, row in enumerate(display_results):
                current_row = row
                
                response += f"{i+1}. **{row[1]}**\n"
                response += f"   📊 Rating: {row[4]} ({row[5]} votes)\n"
                response += f"   💰 Cost: ₹{row[6]} for two people\n"
                response += f"   🏷️ Type: {row[7]}\n"
                response += f"   🛒 Online Order: {row[2]}\n"
                response += f"   📅 Table Booking: {row[3]}\n\n"
            
            
            if total_count > len(display_results):
                response += f"... and {total_count - len(display_results)} more restaurants.\n"
                response += f"Try more specific queries like 'all cafes' or 'all buffet restaurants' to see specific types."
        
        return response
        
    except psycopg2.Error as db_error:
        return f"Database error: {str(db_error)}"
    except IndexError as idx_error:
        row_length = len(current_row) if current_row else "unknown"
        return f"Column index error: {str(idx_error)}. Row has {row_length} columns."
    except Exception as e:
        return f"Unexpected error: {str(e)}"
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()