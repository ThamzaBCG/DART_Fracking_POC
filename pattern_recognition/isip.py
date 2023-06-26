import pandas as pd
import numpy as np

from src.config import config

import src.constants.datasets as ds
import src.constants.query_parameters as q
import src.constants.general as g
import src.constants.completion_columns as cc
from src.pattern_recognition_utils import *

import plotly.subplots as sp
import plotly.graph_objects as go


def flagging_isip(df):

    """
    Flagging ISIP events stage by stage for the input dataframe
    """

    # Preprocess the data
    df = completion_preprocess(df)

    isip_list = []
    stages = df[cc.STAGE_NUMBER].unique()
    for stage in stages:

        print(f"Comienza stage {stage}")

        df_output = detect_oscilations(df[df[cc.STAGE_NUMBER] == stage])

        waves = df_output[df_output["fl_wave_area"] == 1]["wave_area_order"].unique()

        for wave in waves:
            isip = detect_isip(df_output[df_output["wave_area_order"] == wave])
            isip_list.append(isip)

            print(f"Isip encontrado en: {isip}")

        print(f"Finzaliza stage {stage}")


    df["fl_isip_est"] = np.where(df[cc.TIMESTAMP].isin(isip_list), 1, 0)

    return df