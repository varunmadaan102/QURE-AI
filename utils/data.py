from __future__ import annotations

import re
import numpy as np
import pandas as pd
from models.classical import FEATURE_NAMES


def _column_key(name: str) -> str:
    value = str(name).strip().lower().replace("_", " ")
    value = re.sub(r"\s+", " ", value)
    return value


def _aliases_for_feature(feature: str) -> set[str]:
    f = _column_key(feature)
    aliases = {f}
    if f.startswith("mean "):
        base = f[5:]
        aliases.add(f"{base} mean")
    elif f.endswith(" error"):
        base = f[:-6]
        aliases.update({f"{base} se", f"{base} error"})
    elif f.startswith("worst "):
        base = f[6:]
        aliases.add(f"{base} worst")
    return aliases


def normalize_wdbc_columns(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    lookup = {}
    for col in out.columns:
        lookup.setdefault(_column_key(col), col)
    rename = {}
    for feature in FEATURE_NAMES:
        if feature in out.columns:
            continue
        for alias in _aliases_for_feature(feature):
            source = lookup.get(alias)
            if source is not None:
                rename[source] = feature
                break
    if rename:
        out = out.rename(columns=rename)
    return out


def normalize_diagnosis_column(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    candidates = {"diagnosis", "target", "label", "class"}
    for col in out.columns:
        if _column_key(col) in candidates and col != "diagnosis":
            out = out.rename(columns={col: "diagnosis"})
            break
    if "diagnosis" in out.columns:
        values = out["diagnosis"].astype(str).str.strip().str.upper()
        mapping = {"M": "Malignant", "B": "Benign", "0": "Malignant", "1": "Benign", "MALIGNANT": "Malignant", "BENIGN": "Benign"}
        out["diagnosis"] = values.map(lambda x: mapping.get(x, x))
    return out


def validate_input(df: pd.DataFrame):
    df = normalize_diagnosis_column(normalize_wdbc_columns(df))
    errors = []
    if len(df) == 0:
        errors.append("The uploaded CSV contains no rows.")
    required = [c for c in FEATURE_NAMES if c not in df.columns]
    if required:
        errors.append(f"Missing {len(required)} required WDBC feature columns.")
        return {"valid": False, "errors": errors, "missing": required, "numeric": False, "missing_values": None, "rows": len(df)}
    try:
        feature_df = df[FEATURE_NAMES].apply(pd.to_numeric, errors="raise")
        numeric = True
    except Exception:
        feature_df = None
        numeric = False
        errors.append("One or more required feature columns contain non-numeric values.")
    missing_values = int(feature_df.isna().sum().sum()) if feature_df is not None else None
    if missing_values:
        errors.append(f"Found {missing_values} missing feature values.")
    if feature_df is not None and not np.isfinite(feature_df.to_numpy()).all():
        errors.append("One or more feature values are infinite or non-finite.")
    return {"valid": not errors, "errors": errors, "missing": required, "numeric": numeric, "missing_values": missing_values, "rows": len(df)}


def make_sample_frame(df: pd.DataFrame):
    out = normalize_diagnosis_column(normalize_wdbc_columns(df))
    if "index" not in out.columns:
        out.insert(0, "index", range(len(out)))
    if "sample_id" not in out.columns:
        out.insert(1, "sample_id", [f"WDBC-INPUT-{i+1:03d}" for i in range(len(out))])
    return out
