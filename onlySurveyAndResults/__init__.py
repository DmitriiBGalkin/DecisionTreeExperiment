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
    # age = models.IntegerField(
    #     label=Lexicon.age_label,
    #     min=18,
    #     max=100
    # )
    education_level = models.IntegerField(
        choices=[
            (1, Lexicon.education_schueler),
            (2, Lexicon.education_hauptschule),
            (3, Lexicon.education_mittlere_reife),
            (4, Lexicon.education_lehre),
            (5, Lexicon.education_fachabitur),
            (6, Lexicon.education_abitur),
            (7, Lexicon.education_bachelor),
            (8, Lexicon.education_master),
            (9, Lexicon.education_phd),
            (10, Lexicon.education_other),
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
    form_fields = ['gender', 'education_level', 'education_level_other','field_of_study', 'field_of_study_other','income_band', 'subjective_social_status', 'bundesland', 'serious_participation',
                   'feedback']
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if not player.participant.speeder:
            groups = player.session.prescreener_groups_dict
            group_id = player.participant.prescreener_group  # the integer 0–5
            groups[group_id]['current'] += 1
            # optional: write back, but not strictly required
            player.session.prescreener_groups_dict = groups
            # If you want to print total participants:
            current_total = sum(g['current'] for g in groups.values())
            print("Current participants:", current_total)


class Results(Page):
    form_model = 'player'
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


class FinalRedirect(Page):
    @staticmethod
    def is_displayed(player):
        return True
    def js_vars(player):
        bilendi_id = player.participant.label
        redirect_url = f"https://survey.maximiles.com/complete?p=148124_4f493a3f&m={bilendi_id}"
        return dict(redirect_url=redirect_url)

page_sequence = [Survey_Demographics, Results, FinalRedirect]

