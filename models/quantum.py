from __future__ import annotations

import time
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from sklearn.model_selection import train_test_split

from models.classical import RANDOM_STATE, PCA_COMPONENTS, fit_pca, training_data, transform_features

QUANTUM_TRAIN_SAMPLES = 80
QUANTUM_TEST_SAMPLES = 40


def _qiskit_components():
    from qiskit import QuantumCircuit
    from qiskit.circuit import ParameterVector
    from qiskit.quantum_info import Statevector
    from qiskit_machine_learning.kernels import FidelityStatevectorKernel
    from qiskit_machine_learning.algorithms import QSVC
    return QuantumCircuit, ParameterVector, Statevector, FidelityStatevectorKernel, QSVC


def build_feature_map():
    QuantumCircuit, ParameterVector, *_ = _qiskit_components()
    qc = QuantumCircuit(PCA_COMPONENTS, name="QureAI-4Q-FeatureMap")
    params = ParameterVector("x", PCA_COMPONENTS)
    for i in range(PCA_COMPONENTS):
        qc.ry(params[i], i)
    for i in range(PCA_COMPONENTS - 1):
        qc.cx(i, i + 1)
    return qc


def _angle_encode(X):
    # Keep PCA values in a bounded rotation range without changing ordering.
    return np.pi * np.tanh(np.asarray(X, dtype=float))


def _balanced_subset(X, y, n, seed):
    if len(X) <= n:
        return X, y
    X_sub, _, y_sub, _ = train_test_split(
        X, y, train_size=n, stratify=y, random_state=seed
    )
    return X_sub, y_sub


def run_quantum_benchmark():
    """Run a real local Qiskit statevector QSVC experiment.

    The experiment is deliberately small: four PCA dimensions and a bounded
    training subset, making it practical for local demonstration. It is not a
    claim of hardware execution or quantum advantage.
    """
    try:
        _, _, Statevector, FidelityStatevectorKernel, QSVC = _qiskit_components()
    except Exception as exc:
        raise RuntimeError(
            "Qiskit and qiskit-machine-learning are required for the quantum experiment. "
            "Install the versions listed in requirements.txt."
        ) from exc

    _, pca, X_train_pca, X_test_pca, y_train, y_test = fit_pca()
    X_qtrain, y_qtrain = _balanced_subset(X_train_pca, y_train.to_numpy(), QUANTUM_TRAIN_SAMPLES, RANDOM_STATE)
    X_qtest, y_qtest = _balanced_subset(X_test_pca, y_test.to_numpy(), QUANTUM_TEST_SAMPLES, RANDOM_STATE + 1)

    X_qtrain = _angle_encode(X_qtrain)
    X_qtest = _angle_encode(X_qtest)

    feature_map = build_feature_map()
    kernel = FidelityStatevectorKernel(
        feature_map=feature_map,
        statevector_type=Statevector,
        cache_size=len(X_qtrain),
        auto_clear_cache=False,
        shots=None,
        enforce_psd=True,
    )

    start = time.perf_counter()
    qsvc = QSVC(quantum_kernel=kernel)
    qsvc.fit(X_qtrain, y_qtrain)
    pred = qsvc.predict(X_qtest)
    decision = qsvc.decision_function(X_qtest)
    elapsed = time.perf_counter() - start

    metrics = {
        "Accuracy": accuracy_score(y_qtest, pred),
        "Precision": precision_score(y_qtest, pred, zero_division=0),
        "Recall": recall_score(y_qtest, pred, zero_division=0),
        "F1": f1_score(y_qtest, pred, zero_division=0),
        "ROC-AUC": roc_auc_score(y_qtest, decision),
    }
    return {
        "model": qsvc,
        "kernel": kernel,
        "feature_map": feature_map,
        "metrics": metrics,
        "train_size": len(X_qtrain),
        "test_size": len(X_qtest),
        "elapsed_seconds": elapsed,
        "pca": pca,
    }


def predict_quantum_samples(model_result, sample: pd.DataFrame):
    X_pca = transform_features(sample)
    X_q = _angle_encode(X_pca)
    model = model_result["model"]
    pred = model.predict(X_q)
    decision = model.decision_function(X_q)
    return pd.DataFrame({
        "Quantum class": np.where(pred == 1, "Malignant", "Benign"),
        "Quantum decision score": decision.astype(float),
    })


def get_quantum_execution_status():
    return {
        "ideal_simulator": "Local Qiskit statevector QSVC is available when quantum dependencies are installed.",
        "noisy_simulator": "Shot-noise mode can be added as a separate experiment; it is not mixed with the exact benchmark.",
        "real_qpu": "Real QPU execution is optional and requires a configured IBM Quantum backend and credentials.",
    }


def quantum_status():
    return {"implemented": True, "source": "qiskit_statevector_simulation", "train_samples": QUANTUM_TRAIN_SAMPLES, "test_samples": QUANTUM_TEST_SAMPLES}
