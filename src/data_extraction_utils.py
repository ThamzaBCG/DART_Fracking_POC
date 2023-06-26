import requests
import pandas as pd
import json
import os

from src.config import config

import src.constants.datasets as ds
import src.constants.query_parameters as q
import src.constants.general as g


def clean_column_names(df, word_to_remove):
    """
    Remove columname prefix
    """

    # Identify columns which name start with word_to_remove
    column_list = [col for col in df.columns if col.startswith(word_to_remove)]

    # For each column rename it with out word_to_remove
    for col in column_list:
        new_name = col.split(".", 1)[1]  
        df = df.rename(columns={col: new_name})
    
    return df


def retrieve_completion(asset_id, stage_number, limit = 10000, company_id = q.COMPANY_ID):
    """
    Return a Pandas DataFrame with a specific asset and stage
    """

    url = f"""
        https://api.corva.ai/v1/data/corva/{ds.COMPLETION_WITS}?
        company_id={company_id}
        &asset_id={asset_id}
        &query=%7B
        stage_number%23eq%23{stage_number}%7D
        &limit={limit}
    """

    payload = {}
    headers = {
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'Referer': 'https://api.corva.ai/documentation/index.html',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
    'accept': 'application/json',
    'authorization': g.CORVA_API_KEY,
    'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    
    data = json.loads(response.text)

    df = pd.json_normalize(data)

    print("Número de filas totales de la extracción: ", len(df))

    df = df.drop(columns=["data.timestamp"])

    df = clean_column_names(df, "data.")

    df = clean_column_names(df, "cumulative_chemicals.")

    return df


def retrieve_assets_data(limit = 10000, company_id = q.COMPANY_ID):
    """
    Return a Pandas DataFrame with all wells assets
    """

    url = f"""
        https://api.corva.ai/v1/data/corva/{ds.ASSETS}?
        company_id={company_id}
        &limit={limit}
    """

    payload = {}
    headers = {
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'Referer': 'https://api.corva.ai/documentation/index.html',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
    'accept': 'application/json',
    'authorization': g.CORVA_API_KEY,
    'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    data = json.loads(response.text)

    df = pd.json_normalize(data)

    return df



def retrieve_completion_latest(asset_id, limit = 10000, company_id = q.COMPANY_ID):
    """
    Return a Pandas DataFrame with the latest 
    """

    url = f"""
        https://api.corva.ai/v1/data/corva/completion.wits?
        company_id={company_id}
        &asset_id={asset_id}
        &sort=%7Btimestamp%3A%20-1%7D
        &limit={limit}
    """

    payload = {}
    headers = {
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'Referer': 'https://api.corva.ai/documentation/index.html',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
    'accept': 'application/json',
    'authorization': g.CORVA_API_KEY,
    'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    
    data = json.loads(response.text)

    df = pd.json_normalize(data)

    df = clean_column_names(df, "data.")

    df = clean_column_names(df, "cumulative_chemicals.")

    return df


def retrieve_completion_predictions(asset_id, stage_number, limit = 10000, company_id = q.COMPANY_ID):
    """
    Return a Pandas DataFrame with a specific asset and stage
    """

    url = (
        f"https://api.corva.ai/v1/data/corva/completion.predictions?"
        + f"company_id={company_id}"
        + f"&asset_id={asset_id}"
        + f"&query=%7B"
        + f"stage_number%23eq%23{stage_number}%7D"
        + f"&limit={limit}"
    )

    payload = {}
    headers = {
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'Referer': 'https://api.corva.ai/documentation/index.html',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
    'accept': 'application/json',
    'authorization': g.CORVA_API_KEY,
    'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    
    data = json.loads(response.text)

    df_breakdown = pd.json_normalize(
        data, 
        record_path=['data', 'breakdown'],
        meta=[['_id'], ['stage_number'], ["asset_id"]], 
        record_prefix='data.breakdown.', 
        meta_prefix=''
    )

    df_isip = pd.json_normalize(
        data, 
        record_path=['data', 'isip'],
        meta=[['_id'], ['stage_number'], ["asset_id"]], 
        record_prefix='data.isip.', 
        meta_prefix=''
    )

    df_owp = pd.json_normalize(
        data, 
        record_path=['data', 'opening_wellhead_pressure'],
        meta=[['_id'], ['stage_number'], ["asset_id"]], 
        record_prefix='data.opening_wellhead_pressure.', 
        meta_prefix=''
    )

    return df_breakdown, df_isip, df_owp


def retrieve_completion_activity_summary(asset_id, stage_number, limit = 1, company_id = q.COMPANY_ID):
    """
    Return a Pandas DataFrame with activities info at the latest timestamp for the stage
    """

    url = (
        f"https://api.corva.ai/v1/data/corva/completion.activity.summary-stage?"
        + f"company_id={company_id}"
        + f"&asset_id={asset_id}"
        + f"&query=%7B"
        + f"stage_number%23eq%23{stage_number}%7D"
        + f"&sort=%7Btimestamp%3A%20-1%7D"
        + f"&limit={limit}"
    )

    payload = {}
    headers = {
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'Referer': 'https://api.corva.ai/documentation/index.html',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
    'accept': 'application/json',
    'authorization': g.CORVA_API_KEY,
    'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    data = json.loads(response.text)

    df = pd.json_normalize(
        data, 
        record_path=['data', 'activities'], 
        meta=[['_id'], ['timestamp'], ['stage_number']], 
        record_prefix='data.activities.'
    )

    return df