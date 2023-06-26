
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go

import src.constants.datasets as ds
import src.constants.query_parameters as q
import src.constants.general as g
import src.constants.completion_columns as cc


def treatment_plot(df, witdh):
    """
    Create treatment plot from Corva dashboard
    """

    fig, ax1 = plt.subplots(figsize=(witdh, 6))

    # Wellhead pressure
    ax1.plot(df[cc.TIMESTAMP], df[cc.WELLHEAD_PRESSURE], 'r-', label='Wellhead Pressure')
    ax1.set_xlabel('Timestamp')
    ax1.set_ylabel('Pressure (psi)', color='r')
    ax1.tick_params('y', colors='r')

    # Slurry Flow Rate
    ax2 = ax1.twinx()
    ax2.plot(df[cc.TIMESTAMP], df[cc.SLURRY_FLOW_RATE_IN], 'b-', label='Slurry Flow Rate')
    ax2.set_ylabel('Flow Rate (bbl/min)', color='b')
    ax2.tick_params('y', colors='b')

    ax3 = ax1.twinx()
    ax3.spines['right'].set_position(('outward', 40))  
    ax3.plot(df[cc.TIMESTAMP], df[cc.TOTAL_PROPPANT_CONCENTRATION], 'orange', label='Total Proppant Conc')
    ax3.set_ylabel('Proppant Conc (lb/gal)', color='orange')
    ax3.tick_params('y', colors='orange')

    ax4 = ax1.twinx()
    ax4.spines['right'].set_position(('outward', 80))  
    ax4.plot(df[cc.TIMESTAMP], df[cc.TOTAL_PROPPANT_MASS], 'yellow', label='Total Proppant Volume')
    ax4.set_ylabel('Proppant Mass (lb)', color='yellow')
    ax4.tick_params('y', colors='yellow')

    ax5 = ax1.twinx()
    ax5.spines['right'].set_position(('outward', 140))  
    ax5.plot(df[cc.TIMESTAMP], df[cc.TOTAL_SLURRY_VOLUME_IN], 'purple', label='Slurry Volume')
    ax5.set_ylabel('Total Volume (bbl)', color='purple')
    ax5.tick_params('y', colors='purple')

    # Ajustar los subplots
    fig.tight_layout()

    return fig


