from flask import Flask, jsonify
import mysql.connector
import os
from mysql.connector import Error

app = Flask(__name__)

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host='mysql-service',
            port=3306,
            user=os.environ.get('MYSQL_USER', 'user'),
            password=os.environ.get('MYSQL_PASSWORD', 'password'),
            database=os.environ.get('MYSQL_DATABASE', 'myapp')
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

@app.route('/health')
def health():
    try:
        connection = get_db_connection()
        if connection and connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            connection.close()
            return jsonify({
                "status": "healthy",
                "database": "connected",
                "message": "Backend successfully connected to MySQL database!"
            })
        else:
            return jsonify({
                "status": "unhealthy",
                "database": "disconnected",
                "message": "Cannot connect to database"
            }), 500
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/api/data')
def get_data():
    try:
        connection = get_db_connection()
        if connection and connection.is_connected():
            cursor = connection.cursor()
            # Create table if it doesn't exist
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS test_table (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    message VARCHAR(255)
                )
            """)
            
            # Insert sample data
            cursor.execute("INSERT IGNORE INTO test_table (id, message) VALUES (1, 'Hello from Kubernetes!')")
            connection.commit()
            
            # Fetch data
            cursor.execute("SELECT * FROM test_table")
            results = cursor.fetchall()
            connection.close()
            
            return jsonify({
                "data": results,
                "message": "Data retrieved successfully from MySQL"
            })
        else:
            return jsonify({"error": "Database connection failed"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)