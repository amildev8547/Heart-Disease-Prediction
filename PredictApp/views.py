from django.shortcuts import render
from django.http import JsonResponse
import joblib
import os
import numpy as np



MODEL_FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'heart_disease_model.joblib')


# Load the model only once when the module is imported
model = joblib.load(MODEL_FILE_PATH)


def index(request):
    return render(request, 'index.html')

def predict(request):
    if request.method == 'POST':
        input_features = [
            float(request.POST.get('age')),
            float(request.POST.get('sex')),
            float(request.POST.get('cp')),
            float(request.POST.get('trestbps')),
            float(request.POST.get('chol')),
            float(request.POST.get('fbs')),
            float(request.POST.get('restecg')),
            float(request.POST.get('thalach')),
            float(request.POST.get('exang')),
            float(request.POST.get('oldpeak')),
            float(request.POST.get('slope')),
            float(request.POST.get('ca')),
            float(request.POST.get('thal'))
        ]

        # Convert input_features to a NumPy array and reshape it
        input_data = np.array(input_features).reshape(1, -1)

        # Predict using the preloaded model
        prediction = model.predict(input_data)

        result = "The person has Heart Disease" if prediction[0] == 0 else "The person does not have a Heart Disease"

        # Tips and links
        tips_category = 'management_tips' if prediction[0] == 0 else 'prevention_tips'

        tips = {
            "management_tips": [
                "Follow a heart-healthy diet rich in fruits, vegetables, and whole grains.",
                "Engage in regular exercise as recommended by your healthcare provider.",
                "Take prescribed medications as directed by your doctor.",
                "Practice stress-reduction techniques to manage stress levels.",
                "Schedule regular visits with your healthcare provider for monitoring."
            ],
            "prevention_tips": [
                "Maintain a balanced diet with fruits, vegetables, lean proteins, and healthy fats.",
                "Stay physically active to maintain a healthy weight and cardiovascular fitness.",
                "Avoid smoking and seek help to quit if needed.",
                "Limit alcohol consumption to moderate levels.",
                "Practice stress-relief techniques to reduce the impact of stress.",
                "Schedule regular health check-ups for early detection and prevention."
            ]
        }

        youtube_links = {
            "heart_disease_management": "https://www.youtube.com/watch?v=IMBpwpf5crU",
            "heart_disease_prevention": "https://www.youtube.com/watch?v=B6UYNZLpAMs"
        }

        return render(request, 'result.html', {
            'result': result,
            'tips': tips[tips_category],
            'youtube_links': youtube_links
        })

    # If not a POST request, render the input form page (home.html)
    return render(request, 'home.html')
