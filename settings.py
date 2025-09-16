from os import environ

SESSION_CONFIGS = [
    # dict(
    #     name='Survey_without_Random_Order',
    #     app_sequence=['survey','onlySurveyAndResults'],
    #     num_demo_participants=4,
    #     random_order=False,
    #     student_debug=True
    # ),
    dict(
        name='Survey_with_Random_Order',
        app_sequence=['survey','onlySurveyAndResults'],
        participants_needed=8,
        num_demo_participants=10,
        random_order_block=False,
        student_debug=False,
        min_total_time_sec=10
    ),
]
ROOMS = [
    dict(
        name='decision_tree_study',
        display_name='dt_exp',
        # participant_label_file='_rooms/your_study.txt',
        # use_secure_urls=True,
    )
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00,student_debug=False, doc="",current_participants=0,participants_needed=8,random_order_block=False, min_total_time_sec=105
)

PARTICIPANT_FIELDS = ["treeOrder","easyFirst","total_correct_answers","server_timestamp_start","server_timestamp_end","speeder","prescreener_group"]
SESSION_FIELDS = ['participants_needed','prescreener_groups_dict']

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'de'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'EUR'
USE_POINTS = False

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '6289054654300'
