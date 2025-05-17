MEDICAL_CONDITIONS = {
    "Type 2 Diabetes": {
        "description": "Type 2 diabetes is a chronic condition that affects the way the body processes blood sugar (glucose). With type 2 diabetes, the body either doesn't produce enough insulin, or it resists insulin.",
        "symptoms": [
            "Increased thirst",
            "Frequent urination",
            "Increased hunger",
            "Unintended weight loss",
            "Fatigue",
            "Blurred vision",
            "Slow-healing sores",
            "Frequent infections"
        ],
        "treatments": [
            "Healthy eating",
            "Regular exercise",
            "Weight loss",
            "Monitoring blood sugar",
            "Diabetes medications (e.g., Metformin)",
            "Insulin therapy in some cases"
        ],
        "complications": [
            "Heart and blood vessel disease",
            "Nerve damage (neuropathy)",
            "Kidney damage (nephropathy)",
            "Eye damage (retinopathy)",
            "Foot damage",
            "Skin conditions",
            "Hearing impairment",
            "Alzheimer's disease"
        ],
        "monitoring": {
            "blood_glucose_target": "80-130 mg/dL before meals, less than 180 mg/dL after meals",
            "hba1c_target": "Less than 7%",
            "check_frequency": "Check blood sugar at least once a day, more often if on insulin"
        }
    },
    "Pneumonia": {
        "description": "Pneumonia is an infection that inflames the air sacs in one or both lungs. The air sacs may fill with fluid or pus, causing cough with phlegm or pus, fever, chills, and difficulty breathing.",
        "symptoms": [
            "Chest pain when breathing or coughing",
            "Confusion or changes in mental awareness (in adults age 65 and older)",
            "Cough, which may produce phlegm",
            "Fatigue",
            "Fever, sweating and shaking chills",
            "Lower than normal body temperature (in adults older than age 65 and people with weak immune systems)",
            "Nausea, vomiting or diarrhea",
            "Shortness of breath"
        ],
        "treatments": [
            "Antibiotics for bacterial pneumonia",
            "Antiviral medications for viral pneumonia",
            "Fever reducers",
            "Cough medicine",
            "Rest and adequate hydration"
        ],
        "complications": [
            "Bacteria in the bloodstream (bacteremia)",
            "Difficulty breathing",
            "Fluid accumulation around the lungs (pleural effusion)",
            "Lung abscess",
            "Acute respiratory distress syndrome (ARDS)"
        ],
        "monitoring": {
            "temperature": "Monitor for fever",
            "breathing": "Watch for increased difficulty breathing",
            "oxygen_levels": "Maintain oxygen saturation above 94%"
        }
    },
    "Myocardial Infarction": {
        "description": "A myocardial infarction (MI), commonly known as a heart attack, occurs when blood flow decreases or stops to a part of the heart, causing damage to the heart muscle.",
        "symptoms": [
            "Chest pain or discomfort",
            "Pain or discomfort in the arms, left shoulder, elbows, jaw, or back",
            "Shortness of breath",
            "Nausea, indigestion, heartburn, or abdominal pain",
            "Cold sweat",
            "Fatigue",
            "Lightheadedness or sudden dizziness"
        ],
        "treatments": [
            "Aspirin to prevent blood clotting",
            "Thrombolytics to dissolve existing clots",
            "Antiplatelet agents",
            "Beta blockers to relax heart muscle",
            "ACE inhibitors to lower blood pressure",
            "Statins to lower cholesterol",
            "Coronary angioplasty and stenting",
            "Coronary artery bypass surgery in severe cases"
        ],
        "complications": [
            "Abnormal heart rhythms (arrhythmias)",
            "Heart failure",
            "Heart rupture",
            "Valve problems",
            "Pericarditis",
            "Cardiac arrest"
        ],
        "monitoring": {
            "heart_rate": "Target resting heart rate 60-100 bpm",
            "blood_pressure": "Target below 130/80 mmHg",
            "cholesterol": "LDL target below 70 mg/dL for very high-risk patients",
            "activity": "Gradually increasing physical activity as recommended by doctor"
        }
    }
}

