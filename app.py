from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL config
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Shaikshawali@2321#'
app.config['MYSQL_DB'] = 'smart_city'

# File upload config
app.config['UPLOAD_FOLDER'] = 'static/uploads'

mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('login.html')  # Start with user login

# More routes coming next...

from werkzeug.security import generate_password_hash, check_password_hash

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, password))
        mysql.connection.commit()
        cur.close()
        flash("Registered successfully! Please log in.", "success")
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cur.fetchone()
        cur.close()

        if user and check_password_hash(user[3], password):  # user[3] = password hash
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


from werkzeug.utils import secure_filename

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

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO complaints (user_id, address, description, image_path) VALUES (%s, %s, %s, %s)",
                    (session['user_id'], address, description, filename))
        mysql.connection.commit()
        cur.close()

        flash("Complaint submitted successfully!", "success")
        return redirect(url_for('user_dashboard'))

    return render_template('complaint_form.html')


@app.route('/my-complaints')
def my_complaints():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()
    cur.execute("SELECT address, description, image_path, status, submitted_at FROM complaints WHERE user_id = %s ORDER BY submitted_at DESC", (session['user_id'],))
    complaints = cur.fetchall()
    cur.close()

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

        # Hardcoded admin credentials
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

    cur = mysql.connection.cursor()

    # Handle complaint status update
    if request.method == 'POST':
        complaint_id = request.form['complaint_id']
        new_status = request.form['status']
        cur.execute("UPDATE complaints SET status = %s WHERE id = %s", (new_status, complaint_id))
        mysql.connection.commit()
        flash("Complaint status updated!", "success")

    # Fetch all complaints
    cur.execute("""
        SELECT complaints.id, users.name, complaints.address, complaints.description,
               complaints.image_path, complaints.status, complaints.submitted_at
        FROM complaints
        JOIN users ON complaints.user_id = users.id
        ORDER BY complaints.submitted_at DESC
    """)
    complaints = cur.fetchall()

    # Calculate complaint statistics
    cur.execute("SELECT COUNT(*) FROM complaints")
    total_complaints = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM complaints WHERE status = 'pending'")
    pending_complaints = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM complaints WHERE status = 'resolved'")
    resolved_complaints = cur.fetchone()[0]

    cur.close()

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

    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT complaints.id, users.name, complaints.address, complaints.description,
               complaints.image_path, complaints.status, complaints.submitted_at
        FROM complaints
        JOIN users ON complaints.user_id = users.id
        ORDER BY complaints.submitted_at DESC
    """)
    complaints = cur.fetchall()
    cur.close()

    return render_template('admin_complaints.html', complaints=complaints)


@app.route('/admin/view_complaints')
def view_complaints():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    complaints = Complaint.query.all()
    return render_template('complaints_view.html', complaints=complaints)


@app.route('/admin/logout', methods=['POST'])
def admin_logout():
    session.pop('admin_id', None)
    return redirect(url_for('login'))  # redirect to user login page



if __name__ == '__main__':
    app.run(debug=True)

