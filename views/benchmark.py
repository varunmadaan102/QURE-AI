import streamlit as st
import pandas as pd
from models.classical import fit_classical_benchmarks


def render():
    st.title("Model Benchmark")
    st.caption("Classical metrics are computed on the fixed WDBC hold-out split. The quantum benchmark is measured separately on its stated small subset.")
    if st.button("Run Classical Benchmark"):
        with st.spinner("Training classical baselines on the fixed WDBC split..."):
            try:
                results, _, _ = fit_classical_benchmarks()
                st.session_state["classical_benchmark"] = results
            except Exception as exc:
                st.error(f"Benchmark failed: {exc}")
    classical = st.session_state.get("classical_benchmark")
    if classical:
        frame = pd.DataFrame(classical).T
        st.markdown("### Computed classical results")
        st.dataframe(frame.style.format("{:.1%}"), use_container_width=True)
        best = max(classical.items(), key=lambda x: x[1]["F1"])[0]
        st.markdown("### Current best classical model")
        st.success(best)
    else:
        st.info("Run the classical benchmark to calculate the baseline metrics.")

    qresult = st.session_state.get("quantum_result")
    st.markdown("### Quantum benchmark")
    if qresult:
        qframe = pd.DataFrame([qresult["metrics"]], index=["QSVC · Qiskit statevector"])
        st.dataframe(qframe.style.format("{:.1%}"), use_container_width=True)
        st.caption(f"Measured on {qresult['train_size']} training samples and {qresult['test_size']} test samples using the four-component quantum interface.")
    else:
        st.info("Run the Qiskit QSVC experiment from Quantum Analysis to populate the measured quantum benchmark.")

    st.markdown("### Interpretation")
    st.markdown('<div class="research-note">The benchmark answers a research question: how does the measured quantum-kernel classifier compare with classical baselines under the stated preprocessing and evaluation setup? It does not establish clinical validity or quantum advantage.</div>', unsafe_allow_html=True)
