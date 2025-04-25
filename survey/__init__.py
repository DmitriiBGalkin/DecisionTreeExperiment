from otree.api import *
from settings import LANGUAGE_CODE
import random

#LANGUAGE_CODE = 'en' #this just for testing
if LANGUAGE_CODE == 'de':
    from .lexicon_de import Lexicon
else:
    from .lexicon_en import Lexicon
which_language = {'en': False, 'de': False}  # noqa
which_language[LANGUAGE_CODE[:2]] = True

class C(BaseConstants):
    NAME_IN_URL = "DecisionTreeExperiment"
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 21
    # List of tree filenames and correct answers
    TREE_ANSWERS = [
        ['Tree_1.html', True],
        ['Tree_2.html', True],
        ['Tree_3.html', False],
        ['Tree_4.html', True],
        ['Tree_5.html', True],
        ['Tree_6.html', False],
        ['Tree_7.html', False],
        ['Tree_8.html', True],
        ['Tree_9.html', True],
        ['Tree_10.html', False],
        ['Tree_11.html', False],
        ['Tree_12.html', True],
        ['Tree_13.html', False],
        ['Tree_14.html', True],
        ['Tree_15.html', False],
        ['Tree_16.html', True],
        ['Tree_17.html', True],
        ['Tree_18.html', True],
        ['Tree_19.html', True],
        ['Tree_20.html', False],
        ['Tree_21.html', True]
    ]
    payment_for_correct_answer = 0.30
    total_possible = payment_for_correct_answer*(NUM_ROUNDS-2)
    tree_order=list(range(0, 21))
class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    question_loan = models.BooleanField(
        choices=[
            (True, Lexicon.approved),
            (False, Lexicon.denied),
        ],
        label=Lexicon.question_loan_sample1_label,
        widget=widgets.RadioSelectHorizontal,
    )


    is_correct = models.BooleanField(initial=False)
    total_correct_answers=models.IntegerField()
    confidence_level = models.IntegerField(
        choices=[
            (1, Lexicon.confidence_level_1),
            (2, Lexicon.confidence_level_2),
            (3, Lexicon.confidence_level_3),
            (4, Lexicon.confidence_level_4),
            (5, Lexicon.confidence_level_5),
        ],
        label=Lexicon.confidence_level_label,
        widget=widgets.RadioSelectHorizontal,
    )


    familiarity_with_decision_trees = models.IntegerField(
        choices=[
            (1, Lexicon.familiarity_with_decision_trees_1),
            (2, Lexicon.familiarity_with_decision_trees_2),
            (3, Lexicon.familiarity_with_decision_trees_3),
            (4, Lexicon.familiarity_with_decision_trees_4),
            (5, Lexicon.familiarity_with_decision_trees_5),
        ],
        label=Lexicon.familiarity_with_decision_trees_label,
        widget=widgets.RadioSelectHorizontal,
    )
    sample_question_1 = models.BooleanField()
    sample_question_2 = models.BooleanField()
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
    confidence_level_sample1 = models.IntegerField(
        choices=[
            (1, Lexicon.confidence_level_1),
            (2, Lexicon.confidence_level_2),
            (3, Lexicon.confidence_level_3),
            (4, Lexicon.confidence_level_4),
            (5, Lexicon.confidence_level_5),
        ],
        label=Lexicon.confidence_level_label,
        widget=widgets.RadioSelectHorizontal,
    )
    question_loan_sample1=models.IntegerField(
        choices=[
            (1, Lexicon.approved),
            (2, Lexicon.denied),
        ],
        label=Lexicon.question_loan_sample1_label,
        widget=widgets.RadioSelectHorizontal,
    )
    confidence_level_sample2 = models.IntegerField(
        choices=[
            (1, Lexicon.confidence_level_1),
            (2, Lexicon.confidence_level_2),
            (3, Lexicon.confidence_level_3),
            (4, Lexicon.confidence_level_4),
            (5, Lexicon.confidence_level_5),
        ],
        label=Lexicon.confidence_level_label,
        widget=widgets.RadioSelectHorizontal,
    )
    question_loan_sample2 = models.IntegerField(
        choices=[
            (1, Lexicon.approved),
            (2, Lexicon.denied),
        ],
        label=Lexicon.question_loan_sample1_label,
        widget=widgets.RadioSelectHorizontal,
    )
    subjective_social_status = models.IntegerField(
        choices=[(i, str(i)) for i in range(1, 11)],
        label=Lexicon.subjective_social_status_label,
        widget=widgets.RadioSelectHorizontal
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


# FUNCTIONS

def creating_session(subsession: Subsession):
    if subsession.round_number == 1:
        easy_trees = list(range(11))         # Tree_1 to Tree_11
        hard_trees = list(range(11, 21))     # Tree_12 to Tree_21

        for player in subsession.get_players():
            participant = player.participant
            use_random = subsession.session.config.get('random_order', False)

            if use_random:
                # Randomly assign whether participant sees easy or hard trees first
                easy_first = random.choice([True, False])
                participant.easyFirst = easy_first

                easy_part = easy_trees.copy()
                hard_part = hard_trees.copy()
                random.shuffle(easy_part)
                random.shuffle(hard_part)

                if easy_first:
                    full_order = easy_part + hard_part
                else:
                    full_order = hard_part + easy_part

            else:
                # Fixed order from 0 to 20 (Tree_1.html to Tree_21.html)
                participant.easyFirst = True  # or set to None if not used
                full_order = list(range(21))

            participant.treeOrder = full_order
            print(f'Random Order: {use_random} | EasyFirst: {participant.vars["easyFirst"]} | Tree Order: {full_order}')

# PAGES
class IntroductionGeneral(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1
    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            Lexicon=Lexicon,
            **which_language)


class IntroductionDecisionTrees(Page):
    form_model = 'player'
    form_fields = ['familiarity_with_decision_trees']
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1
    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            svg_template='survey/Trees/Tree_Sample_1.html',
            Lexicon=Lexicon,
            **which_language)


