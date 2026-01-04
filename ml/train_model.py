import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score

# -----------------------------
# Load dataset
# -----------------------------
df = pd.read_csv("../dataset/scam_messages.csv")

X = df[["message", "amount", "sender_type"]]
y = df["label"]

# -----------------------------
# Train-test split
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# -----------------------------
# Feature processing
# -----------------------------
preprocessor = ColumnTransformer(
    transformers=[
        ("text", TfidfVectorizer(stop_words="english", max_features=3000), "message"),
        ("sender", OneHotEncoder(handle_unknown="ignore"), ["sender_type"]),
        ("amount", "passthrough", ["amount"])
    ]
)

# -----------------------------
# Model pipeline
# -----------------------------
model = Pipeline(
    steps=[
        ("preprocessing", preprocessor),
        ("classifier", LogisticRegression(max_iter=1000))
    ]
)

# -----------------------------
# Train model
# -----------------------------
model.fit(X_train, y_train)

# -----------------------------
# Evaluation
# -----------------------------
y_pred = model.predict(X_test)

print("\n✅ Model Evaluation\n")
print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

# -----------------------------
# Save model
# -----------------------------
joblib.dump(model, "../backend/saved_models/scam_classifier.pkl")

print("\n🎯 Model saved to backend/saved_models/")
