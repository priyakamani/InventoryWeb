from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)


# Function to connect to the SQLite database
def connect_db():
    return sqlite3.connect('ims.db')


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
            query += " AND BD.BALE_NO LIKE ?"
            params.append(f"%{bale_no}%")
        if item_name:
            query += " AND ID.ITEM_NAME LIKE ?"
            params.append(f"%{item_name}%")
        if design:
            query += " AND ID.DESIGN LIKE ?"
            params.append(f"%{design}%")
        if color:
            query += " AND ID.COLOR LIKE ?"
            params.append(f"%{color}%")
        if status_loose == 'LOOSE':
            query += " AND ID.STATUS_LOOSE = 'LOOSE'"
        elif status_loose == 'PACKED':
            query += " AND ID.STATUS_LOOSE IS NULL"

        conn = connect_db()
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
