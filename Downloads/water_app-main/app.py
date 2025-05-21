# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, flash, redirect, url_for, send_file
import joblib
import os
from datetime import datetime
import json
import pandas as pd
import numpy as np
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from io import BytesIO

app = Flask(__name__)
app.secret_key = 'votre_cle_secrete_super_securisee'

# Charger le modèle
model = joblib.load('models/best_model.pkl')

# Liste des caractéristiques avec descriptions et ordre fixe
FEATURES_ORDER = [
    'ph', 'Hardness', 'Solids', 'Chloramines', 
    'Sulfate', 'Conductivity', 'Organic_carbon', 
    'Trihalomethanes', 'Turbidity'
]

FEATURES_INFO = {
    'ph': {'unit': '', 'desc': 'Potentiel hydrogène (acidité/alcalinité)'},
    'Hardness': {'unit': 'mg/L', 'desc': 'Dureté de l\'eau (teneur en minéraux)'},
    'Solids': {'unit': 'ppm', 'desc': 'Solides dissous totaux'},
    'Chloramines': {'unit': 'mg/L', 'desc': 'Concentration en chloramines'},
    'Sulfate': {'unit': 'mg/L', 'desc': 'Concentration en sulfate'},
    'Conductivity': {'unit': 'μS/cm', 'desc': 'Conductivité électrique'},
    'Organic_carbon': {'unit': 'mg/L', 'desc': 'Carbone organique total'},
    'Trihalomethanes': {'unit': 'μg/L', 'desc': 'Concentration en trihalométhanes'},
    'Turbidity': {'unit': 'NTU', 'desc': 'Turbidité (netteté de l\'eau)'}
}


@app.route('/')
def index():
    """Page d'accueil avec le formulaire de saisie"""
    return render_template('index.html', features=FEATURES_INFO)


@app.route('/predict', methods=['POST'])
def predict():
    try:
        # 1. Récupération et validation des données
        input_data = {}
        for feature in FEATURES_ORDER:
            value = request.form.get(feature)
            if not value:
                flash(f"La valeur pour {feature} est manquante", "error")
                return redirect(url_for('index'))
            try:
                input_data[feature] = float(value)
            except ValueError:
                flash(f"Valeur invalide pour {feature}", "error")
                return redirect(url_for('index'))

        # 2. Création d'un DataFrame avec les données dans le bon ordre
        input_df = pd.DataFrame([input_data], columns=FEATURES_ORDER)

        # 3. Prédiction
        prediction = model.predict(input_df)[0]
        
        # Gestion de la confiance selon si le modèle a predict_proba ou non
        try:
            confidence = round(np.max(model.predict_proba(input_df)[0]) * 100, 2)
        except AttributeError:
            confidence = None

        # 4. Préparation des résultats
        if prediction == 1:
            result = {
                'message': "L'eau est POTABLE",
                'class': "success",
                'icon': "check-circle",
                'emoji': "💧✅",
                'color': "#2ecc71"
            }
        else:
            result = {
                'message': "L'eau est NON POTABLE",
                'class': "danger",
                'icon': "exclamation-triangle",
                'emoji': "🚱❌",
                'color': "#e74c3c"
            }

        # 5. Formatage des données pour l'affichage
        input_values = {
            k: {
                'value': v,
                'unit': FEATURES_INFO[k]['unit'],
                'desc': FEATURES_INFO[k]['desc']
            }
            for k, v in input_data.items()
        }

        # 6. Enregistrement des résultats
        log_prediction(input_data, prediction, confidence)

        return render_template('results.html',
                            prediction=prediction,
                            confidence=confidence,
                            input_values=input_values,
                            analysis_date=datetime.now().strftime("%d/%m/%Y %H:%M"),
                            **result)

    except Exception as e:
        app.logger.error(f"Erreur lors de la prédiction: {str(e)}", exc_info=True)
        flash("Une erreur technique est survenue lors de l'analyse. Veuillez réessayer.", "error")
        return redirect(url_for('index'))


def log_prediction(input_data, prediction, confidence):
    """Enregistre les prédictions dans un fichier log"""
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'input_data': input_data,
        'prediction': int(prediction),
        'confidence': float(confidence) if confidence is not None else None,
        'model_type': str(type(model))
    }
    
    log_file = 'logs/predictions.log'
    
    try:
        os.makedirs('logs', exist_ok=True)
        with open(log_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
    except Exception as e:
        app.logger.error(f"Erreur lors de l'enregistrement du log: {str(e)}")


@app.route('/generate-pdf', methods=['POST'])
def generate_pdf():
    try:
        # Get the data from the form
        data = request.form.to_dict()
        
        # Create a BytesIO buffer to store the PDF
        buffer = BytesIO()
        
        # Create the PDF document
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        elements = []
        
        # Add title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30
        )
        elements.append(Paragraph("Rapport d'Analyse de Potabilité d'Eau", title_style))
        elements.append(Spacer(1, 20))
        
        # Add date
        date_style = ParagraphStyle(
            'DateStyle',
            parent=styles['Normal'],
            fontSize=12,
            textColor=colors.gray
        )
        elements.append(Paragraph(f"Date d'analyse: {datetime.now().strftime('%d/%m/%Y %H:%M')}", date_style))
        elements.append(Spacer(1, 30))
        
        # Add parameters table
        table_data = [['Paramètre', 'Valeur', 'Unité', 'Description']]
        for feature, info in FEATURES_INFO.items():
            value = data.get(feature, 'N/A')
            table_data.append([
                feature,
                str(value),
                info['unit'],
                info['desc']
            ])
        
        # Create the table
        table = Table(table_data, colWidths=[100, 80, 80, 200])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 30))
        
        # Add conclusion
        conclusion_style = ParagraphStyle(
            'ConclusionStyle',
            parent=styles['Normal'],
            fontSize=14,
            spaceAfter=20
        )
        elements.append(Paragraph("Conclusion:", conclusion_style))
        elements.append(Paragraph(
            "Ce rapport présente les résultats de l'analyse de potabilité de l'eau. "
            "Les valeurs sont comparées aux normes en vigueur pour déterminer la qualité de l'eau.",
            styles['Normal']
        ))
        
        # Build the PDF
        doc.build(elements)
        
        # Move to the beginning of the BytesIO buffer
        buffer.seek(0)
        
        # Return the PDF as a downloadable file
        return send_file(
            buffer,
            as_attachment=True,
            download_name=f'analyse_eau_{datetime.now().strftime("%Y%m%d_%H%M")}.pdf',
            mimetype='application/pdf'
        )
        
    except Exception as e:
        app.logger.error(f"Erreur lors de la génération du PDF: {str(e)}", exc_info=True)
        flash("Une erreur est survenue lors de la génération du PDF.", "error")
        return redirect(url_for('index'))


if __name__ == '__main__':
    os.makedirs('models', exist_ok=True)
    app.run(debug=True)