def treatment_plot_plotly(df, xaxis):

    var_dict = {
        "Wellhead Pressure": {"var": cc.WELLHEAD_PRESSURE, "axis_title": "Pressure (psi)", "color": "#d62728"},
        "Slurry Flow Rate": {"var": cc.SLURRY_FLOW_RATE_IN, "axis_title": "Flow Rate (bbl/min)", "color": "#1f77b4"},
        "Total Proppant Conc": {"var": cc.TOTAL_PROPPANT_CONCENTRATION, "axis_title": "Proppant Conc (lb/gal)", "color": "#ff7f0e"},
        "Total Proppant Volume": {"var": cc.TOTAL_PROPPANT_MASS, "axis_title": "Proppant Mass (lb)", "color": "#FFCD00"},
        "Slurry Volume": {"var": cc.TOTAL_SLURRY_VOLUME_IN, "axis_title": "Total Volume (bbl)", "color": "#9467bd"}
    }

    parameters_dict = {
        "2023-06-13 06:17:36": {"line_width": 3, "line_dash": "dash", "color": "#d62728", "text": "ISIP", "text_size": 12, "text_family": "Courier New, monospace"},
        "2023-06-13 04:33:57": {"line_width": 3, "line_dash": "dash", "color": "#d62728", "text": "Breackdown", "text_size": 12, "text_family": "Courier New, monospace"},
        "2023-06-13 04:19:11": {"line_width": 3, "line_dash": "dash", "color": "#00FFFF", "text": "Rate start", "text_size": 12, "text_family": "Courier New, monospace"},
        "2023-06-13 04:19:08": {"line_width": 3, "line_dash": "dash", "color": "#00FF7F", "text": "Opening Wellhead Pressure", "text_size": 12, "text_family": "Courier New, monospace"},
        "2023-06-13 04:35:46": {"line_width": 3, "line_dash": "dash", "color": "#FFA500", "text": "Proppant Injection", "text_size": 12, "text_family": "Courier New, monospace"},
    }

    fig = go.Figure()

    k = 1
    for var in var_dict.keys():

        fig.add_trace(go.Scatter(
            x=df[xaxis],
            y=df[var_dict[var]["var"]],
            name=var,
            line=dict(color=var_dict[var]["color"]),
            yaxis= f"y{k}"
        ))

        k = k + 1

    for param in parameters_dict.keys():

        fig.add_vline(
            x=param, 
            line_width=parameters_dict[param]["line_width"], 
            line_dash=parameters_dict[param]["line_dash"], 
            line_color=parameters_dict[param]["color"]
            )
        
        fig.add_annotation(
            x=param,
            y=max(df[cc.WELLHEAD_PRESSURE]),
            text=parameters_dict[param]["text"],
            font=dict(
                family=parameters_dict[param]["text_family"],
                size=parameters_dict[param]["text_size"],
                color=parameters_dict[param]["color"]
            )
        )


    # Create axis objects
    fig.update_layout(
        xaxis=dict(domain=[0.1, 0.85]),
        yaxis=dict(
            title=var_dict["Wellhead Pressure"]["axis_title"],
            titlefont=dict(
                color=var_dict["Wellhead Pressure"]["color"]
            ),
            tickfont=dict(
                color=var_dict["Wellhead Pressure"]["color"]
            )
        ),
        yaxis2=dict(
            title=var_dict["Slurry Flow Rate"]["axis_title"],
            titlefont=dict(
                color=var_dict["Slurry Flow Rate"]["color"]
            ),
            tickfont=dict(
                color=var_dict["Slurry Flow Rate"]["color"]
            ),
            overlaying="y",
            side="right"
        ),
        yaxis3=dict(
            title=var_dict["Total Proppant Conc"]["axis_title"],
            titlefont=dict(
                color=var_dict["Total Proppant Conc"]["color"]
            ),
            tickfont=dict(
                color=var_dict["Total Proppant Conc"]["color"]
            ),
            anchor="free",
            overlaying="y",
            side="left",
            position = 0.05
        ),
        yaxis4=dict(
            title=var_dict["Total Proppant Volume"]["axis_title"],
            titlefont=dict(
                color=var_dict["Total Proppant Volume"]["color"]
            ),
            tickfont=dict(
                color=var_dict["Total Proppant Volume"]["color"]
            ),
            anchor="free",
            overlaying="y",
            side="right",
            position = 0.9
        ),
        yaxis5=dict(
            title=var_dict["Slurry Volume"]["axis_title"],
            titlefont=dict(
                color=var_dict["Slurry Volume"]["color"]
            ),
            tickfont=dict(
                color=var_dict["Slurry Volume"]["color"]
            ),
            anchor="free",
            overlaying="y",
            side="right",
            position = 0.95
        )
    )

    # Update layout properties
    fig.update_layout(
        title_text="Treatment plot",
        width=1800
    )

    fig.update_layout(hovermode="x unified")

    return fig


