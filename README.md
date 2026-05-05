# Full_Stack_Assessment_Task

This project is a **Flask-based backend** developed to integrate with a pre-built Admin UI.
As per the requirement, the frontend (HTML, CSS, JavaScript) was **not modified**, and the backend was designed to work seamlessly with the existing UI.

---

## 🚀 Features

* Admin Login (Session-based authentication)
* Secure password hashing using Bcrypt
* Opportunity Management (Create, Read, Update, Delete)
* Data stored using SQLite database
* Fully compatible with existing Admin UI
* Single Page Application behavior handled by frontend

---

## 🛠️ Tech Stack

* Python
* Flask
* Flask-SQLAlchemy
* Flask-Bcrypt
* Flask-CORS
* SQLite

---

## 📂 Project Structure

```id="d0h4b9"
sky/
│
├── app.py
├── requirements.txt
├── .gitignore
│
├── templates/
│   └── admin.html
│
├── static/
│   ├── css/
│   │   └── admin.css
│   ├── js/
│   │   └── admin.js
│   └── image/
```

---

## ⚙️ Installation & Setup

1. Clone the repository:

```id="qv7m1z"
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

2. Install dependencies:

```id="l0nh2c"
pip install -r requirements.txt
```

3. Run the application:

```id="c5q9af"
python app.py
```

4. Open in browser:

```id="q3mdg7"
http://127.0.0.1:5000/
```

---

## 🔐 Default Login Credentials

```id="r2t8xy"
Email: admin@gmail.com
Password: 12345678
```

---

## 📡 API Endpoints

### Authentication

* POST /api/login
* GET /api/logout

### Opportunities

* GET /api/opportunities
* POST /api/opportunities
* PUT /api/opportunities/<id>
* DELETE /api/opportunities/<id>

---

## ⚠️ Important Notes

* The frontend UI (`admin.html`, CSS, JS) is **used as provided and not modified**, as per assignment requirements.
* The backend is built to match the existing UI functionality.
* SQLite database is used for simplicity.
* Ensure static files are placed correctly for proper UI rendering.

---

## 📌 Future Improvements

* Add Signup & Forgot Password functionality
* Implement JWT authentication
* Use MySQL/PostgreSQL for production
* Deploy on cloud platforms (Render, AWS, etc.)

---

## 👨‍💻 Author

C Parveen


---
