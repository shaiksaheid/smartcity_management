from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import psycopg2
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this in production

# PostgreSQL Config
DB_HOST = 'dpg-cvrlc021i9vc739hvj00-a.postgresql.render.com'
DB_NAME = 'smartcity_db'
DB_USER = 'smartcity_db_user'
DB_PASS = 'YtEz5JKRBBDVwlebCbVnV2PHXJ3lBWGj'

# File upload config
app.config['UPLOAD_FOLDER'] = 'static/uploads'

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, password))
        conn.commit()
        cur.close()
        conn.close()

        flash("Registered successfully! Please log in.", "success")
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user and check_password_hash(user[3], password):  # user[3] is hashed password
            session['user_id'] = user[0]
            session['user_name'] = user[1]
            flash("Logged in successfully!", "success")
            return redirect(url_for('user_dashboard'))
        else:
            flash("Invalid credentials. Please try again.", "danger")
    return render_template('login.html')

@app.route('/dashboard')
def user_dashboard():
    if 'user_id' in session:
        return render_template('dashboard.html', name=session['user_name'])
    return redirect(url_for('login'))

@app.route('/submit-complaint', methods=['GET', 'POST'])
def submit_complaint():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        address = request.form['address']
        description = request.form['description']
        image = request.files['image']

        filename = secure_filename(image.filename)
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO complaints (user_id, address, description, image_path) VALUES (%s, %s, %s, %s)",
                    (session['user_id'], address, description, filename))
        conn.commit()
        cur.close()
        conn.close()

        flash("Complaint submitted successfully!", "success")
        return redirect(url_for('user_dashboard'))

    return render_template('complaint_form.html')

@app.route('/my-complaints')
def my_complaints():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT address, description, image_path, status, submitted_at FROM complaints WHERE user_id = %s ORDER BY submitted_at DESC", (session['user_id'],))
    complaints = cur.fetchall()
    cur.close()
    conn.close()

    return render_template('complaints_view.html', complaints=complaints)

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('login'))

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == 'admin@smartcity.com' and password == 'admin123':
            session['admin_id'] = 1
            session['admin_name'] = 'Admin'
            return redirect(url_for('admin_dashboard'))
        else:
            flash("Invalid credentials", "danger")

    return render_template('admin_login.html')

@app.route('/admin/dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    if 'admin_id' not in session:
        return redirect(url_for('admin_login'))

    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == 'POST':
        complaint_id = request.form['complaint_id']
        new_status = request.form['status']
        cur.execute("UPDATE complaints SET status = %s WHERE id = %s", (new_status, complaint_id))
        conn.commit()
        flash("Complaint status updated!", "success")

    cur.execute("""
        SELECT complaints.id, users.name, complaints.address, complaints.description,
               complaints.image_path, complaints.status, complaints.submitted_at
        FROM complaints
        JOIN users ON complaints.user_id = users.id
        ORDER BY complaints.submitted_at DESC
    """)
    complaints = cur.fetchall()

    cur.execute("SELECT COUNT(*) FROM complaints")
    total_complaints = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM complaints WHERE status = 'pending'")
    pending_complaints = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM complaints WHERE status = 'resolved'")
    resolved_complaints = cur.fetchone()[0]

    cur.close()
    conn.close()

    return render_template(
        'admin_dashboard.html',
        complaints=complaints,
        total_complaints=total_complaints,
        pending_complaints=pending_complaints,
        resolved_complaints=resolved_complaints
    )

@app.route('/admin/complaints')
def admin_complaints():
    if 'admin_id' not in session:
        return redirect(url_for('admin_login'))

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT complaints.id, users.name, complaints.address, complaints.description,
               complaints.image_path, complaints.status, complaints.submitted_at
        FROM complaints
        JOIN users ON complaints.user_id = users.id
        ORDER BY complaints.submitted_at DESC
    """)
    complaints = cur.fetchall()
    cur.close()
    conn.close()

    return render_template('admin_complaints.html', complaints=complaints)

@app.route('/admin/logout', methods=['POST'])
def admin_logout():
    session.pop('admin_id', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
