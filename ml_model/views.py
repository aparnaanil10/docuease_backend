from django.shortcuts import render
import json
import joblib
import os
import numpy as np
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
BASE_DIR= os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH= os.path.join(BASE_DIR, 'ml_model', 'ml_model')

model = joblib.load(os.path.join(MODEL_PATH, 'disease_model.pkl'))
label_encoder = joblib.load(os.path.join(MODEL_PATH, 'label_encoder.pkl'))
symptom_list = joblib.load(os.path.join(MODEL_PATH, 'symptom_list.pkl'))

@csrf_exempt
def predict_disease(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            symptoms = data.get("symptoms", [])
            print("Received symptoms:", symptoms)

            if not symptoms or not isinstance(symptoms, list):
                return JsonResponse({"error": "Symptoms must be a list"}, status=400)

            input_vector = [0] * len(symptom_list)
            for symptom in symptoms:
                if symptom in symptom_list:
                    index = symptom_list.index(symptom)
                    input_vector[index] = 1

            prediction_encoded = model.predict([input_vector])[0]
            prediction_label = label_encoder.inverse_transform([prediction_encoded])[0]

            return JsonResponse({"predicted_disease": prediction_label})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)