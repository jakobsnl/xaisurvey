import os
import json

from config import IMAGE_FOLDER
from get_database import get_database

def populate_samples():
    db = get_database()
    collection = db['combinations']

    # Iterate through all folders and methods
    combinations = []
    object_folders = [f for f in os.listdir(IMAGE_FOLDER) if os.path.isdir(os.path.join(IMAGE_FOLDER, f))]
    for folder in object_folders:
        folder_path = os.path.join(IMAGE_FOLDER, folder)
        methods = [m for m in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, m))]
        for method in methods:
            method_path = os.path.join(folder_path, method)
            thresholds = [t for t in os.listdir(method_path) if t.endswith('.jpg')]
            for threshold in thresholds:
                combinations.append({
                    'sample': folder,
                    'method': method,
                    'threshold': threshold,
                    'used': False  # Mark as unused initially
                })

    # Insert all combinations into MongoDB
    if combinations:
        collection.insert_many(combinations)
        print(f"Inserted {len(combinations)} combinations into MongoDB.")
    else:
        print("No combinations found to insert.")

if __name__ == "__main__":
    populate_samples()