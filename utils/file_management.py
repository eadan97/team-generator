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
        # Add any missing columns to the DataFrame
        missing_cols = [col for col in columns if col not in df.columns]
        for col in missing_cols:
            df[col] = 0
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

def get_bk_players_list():
    bk_dir = os.path.join(st.session_state.config["data_dir"], "bks")
    if not os.path.exists(bk_dir):
        st.warning(f"Backups directory does not exist: {bk_dir}")
        return []
    return [os.path.join(bk_dir, f) for f in os.listdir(bk_dir) if os.path.isfile(os.path.join(bk_dir, f))]

def load_players(filename=None):
    player_base_columns = st.session_state.config["player_base_columns"]
    player_stats = st.session_state.config["player_stats"]
    goalkeeper_stats = st.session_state.config["goalkeeper_stats"]

    player_columns = player_base_columns + player_stats + goalkeeper_stats

    file_path = os.path.join(
        st.session_state.config["data_dir"], st.session_state.config["players_filename"]) if filename is None else filename

    df = load_or_create_json_dataframe(file_path, player_columns)
    st.write(f"Loaded players from {file_path}: {len(df)} records")
    if len(df) == 0:
        df = pd.DataFrame(columns=player_columns)

    return df


def save_players(df):
    file_path = os.path.join(
        st.session_state.config["data_dir"], st.session_state.config["players_filename"])

    save_dataframe_to_json(df, file_path)
