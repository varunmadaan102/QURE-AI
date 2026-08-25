import streamlit as st
from models.classical import fit_pca
from components.pipeline import pipeline


def render():
    st.title("Preprocessing")
    st.caption("The preprocessing basis is fitted on the training split and reused for held-out data. The quantum interface uses four PCA components.")
    pipeline(["30 original features", "StandardScaler", "PCA", "4 quantum-compatible components"])
    st.markdown("### Step 1 — Standardization")
    st.code("StandardScaler", language="text")
    st.write("Features are standardized before dimensionality reduction so measurements on different scales contribute comparably.")
    st.markdown("### Step 2 — PCA")
    try:
        _, pca, X_train_pca, _, _, _ = fit_pca()
        explained = pca.explained_variance_ratio_
        cols = st.columns(4)
        for c, label, val in zip(cols, ["PC1", "PC2", "PC3", "PC4"], explained):
            c.metric(label, f"{val:.1%}")
        st.metric("Variance retained by four components", f"{explained.sum():.1%}")
        st.markdown("### Example transformed training sample")
        row = X_train_pca[0]
        cols = st.columns(4)
        for c, label, val in zip(cols, ["PC1", "PC2", "PC3", "PC4"], row):
            c.metric(label, f"{val:.3f}")
        st.caption("The example is a transformed dataset sample, not a patient-specific result.")
    except Exception as exc:
        st.warning(f"PCA computation unavailable: {exc}")
    st.markdown('<div class="research-note">PCA is used to compress the 30-feature WDBC representation into four inputs for the four-qubit experiment. Dimensionality reduction alone is not evidence of quantum advantage.</div>', unsafe_allow_html=True)
