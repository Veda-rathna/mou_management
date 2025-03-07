import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

# Dummy Data for Training
data = {
    "previous_renewals": [5, 3, 8, 0, 2, 7, 10, 1],
    "industry_trend": [0.8, 0.6, 0.9, 0.2, 0.5, 0.7, 0.95, 0.3],
    "renewal_status": [1, 0, 1, 0, 0, 1, 1, 0]
}

df = pd.DataFrame(data)
X = df.drop(columns=["renewal_status"])
y = df["renewal_status"]

# Train the Model
model = RandomForestClassifier(n_estimators=100)
model.fit(X, y)

# Save the Model
joblib.dump(model, "renewal_model.pkl")

def predict_renewal(previous_renewals, industry_trend):
    model = joblib.load("renewal_model.pkl")
    prediction = model.predict([[previous_renewals, industry_trend]])
    return prediction[0]
