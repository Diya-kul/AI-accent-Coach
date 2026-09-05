# save_model_scaler.py
import joblib
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
import numpy as np

# Example training data (replace with your actual features)
X_train = np.random.rand(100, 13)   # 100 samples, 13 features
y_train = np.random.randint(0, 3, 100)  # 3 accent classes: 0,1,2

# 1. Fit scaler
scaler = StandardScaler()
scaler.fit(X_train)

# Save scaler
joblib.dump(scaler, "backend/models/scaler.pkl")

# 2. Train a simple model (replace with your actual model)
model = LogisticRegression(max_iter=1000)
model.fit(scaler.transform(X_train), y_train)

# Save model
joblib.dump(model, "backend/models/accent_model.pkl")

print("Scaler and model saved successfully!")


# Run the command on terminal of root directory
# : python save_model_scaler.py