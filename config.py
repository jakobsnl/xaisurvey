IMAGE_FOLDER = 'data'
NUM_SAMPLES = 2 # max: len(data)=75, as the setup is built for users seeing each sample once
NUM_CHECKS = 2
NUM_EXTRA_CHECKS = 2
RESERVATION_TIMEOUT = 20 * 60  # seconds
CHECKS = [
    {
        'type': 'attention', 
        'question': "This is a manipulation check, please select '1 - Not at all' for this question.",
        'correct_answers': ['1 - Not at all'],
        'scale': ['1 - Not at all', '2', '3', '4', '5 - Perfectly aligned']
    },
    {
        'type': 'attention', 
        'question': "This is a manipulation check, please select '2' for this question.",
        'correct_answers': ['2'],
        'scale': ['1 - Not at all', '2', '3', '4', '5 - Perfectly aligned']
    },
    {
        'type':'attention', 
        'question': "This is a manipulation check, please select '3' for this question.",
        'correct_answers': ['3'],
        'scale': ['1 - Not at all', '2', '3', '4', '5 - Perfectly aligned']
    },
    {
        'type': 'attention', 
        'question': "This is a manipulation check, please select '4' for this question.",  
        'correct_answers': ['4'],
        'scale': ['1 - Not at all', '2', '3', '4', '5 - Perfectly aligned']
    },
    {
        'type': 'attention', 
        'question': "This is a manipulation check, please select '5 - Perfectly aligned' for this question.",
        'correct_answers': ['5 - Perfectly aligned'],
        'scale': ['1 - Not at all', '2', '3', '4', '5 - Perfectly aligned']
    },
    {
        'type': 'attention_note',
        'note': "The test you are about to take part in is very simple, when asked for a score you must select '1 - Not at all'.",
        'question': 'Based on the text you read above, what score have you been asked to enter?',
        'correct_answers': ['1 - Not at all'],
        'scale': ['1 - Not at all', '2', '3', '4', '5 - Perfectly aligned']
    },
    {
        'type': 'attention_note',
        'note': "The test you are about to take part in is very simple, when asked for a score you must select '2'.",
        'question': 'Based on the text you read above, what score have you been asked to enter?',
        'correct_answers': ['2'],
        'scale': ['1 - Not at all', '2', '3', '4', '5 - Perfectly aligned']
    },
    {
        'type': 'attention_note',
        'note': "The test you are about to take part in is very simple, when asked for a score you must select '3'.",
        'question': 'Based on the text you read above, what score have you been asked to enter?',
        'correct_answers': ['3'],
        'scale': ['1 - Not at all', '2', '3', '4', '5 - Perfectly aligned']
    },
    {
        'type': 'attention_note',
        'note': "The test you are about to take part in is very simple, when asked for a score you must select '4'.",
        'question': 'Based on the text you read above, what score have you been asked to enter?',
        'correct_answers': ['4'],
        'scale': ['1 - Not at all', '2', '3', '4', '5 - Perfectly aligned']
    },
    {
        'type': 'attention_note',
        'note': "The test you are about to take part in is very simple, when asked for a score you must select '5 - Perfectly aligned'.",
        'question': 'Based on the text you read above, what score have you been asked to enter?',
        'correct_answers': ['5 - Perfectly aligned'],
        'scale': ['1 - Not at all', '2', '3', '4', '5 - Perfectly aligned']
    }
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