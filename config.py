#display class label with groundtruth
#MONGODB_CONNECTION_STRING = 'mongodb+srv://streamlit:hertie@xai-survey.zyysxjv.mongodb.net/?retryWrites=true&w=majority&appName=xai-survey'
IMAGE_FOLDER = 'data'
RESULTS_FILE = 'results.json'
NUM_SAMPLES = 1

QUESTION_SCALE_MAP = {
    'familarity': {
        'question': 'How familiar are you with machine learning and AI concepts?',
        'scale': ['Not familiar', 'Somewhat familiar', 'Very familiar']
    },
    'alignment': {
        'question': 'To what degree is the explanation aligned with the classified object?',
        'scale': ['1 - Not at all', '2', '3', '4', '5 - Perfectly aligned']
    },
    'relevance': {
        'question': 'Does the highlighted area, that is not aligned with ground truth, make sense for the classification?',
        'scale': ['1 - Not at all', '2', '3', '4', '5 - Perfectly relevant', 'The explanation is perfectly aligned']
    }
}

EXAMPLE_IMAGES = [
    ('data/n01582220/DeepLift/0.jpg', 1),
    ('data/n03584254/GradCAM_smoothxGuidedBackprop/70.jpg', 5)
]