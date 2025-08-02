#importing all necessary libraries
import mysql.connector
import pandas as pd;

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "ABCD@29",
    "database": "avdevs_DB"
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

def get_all_customers():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM customers")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

def get_customer_transactions(customer_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM transactions WHERE customer_id=%s", (customer_id,))
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

def insert_transaction(customer_id, amount):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO transactions (customer_id, amount) VALUES (%s, %s)",(customer_id, amount))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Transaction added successfully"}

def get_top_spenders():
    conn = get_connection()
    data = pd.read_sql("SELECT c.name, SUM(t.amount) as total_spent "
                     "FROM customers c JOIN transactions t ON c.id = t.customer_id "
                     "GROUP BY c.id ORDER BY total_spent DESC", conn)
    conn.close()
    return df.head(2).to_dict(orient="records")

def download_report_csv():
    conn = get_connection()
    data = pd.read_sql("SELECT * FROM transactions", conn)
    conn.close()
    return df.to_csv(index=False)