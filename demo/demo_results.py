DEMO_MODE = True

ILLUSTRATIVE_BENCHMARK = {
    "Logistic Regression": {"Accuracy": 0.951, "Precision": 0.940, "Recall": 0.928, "F1": 0.934, "ROC-AUC": 0.971},
    "Classical SVM": {"Accuracy": 0.965, "Precision": 0.957, "Recall": 0.946, "F1": 0.951, "ROC-AUC": 0.980},
    "XGBoost": {"Accuracy": 0.974, "Precision": 0.968, "Recall": 0.959, "F1": 0.963, "ROC-AUC": 0.987},
    "QSVC": {"Accuracy": 0.962, "Precision": 0.951, "Recall": 0.940, "F1": 0.945, "ROC-AUC": 0.978},
}

ILLUSTRATIVE_RESOURCES = {
    "Qubits": 4,
    "PCA dimensions": 4,
    "Circuit depth": 6,
    "Shots": 1024,
    "Kernel evaluation time": "2.84 s",
    "Noise sensitivity": "4.7% degradation",
}

ILLUSTRATIVE_EXPLANATION = {
    "Radius-related feature": 0.88,
    "Concavity-related feature": 0.76,
    "Perimeter-related feature": 0.64,
    "Texture-related feature": 0.49,
    "Smoothness-related feature": 0.31,
}
