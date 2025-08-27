import joblib
import numpy as np
from sklearn.linear_model import LogisticRegression

# Training data (temperature → 0 = normal, 1 = needs cooling)
X = np.array([[25], [26], [27], [28], [29], [30], [31], [32], [33]])
y = np.array([0,   0,   0,   0,   0,   1,   1,   1,   1])

model = LogisticRegression()
model.fit(X, y)

# Save the model
joblib.dump(model, "cooling_model.pkl")
print("Model saved as cooling_model.pkl")