def completion_plot_events(df, dom = [0.15, 0.9], colors = g.PALETTE):

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df[cc.TIMESTAMP],
        y=df[cc.WELLHEAD_PRESSURE],
        name="Wellhead Pressure",
        line=dict(color=colors[0]),
        yaxis= "y1"
    ))

    fig.add_trace(go.Scatter(
        x=df[cc.TIMESTAMP],
        y=df[cc.SLURRY_FLOW_RATE_IN],
        name="Slurry Flow Rate",
        line=dict(color=colors[1]),
        yaxis= "y2"
    ))

    fig.add_trace(go.Scatter(
        x=df[cc.TIMESTAMP],
        y=df[cc.TOTAL_PROPPANT_CONCENTRATION],
        name="Total proppant conc",
        line=dict(color=colors[2]),
        yaxis= "y3"
    ))

    fig.add_trace(go.Scatter(
        x= df[df["fl_isip_est"] == 1][cc.TIMESTAMP],
        y= df[df["fl_isip_est"] == 1][cc.WELLHEAD_PRESSURE],
        mode='markers',
        marker=dict(size=10),
        name="ISIP Est."
    ))

    fig.add_trace(go.Scatter(
        x= df[df["fl_isip"] == 1][cc.TIMESTAMP],
        y= df[df["fl_isip"] == 1][cc.WELLHEAD_PRESSURE],
        mode='markers',
        marker=dict(size=10),
        name="ISIP Corva"
    ))

    fig.add_trace(go.Scatter(
        x= df[df["fl_rate_start_est"] == 1][cc.TIMESTAMP],
        y= df[df["fl_rate_start_est"] == 1][cc.SLURRY_FLOW_RATE_IN],
        mode='markers',
        marker=dict(size=10),
        name="Rate Start Est."
    ))

    fig.add_trace(go.Scatter(
        x= df[df["fl_rate_start"] == 1][cc.TIMESTAMP],
        y= df[df["fl_rate_start"] == 1][cc.SLURRY_FLOW_RATE_IN],
        mode='markers',
        marker=dict(size=10),
        name="Rate Start Corva"
    ))

    fig.add_trace(go.Scatter(
        x= df[df["fl_proppant_injection_est"] == 1][cc.TIMESTAMP],
        y= df[df["fl_proppant_injection_est"] == 1][cc.SLURRY_FLOW_RATE_IN],
        mode='markers',
        marker=dict(size=10),
        name="Proppant injection Est."
    ))

    fig.add_trace(go.Scatter(
        x= df[df["fl_proppant_injection"] == 1][cc.TIMESTAMP],
        y= df[df["fl_proppant_injection"] == 1][cc.SLURRY_FLOW_RATE_IN],
        mode='markers',
        marker=dict(size=10),
        name="Proppant injection Corva"
    ))

    fig.update_layout(
            xaxis=dict(domain=dom, showgrid=False),
            yaxis=dict(
                title="PSI",
                titlefont=dict(
                    color=colors[0]
                ),
                tickfont=dict(
                    color=colors[0]
                ),
                showgrid=False
            ),
            yaxis2=dict(
                title="Flow rate",
                titlefont=dict(
                    color=colors[1]
                ),
                tickfont=dict(
                    color=colors[1]
                ),
                overlaying="y",
                side="right",
                showgrid=False
            ),
            yaxis3=dict(
                title="Total proppant conc",
                titlefont=dict(
                    color=colors[2]
                ),
                tickfont=dict(
                    color=colors[2]
                ),
                anchor="free",
                overlaying="y",
                side="left",
                position = 0.05
            ),
    )

    fig.update_layout(
        title_text="Treatment plot",
        hovermode="x unified"
    )

    return fig


def line_chart_multi_axis(df, x, var_list, colors=g.PALETTE, dom=[0.15, 0.85], template = "plotly_dark"):


    fig = go.Figure()

    k = 0
    for var in var_list:

        fig.add_trace(go.Scatter(
            x=df[x],
            y=df[var],
            name=var,
            line=dict(color=colors[k]),
            yaxis= f"y{k+1}"
        ))

        k = k + 1

    fig.update_layout(
        xaxis=dict(domain=dom, showgrid=False),
        yaxis=dict(
            title=var_list[0],
            titlefont=dict(
                color=colors[0]
            ),
            tickfont=dict(
                color=colors[0]
            ),
            showgrid=False
        ),
        yaxis2=dict(
            title=var_list[1],
            titlefont=dict(
                color=colors[1]
            ),
            tickfont=dict(
                color=colors[1]
            ),
            overlaying="y",
            side="right",
            showgrid=False
        )
    )

    if len(var_list) > 2:
        k = 2

        for var in var_list[2:]:
            
            side = "left" if k%2 == 0 else 'right'
            pos = dom[0]- 0.05*int(k/2) if k%2 == 0 else dom[1] + 0.05*int(k/2)

            if k == 2:

                fig.update_layout(
                    yaxis3 = dict(
                        title=var_list[k],
                        titlefont=dict(
                                color=colors[k]
                            ),
                            tickfont=dict(
                                color=colors[k]
                            ),
                        anchor="free",
                        overlaying="y",
                        side=side,
                        position=pos,
                        showgrid=False
                    )
                )
            
            if k == 3:

                fig.update_layout(
                    yaxis4 = dict(
                        title=var_list[k],
                        titlefont=dict(
                                color=colors[k]
                            ),
                            tickfont=dict(
                                color=colors[k]
                            ),
                        anchor="free",
                        overlaying="y",
                        side=side,
                        position=pos,
                        showgrid=False
                    )
                )

            if k == 4:

                fig.update_layout(
                    yaxis5 = dict(
                        title=var_list[k],
                        titlefont=dict(
                                color=colors[k]
                            ),
                            tickfont=dict(
                                color=colors[k]
                            ),
                        anchor="free",
                        overlaying="y",
                        side=side,
                        position=pos,
                        showgrid=False
                    )
                )

            k = k + 1

    fig.update_layout(
        title_text="Default",
        width=1800,
        hovermode="x unified",
        template=template
    )

    # fig.update_layout(hovermode="x unified")

    fig.show()