MEDICATIONS = {
    "Metformin": {
        "class": "Biguanide",
        "uses": ["Type 2 diabetes"],
        "mechanism": "Decreases glucose production in the liver and increases insulin sensitivity",
        "side_effects": [
            "Nausea",
            "Vomiting",
            "Diarrhea",
            "Stomach pain",
            "Loss of appetite",
            "Metallic taste"
        ],
        "contraindications": [
            "Kidney disease",
            "Liver disease",
            "Heart failure",
            "Alcohol abuse"
        ],
        "dosing": "Starting dose 500mg once or twice daily with meals, can be increased gradually"
    },
    "Lisinopril": {
        "class": "ACE inhibitor",
        "uses": ["Hypertension", "Heart failure", "Post-myocardial infarction"],
        "mechanism": "Prevents conversion of angiotensin I to angiotensin II, reducing blood pressure",
        "side_effects": [
            "Dry cough",
            "Dizziness",
            "Headache",
            "Fatigue",
            "Hypotension"
        ],
        "contraindications": [
            "Pregnancy",
            "History of angioedema",
            "Bilateral renal artery stenosis"
        ],
        "dosing": "Starting dose 10mg once daily, can be adjusted based on blood pressure response"
    },
    "Azithromycin": {
        "class": "Macrolide antibiotic",
        "uses": ["Bacterial infections", "Pneumonia", "Bronchitis", "Sinusitis"],
        "mechanism": "Inhibits bacterial protein synthesis",
        "side_effects": [
            "Nausea",
            "Vomiting",
            "Diarrhea",
            "Abdominal pain",
            "QT interval prolongation (rare)"
        ],
        "contraindications": [
            "Known hypersensitivity",
            "History of cholestatic jaundice with macrolides"
        ],
        "dosing": "Typical dose 500mg on day 1, followed by 250mg daily for 4 days"
    },
    "Aspirin": {
        "class": "NSAID, antiplatelet",
        "uses": ["Pain relief", "Fever reduction", "Prevention of blood clots", "Heart attack prevention"],
        "mechanism": "Inhibits prostaglandin synthesis and platelet aggregation",
        "side_effects": [
            "Stomach irritation",
            "Heartburn",
            "Gastrointestinal bleeding",
            "Tinnitus (with high doses)"
        ],
        "contraindications": [
            "Bleeding disorders",
            "Peptic ulcer disease",
            "Children with viral illnesses (risk of Reye's syndrome)"
        ],
        "dosing": "For heart attack prevention: 81-325mg daily"
    },
    "Atorvastatin": {
        "class": "Statin",
        "uses": ["High cholesterol", "Prevention of cardiovascular disease"],
        "mechanism": "Inhibits HMG-CoA reductase, reducing cholesterol production in the liver",
        "side_effects": [
            "Muscle pain",
            "Liver enzyme elevation",
            "Headache",
            "Joint pain",
            "Diarrhea"
        ],
        "contraindications": [
            "Active liver disease",
            "Pregnancy",
            "Breastfeeding"
        ],
        "dosing": "10-80mg once daily, typically taken in the evening"
    },
    "Metoprolol": {
        "class": "Beta blocker",
        "uses": ["Hypertension", "Angina", "Heart failure", "Post-myocardial infarction"],
        "mechanism": "Blocks beta-1 adrenergic receptors, reducing heart rate and blood pressure",
        "side_effects": [
            "Fatigue",
            "Dizziness",
            "Bradycardia",
            "Hypotension",
            "Shortness of breath in patients with asthma"
        ],
        "contraindications": [
            "Severe bradycardia",
            "Heart block greater than first degree",
            "Cardiogenic shock",
            "Decompensated heart failure"
        ],
        "dosing": "For MI: 25-100mg twice daily"
    }
}

VITAL_SIGNS = {
    "temperature": {
        "normal_range": "36.5-37.5°C (97.7-99.5°F)",
        "interpretations": {
            "high": "Above 38.0°C (100.4°F) indicates fever, possibly due to infection, inflammation, or medication reaction",
            "low": "Below 36.0°C (96.8°F) indicates hypothermia, possibly due to cold exposure, shock, or certain medications"
        }
    },
    "heart_rate": {
        "normal_range": "60-100 beats per minute (bpm) at rest",
        "interpretations": {
            "high": "Above 100 bpm (tachycardia) may indicate stress, anxiety, infection, dehydration, or heart problems",
            "low": "Below 60 bpm (bradycardia) may be normal in athletes or indicate medication effects, heart block, or hypothyroidism"
        }
    },
    "blood_pressure": {
        "normal_range": "Less than 120/80 mmHg",
        "interpretations": {
            "elevated": "120-129/<80 mmHg indicates elevated blood pressure",
            "stage1": "130-139/80-89 mmHg indicates stage 1 hypertension",
            "stage2": "≥140/≥90 mmHg indicates stage 2 hypertension",
            "crisis": "≥180/≥120 mmHg indicates hypertensive crisis",
            "low": "<90/60 mmHg indicates hypotension"
        }
    },
    "oxygen_saturation": {
        "normal_range": "95-100%",
        "interpretations": {
            "mild_hypoxemia": "91-94% indicates mild hypoxemia",
            "moderate_hypoxemia": "86-90% indicates moderate hypoxemia",
            "severe_hypoxemia": "≤85% indicates severe hypoxemia requiring immediate intervention"
        }
    }
}

def get_medical_knowledge():
    return {
        "conditions": MEDICAL_CONDITIONS,
        "medications": MEDICATIONS,
        "vital_signs": VITAL_SIGNS
    }

def get_condition_info(condition_name):
    return MEDICAL_CONDITIONS.get(condition_name, {"description": "Information not available"})

def get_medication_info(medication_name):
    return MEDICATIONS.get(medication_name, {"description": "Information not available"})

def interpret_vital_sign(vital_name, value):
    if vital_name not in VITAL_SIGNS:
        return "Unknown vital sign"
    
    vital_info = VITAL_SIGNS[vital_name]
    
    if vital_name == "temperature":
        if value > 38.0:
            return vital_info["interpretations"]["high"]
        elif value < 36.0:
            return vital_info["interpretations"]["low"]
        else:
            return f"Normal temperature within range {vital_info['normal_range']}"
    
    elif vital_name == "heart_rate":
        if value > 100:
            return vital_info["interpretations"]["high"]
        elif value < 60:
            return vital_info["interpretations"]["low"]
        else:
            return f"Normal heart rate within range {vital_info['normal_range']}"
    
    elif vital_name == "oxygen_saturation":
        if value < 86:
            return vital_info["interpretations"]["severe_hypoxemia"]
        elif value < 91:
            return vital_info["interpretations"]["moderate_hypoxemia"]
        elif value < 95:
            return vital_info["interpretations"]["mild_hypoxemia"]
        else:
            return f"Normal oxygen saturation within range {vital_info['normal_range']}"
    
    return "Cannot interpret this vital sign value"
