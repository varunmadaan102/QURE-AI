import streamlit as st


def conceptual_circuit():
    st.markdown("### 4-qubit feature map")
    st.code(
        """Q0 ── RY(PC1) ──●────────
                 │
Q1 ── RY(PC2) ──X────────

Q2 ── RY(PC3) ──●────────
                 │
Q3 ── RY(PC4) ──X────────""",
        language="text",
    )
    st.caption("Conceptual feature-map circuit. It is illustrative unless connected to an executed Qiskit pipeline.")
