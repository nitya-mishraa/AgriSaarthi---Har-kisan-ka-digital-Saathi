import os
import base64
import json
import random
import numpy as np

# Mock models for demonstration
# In a production environment, these would be trained ML models

# Crop recommendation model
def predict_crop(nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall):
    """
    Predict the best crop based on soil and climate parameters.
    
    Args:
        nitrogen (float): Nitrogen content in soil (mg/kg)
        phosphorus (float): Phosphorus content in soil (mg/kg)
        potassium (float): Potassium content in soil (mg/kg)
        temperature (float): Temperature in Celsius
        humidity (float): Humidity (percentage)
        ph (float): pH value of soil
        rainfall (float): Rainfall in mm
        
    Returns:
        str: Recommended crop
    """
    # Simplified logic for crop recommendation
    # In a real implementation, this would use a trained ML model
    
    # Check pH range first
    if ph < 5.5:
        # Acidic soil crops
        if rainfall > 200 and temperature > 25:
            return "Rice"
        elif temperature < 20:
            return "Tea"
        else:
            return "Sweet Potato"
    elif ph > 7.5:
        # Alkaline soil crops
        if temperature > 25 and rainfall < 100:
            return "Cotton"
        elif nitrogen > 40 and phosphorus > 40:
            return "Chickpea"
        else:
            return "Barley"
    else:
        # Neutral pH
        if nitrogen > 80 and phosphorus > 40 and potassium > 40:
            if temperature > 30 and humidity > 80:
                return "Sugarcane"
            elif temperature > 25 and rainfall > 200:
                return "Maize"
            else:
                return "Wheat"
        elif nitrogen < 40:
            return "Millet"
        else:
            if temperature > 30 and rainfall < 100:
                return "Mustard"
            else:
                return "Soybean"

# Plant disease detection model
def detect_disease(image_base64):
    """
    Detect plant disease from an image.
    
    Args:
        image_base64 (str): Base64 encoded image
        
    Returns:
        tuple: (disease_name, disease_cause, treatment)
    """
    try:
        # In a real application, this would use a trained ML model
        # Here we're using a simplified demo version
        import random
        
        # Common plant diseases for demonstration
        diseases = [
            {
                "name": "Late Blight",
                "cause": "Caused by the fungus Phytophthora infestans. Spreads rapidly in cool, wet weather with temperatures between 10-24°C.",
                "treatment": "Use fungicides containing copper or chlorothalonil. Remove and destroy infected plants. Ensure proper spacing for air circulation. Plant resistant varieties."
            },
            {
                "name": "Powdery Mildew",
                "cause": "Caused by various fungi species. Thrives in humid conditions with moderate temperatures. Poor air circulation contributes to its spread.",
                "treatment": "Apply sulfur-based fungicides or neem oil. Increase plant spacing for better air circulation. Remove and destroy affected leaves. Use resistant varieties when possible."
            },
            {
                "name": "Early Blight",
                "cause": "Caused by the fungus Alternaria solani. Favored by warm, humid conditions and extended periods of leaf wetness.",
                "treatment": "Apply copper-based fungicides. Practice crop rotation. Remove and destroy infected plants. Maintain proper plant spacing and avoid overhead watering."
            },
            {
                "name": "Bacterial Leaf Spot",
                "cause": "Caused by various bacteria species. Spread through water splashing, contaminated tools, and infected seeds. Common in warm, wet conditions.",
                "treatment": "Apply copper-based bactericides. Avoid overhead irrigation. Remove infected plants. Sanitize garden tools. Use disease-free seeds or transplants."
            },
            {
                "name": "Leaf Rust",
                "cause": "Caused by fungi in the Puccinia genus. Spores spread easily by wind. Development is favored by high humidity and moderate temperatures.",
                "treatment": "Apply fungicides with active ingredients like tebuconazole or propiconazole. Remove infected plant material. Increase air circulation. Plant resistant varieties."
            }
        ]
        
        # Simulate disease detection with a random selection
        # In a real app, this would analyze the image using computer vision
        disease = random.choice(diseases)
        return disease["name"], disease["cause"], disease["treatment"]
        
    except Exception as e:
        return f"Error in disease detection: {str(e)}", "", ""
