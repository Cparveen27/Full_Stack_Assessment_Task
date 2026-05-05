from flask import Flask, request, jsonify, session, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = "secret123"

# Allow frontend to work without modification
CORS(app, supports_credentials=True)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# ================= MODELS =================

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))

class Opportunity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer)
    name = db.Column(db.String(200))
    duration = db.Column(db.String(50))
    start_date = db.Column(db.String(50))
    description = db.Column(db.Text)
    skills = db.Column(db.Text)
    category = db.Column(db.String(50))
    future = db.Column(db.Text)
    applicants = db.Column(db.Integer)

# ================= HELPERS =================

def get_json():
    return request.get_json() if request.is_json else request.form

def auth_user():
    return session.get("user_id")

# ================= PAGE =================

@app.route("/")
def index():
    return render_template("admin.html")

# ================= AUTH =================

@app.route("/api/signup", methods=["POST"])
def signup():
    data = get_json()

    if Admin.query.filter_by(email=data.get("email")).first():
        return jsonify({"success": False, "message": "User exists"})

    hashed = bcrypt.generate_password_hash(data.get("password")).decode("utf-8")

    user = Admin(
        name=data.get("name"),
        email=data.get("email"),
        password=hashed
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({"success": True})


@app.route("/api/login", methods=["POST"])
def login():
    data = get_json()

    user = Admin.query.filter_by(email=data.get("email")).first()

    if not user or not bcrypt.check_password_hash(user.password, data.get("password")):
        return jsonify({"success": False, "message": "Invalid credentials"})

    session["user_id"] = user.id

    return jsonify({
        "success": True,
        "user": {
            "name": user.name,
            "email": user.email
        }
    })


@app.route("/api/logout")
def logout():
    session.clear()
    return jsonify({"success": True})

# ================= OPPORTUNITIES =================

@app.route("/api/opportunities", methods=["GET"])
def get_opportunities():
    user_id = auth_user()

    if not user_id:
        return jsonify({"success": False, "data": []})

    data = Opportunity.query.filter_by(admin_id=user_id).all()

    result = []
    for o in data:
        result.append({
            "id": o.id,
            "name": o.name,
            "duration": o.duration,
            "startDate": o.start_date,
            "description": o.description,
            "skills": o.skills.split(",") if o.skills else [],
            "category": o.category,
            "futureOpportunities": o.future,
            "applicants": o.applicants or 0
        })

    return jsonify({"success": True, "data": result})


@app.route("/api/opportunities", methods=["POST"])
def create_opportunity():
    user_id = auth_user()

    if not user_id:
        return jsonify({"success": False})

    data = get_json()

    opp = Opportunity(
        admin_id=user_id,
        name=data.get("name"),
        duration=data.get("duration"),
        start_date=data.get("startDate"),
        description=data.get("description"),
        skills=",".join(data.get("skills", [])),
        category=data.get("category"),
        future=data.get("futureOpportunities"),
        applicants=data.get("applicants")
    )

    db.session.add(opp)
    db.session.commit()

    return jsonify({"success": True})


@app.route("/api/opportunities/<int:id>", methods=["PUT"])
def update_opportunity(id):
    user_id = auth_user()
    data = get_json()

    opp = Opportunity.query.get(id)

    if not opp or opp.admin_id != user_id:
        return jsonify({"success": False})

    opp.name = data.get("name")
    opp.duration = data.get("duration")
    opp.start_date = data.get("startDate")
    opp.description = data.get("description")
    opp.skills = ",".join(data.get("skills", []))
    opp.category = data.get("category")
    opp.future = data.get("futureOpportunities")
    opp.applicants = data.get("applicants")

    db.session.commit()

    return jsonify({"success": True})


@app.route("/api/opportunities/<int:id>", methods=["DELETE"])
def delete_opportunity(id):
    user_id = auth_user()

    opp = Opportunity.query.get(id)

    if not opp or opp.admin_id != user_id:
        return jsonify({"success": False})

    db.session.delete(opp)
    db.session.commit()

    return jsonify({"success": True})


# ================= RUN =================

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

        # create default user
        if not Admin.query.first():
            admin = Admin(
                name="Admin",
                email="admin@example.com",
                password=bcrypt.generate_password_hash("12345678").decode("utf-8")
            )
            db.session.add(admin)
            db.session.commit()

    app.run(debug=True)