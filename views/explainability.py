import streamlit as st
import pandas as pd
from demo.demo_results import ILLUSTRATIVE_EXPLANATION


def render():
    st.title("Explainability")
    st.caption("Model Explainability — Prototype")
    st.markdown("The current contribution chart is illustrative. Production implementation will connect an explanation method to the selected model.")
    frame = pd.DataFrame({"Feature": list(ILLUSTRATIVE_EXPLANATION.keys()), "Relative contribution": list(ILLUSTRATIVE_EXPLANATION.values())}).set_index("Feature")
    st.bar_chart(frame, horizontal=True)
    st.markdown('<div class="research-note">If SHAP is connected to a classical model, it should be labelled as a classical-model explanation. It should not be presented as an explanation of the internal quantum state.</div>', unsafe_allow_html=True)
