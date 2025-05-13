IMAGE_FOLDER = 'data'
NUM_SAMPLES = 2

QUESTION_SCALE_MAP = {
    'familarity': {
        'question': 'How familiar are you with machine learning and AI concepts?',
        'scale': ['Not familiar', 'Somewhat familiar', 'Very familiar']
    },
    'alignment': {
        'question': 'To what degree is the explanation (right) aligned with the classified object bordered in green (left)?',
        'scale': ['1 - Not at all', '2', '3', '4', '5 - Perfectly aligned']
    },
    'relevance': {
        #Does the part of the explanation, that does not cover the green-highlighted object, appear meaningful for the classificationl?
        'question': 'Does the explanation outside the green-highlighted object appear meaningful for classifying the image?',
        'scale': ['1 - Not at all', '2', '3', '4', '5 - Perfectly relevant', 'The explanation is perfectly aligned']
    }
}

EXAMPLE_IMAGES = [
    ('assets/n01582220/DeepLift/70.jpg', 4),
    ('data/n01978455/GuidedGradCam/0.jpg', 1)
]