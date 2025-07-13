import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import joblib

def train_model(data_path="data/edf_training_data.csv", model_path="data/model.pkl"):
    df = pd.read_csv(data_path)

    # Features and label
    X = df[["arrival_time", "execution_time", "deadline", "priority", "task_type"]]
    y = df["wait_time"]  # We’re training to minimize this

    # Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Evaluate
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    print(f"Model trained. MAE: {round(mae, 2)}")

    # Save model
    joblib.dump(model, model_path)
    print(f"Model saved to {model_path}")

if __name__ == "__main__":
    train_model()
