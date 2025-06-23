import mysql.connector
from settings import DATABASE_CONFIG

def migrate():
    # Read and split SQL statements
    with open('./create.sql', 'r', encoding='utf-8') as f:
        sql_content = f.read()
    statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]

    # Connect and execute
    conn = mysql.connector.connect(**DATABASE_CONFIG)
    cursor = conn.cursor()
    try:
        for stmt in statements:
            try:
                cursor.execute(stmt)
            except Exception as e:
                print(f"[ERROR] Failed to execute statement: {stmt}\nError: {e}")
                conn.rollback()
                continue
        conn.commit()
    finally:
        cursor.close()
        conn.close()
        
if __name__ == "__main__":
    migrate()
    print("[INFO] Migration completed successfully!")