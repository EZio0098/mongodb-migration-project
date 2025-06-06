
import pandas as pd
from pymongo import MongoClient
import os

mongo_uri = os.getenv("MONGO_URI", "mongodb://admin:password@mongodb:27017/")
client = MongoClient(mongo_uri)
db = client["medical_db"]
collection = db["patients"]

df = pd.read_csv("healthcare_dataset.csv")
df.columns = [col.strip() for col in df.columns]
print(" Colonnes du CSV:", df.columns.tolist())
print(" Doublons détectés:", df.duplicated().sum())
print(" Valeurs manquantes par colonne:\n", df.isnull().sum())

df.drop_duplicates(inplace=True)
df.fillna("Inconnu", inplace=True)

df['Date of Admission'] = pd.to_datetime(df['Date of Admission'], errors='coerce')
df['Discharge Date'] = pd.to_datetime(df['Discharge Date'], errors='coerce')

for col in df.columns:
    if "Billing Amount" in col:
        billing_column = col
        break

df[billing_column] = df[billing_column].apply(lambda x: float(str(x).replace(',', '')))

df.rename(columns={
    'Patient ID': 'patient_id',
    'Name': 'name',
    'Age': 'age',
    'Gender': 'gender',
    'Blood Type': 'blood_type',
    'Medical Condition': 'medical_condition',
    'Date of Admission': 'date_of_admission',
    'Doctor': 'doctor',
    'Hospital': 'hospital',
    'Insurance Provider': 'insurance_provider',
    billing_column: 'billing_amount',
    'Room Number': 'room_number',
    'Admission Type': 'admission_type',
    'Discharge Date': 'discharge_date',
    'Medication': 'medication',
    'Test Results': 'test_results'
}, inplace=True)

collection.insert_many(df.to_dict('records'))
print(f" Migration réussie de {len(df)} documents vers MongoDB.")
