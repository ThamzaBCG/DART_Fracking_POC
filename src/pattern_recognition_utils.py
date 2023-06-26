import pandas as pd
import numpy as np
import math

from src.data_extraction_utils import retrieve_completion, retrieve_completion_latest
from src.plot_utils import treatment_plot, treatment_plot_plotly

from src.config import config

import src.constants.datasets as ds
import src.constants.query_parameters as q
import src.constants.general as g
import src.constants.completion_columns as cc

import plotly.subplots as sp
import plotly.graph_objects as go


def first_derivative(x, y):
    """
    Return the first derivative for a serie
    """

    n = len(x)
    dx = x[1] - x[0]  # Suponemos que los puntos están igualmente espaciados
    dy = np.zeros(n)
    
    # Aproximación de la primera derivada utilizando diferencia central
    for i in range(1, n-1):   
        dy[i] = (y[i+1] - y[i-1]) / (2*dx)
    
    # Aproximación de la primera derivada en los extremos utilizando diferencia hacia adelante y hacia atrás
    dy[0] = (y[1] - y[0]) / dx
    dy[n-1] = (y[n-1] - y[n-2]) / dx
    
    return dy


def second_derivative(x, y):
    """
    return second derivative for a serie
    """

    n = len(x)
    dx = x[1] - x[0]  # Suponemos que los puntos están igualmente espaciados
    d2x = np.zeros(n)
    
    # Aproximación de la segunda derivada utilizando diferencia central
    for i in range(1, n-1):
        d2x[i] = (y[i+1] - 2*y[i] + y[i-1]) / (dx**2)
    
    # Aproximación de la segunda derivada en los extremos utilizando diferencia hacia adelante y hacia atrás
    d2x[0] = (y[2] - 2*y[1] + y[0]) / (dx**2)
    d2x[n-1] = (y[n-1] - 2*y[n-2] + y[n-3]) / (dx**2)
    
    return d2x


def remove_nan(l):
    """
    Remvove nan's in a list
    """
    return [x for x in l if not math.isnan(x)]


def calculate_amplitude(window):
    """
    Calculate the amplitude for last n rows (window)
    """
    return max(window) - min(window)


def completion_preprocess(df, local_max_th = 10, local_min_th = 1.1):

    # 1st & 2cd derivatives for Wellhead pressure and Slurry flow rate
    df = df.sort_values(by=cc.TIMESTAMP, ascending=True)

    # Rolling average of flow rates
    df["flow_rate_rolling_avg"] = df[cc.SLURRY_FLOW_RATE_IN].rolling(window=3).mean()

    # flagging peaks
    df["fl_peak"] = np.where(
        ((df["flow_rate_rolling_avg"] / df[cc.SLURRY_FLOW_RATE_IN]) > local_min_th)
        & (df[cc.SLURRY_FLOW_RATE_IN] > 0),
        1, 0)

    df["fl_peak"] =np.where(
        ((df[cc.SLURRY_FLOW_RATE_IN] / df["flow_rate_rolling_avg"]) > local_max_th)
        & (df[cc.SLURRY_FLOW_RATE_IN] > 0),
        1, df["fl_peak"]
    )

    df["fl_peak"] = np.where(
        (df['fl_peak'].shift(1) == 1) | (df['fl_peak'].shift(-1) == 1), 
        1, df["fl_peak"]
    )

    df[cc.D_WELLHEAD_PRESSURE] = first_derivative(list(df[cc.TIMESTAMP]), list(df[cc.WELLHEAD_PRESSURE]))
    df[cc.D2_WELLHEAD_PRESSURE] = second_derivative(list(df[cc.TIMESTAMP]), list(df[cc.WELLHEAD_PRESSURE]))

    df[cc.D_SLURRY_FLOW_RATE] = first_derivative(list(df[cc.TIMESTAMP]), list(df[cc.SLURRY_FLOW_RATE_IN]))
    df[cc.D2_SLURRY_FLOW_RATE] = second_derivative(list(df[cc.TIMESTAMP]), list(df[cc.SLURRY_FLOW_RATE_IN]))

    df[cc.D_TOTAL_PROPPANT_CONC] = first_derivative(list(df[cc.TIMESTAMP]), list(df[cc.TOTAL_PROPPANT_CONCENTRATION]))
    df[cc.D2_TOTAL_PROPPANT_CONC] = second_derivative(list(df[cc.TIMESTAMP]), list(df[cc.TOTAL_PROPPANT_CONCENTRATION]))

    # Remove peaks
    df[cc.D_SLURRY_FLOW_RATE] = np.where(df["fl_peak"] == 1, 0, df[cc.D_SLURRY_FLOW_RATE])

    # Rolling variance of Wellhead pressure
    # df["d_pressure_rolling_variance"] = df["d_slurry_flow_rate"].rolling(window=10).var()

    # Previous/post value
    # df[cc.SLURRY_FLOW_RATE_IN + "_prv"] = df[cc.SLURRY_FLOW_RATE_IN].shift()
    # df[cc.SLURRY_FLOW_RATE_IN + "_post"] = df[cc.SLURRY_FLOW_RATE_IN].shift(-1)

    # Amplitude for waves section
    df[cc.A_D_WELLHEAD_PRESSURE] = df["d_wellhead_pressure"].rolling(window=5).apply(calculate_amplitude)

    return df


