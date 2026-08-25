import streamlit as st


def pipeline(items):
    rows = [items] if len(items) <= 5 else [items[:4], items[4:]]
    html = '<div class="pipeline-shell">'
    number = 1
    for row_index, row in enumerate(rows):
        html += '<div class="pipeline-row">'
        for i, item in enumerate(row):
            html += (
                '<div class="pipeline-step">'
                f'<div class="pipeline-number">{number}</div>'
                f'<div class="pipeline-name">{item}</div>'
                '</div>'
            )
            if i < len(row) - 1:
                html += '<div class="pipeline-arrow">→</div>'
            number += 1
        html += '</div>'
        if row_index < len(rows) - 1:
            html += '<div class="pipeline-row-connector">↓</div>'
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)
