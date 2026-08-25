# QureAI — SIH 2026 Hybrid Quantum Disease-Risk Prototype

QureAI is a research prototype for comparing classical ML and a quantum-kernel QSVC workflow on the public Breast Cancer Wisconsin Diagnostic (WDBC) dataset.

## What is computed

### Classical branch
CSV → schema normalization → validation → StandardScaler → Logistic Regression / SVM / XGBoost → per-sample predictions.

### Quantum branch
CSV → StandardScaler + PCA (4 components) → bounded angle encoding → 4-qubit RY + linear CX feature map → fidelity statevector quantum kernel → QSVC → per-sample quantum prediction.

The quantum experiment is a **local statevector simulation**, not real quantum hardware. Qiskit Machine Learning documents `FidelityStatevectorKernel` as a reference kernel optimized for classically simulated statevectors, and `QSVC` accepts a quantum kernel directly. See the official Qiskit Machine Learning documentation for the current API.

## Clinician-facing safeguards

- Input schema and numeric validation before inference.
- Sample-by-sample model outputs instead of a single opaque result.
- Model agreement indicator.
- Simple out-of-distribution/data-quality flag against the public WDBC training distribution.
- Local Logistic Regression contribution view for the selected sample.
- Clear separation between computed classical results and measured quantum simulation results.
- No treatment recommendation and no claim of clinical validation.

## Data boundary

The current prototype is based on the public WDBC dataset and its 30 diagnostic measurements. It is not a production clinical system and should not be used to diagnose or treat patients.

## Run

```powershell
python -m venv .venv
.venv\\Scripts\\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

## Demo workflow

1. Open **Patient / Sample Analysis**.
2. Load the demo case or upload a compatible CSV.
3. Review the full input table.
4. Run **Classical Analysis**.
5. Select any sample to inspect all classical models individually.
6. Open **Quantum Analysis** and run the local Qiskit QSVC experiment.
7. Return to the selected sample to see the quantum result alongside the classical results.
8. Use **Model Benchmark** to compare measured metrics.

## Scientific boundary

The application is intended for research demonstration and model-development education. It does not establish clinical validity, prospective performance, safety, or quantum advantage.
