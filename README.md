
# 🌆 Smart City Management System

A full-stack web application that empowers citizens to report civic issues and enables municipal administrators to manage and resolve them efficiently. The system enhances urban governance by improving communication between residents and authorities.

---

## 🧩 Features

- 👥 **User and Admin Authentication**
- 📝 **Complaint Submission** with description, location, and optional image upload
- 📋 **Admin Dashboard** for viewing and updating complaint statuses
- 🔄 **Real-time Complaint Status Tracking**
- 🖼️ **Image Upload Support** for better issue visibility
- 🗄️ **PostgreSQL Integration** for structured and reliable data management
- 📱 **Responsive Design** supporting all device sizes

---

## 🛠️ Tech Stack

| Component    | Technology               |
|--------------|---------------------------|
| Backend      | Python, Flask             |
| Frontend     | HTML, CSS (Flask Templates) |
| Database     | PostgreSQL                |
| ORM          | SQLAlchemy                |
| Auth System  | Flask-Login, Werkzeug     |

---

## 📁 Project Structure

```
smartcity_management/
│
├── static/uploads/              # Uploaded complaint images
├── templates/                   # HTML templates
│   ├── admin_login.html
│   ├── admin_dashboard.html
│   ├── admin_complaints.html
│   ├── dashboard.html
│   ├── complaint_form.html
│   ├── complaints_view.html
│   ├── login.html
│   └── register.html
│
├── app.py                       # Main Flask application
├── requirements.txt             # Python dependencies
├── smart_city_pg.sql            # PostgreSQL schema
├── Procfile                     # (Optional) Deployment config
└── .gitattributes               # Git config
```

---

## ⚙️ Installation Guide

1. **Clone the Repository**
   ```bash
   git clone https://github.com/shaiksaheid/smartcity_management.git
   cd smartcity_management
   ```

2. **Create and Activate Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up PostgreSQL Database**
   - Create a PostgreSQL database
   - Import the schema:
     ```bash
     psql -U yourusername -d yourdbname -f smart_city_pg.sql
     ```
   - Update the database URI in `app.py` accordingly.

5. **Run the Application**
   ```bash
   python app.py
   ```

6. **Access the App**
   Open your browser and visit: [http://localhost:5000](http://localhost:5000)

---

## 🧪 Sample Test Credentials (For Development Only)

- **Admin Login**
  - Username: `admin`
  - Password: `admin123`
- **Regular User**
  - Register via the registration form

---

## 🧠 Future Enhancements

- Push/email notifications on complaint status updates
- Data analytics and reports for authorities
- Geo-mapping integration for visual complaint tracking
- REST API for mobile app support

---

## 📄 License

This project was developed as part of the **Database Management Systems Lab** coursework  
**CMR Technical Campus – Department of CSE (AI & ML)**  
Academic Year: *2024–2025*

---

## 👨‍💻 Author

**Shaik Shaheid**  
GitHub: [@shaiksaheid](https://github.com/shaiksaheid)
