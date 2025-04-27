from otree.api import *
from settings import LANGUAGE_CODE
import random
import time

#LANGUAGE_CODE = 'en' #this just for testing
if LANGUAGE_CODE == 'de':
    from .lexicon_de import Lexicon
else:
    from .lexicon_en import Lexicon
which_language = {'en': False, 'de': False}  # noqa
which_language[LANGUAGE_CODE[:2]] = True

class C(BaseConstants):
    NAME_IN_URL = "onlySurveyAndResults"
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    payment_for_correct_answer = 0.30
    total_possible = payment_for_correct_answer*(NUM_ROUNDS)
    tree_order=list(range(0, 21))
class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # Survey Questions
    gender = models.IntegerField(
        choices=[
            (1, Lexicon.gender_male),
            (2, Lexicon.gender_female),
            (3, Lexicon.gender_diverse),
            (4, Lexicon.gender_no_answer),
        ],
        label=Lexicon.gender_label
    )
    age = models.IntegerField(
        label=Lexicon.age_label,
        min=18,
        max=100
    )
    education_level = models.StringField(
        choices=[
            Lexicon.education_schueler,
            Lexicon.education_hauptschule,
            Lexicon.education_mittlere_reife,
            Lexicon.education_lehre,
            Lexicon.education_fachabitur,
            Lexicon.education_abitur,
            Lexicon.education_bachelor,
            Lexicon.education_master,
            Lexicon.education_phd,
            Lexicon.education_other,
        ],
        label=Lexicon.education_label
    )
    field_of_study = models.StringField(
        choices=[
            Lexicon.study_none,
            Lexicon.study_engineering,
            Lexicon.study_computer_science,
            Lexicon.study_mathematics,
            Lexicon.study_natural_sciences,
            Lexicon.study_medicine,
            Lexicon.study_economics,
            Lexicon.study_law,
            Lexicon.study_social_sciences,
            Lexicon.study_education,
            Lexicon.study_humanities,
            Lexicon.study_other,
        ],
        label=Lexicon.study_label
    )
    field_of_study_other = models.StringField(
        label=Lexicon.study_other_label,
        blank=True,
    )
    education_level_other = models.StringField(
        label="Falls Sie 'Anderer Abschluss' gewählt haben, bitte angeben:",
        blank=True,  # This allows the field to remain empty
    )
    serious_participation = models.BooleanField(
        choices=[
            (1, Lexicon.participation_serious),
            (2, Lexicon.participation_not_serious),
        ],
        label=Lexicon.participation_label
    )
    feedback = models.LongStringField(
        label=Lexicon.feedback_label,
        blank=True,
    )
    bundesland = models.StringField(
        choices=[
            (1, "Baden-Württemberg"),
            (2, "Bayern"),
            (3, "Berlin"),
            (4, "Brandenburg"),
            (5, "Bremen"),
            (6, "Hamburg"),
            (7, "Hessen"),
            (8, "Mecklenburg-Vorpommern"),
            (9, "Niedersachsen"),
            (10, "Nordrhein-Westfalen"),
            (11, "Rheinland-Pfalz"),
            (12, "Saarland"),
            (13, "Sachsen"),
            (14, "Sachsen-Anhalt"),
            (15, "Schleswig-Holstein"),
            (16, "Thüringen"),
        ],
        label=Lexicon.state_label,
    )
    subjective_social_status = models.IntegerField(
        choices=[(i, str(i)) for i in range(10, 0, -1)],
        label=Lexicon.subjective_social_status_label
    )
    income_band = models.IntegerField(
        choices=[
            (1, Lexicon.income_band_1),
            (2, Lexicon.income_band_2),
            (3, Lexicon.income_band_3),
            (4, Lexicon.income_band_4),
            (5, Lexicon.income_band_5),
            (6, Lexicon.income_band_6),
            (7, Lexicon.income_band_7),
            (8, Lexicon.income_band_8),
        ],
        label=Lexicon.income_band_label
    )
    #Creating time-stamps for each page:
    # Survey_Demographics_TS = models.FloatField()
    # Results_TS = models.FloatField()


    Survey_Demographics_SF = models.LongStringField(
        label=Lexicon.feedback_label_SF,
        blank=True,
    )
    Results_SF = models.LongStringField(
        label=Lexicon.feedback_label_SF,
        blank=True,
    )


class Survey_Demographics(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == C.NUM_ROUNDS
    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            Lexicon=Lexicon,
            **which_language)
    form_model = 'player'
    form_fields = ['gender', 'age', 'education_level', 'education_level_other','field_of_study', 'field_of_study_other','income_band', 'subjective_social_status', 'bundesland', 'serious_participation',
                   'feedback',"Survey_Demographics_SF"]
    # @staticmethod
    # def before_next_page(player: Player, timeout_happened):
    #     player.Survey_Demographics_TS = time.time()

class Results(Page):
    form_model = 'player'
    form_fields = ["Results_SF"]
    @staticmethod
    def is_displayed(player):
        return player.round_number == C.NUM_ROUNDS
    def vars_for_template(player: Player):
        return dict(
            total_score = player.participant.total_correct_answers,
            Lexicon = Lexicon,
            **which_language)

    # @staticmethod
    # def before_next_page(player: Player, timeout_happened):
    #     player.Results_TS = time.time()




page_sequence = [Survey_Demographics, Results]

