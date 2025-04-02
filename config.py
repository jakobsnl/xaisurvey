#display class label with groundtruth

IMAGE_FOLDER = "images"
RESULTS_FILE = "results.json"
NUM_SAMPLES = 2

QUESTION_SCALE_MAP = {
    'familarity': {
        'question': "How familiar are you with machine learning and AI concepts?",
        'scale': ["Not familiar", "Somewhat familiar", "Very familiar"]
    },
    'alignment': {
        'question': "To what degree is the explanation aligned with the classified object?",
        'scale': ["1 - Not at all", "2", "3", "4", "5 - Perfectly aligned"]
    },
    'relevance': {
        'question': "Does the highlighted area make sense for the classification?",
        'scale': ["1 - Not at all", "2", "3", "4", "5 - Perfectly relevant"]
    }
}

EXAMPLE_IMAGES = [
    ("images/01/exs/GradCAM/10.png", "images/01/groundtruth.png", 1),
    ("images/02/exs/GradCAM/20.png", "images/02/groundtruth.png", 5)
]