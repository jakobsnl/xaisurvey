import random
import streamlit as st

from datetime import datetime, timedelta
from pymongo import ReturnDocument

from config import CHECKS, NUM_SAMPLES, RESERVATION_TIMEOUT, NUM_CHECKS, NUM_EXTRA_CHECKS

def draw_explanations(session_state) -> list:
    """
    Draw balanced explanations from the database, reserving them for the user.
    - Ensures global fairness: every folder–method combo is forced toward equal count.
    - Guarantees exactly NUM_SAMPLES distinct folders.
    - Uses reservation scheme with expiry.
    """

    all_explanations = session_state.db['combinations']
    now = datetime.now()

    # helper: get explanations at given count, excluding reserved
    def get_available_explanations(count, folder=None):
        query = {
            "count": count,
            "$or": [
                {"reserved_until": {"$exists": False}},
                {"reserved_until": {"$lt": now.isoformat()}},
            ]
        }
        if folder is not None:
            query["sample"] = folder
        return list(all_explanations.find(query))

    # Determine current global min count
    global_min_sample_count = all_explanations.find_one(sort=[("count", 1)])['count']

    # Pick NUM_SAMPLES distinct folders
    all_folders = all_explanations.distinct("sample")
    if len(all_folders) < NUM_SAMPLES:
        raise RuntimeError("Not enough distinct folders to draw from!")

    random.shuffle(all_folders)
    selected_folders = all_folders[:NUM_SAMPLES]

    drawn_explanations = []

    # For each folder, enforce fairness
    for folder in selected_folders:
        result = None
        while result is None:
            min_sample_count = global_min_sample_count
            available = []
            while not available:
                available = get_available_explanations(min_sample_count, folder)
                if available:
                    break
                min_sample_count += 1

            # pick one method randomly from this folder
            min_methods_seen = min([st.session_state.method_count[m['method']] for m in available])
            candidates = [m for m in available if st.session_state.method_count[m['method']] == min_methods_seen]

            sample = random.choice(candidates)

            reservation_expiry = now + timedelta(seconds=RESERVATION_TIMEOUT)
            result = all_explanations.find_one_and_update(
                {
                    "_id": sample["_id"],
                    "$or": [
                        {"reserved_until": {"$exists": False}},
                        {"reserved_until": {"$lt": now.isoformat()}},
                    ],
                },
                {"$set": {"reserved_until": reservation_expiry.isoformat()}},
                return_document=ReturnDocument.AFTER,
            )

            if result:
                drawn_explanations.append(result)
                st.session_state.method_count[sample['method']] += 1

    assert len(drawn_explanations) == NUM_SAMPLES, (
        f"Expected {NUM_SAMPLES}, got {len(drawn_explanations)}"
    )
    print(f"Sampled {len(drawn_explanations)} explanations")
    return drawn_explanations


def draw_checks() -> list:
    """
    Draw manipulation checks from the config.
    """
    attention_checks = random.sample(CHECKS[:6], k=NUM_CHECKS)
    attention_checks_extra = random.sample(CHECKS[6:], k=NUM_EXTRA_CHECKS)
    return [*attention_checks, *attention_checks_extra]


def draw_samples(session_state) -> list:
    """
    Draw samples and checks, returning a combined list.
    """
    # init samples list
    samples = []
        
    # draw randomly balanced explanations
    explanations = draw_explanations(st.session_state)
    for explanation in explanations:
        sample_folder = explanation['sample']
        method = explanation['method']
        threshold = explanation['threshold']
        samples.append({
            'type': 'xai',
            'object_folder': sample_folder,
            'method': method,
            'threshold': threshold
        })
        print(f'Sampled: {sample_folder}, {method}, {threshold}')

    # add manipulation checks at random positions
    checks = draw_checks()
    for check in checks:
        insert_index = random.randint(0, len(samples))
        samples.insert(insert_index, check)
        
    return samples