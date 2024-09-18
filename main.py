from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)

# MySQL database configuration
db_config = {
    'host': "sql12.freemysqlhosting.net",
    'user': 'sql12731859',
    'password': 'n8uA3aJCCQ',
    'database': 'sql12731859',
    'port':'3306'
}

db_config = {
    'host': 'sql12.freemysqlhosting.net',  # e.g., 'localhost' or a remote host
    'user': 'sql12731859',  # e.g., 'root'
    'password': 'n8uA3aJCCQ',  # Your MySQL password
    'database': 'sql12731859',
    'port': '3306'# Your MySQL database name
}
@app.route('/check_db')
def check_db_connection():
    try:
        # Try connecting to the MySQL database
        conn = mysql.connector.connect(**db_config)

        # If the connection is successful
        if conn.is_connected():
            conn.close()
            return jsonify({'status': 'success', 'message': 'Database connection successful!'}), 200
        else:
            return jsonify({'status': 'error', 'message': 'Failed to connect to the database.'}), 500
    except mysql.connector.Error as err:
        # Catch and return any error that occurs
        return jsonify({'status': 'error', 'message': str(err)}), 500


if __name__ == '__main__':
    app.run(debug=True)
