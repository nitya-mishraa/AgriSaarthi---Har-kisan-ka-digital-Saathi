import os
import logging
import base64

from flask import (
    Flask, render_template, request,
    redirect, url_for, flash, session
)
from flask_login import (
    LoginManager, login_user,
    logout_user, login_required, current_user
)
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.middleware.proxy_fix import ProxyFix

from extensions import db
from models import (
    User,
    FarmDiary,
    TaskPlanner,
    CropRecommendation,
    FertilizerRecommendation
)

from utils.ml_models import predict_crop, detect_disease
from utils.fertilizer_ml import (
    predict_fertilizer_ml,
    get_crop_and_soil_lists
)
from utils.translate import translate_text, SUPPORTED_LANGUAGES

# ================= LOGGING =================
logging.basicConfig(level=logging.INFO)

# ================= APP =====================
app = Flask(__name__)
app.secret_key = "dev_secret_key"
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# ================= DATABASE =================
DATABASE_URL = os.environ.get("DATABASE_URL")

if not DATABASE_URL:
    DATABASE_URL = "sqlite:///agrisaarthi.db"

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# ================= LOGIN ====================
login_manager = LoginManager(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


with app.app_context():
    db.create_all()

# ================= ROUTES ===================

@app.route("/")
def index():
    return render_template("index.html")


# ---------- AUTH ----------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user = User(
            username=request.form["username"],
            email=request.form["email"],
            password_hash=generate_password_hash(request.form["password"])
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(username=request.form["username"]).first()
        if user and check_password_hash(user.password_hash, request.form["password"]):
            login_user(user)
            return redirect(url_for("index"))
        flash("Invalid credentials")
    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


# ---------- CROP RECOMMENDATION ----------
@app.route("/crop-recommendation", methods=["GET", "POST"])
def crop_recommendation():
    if request.method == "POST":
        try:
            prediction = predict_crop(
                float(request.form["nitrogen"]),
                float(request.form["phosphorus"]),
                float(request.form["potassium"]),
                float(request.form["temperature"]),
                float(request.form["humidity"]),
                float(request.form["ph"]),
                float(request.form["rainfall"])
            )
            return render_template(
                "crop_recommendation.html",
                prediction=prediction
            )
        except Exception as e:
            return render_template(
                "crop_recommendation.html",
                error=str(e)
            )

    return render_template("crop_recommendation.html")


# ---------- FERTILIZER RECOMMENDATION ----------
@app.route("/fertilizer-recommendation", methods=["GET", "POST"])
def fertilizer_recommendation():

    crops, soils = get_crop_and_soil_lists()

    if request.method == "POST":
        try:
            prediction = predict_fertilizer_ml(
                temperature=float(request.form["temperature"]),
                moisture=float(request.form["moisture"]),
                rainfall=float(request.form["rainfall"]),
                ph=float(request.form["ph"]),
                nitrogen=float(request.form["nitrogen"]),
                phosphorus=float(request.form["phosphorus"]),
                potassium=float(request.form["potassium"]),
                carbon=float(request.form["carbon"]),
                soil=request.form["soil"],
                crop=request.form["crop"]
            )

            return render_template(
                "fertilizer_recommendation.html",
                prediction=prediction,
                crops=crops,
                soils=soils
            )

        except Exception as e:
            return render_template(
                "fertilizer_recommendation.html",
                error=str(e),
                crops=crops,
                soils=soils
            )

    return render_template(
        "fertilizer_recommendation.html",
        crops=crops,
        soils=soils
    )


# ---------- DISEASE DETECTION ----------
@app.route("/disease-detection", methods=["GET", "POST"])
def disease_detection():
    if request.method == "POST":
        try:
            if "plant_image" not in request.files:
                return render_template(
                    "disease_detection.html",
                    error="No image uploaded"
                )

            file = request.files["plant_image"]
            if file.filename == "":
                return render_template(
                    "disease_detection.html",
                    error="No file selected"
                )

            image_bytes = file.read()
            image_base64 = base64.b64encode(image_bytes).decode("utf-8")

            disease_name, disease_cause, disease_cure = detect_disease(image_base64)

            return render_template(
                "disease_detection.html",
                result={
                    "disease_name": disease_name,
                    "disease_cause": disease_cause,
                    "disease_cure": disease_cure,
                },
                image=image_base64
            )

        except Exception as e:
            return render_template(
                "disease_detection.html",
                error=str(e)
            )

    return render_template("disease_detection.html")


# ---------- KNOWLEDGE HUB ----------
@app.route("/knowledge-hub")
def knowledge_hub():
    return render_template("knowledge_hub.html")


# ---------- FARM DIARY ----------
@app.route("/farm-diary")
@login_required
def farm_diary():
    return render_template("farm_diary.html")


# ---------- TASK PLANNER ----------
@app.route("/task-planner")
@login_required
def task_planner():
    return render_template("task_planner.html")


# ---------- LANGUAGE ----------
@app.route("/set-language", methods=["POST"])
def set_language():
    session["language"] = request.form.get("language", "en")
    return redirect(request.referrer or url_for("index"))


# ---------- TRANSLATION HELPER ----------
@app.context_processor
def inject_translation():
    def translate(text):
        lang = session.get("language", "en")
        return translate_text(text, lang)

    return {
        "translate": translate,
        "current_language": session.get("language", "en"),
        "SUPPORTED_LANGUAGES": SUPPORTED_LANGUAGES
    }


# ================= RUN ======================
if __name__ == "__main__":
    app.run(debug=True)
