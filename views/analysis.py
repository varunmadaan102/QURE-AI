import streamlit as st
import pandas as pd
from components.pipeline import pipeline
from models.classical import FEATURE_NAMES, predict_samples, explain_logistic_sample, transform_features
from utils.data import validate_input, make_sample_frame


def _demo_sample():
    from sklearn.datasets import load_breast_cancer
    data = load_breast_cancer()
    row = pd.DataFrame([data.data[0]], columns=FEATURE_NAMES)
    row.insert(0, "sample_id", "WDBC-DEMO-001")
    row.insert(0, "index", 0)
    row["diagnosis"] = "Benign" if data.target[0] == 1 else "Malignant"
    return row


def _quality_flags(df):
    from models.classical import dataset_reference_stats
    means, stds = dataset_reference_stats()
    x = df[FEATURE_NAMES].astype(float)
    z = ((x - means) / stds).abs()
    max_z = z.max(axis=1)
    return max_z


def render():
    st.title("Patient / Sample Analysis")
    st.caption("Clinician-oriented research interface. The current model is trained on the public WDBC dataset and is not clinically validated.")
    c1, c2 = st.columns([1, 1])
    with c1:
        if st.button("Load Demo Case", use_container_width=True):
            st.session_state["input_df"] = _demo_sample()
            st.session_state["input_source"] = "Synthetic demo case"
            st.session_state.pop("predictions", None)
            st.session_state.pop("quantum_predictions", None)
    with c2:
        uploaded = st.file_uploader("Upload CSV", type=["csv"], label_visibility="collapsed")
        if uploaded is not None:
            try:
                st.session_state["input_df"] = make_sample_frame(pd.read_csv(uploaded))
                st.session_state["input_source"] = uploaded.name
                st.session_state.pop("predictions", None)
                st.session_state.pop("quantum_predictions", None)
            except Exception as exc:
                st.error(f"Could not read CSV: {exc}")

    if "input_df" not in st.session_state:
        st.info("Load the prepared demo case or upload a CSV containing the 30 WDBC feature columns.")
        return

    df = st.session_state["input_df"]
    validation = validate_input(df)
    if validation["valid"]:
        st.success(f"Input loaded · {st.session_state.get('input_source', 'CSV')} · {len(df)} sample(s)")
    else:
        st.error("Input validation failed.")
        for error in validation["errors"]:
            st.write(f"• {error}")
        return

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Samples", len(df))
    m2.metric("Features", len(FEATURE_NAMES))
    m3.metric("Missing values", validation["missing_values"])
    m4.metric("Task", "Binary classification")

    st.markdown("### Input preview")
    st.dataframe(df.head(10), use_container_width=True, hide_index=True)

    st.markdown("### Data validation")
    pipeline(["Load", "Validate", "Preprocess", "Model", "Benchmark", "Explain"])
    for label in ["Dataset loaded", "Required features detected", "Missing-value check completed", "Identifiers excluded from prediction"]:
        st.write("✓ " + label)
    st.markdown('<div class="status-ok">Validation Status: PASS</div>', unsafe_allow_html=True)

    st.markdown("### Run analysis")
    if st.button("Run Classical Analysis", type="primary"):
        with st.status("Computing patient/sample predictions", expanded=True) as status:
            st.write("Validating feature schema")
            st.write("Applying StandardScaler")
            st.write("Running Logistic Regression")
            st.write("Running Classical SVM")
            st.write("Running XGBoost")
            predictions = predict_samples(df)
            st.session_state["predictions"] = predictions
            st.session_state["selected_sample"] = 0
            status.update(label="Classical analysis complete", state="complete")

    predictions = st.session_state.get("predictions")
    if predictions is None:
        return

    st.markdown("### Individual sample results")
    result_view = predictions.copy()
    result_view.insert(0, "Sample", df["sample_id"].astype(str).tolist())
    display_cols = ["Sample"] + [c for c in result_view.columns if c != "Sample" and "probability" not in c]
    st.dataframe(result_view[display_cols], use_container_width=True, hide_index=True)

    sample_labels = df["sample_id"].astype(str).tolist()
    selected = st.selectbox("Review sample", range(len(sample_labels)), format_func=lambda i: sample_labels[i])
    row = df.iloc[[selected]]
    result = predictions.iloc[selected]
    quality_z = float(_quality_flags(row).iloc[0])

    st.markdown("### Clinician review panel")
    a, b, c = st.columns(3)
    a.metric("Selected sample", sample_labels[selected])
    b.metric("Largest reference z-score", f"{quality_z:.1f}")
    agreement = sum(str(result[c]).startswith("Malignant") for c in predictions.columns if c.endswith(" class"))
    c.metric("Model agreement", f"{agreement}/{len([c for c in predictions.columns if c.endswith(' class')])}")
    if quality_z > 4:
        st.warning("Input contains at least one feature far outside the public WDBC training distribution. Treat the prediction as low-confidence and review the raw measurements.")
    else:
        st.info("Input distribution is within the simple reference range used by this prototype. This is a data-quality flag, not a clinical confidence measure.")

    cards = []
    for name in ["Logistic Regression", "Classical SVM", "XGBoost"]:
        cards.append((name, result[f"{name} class"], float(result[f"{name} probability"])))
    cols = st.columns(len(cards))
    for col, (name, label, prob) in zip(cols, cards):
        with col:
            st.markdown(f'<div class="result-card"><div class="result-kicker">{name}</div><div class="result-value">{label}</div><div class="result-meta">Model probability: {prob:.1%}</div></div>', unsafe_allow_html=True)

    st.markdown("### Local model explanation")
    explanation = explain_logistic_sample(row).head(8)
    st.caption("Logistic Regression contribution view. Contributions describe the model's calculation; they are not causal or clinical explanations.")
    st.dataframe(explanation, use_container_width=True, hide_index=True)

    st.markdown("### Quantum result")
    qpred = st.session_state.get("quantum_predictions")
    if qpred is not None:
        qrow = qpred.iloc[selected]
        st.markdown(f'<div class="result-card"><div class="result-kicker">QSVC · local Qiskit statevector simulation</div><div class="result-value">{qrow["Quantum class"]}</div><div class="result-meta">Decision score: {float(qrow["Quantum decision score"]):.3f}</div></div>', unsafe_allow_html=True)
    else:
        st.info("Run the quantum experiment from Quantum Analysis to add a measured local-Qiskit QSVC result to each sample.")

    st.warning("Research prototype only. Do not use these outputs as a diagnosis or treatment decision. The model was developed on the public WDBC dataset and has not undergone clinical validation.")
