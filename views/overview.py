import streamlit as st
from components.pipeline import pipeline


def render():
    st.markdown("""
    <div class="hero"><h1>QureAI</h1><p>Hybrid Quantum Machine Learning for Biomedical Risk Prediction</p><div class="hero-tag">We don't assume quantum advantage. We measure it.</div><div class="hero-line"></div></div>
    """, unsafe_allow_html=True)
    st.markdown("### Platform at a glance")
    cards = [
        ("Biomedical Data", "WDBC", "569 samples · 30 continuous features", "accent-blue"),
        ("Classical ML", "SVM · XGBoost · Logistic Regression", "Scikit-learn / XGBoost", "accent-green"),
        ("Quantum ML", "Quantum Kernel + QSVC", "Qiskit-ready hybrid workflow", "accent-purple"),
        ("Benchmarking", "Accuracy · F1 · ROC-AUC", "Measured comparison when experiments are connected", "accent-amber"),
    ]
    cols = st.columns(4, gap="small")
    for col, (kicker, title, body, accent) in zip(cols, cards):
        with col:
            st.markdown(f'<div class="q-card {accent}"><div class="kicker">{kicker}</div><div class="title">{title}</div><div class="body">{body}</div></div>', unsafe_allow_html=True)
    st.write("")
    st.markdown("### Research pipeline")
    pipeline(["Biomedical Data", "Validation", "Scaling + PCA", "Classical + Quantum ML", "Benchmark", "Model Selection", "Risk Prediction", "Explainability"])
    st.write("")
    st.markdown('<div class="core-statement"><div class="quote">We don\'t assume quantum advantage. We measure it.</div><div class="sub">The platform is designed to compare strong classical baselines with a quantum-kernel branch under a common evaluation protocol.</div></div>', unsafe_allow_html=True)
    st.write("")
    c1,c2,c3=st.columns([1.2,1.2,1])
    with c1:
        st.markdown("**Proof-of-concept dataset**"); st.caption("Breast Cancer Wisconsin (Diagnostic) / WDBC"); st.write("569 samples · 30 predictive features · binary M/B target")
    with c2:
        st.markdown("**Current prototype**"); st.caption("Interactive demo + computed classical branch"); st.write("CSV validation, preprocessing, classical inference and quantum workflow visualization")
    with c3:
        st.markdown("**Status**"); st.caption("Research prototype"); st.write("Quantum benchmark values remain illustrative until measured")
    st.caption("Research prototype — not a clinically validated diagnostic system.")
