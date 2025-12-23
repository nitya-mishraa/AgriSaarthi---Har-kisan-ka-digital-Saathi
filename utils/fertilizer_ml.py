import os
import joblib
import pandas as pd

BASE_DIR = os.path.dirname(__file__)

model = joblib.load(os.path.join(BASE_DIR, "fertilizer_model.pkl"))
crop_encoder = joblib.load(os.path.join(BASE_DIR, "crop_encoder.pkl"))
soil_encoder = joblib.load(os.path.join(BASE_DIR, "soil_encoder.pkl"))
fertilizer_encoder = joblib.load(os.path.join(BASE_DIR, "fertilizer_encoder.pkl"))


def predict_fertilizer_ml(
    temperature, moisture, rainfall, ph,
    nitrogen, phosphorus, potassium, carbon,
    soil, crop
):
    soil_enc = soil_encoder.transform([soil])[0]
    crop_enc = crop_encoder.transform([crop])[0]

    X = pd.DataFrame([[
        temperature, moisture, rainfall, ph,
        nitrogen, phosphorus, potassium, carbon,
        soil_enc, crop_enc
    ]], columns=[
        "Temperature", "Moisture", "Rainfall", "PH",
        "Nitrogen", "Phosphorous", "Potassium", "Carbon",
        "Soil", "Crop"
    ])

    pred = model.predict(X)
    return fertilizer_encoder.inverse_transform(pred)[0]


def get_crop_and_soil_lists():
    return list(crop_encoder.classes_), list(soil_encoder.classes_)