# Functions to detect oscilation on curves

def remove_consecutive_ts(ts_array, upper_th = 2, bottom_th = 1):

    ts_array = np.sort(ts_array)

    ts_shift = ts_array[0:-1]

    ts_shift = np.insert(ts_shift, 0, ts_shift[0])

    dist = ts_array - ts_shift

    return ts_array[(dist < bottom_th) | (dist > upper_th)]


def detect_oscilations(df, perct_th = 0.01, ampl_th = 5, save_image = False):

    """
    Inputs:
        df: a dataframe filtered by a specific stage
    Outputs:
        df: a dataframe with additional column "fl_wave_area", which identify the oscilation area
    """

    # initiate flag
    df["fl_wave_area"] = 0
    df["wave_area_order"] = 0

    perct = np.percentile(df["d_slurry_flow_rate"], perct_th)

    print(perct)

    ts_list = np.array(df[df["d_slurry_flow_rate"] <= perct][cc.TIMESTAMP])

    if len(ts_list) > 1: ts_list = remove_consecutive_ts(ts_list, 20, 10)

    print(ts_list)
    # if len(ts_list) == 0: print(f"Haven't found any time with this threshold: {perct_th}")
    
    max_ts = df[cc.TIMESTAMP].max()

    k = 1
    for ts in ts_list:
        print(f"start: {ts}")
        while abs(df.loc[df[cc.TIMESTAMP] == ts, "a_d_wellhead_pressure"].values[0]) > ampl_th:
            
            # print(ts, df.loc[df[cc.TIMESTAMP] == ts, "a_d_wellhead_pressure"].values[0])
            df.loc[df[cc.TIMESTAMP] == ts, 'fl_wave_area'] = 1
            df.loc[df[cc.TIMESTAMP] == ts, 'wave_area_order'] = k
            
            ts = ts + 1
            while (len(df[df[cc.TIMESTAMP] == ts]) == 0) & (ts < max_ts):
                ts = ts + 1
        k = k + 1

    if save_image == True:
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=df[cc.TIMESTAMP],
            y=df[cc.WELLHEAD_PRESSURE],
            name="Wellhead Pressure",
            line=dict(color="blue"),
            yaxis= "y1"
        ))

        fig.add_trace(go.Scatter(
            x=df[df["fl_wave_area"] == 1][cc.TIMESTAMP],
            y=df[df["fl_wave_area"] == 1][cc.WELLHEAD_PRESSURE],
            name="Oscilation",
            mode='markers',
            marker=dict(color="red"),
            yaxis= "y1"
        ))

        fig.update_layout(
            title_text="Default",
            hovermode="x unified",
            template="plotly_dark"
        )

        fig.show()
    
    return df


# ISIP event
def detect_isip(df, save_image = False):

    """
    input:
        df: completion dataframe filtered by oscilation area
    output:
        x_intersc: ISIP timestamp 
    """
    
    x = cc.TIMESTAMP
    y = cc.WELLHEAD_PRESSURE

    coefficients = np.polyfit(df[x], df[y], 1)
    slope = coefficients[0]
    intercept = coefficients[1]

    df["y_est"] = slope*df[x] + intercept

    df["ts_next"] = df[x] + 1

    df_right = df[[x, y]]
    df_right = df_right.rename(columns={y : "y_next"})

    df = df.merge(
        df_right,
        how = 'left',
        left_on = "ts_next",
        right_on = x
    )

    df = df.drop(columns=["timestamp_y"])

    df = df.rename(columns={"timestamp_x" : "timestamp"})

    df['fl_intersc'] = np.where(
        (df[y] <= df["y_est"]) & (df["y_est"] <= df["y_next"]),
        1, 0
    )

    x_intersc = df[df['fl_intersc'] == 1][x].min()

    if save_image == True:

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=df[x],
            y=df[y],
            name="Wellhead pressure",
            line=dict(color="blue"),
            yaxis= "y1"
        ))

        fig.add_trace(go.Scatter(
            x=df[x],
            y=slope * df[x] + intercept,
            name="lineal regression",
            line=dict(color="red")
        ))

        fig.add_trace(go.Scatter(
            x= [x_intersc],
            y= df[df[x] == x_intersc][y],
            mode='markers',
            marker=dict(size=10),
            name="Intersec"
        ))

        fig.update_layout(
            title_text="Default",
            hovermode="x unified",
            template="plotly_dark"
        )

        fig.show()

    return x_intersc