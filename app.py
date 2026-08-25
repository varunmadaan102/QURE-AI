import streamlit as st


st.set_page_config(
    page_title="QureAI — Hybrid Quantum Disease-Risk Platform",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
:root {
    --bg:#050b14; --sidebar:#060e19; --panel:#091522; --panel2:#0b1827;
    --border:#1a3148; --strong:#23445f; --text:#edf5fc; --muted:#8ea3b8;
    --blue:#28b7ff; --green:#34d399; --purple:#a78bfa; --amber:#f5b942; --red:#fb7185;
}
.stApp {background:var(--bg); color:var(--text)}
[data-testid="stHeader"] {background:rgba(5,11,20,.92)}
[data-testid="stToolbar"] {opacity:.65}
.block-container {max-width:1180px; padding-top:1.6rem; padding-bottom:3rem}
section[data-testid="stSidebar"] {background:var(--sidebar); border-right:1px solid #14263a}
section[data-testid="stSidebar"] > div {padding-top:1.15rem}
h1,h2,h3,h4 {color:var(--text)!important; letter-spacing:-.025em}
h1 {font-size:2.1rem!important} h2 {font-size:1.45rem!important} h3 {font-size:1.05rem!important}
p,li,.stMarkdown {color:#c8d5e3}.small-muted{color:var(--muted);font-size:.78rem}
.brand{padding:.2rem .2rem .9rem}.brand-title{color:#f7fbff;font-size:1.45rem;font-weight:800;letter-spacing:-.03em}.brand-subtitle{color:var(--muted);font-size:.78rem;line-height:1.35}
.demo-banner{margin:.25rem 0 1rem;padding:.7rem .8rem;border-radius:10px;border:1px solid #6b5115;background:#12130f}.demo-banner strong{color:#ffd45e;font-size:.82rem}.demo-banner span{display:block;margin-top:.25rem;color:#aeb9c6;font-size:.72rem;line-height:1.4}
.nav-label{color:#5f88ad;font-size:.68rem;font-weight:800;letter-spacing:.09em;text-transform:uppercase;margin:.8rem 0 .3rem}
div[role="radiogroup"]{gap:.12rem}div[role="radiogroup"] label{border-radius:8px!important;padding:.38rem .5rem!important;color:#b9c7d8!important}div[role="radiogroup"] label:hover{background:#0d1b2d!important;color:#f2f7fc!important}div[role="radiogroup"] label[data-checked="true"]{background:#0b2038!important;color:#eaf7ff!important;border-left:2px solid var(--blue)}div[role="radiogroup"] label p{font-size:.84rem!important}
.hero{position:relative;overflow:hidden;padding:1.45rem 1.6rem;margin-bottom:1rem;border:1px solid #183451;border-radius:16px;background:radial-gradient(circle at 92% 25%,rgba(25,181,254,.15),transparent 25%),radial-gradient(circle at 78% 80%,rgba(167,139,250,.08),transparent 25%),linear-gradient(135deg,#07111e 0%,#091a2b 70%,#082338 100%)}
.hero h1{margin:0;font-size:2.35rem!important}.hero p{margin:.3rem 0 0;color:#b9c9da}.hero-tag{display:inline-block;margin-top:.8rem;color:#28c7ff;font-weight:700;font-size:.92rem}.hero-line{width:72px;height:3px;margin-top:.65rem;border-radius:4px;background:linear-gradient(90deg,#2563eb,#19b5fe)}
.q-card{height:100%;min-height:112px;padding:1rem 1.05rem;border:1px solid var(--border);border-radius:13px;background:linear-gradient(145deg,#0a1523,#09121e)}.q-card:hover{border-color:#275174}.q-card .kicker{color:#6f9fc6;font-size:.73rem;font-weight:800;letter-spacing:.05em;text-transform:uppercase}.q-card .title{margin-top:.25rem;color:#f3f7fb;font-weight:750;font-size:1rem;line-height:1.35}.q-card .body{margin-top:.4rem;color:#9eafc2;font-size:.82rem;line-height:1.45}.accent-blue{border-color:#164c75}.accent-green{border-color:#185642}.accent-purple{border-color:#48316d}.accent-amber{border-color:#614d1e}
.core-statement{padding:.95rem 1.05rem;border-radius:12px;background:linear-gradient(90deg,rgba(25,181,254,.07),rgba(167,139,250,.04));border:1px solid #1b3c59}.core-statement .quote{color:#25c4ff;font-size:1.05rem;font-weight:800}.core-statement .sub{color:#91a4b8;margin-top:.28rem;font-size:.8rem}
.research-note{padding:.8rem 1rem;border:1px solid #174764;border-left:3px solid var(--blue);background:#081827;border-radius:10px;color:#c7d7e7}
.pipeline-shell{width:100%;padding:.9rem;border:1px solid #172d43;border-radius:13px;background:#07111d;box-sizing:border-box}.pipeline-row{display:flex;align-items:center;width:100%;gap:9px}.pipeline-step{flex:1;min-width:0;min-height:70px;padding:.55rem .4rem;border:1px solid #21405d;border-radius:10px;background:#091827;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;box-sizing:border-box}.pipeline-number{color:#19b5fe;font-size:.68rem;font-weight:800;margin-bottom:.22rem}.pipeline-name{color:#dce8f3;font-size:.78rem;font-weight:650;line-height:1.2}.pipeline-arrow{flex:0 0 20px;text-align:center;color:#19b5fe;font-size:1rem}.pipeline-row-connector{height:23px;display:flex;align-items:center;justify-content:center;color:#19b5fe;font-size:1rem}
.result-card{padding:1.1rem 1.2rem;border:1px solid #21405d;border-radius:13px;background:#091827}.result-kicker{color:#6f9fc6;font-size:.72rem;font-weight:800;letter-spacing:.08em;text-transform:uppercase}.result-value{margin-top:.2rem;color:#f3f8fc;font-size:1.5rem;font-weight:800}.result-meta{margin-top:.2rem;color:#94a9bd;font-size:.78rem}
.status-ok{padding:.7rem .85rem;border:1px solid #185642;border-radius:9px;background:#0b3428;color:#b9f4db}.status-warn{padding:.7rem .85rem;border:1px solid #66521b;border-radius:9px;background:#211d0d;color:#f4d77c}.status-danger{padding:.7rem .85rem;border:1px solid #6a2937;border-radius:9px;background:#301720;color:#ffc4ce}
[data-testid="stVerticalBlockBorderWrapper"]{background:#091827;border-color:#21405d!important;border-radius:10px}div[data-testid="stMetric"]{background:#091522;border:1px solid #193149;border-radius:11px;padding:.7rem .8rem}div[data-testid="stMetricLabel"]{color:#8fa3b9!important}div[data-testid="stMetricValue"]{color:#f0f6fb!important}.stButton>button{border-radius:8px;border:1px solid #1d567d;background:#0b2943;color:#eaf7ff}.stButton>button:hover{border-color:#27bdfc;background:#0e3655}.stDataFrame,[data-testid="stTable"]{border:1px solid #1a3046;border-radius:10px}.stTabs [data-baseweb="tab"]{color:#8fa3b9}.stTabs [aria-selected="true"]{color:#27c4ff!important}code{background:#0b1725!important;color:#b9dcff!important}footer{visibility:hidden}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("""
    <div class="brand"><div class="brand-title">🧬 QureAI</div><div class="brand-subtitle">Hybrid Quantum<br>Disease-Risk Platform</div></div>
    <div class="demo-banner"><strong>◉ RESEARCH PROTOTYPE</strong><span>Classical inference is computed<br>Quantum simulation is measured locally</span></div>
    <div class="nav-label">Navigation</div>
    """, unsafe_allow_html=True)
    page = st.radio("Navigation", [
        "Overview", "Patient / Sample Analysis", "Preprocessing",
        "Quantum Analysis", "Model Benchmark", "Explainability", "About / Limitations"
    ], label_visibility="collapsed")
    st.markdown("""
    <div style="height:1px;background:#14263a;margin:1rem 0"></div>
    <div class="small-muted"><b style="color:#b8c9da">SIH 2026</b> · SIH26139</div>
    <div class="small-muted" style="margin-top:.35rem">Research prototype · Not clinically validated</div>
    """, unsafe_allow_html=True)


def render_selected_page(selected_page):
    # Keep page imports lazy so a broken optional view cannot blank the entire app.
    modules = {
        "Overview": ("views.overview", "render"),
        "Patient / Sample Analysis": ("views.analysis", "render"),
        "Preprocessing": ("views.preprocessing", "render"),
        "Quantum Analysis": ("views.quantum", "render"),
        "Model Benchmark": ("views.benchmark", "render"),
        "Explainability": ("views.explainability", "render"),
        "About / Limitations": ("views.limitations", "render"),
    }
    module_name, function_name = modules[selected_page]
    try:
        from importlib import import_module
        module = import_module(module_name)
        getattr(module, function_name)()
    except Exception as exc:
        st.error("This page could not be loaded.")
        st.exception(exc)
        st.info("The QureAI shell is running. Check the traceback above rather than restarting or moving files.")


render_selected_page(page)
