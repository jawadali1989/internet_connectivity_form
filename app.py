from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DATABASE = 'connectivity_form.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS form (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            reg_no TEXT,
            nust_email TEXT,
            full_name TEXT,
            contact_number TEXT,
            program TEXT,
            department TEXT,
            device_name TEXT,
            mac_address TEXT,
            advisor_status TEXT DEFAULT 'Pending',
            it_status TEXT DEFAULT 'Pending'
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('student_form.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = (
        request.form['reg_no'],
        request.form['nust_email'],
        request.form['full_name'],
        request.form['contact_number'],
        request.form['program'],
        request.form['department'],
        request.form['device_name'],
        request.form['mac_address']
    )
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''
        INSERT INTO form (reg_no, nust_email, full_name, contact_number, program, department, device_name, mac_address)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', data)
    conn.commit()
    conn.close()
    return "Form Submitted Successfully!"

@app.route('/advisor')
def advisor_panel():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT * FROM form WHERE advisor_status='Pending'")
    forms = c.fetchall()
    conn.close()
    return render_template('advisor_panel.html', forms=forms)

@app.route('/advisor/update/<int:form_id>/<string:status>')
def advisor_update(form_id, status):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("UPDATE form SET advisor_status=? WHERE id=?", (status, form_id))
    conn.commit()
    conn.close()
    return redirect(url_for('advisor_panel'))

@app.route('/it')
def it_panel():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT * FROM form WHERE advisor_status='Recommended' AND it_status='Pending'")
    forms = c.fetchall()
    conn.close()
    return render_template('it_panel.html', forms=forms)

@app.route('/it/update/<int:form_id>/<string:status>')
def it_update(form_id, status):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("UPDATE form SET it_status=? WHERE id=?", (status, form_id))
    conn.commit()
    conn.close()
    return redirect(url_for('it_panel'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)