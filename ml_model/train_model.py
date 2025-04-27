# ml_model/train_model.py

import pandas as pd
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import joblib
import os

# Load the dataset
data_path = os.path.join('dataset', 'training_data.csv')
df = pd.read_csv(data_path)

# Features and target
X = df.drop(columns=['prognosis'])
y = df['prognosis']

X=X.fillna(0)

# Encode the target labels
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# Train the model
model = MultinomialNB()
model.fit(X, y_encoded)

# Save model and encoders
if not os.path.exists('ml_model/ml_model'):
    os.makedirs('ml_model/ml_model')

joblib.dump(model, 'ml_model/ml_model/disease_model.pkl')
joblib.dump(label_encoder, 'ml_model/ml_model/label_encoder.pkl')
joblib.dump(X.columns.tolist(), 'ml_model/ml_model/symptom_list.pkl')

print("✅ Model training complete and files saved.")
