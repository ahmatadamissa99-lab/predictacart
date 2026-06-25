
import joblib
import os
import json
import numpy as np

PRODUCT_IDS = [
    "PROD_001", "PROD_002", "PROD_003",
    "PROD_004", "PROD_005", "PROD_006",
    "PROD_007", "PROD_008", "PROD_009", "PROD_010"
]

def model_fn(model_dir):
    model  = joblib.load(os.path.join(model_dir, "recommender_v1.pkl"))
    scaler = joblib.load(os.path.join(model_dir, "scaler.pkl"))
    return (model, scaler)

def input_fn(request_body, content_type):
    data = json.loads(request_body)
    return np.array(data["inputs"], dtype=np.float64)

def predict_fn(input_data, model):
    clf, scaler = model
    scaled = scaler.transform(input_data)
    proba  = clf.predict_proba(scaled)[:, 1]
    result = []
    for prob in proba:
        np.random.seed(int(prob * 1000))
        top5 = np.random.choice(
            PRODUCT_IDS, size=5, replace=False
        ).tolist()
        result.append(top5)
    return result

def output_fn(prediction, accept):
    return json.dumps({"predictions": prediction})
