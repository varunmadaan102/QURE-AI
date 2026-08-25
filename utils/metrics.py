import pandas as pd


def metrics_frame(results):
    return pd.DataFrame(results).T.reset_index().rename(columns={"index": "Model"})