class InstructionsSample(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1
    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            Lexicon=Lexicon,
            **which_language)

class SampleQuestion_1(Page):
    form_model = "player"
    form_fields = ["question_loan_sample1","confidence_level_sample1"]

    @staticmethod
    def is_displayed(player):
        return player.round_number == 1
    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            svg_template='survey/Trees/Tree_Sample_1.html',
            Lexicon=Lexicon,
            **which_language)

    def error_message(player, values):
        if values['question_loan_sample1'] != 2:
            return Lexicon.please_select_correct_answer

class SampleQuestion_2(Page):
    form_model = "player"
    form_fields = ["question_loan_sample2", "confidence_level_sample2"]
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1
    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            svg_template='survey/Trees/Tree_Sample_2.html',
            Lexicon=Lexicon,
            **which_language)

    def error_message(player, values):
        if values['question_loan_sample2'] != 1:
            return Lexicon.please_select_correct_answer

class PreMainStudy(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1
    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            Lexicon=Lexicon,
            **which_language)

class Tree_Question(Page):
    form_model = "player"
    form_fields = ["question_loan", "confidence_level"]
    @staticmethod
    def is_displayed(player):
        return player.round_number not in [6, 11]
    @staticmethod
    def vars_for_template(player: Player):
        round_number = player.round_number
        tree_number = player.participant.treeOrder[round_number]
        tree_template = C.TREE_ANSWERS[tree_number][0]
        number_of_rounds=C.NUM_ROUNDS
        print(num_attention_checks_before,'tree number',tree_number,'round number',player.round_number,tree_template)
        return dict(
            svg_template=f'survey/Trees/{tree_template}',
            Lexicon=Lexicon,
            number_of_rounds=number_of_rounds,
            **which_language)
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        round_number = player.round_number
        tree_number = player.participant.treeOrder[round_number]
        player.is_correct = int(player.question_loan == C.TREE_ANSWERS[tree_number][1])
        player.payoff = player.is_correct * C.payment_for_correct_answer
        print(player.is_correct)
        print(C.payment_for_correct_answer)
        print(player.payoff)


class Survey_Demographics(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == C.NUM_ROUNDS
    @staticmethod
    def vars_for_template(player: Player):
        player.total_correct_answers = sum(p.is_correct for p in player.in_all_rounds())
        return dict(
            Lexicon=Lexicon,
            **which_language)
    form_model = 'player'
    form_fields = ['gender', 'age', 'education_level', 'education_level_other','field_of_study', 'field_of_study_other','income_band', 'subjective_social_status', 'bundesland', 'serious_participation',
                   'feedback']

class Results(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == C.NUM_ROUNDS
    def vars_for_template(player: Player):
        return dict(
            total_score = player.total_correct_answers,
            Lexicon = Lexicon,
            **which_language)


class TEST_Tree_Question(Page):
    form_model = "player"
    form_fields = ["question_loan", "confidence_level"]
    @staticmethod
    def vars_for_template(player: Player):
        round_index = player.round_number - 1  # zero-indexed
        tree_template = C.TREE_ANSWERS[round_index][0]
        number_of_rounds=C.NUM_ROUNDS
        return dict(
            svg_template='survey/Trees/TREE_TEST.html',
            Lexicon=Lexicon,
            number_of_rounds=number_of_rounds,
            **which_language)
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.is_correct = int(player.question_loan == C.TREE_ANSWERS[player.round_number - 1][1])
        player.payoff = player.is_correct * C.payment_for_correct_answer
        print(player.is_correct)
        print(C.payment_for_correct_answer)
        print(player.payoff)


#Actual sequence
page_sequence = [IntroductionGeneral, IntroductionDecisionTrees, InstructionsSample,SampleQuestion_1, SampleQuestion_2, PreMainStudy, Tree_Question, Survey_Demographics, Results]

#For testing the randomisation technique
#page_sequence = [Tree_Question, Survey_Demographics, Results]

#For testing the tree view
#page_sequence = [TEST_Tree_Question]

#For testing the survey
#page_sequence = [Survey_Demographics]
