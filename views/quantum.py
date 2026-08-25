import streamlit as st
from components.pipeline import pipeline
from components.circuit import conceptual_circuit
from models.quantum import get_quantum_execution_status, run_quantum_benchmark, predict_quantum_samples, quantum_status


def render():
    st.title("Quantum Analysis")
    st.caption("Measured local Qiskit statevector experiment using a four-qubit feature map and quantum kernel QSVC.")
    pipeline(["PCA Features", "Quantum Feature Map", "Quantum Kernel", "QSVC", "Prediction"])

    st.markdown("### Quantum Feature Map")
    st.caption("The four PCA components are angle-encoded with RY rotations followed by a linear entangling chain.")
    conceptual_circuit()

    st.markdown("### What is actually executed")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Quantum kernel**")
        st.write("Qiskit constructs a fidelity-based statevector kernel from the feature map. Kernel values are calculated from overlaps between encoded quantum states.")
    with c2:
        st.markdown("**Hybrid QSVC**")
        st.write("The measured quantum kernel is supplied to QSVC, which performs the classical support-vector optimization around that kernel.")

    st.markdown("### Run quantum experiment")
    st.caption("The local experiment uses a bounded stratified subset so it remains practical on a laptop/Streamlit instance. This is a simulation, not real QPU execution.")
    if st.button("Run Qiskit QSVC Experiment", type="primary"):
        with st.status("Running Qiskit statevector experiment", expanded=True) as status:
            try:
                result = run_quantum_benchmark()
                st.session_state["quantum_result"] = result
                if "input_df" in st.session_state:
                    st.session_state["quantum_predictions"] = predict_quantum_samples(result, st.session_state["input_df"])
                status.update(label="Quantum experiment complete", state="complete")
            except Exception as exc:
                status.update(label="Quantum experiment unavailable", state="error")
                st.error(str(exc))
                st.info("The classical application remains usable. Check that qiskit and qiskit-machine-learning are installed from requirements.txt.")

    result = st.session_state.get("quantum_result")
    if result:
        st.markdown("### Measured quantum benchmark")
        cols = st.columns(5)
        for col, (metric, value) in zip(cols, result["metrics"].items()):
            col.metric(metric, f"{value:.1%}")
        a, b, c = st.columns(3)
        a.metric("Quantum train samples", result["train_size"])
        b.metric("Quantum test samples", result["test_size"])
        c.metric("Execution time", f"{result['elapsed_seconds']:.2f} s")
        st.success("QSVC result above was computed by the local Qiskit statevector simulation.")
        st.caption("These metrics are measured simulation results for the stated subset and configuration. They do not demonstrate quantum advantage or clinical validity.")

        st.markdown("### Individual quantum predictions")
        qp = st.session_state.get("quantum_predictions")
        if qp is not None and "input_df" in st.session_state:
            view = qp.copy()
            view.insert(0, "Sample", st.session_state["input_df"]["sample_id"].astype(str).tolist())
            st.dataframe(view, use_container_width=True, hide_index=True)
    else:
        status = get_quantum_execution_status()
        a, b, c = st.tabs(["Local statevector", "Noisy experiment", "Real QPU — Optional"])
        with a:
            st.info(status["ideal_simulator"])
        with b:
            st.info(status["noisy_simulator"])
        with c:
            st.info(status["real_qpu"])

    st.markdown("### Research boundary")
    st.markdown('<div class="research-note">The quantum layer is a measured local simulation. It is included to test the hybrid QML hypothesis; no quantum advantage is assumed, and no real hardware claim is made.</div>', unsafe_allow_html=True)
