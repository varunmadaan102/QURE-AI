import streamlit as st


def render():
    st.title("About / Limitations")
    st.markdown("### What this prototype demonstrates")
    st.write("A research-oriented workflow combining classical ML with a quantum-kernel/QSVC concept, with benchmarking treated as an empirical question.")
    st.markdown("### Limitations")
    for item in [
        "WDBC is a small public dataset.",
        "It is not representative of all clinical populations.",
        "WDBC is a binary classification proof-of-concept.",
        "It does not establish prospective early-detection performance.",
        "Quantum-kernel computation can become expensive as dataset size grows.",
        "PCA can discard information.",
        "Simulator performance does not automatically transfer to real hardware.",
        "The model is not clinically validated.",
        "The system does not replace doctors.",
        "Quantum advantage is not assumed.",
    ]:
        st.write("• " + item)
    st.error("RESEARCH PROTOTYPE — NOT AN AUTONOMOUS DIAGNOSTIC SYSTEM")
    st.markdown("### Integration boundary")
    st.code("UI → structured result object\nmodels/classical.py\nmodels/quantum.py\n        ↓\nFuture API / experiment registry", language="text")
