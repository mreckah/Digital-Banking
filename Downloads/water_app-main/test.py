import joblib
import pandas as pd

# Chargez le modèle
model = joblib.load('models/best_model.pkl')

# Testez avec des données factices
test_data = {
    'ph': 7.0,
    'Hardness': 10000,
    'Solids': 10000,
    'Chloramines': 100050,
    'Sulfate': 90000,
    'Conductivity': 110,
    'Organic_carbon':8.0,
    'Trihalomethanes': 10,
    'Turbidity': 10000
}

# Créez le DataFrame correctement
df = pd.DataFrame([test_data], columns=test_data.keys())

# Vérifiez les colonnes
if hasattr(model, 'feature_names_in_'):
    df = df[model.feature_names_in_]

# Faites la prédiction
print("Probabilité:", model.predict_proba(df)[0][1])