IMAGE_FOLDER = 'data'
NUM_SAMPLES = 75

QUESTION_SCALE_MAP = {
    'familarity': {
        'question': 'How familiar are you with machine learning and AI concepts?',
        'scale': ['Not familiar', 'Somewhat familiar', 'Very familiar']
    },
    'alignment': {
        'question': 'To what degree does the importance map (right) align with the classified object bordered in green (left)?',
        'scale': ['1 - Not at all', '2', '3', '4', '5 - Perfectly aligned']
    },
    'relevance': {
        'question': 'Does the importance map not related to the green-highlighted object appear meaningful for classifying the image?',
        'scale': ['1 - Not at all', '2', '3', '4', '5 - Perfectly meaningful', 'The importance map is perfectly aligned']
    }
}

EXAMPLE_IMAGES = {
    'DeepLift': [
        ('assets/n03095699/DeepLift/0.jpg', 'The majority of importance is assigned to the space between bridge and ship, making it not aligned very well.'), #bridge
        ('assets/n01695060/DeepLift/0.jpg', 'The same applies here, yet one can argue, that for the komodo dragon, a humans attention is lead towards the groundtruth here.') #komodo dragon
    ],
    'GradCAM': [
        ('assets/n03095699/GradCAM/0.jpg', 'Even though medium importance is assigned to the bridge (right), the majority of importance is assigned to the ship.'), 
        ('assets/n01695060/GradCAM/0.jpg', 'Even better focus on the **ground truth**. Artifacts like on the right (0 importance) can be ignored for the survey, if not in relevant parts of the image.')
    ],
    'GuidedBackprop': [
        ('assets/n03095699/GuidedBackprop/0.jpg', 'significant importance is assigned to the bridge. For question 2, this requires You to decide, if a bridge is relevant for classifying the ground truth object as a container ship, or not.'),
        ('assets/n01695060/GuidedBackprop/0.jpg', 'Again, some importance on the background, but to smaller extent.')
    ],
    'LRP_EpsilonAlpha2Beta1': [
        ('assets/n03095699/LRP_EpsilonAlpha2Beta1/0.jpg', 'Almost perfect alignment with the ground truth object.'),
        ('assets/n01695060/LRP_EpsilonAlpha2Beta1/0.jpg', 'Same here.')
    ]     
}