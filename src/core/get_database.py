import streamlit as st

from pymongo import MongoClient


def get_database() -> MongoClient:
    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(st.secrets.mongo['MONGODB_CONNECTION_STRING'])

    # Create the database for our example (we will use the same database throughout the tutorial
    return client['xai-survey']
