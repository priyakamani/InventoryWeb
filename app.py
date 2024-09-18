from flask import Flask, render_template, request
import mysql
from mysql.connector import Error

app = Flask(__name__)


# Function to connect to the MySQL database
def connect_db():
    try:
        connection = mysql.connector.connect(
            host='sql12.freemysqlhosting.net',  # e.g., 'localhost'
            database='sql12731859',  # replace with your database name
            user='sql12731859',  # replace with your MySQL username
            password='n8uA3aJCCQ'  # replace with your MySQL password
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None


# Route for the search page
@app.route('/', methods=['GET', 'POST'])
def search():
    results = []
    if request.method == 'POST':
        bale_no = request.form.get('bale_no')
        item_name = request.form.get('item_name')
        design = request.form.get('design')
        color = request.form.get('color')
        status_loose = request.form.get('status_loose')

        query = """
            SELECT BD.SERIAL_NO, BD.BALE_NO, ID.ITEM_NAME, ID.DESIGN, ID.COLOR, ID.STATUS_LOOSE, ID.MTRS
            FROM BALE_DETAILS BD
            JOIN ITEM_DATA ID ON BD.SERIAL_NO = ID.BALE_ID
            WHERE ID.SOLD_KEPT IS NULL
        """
        params = []

        if bale_no:
            query += " AND BD.BALE_NO LIKE %s"
            params.append(f"%{bale_no}%")
        if item_name:
            query += " AND ID.ITEM_NAME LIKE %s"
            params.append(f"%{item_name}%")
        if design:
            query += " AND ID.DESIGN LIKE %s"
            params.append(f"%{design}%")
        if color:
            query += " AND ID.COLOR LIKE %s"
            params.append(f"%{color}%")
        if status_loose == 'LOOSE':
            query += " AND ID.STATUS_LOOSE = 'LOOSE'"
        elif status_loose == 'PACKED':
            query += " AND ID.STATUS_LOOSE IS NULL"

        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            results = cursor.fetchall()
            conn.close()

    # Transform the results to replace NULL with 'PACKED'
    transformed_results = []
    for row in results:
        status = 'PACKED' if row[5] is None else 'LOOSE'
        transformed_results.append(row[:5] + (status, row[6]))

    return render_template('search.html', results=transformed_results)


if __name__ == '__main__':
    app.run(debug=True)
