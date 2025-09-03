import random
from datetime import datetime, timedelta
from collections import defaultdict
from tqdm import tqdm

NUM_IMAGES = 75
NUM_METHODS = 12
NUM_SAMPLES = 75
NUM_PARTICIPANTS = 200
RESERVATION_TIMEOUT = 60


# --- Mock DB entry structure ---
class MockCollection:

    def __init__(self):
        self.docs = []
        for img in range(NUM_IMAGES):
            for method in range(NUM_METHODS):
                self.docs.append({
                    '_id': f'{img}-{method}',
                    'sample': img,
                    'method': method,
                    'times_shown': 0,
                    'reserved_until': None,
                })

    def find(self, query) -> list:
        result = []
        for d in self.docs:
            if d['times_shown'] != query.get('times_shown'):
                continue
            if 'sample' in query and d['sample'] != query['sample']:
                continue
            # reserved filter
            if d['reserved_until'] and d['reserved_until'] >= query['$or'][1][
                    'reserved_until']['$lt']:
                continue
            result.append(d)
        return result

    def find_one(self) -> dict | None:
        return min(self.docs, key=lambda d: d['times_shown'])

    def distinct(self, field) -> list:
        return list(sorted(set(d[field] for d in self.docs)))

    def find_one_and_update(self, query, update, return_document=None) -> dict | None:
        for d in self.docs:
            if d['_id'] != query['_id']:
                continue
            if d['reserved_until'] and d['reserved_until'] >= query['$or'][1][
                    'reserved_until']['$lt']:
                continue
            d.update(update['$set'])
            d["times_shown"] += 1
            return d
        return None


# --- Session state mock ---
class SessionState:

    def __init__(self, db):
        self.db = {'combinations': db}
        self.method_count = defaultdict(int)


# --- Draw samples function ---
def draw_samples(session_state) -> list:
    all_samples = session_state.db['combinations']
    now = datetime.now()

    def get_available_samples(count, folder=None) -> list:
        query = {
            'times_shown':
            count,
            '$or': [
                {
                    'reserved_until': {
                        '$exists': False
                    }
                },
                {
                    'reserved_until': {
                        '$lt': now.isoformat()
                    }
                },
            ],
        }
        if folder is not None:
            query['sample'] = folder
        return list(all_samples.find(query))

    global_min = all_samples.find_one()['times_shown']

    all_folders = all_samples.distinct('sample')
    if len(all_folders) < NUM_SAMPLES:
        raise RuntimeError('Not enough distinct folders to draw from!')

    random.shuffle(all_folders)
    selected_folders = all_folders[:NUM_SAMPLES]

    drawn_samples = []
    for folder in selected_folders:
        result = None
        while result is None:
            count = global_min
            available = []
            while not available:
                available = get_available_samples(count, folder)
                if available:
                    break
                count += 1

            min_methods_seen = min(session_state.method_count[m['method']]
                                   for m in available)
            candidates = [
                m for m in available
                if session_state.method_count[m['method']] == min_methods_seen
            ]

            sample = random.choice(candidates)
            session_state.method_count[sample['method']] += 1

            reservation_expiry = now  #+ timedelta(seconds=RESERVATION_TIMEOUT)
            result = all_samples.find_one_and_update(
                {
                    '_id':
                    sample['_id'],
                    '$or': [
                        {
                            'reserved_until': {
                                '$exists': False
                            }
                        },
                        {
                            'reserved_until': {
                                '$lt': now.isoformat()
                            }
                        },
                    ],
                },
                {'$set': {
                    'reserved_until': reservation_expiry.isoformat()
                }},
                return_document=True,
            )
            if result:
                drawn_samples.append(result)

    assert len(drawn_samples) == NUM_SAMPLES
    return drawn_samples


# --- Run simulation ---
if __name__ == '__main__':
    db = MockCollection()
    session_state = SessionState(db)

    max_method_diffs = []

    for _ in tqdm(range(NUM_PARTICIPANTS), desc='Simulating participants'):
        # Reset per-participant method counts
        session_state.method_count = defaultdict(int)
        drawn = draw_samples(session_state)
        # Compute per-participant method distribution
        per_method = defaultdict(int)
        for d in drawn:
            per_method[d['method']] += 1
        max_diff = max(per_method.values()) - min(per_method.values())
        max_method_diffs.append(max_diff)

    # summarize distribution over all participants
    print('\nMaximum method display difference per participant (max-min):')
    for idx, diff in enumerate(max_method_diffs, 1):
        print(f'Participant {idx}: {diff}')

    overall_max_diff = max(max_method_diffs)
    overall_min_diff = min(max_method_diffs)
    print(
        f'\nAcross all participants: min max_diff={overall_min_diff}, max max_diff={overall_max_diff}'
    )

    # summarize overall per-method distribution
    per_method_total = defaultdict(int)
    per_image_total = defaultdict(int)
    for d in db.docs:
        per_method_total[d['method']] += d['times_shown']
        per_image_total[d['sample']] += d['times_shown']

    print('\nOverall per-method distribution:')
    for m in sorted(per_method_total):
        print(f'Method {m}: {per_method_total[m]}')

    print('\nOverall per-image distribution:')
    for img in sorted(per_image_total):
        print(f'Image {img}: {per_image_total[img]}')

    print('\nOverall min shown:', min(d['times_shown'] for d in db.docs))
    print('Overall max shown:', max(d['times_shown'] for d in db.docs))
