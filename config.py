IMAGE_FOLDER = 'data'
NUM_SAMPLES = 75 #75
NUM_CHECKS = 3 #3
RESERVATION_TIMEOUT = 20 * 60  # seconds

ATTENTION_CHECKS = [
    {'type': 'manipulation', 'question': 'I swim across the Atlantic Ocean to get to work every day', 'correct_answers': ['Strongly Disagree', 'Disagree']},
    {'type': 'manipulation', 'question': 'I was born on the Moon and have never been to Earth', 'correct_answers': ['Strongly Disagree', 'Disagree']},
    {'type': 'manipulation', 'question': 'I have a pet unicorn that lives in my backyard', 'correct_answers': ['Strongly Disagree', 'Disagree']},
    {'type': 'manipulation', 'question': 'I can teleport to any place in the world instantly', 'correct_answers': ['Strongly Disagree', 'Disagree']},
    {'type': 'manipulation', 'question': 'I have a superpower that allows me to fly like a bird', 'correct_answers': ['Strongly Disagree', 'Disagree']},
    {'type': 'attention', 'question': "The colour test you are about to take part in is very simple, when asked for your favourite colour you must select 'Green'.", 'correct_answers': ['Green']},
    {'type': 'attention', 'question': "The colour test you are about to take part in is very simple, when asked for your favourite colour you must select 'Orange'.", 'correct_answers': ['Orange']},
    {'type': 'attention', 'question': "The colour test you are about to take part in is very simple, when asked for your favourite colour you must select 'Blue'.", 'correct_answers': ['Blue']},
    {'type': 'attention', 'question': "The colour test you are about to take part in is very simple, when asked for your favourite colour you must select 'Red'.", 'correct_answers': ['Red']},
    {'type': 'attention', 'question': "The colour test you are about to take part in is very simple, when asked for your favourite colour you must select 'Brown'.", 'correct_answers': ['Brown']},
    # Add more if needed
]

QUESTION_SCALE_MAP = {
    'familarity': {
        'question': 'How familiar are you with Machine Learning and concepts of Artificial Intelligence?',
        'scale': ['Not familiar', 'Somewhat familiar', 'Very familiar']
    },
    'alignment': {
        'question': 'To what degree does the importance map (right) align with the classified object bordered in green (left)?',
        'scale': ['1 - Not at all', '2', '3', '4', '5 - Perfectly aligned']
    },
    'relevance': {
        'question': 'Does the importance map not related to the green-highlighted object appear meaningful for classifying the image?',
        'scale': ['1 - Not at all', '2', '3', '4', '5 - Perfectly meaningful', 'The importance map is perfectly aligned']
    },
    'self_evaluation': {
        'question': 'Considering your level of focus/ distraction thoughout this survey: What is the quality of the data provided by you?',
        'scale': ['1 - Very bad', '2 - Bad', '3 - Okay', '4 - Good', '5 - Very good']
    },
}

EXAMPLE_IMAGES = {
    'DeepLift': [
        ('assets/n03095699/DeepLift/0.jpg', 'The majority of importance is assigned to the space between bridge and ship, making it not aligned very well. Also, this area does not contain information, that would tell us as humans that a container ship might be present in the image.'), #bridge
        ('assets/n01695060/DeepLift/0.jpg', 'The same applies here, yet one can argue that for the komodo dragon, human attention is lead towards the **ground truth** here (due to the shape).') #komodo dragon
    ],
    'GradCAM': [
        ('assets/n03095699/GradCAM/0.jpg', 'Even though medium importance is assigned to the bridge (right), the majority of importance is assigned to the ship, making this a more intuituve explanation.'), 
        ('assets/n01695060/GradCAM/0.jpg', 'Even better focus on the **ground truth**. Important note: Artifacts like on the right (grey, 0 importance) can be ignored for the survey, if not in relevant parts of the image.')
    ],
    'GuidedBackprop': [
        ('assets/n03095699/GuidedBackprop/0.jpg', 'Significant importance is assigned to the bridge. For question 2, this requires you to decide, if a bridge is relevant for classifying the ground truth object as a container ship, or not.'),
        ('assets/n01695060/GuidedBackprop/0.jpg', 'Again, some importance on the background, but to a smaller extent. In contrast, the majority of importance is assigned to the komodo dragon, which is the ground truth object.')
    ],
    'LRP_EpsilonAlpha2Beta1': [
        ('assets/n03095699/LRP_EpsilonAlpha2Beta1/0.jpg', 'Almost perfect alignment with the ground truth object, even though it is not fully covered/ aligned (Not technically bad if explanation is intuitively leading to the ground truth).'),
        ('assets/n01695060/LRP_EpsilonAlpha2Beta1/0.jpg', 'Same here.')
    ]     
}