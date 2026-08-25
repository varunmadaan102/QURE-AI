from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

FEATURE_NAMES = list(load_breast_cancer().feature_names)
RANDOM_STATE = 42
PCA_COMPONENTS = 4

try:
    from xgboost import XGBClassifier
    XGBOOST_AVAILABLE = True
except Exception:
    XGBClassifier = None
    XGBOOST_AVAILABLE = False


def training_data():
    data = load_breast_cancer()
    y = (data.target == 0).astype(int)  # 1 = malignant, 0 = benign
    return pd.DataFrame(data.data, columns=FEATURE_NAMES), pd.Series(y, name="diagnosis")


def build_models():
    models = {
        "Logistic Regression": LogisticRegression(max_iter=3000, random_state=RANDOM_STATE),
        "Classical SVM": SVC(kernel="rbf", probability=True, random_state=RANDOM_STATE),
    }
    if XGBOOST_AVAILABLE:
        models["XGBoost"] = XGBClassifier(
            n_estimators=180,
            max_depth=3,
            learning_rate=0.05,
            subsample=0.9,
            colsample_bytree=0.9,
            eval_metric="logloss",
            random_state=RANDOM_STATE,
            n_jobs=1,
        )
    return models


def prepare_split(X, y, test_size=0.2):
    return train_test_split(X, y, test_size=test_size, stratify=y, random_state=RANDOM_STATE)


def _metrics(y_true, pred, score):
    return {
        "Accuracy": accuracy_score(y_true, pred),
        "Precision": precision_score(y_true, pred, zero_division=0),
        "Recall": recall_score(y_true, pred, zero_division=0),
        "F1": f1_score(y_true, pred, zero_division=0),
        "ROC-AUC": roc_auc_score(y_true, score),
    }


def fit_classical_benchmarks():
    X, y = training_data()
    X_train, X_test, y_train, y_test = prepare_split(X, y)
    results, fitted = {}, {}
    for name, model in build_models().items():
        pipe = Pipeline([("scaler", StandardScaler()), ("model", model)])
        pipe.fit(X_train, y_train)
        pred = pipe.predict(X_test)
        score = pipe.predict_proba(X_test)[:, 1]
        results[name] = _metrics(y_test, pred, score)
        fitted[name] = pipe
    return results, fitted, (X_train, X_test, y_train, y_test)


def fit_inference_models():
    """Fit the classical models on all public WDBC training samples for inference."""
    X, y = training_data()
    fitted = {}
    for name, model in build_models().items():
        pipe = Pipeline([("scaler", StandardScaler()), ("model", model)])
        pipe.fit(X, y)
        fitted[name] = pipe
    return fitted


def fit_pca():
    X, y = training_data()
    X_train, X_test, y_train, y_test = prepare_split(X, y)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    pca = PCA(n_components=PCA_COMPONENTS, random_state=RANDOM_STATE)
    X_train_pca = pca.fit_transform(X_train_scaled)
    X_test_pca = pca.transform(X_test_scaled)
    return scaler, pca, X_train_pca, X_test_pca, y_train, y_test


def fit_full_preprocessor():
    X, _ = training_data()
    scaler = StandardScaler().fit(X)
    pca = PCA(n_components=PCA_COMPONENTS, random_state=RANDOM_STATE).fit(scaler.transform(X))
    return scaler, pca


def transform_features(sample: pd.DataFrame):
    scaler, pca = fit_full_preprocessor()
    X = sample[FEATURE_NAMES].astype(float).to_numpy()
    return pca.transform(scaler.transform(X))


def predict_samples(sample: pd.DataFrame):
    clean = sample[FEATURE_NAMES].astype(float)
    fitted = fit_inference_models()
    rows = []
    for idx, (_, row) in enumerate(clean.iterrows()):
        result = {"row": idx}
        for name, model in fitted.items():
            pred = int(model.predict(row.to_frame().T)[0])
            prob = float(model.predict_proba(row.to_frame().T)[0, 1])
            result[f"{name} class"] = "Malignant" if pred == 1 else "Benign"
            result[f"{name} probability"] = prob
        rows.append(result)
    return pd.DataFrame(rows)


def predict_sample(sample: pd.DataFrame):
    return predict_samples(sample).iloc[0].to_dict()


def explain_logistic_sample(sample: pd.DataFrame):
    """Return local linear contributions for Logistic Regression.

    These are model contributions, not clinical causal effects.
    """
    fitted = fit_inference_models()["Logistic Regression"]
    scaler = fitted.named_steps["scaler"]
    model = fitted.named_steps["model"]
    x = sample[FEATURE_NAMES].astype(float).to_numpy()[0]
    z = scaler.transform([x])[0]
    contributions = z * model.coef_[0]
    frame = pd.DataFrame({"Feature": FEATURE_NAMES, "Contribution": contributions})
    frame["Absolute"] = frame["Contribution"].abs()
    return frame.sort_values("Absolute", ascending=False).drop(columns="Absolute")


def dataset_reference_stats():
    X, _ = training_data()
    return X.mean(), X.std(ddof=0).replace(0, 1.0)
