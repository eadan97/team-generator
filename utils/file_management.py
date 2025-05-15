import os
import json
import pandas as pd
import streamlit as st


def load_or_create_json_dataframe(json_path, columns):
    """
    Loads a JSON file into a pandas DataFrame. If the file does not exist,
    creates a new DataFrame with the specified columns and saves it as JSON.

    Args:
        json_path (str): Path to the JSON file.
        columns (list): List of column names for the DataFrame.

    Returns:
        pd.DataFrame: The loaded or newly created DataFrame.
    """
    if os.path.exists(json_path):
        with open(json_path, 'r') as f:
            data = json.load(f)
        df = pd.DataFrame(data)
    else:
        df = pd.DataFrame(columns=columns)
        df.to_json(json_path, orient='records', indent=2)
    return df


def save_dataframe_to_json(df, json_path):
    """
    Saves a pandas DataFrame to a JSON file.

    Args:
        df (pd.DataFrame): The DataFrame to save.
        json_path (str): Path to the JSON file.
    """
    df.to_json(json_path, orient='records', indent=2)


def load_players():
    player_columns = st.session_state.config["players_columns"]
    file_path = os.path.join(
        st.session_state.config["data_dir"], st.session_state.config["players_filename"])

    df = load_or_create_json_dataframe(file_path, player_columns)

    if len(df) == 0:
        df = pd.DataFrame(columns=player_columns)

    return df


def save_players(df):
    file_path = os.path.join(
        st.session_state.config["data_dir"], st.session_state.config["players_filename"])

    save_dataframe_to_json(df, file_path)
