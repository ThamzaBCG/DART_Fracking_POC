
import pandas as pd
import numpy as np

from src.config import config

import src.constants.datasets as ds
import src.constants.query_parameters as q
import src.constants.general as g
import src.constants.completion_columns as cc

from src.data_extraction_utils import (
    retrieve_completion, 
    retrieve_completion_predictions,
    retrieve_completion_activity_summary
)

for stage in range(1, 55):

    print(f"Stage {stage} start")

    asset_id = 48334939

    # Fetch completion wits data
    df_completion = retrieve_completion(asset_id, stage, limit=100000)
    df_completion[cc.DATE] = pd.to_datetime(df_completion[cc.TIMESTAMP], unit='s')

    # Fetch completion predictions data
    df_breakdown, df_isip, df_owp = retrieve_completion_predictions(asset_id, stage)

    breakdown_list = list(df_breakdown["data.breakdown.timestamp"])

    isip_list = list(df_isip["data.isip.timestamp"])

    owp_list = list(df_owp["data.opening_wellhead_pressure.timestamp"])

    # Fetch activities data at end of the stage
    df_activity = retrieve_completion_activity_summary(asset_id, stage)

    # Identify Breackdown, ISIP, Wellhead Pressure points using completion predictions
    df_completion["fl_breakdown"] = np.where(
        df_completion[cc.TIMESTAMP].isin(breakdown_list), 1, 0)

    df_completion["fl_isip"] = np.where(
        df_completion[cc.TIMESTAMP].isin(isip_list), 1, 0)

    df_completion["fl_opening_wellhead_pressure"] = np.where(
        df_completion[cc.TIMESTAMP].isin(owp_list), 1, 0)
    
    pad_start = df_activity[df_activity["data.activities.activity"] == "Pad"]["data.activities.start"].values[0]
    pad_end = df_activity[df_activity["data.activities.activity"] == "Pad"]["data.activities.end"].values[0]

    df_completion["fl_rate_start"] = np.where(
        df_completion[cc.TIMESTAMP] == pad_start, 1, 0
    )

    df_completion["fl_proppant_injection"] = np.where(
        df_completion[cc.TIMESTAMP] == pad_end, 1, 0
    )

    # Save the into csv
    if stage == 1:
        df_completion.to_csv(config.output_dir / "completion_wits_48334939.csv", index = False)
    else:
        df_completion.to_csv(config.output_dir / "completion_wits_48334939.csv", 
                            mode = 'a', header = False, index = False)
        
    print(f"Stage {stage} finished")


df_completion = pd.read_csv(config.output_dir / "completion_wits_48334939.csv")
len(df_completion)


