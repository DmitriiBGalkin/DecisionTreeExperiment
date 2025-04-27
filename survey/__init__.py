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
    total_possible = payment_for_correct_answer*(NUM_ROUNDS)
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
        widget=widgets.RadioSelectHorizontal
    )


    is_correct = models.BooleanField(initial=False)
    total_correct_answers=models.IntegerField()

    confidence_level = models.IntegerField(
        blank=True,
        label=Lexicon.confidence_level_label
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
    confidence_level_sample1 = models.IntegerField(
        blank=True,
        label=Lexicon.confidence_level_label
    )
    question_loan_sample1 = models.BooleanField(
        choices=[
            (True, Lexicon.approved),
            (False, Lexicon.denied),
        ],
        label=Lexicon.question_loan_sample1_label,
        widget=widgets.RadioSelectHorizontal,
    )
    confidence_level_sample2 = models.IntegerField(
        blank=True,
        label=Lexicon.confidence_level_label
    )
    question_loan_sample2 = models.BooleanField(
        choices=[
            (True, Lexicon.approved),
            (False, Lexicon.denied),
        ],
        label=Lexicon.question_loan_sample1_label,
        widget=widgets.RadioSelectHorizontal,
    )

    #Creating time-stamps for each page:
    # IntroductionGeneral_TS = models.FloatField()
    # IntroductionDecisionTrees_TS = models.FloatField()
    # InstructionsSample_TS = models.FloatField()
    # SampleQuestion_1_TS = models.FloatField()
    # SampleQuestion_2_TS = models.FloatField()
    # PreMainStudy_TS = models.FloatField()
    # Tree_Question_TS = models.FloatField()
    # Survey_Demographics_TS = models.FloatField()
    # Results_TS = models.FloatField()

    IntroductionGeneral_SF = models.LongStringField(
        label=Lexicon.feedback_label_SF,
        blank=True,
    )
    IntroductionDecisionTrees_SF = models.LongStringField(
        label=Lexicon.feedback_label_SF,
        blank=True,
    )
    InstructionsSample_SF = models.LongStringField(
        label=Lexicon.feedback_label_SF,
        blank=True,
    )
    SampleQuestion_1_SF = models.LongStringField(
        label=Lexicon.feedback_label_SF,
        blank=True,
    )
    SampleQuestion_2_SF = models.LongStringField(
        label=Lexicon.feedback_label_SF,
        blank=True,
    )
    PreMainStudy_SF = models.LongStringField(
        label=Lexicon.feedback_label_SF,
        blank=True,
    )
    Tree_Question_SF = models.LongStringField(
        label=Lexicon.feedback_label_SF,
        blank=True,
    )
    PostMainStudy_SF = models.LongStringField(
        label=Lexicon.feedback_label_SF,
        blank=True,
    )

def confidence_level_error_message(player, value):
    if value is None:
        return Lexicon.move_slider_warning
def confidence_level_sample1_error_message(player, value):
    if value is None:
        return Lexicon.move_slider_warning
def confidence_level_sample2_error_message(player, value):
    if value is None:
        return Lexicon.move_slider_warning
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

class PreStudyInfo(Page):
    def is_displayed(player):
        return player.session.config.get('student_debug', False) and player.round_number == 1

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            Lexicon=Lexicon,
            **which_language)
class IntroductionGeneral(Page):
    form_model = 'player'
    form_fields = ['IntroductionGeneral_SF']
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1
    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            Lexicon=Lexicon,
            **which_language)
    # @staticmethod
    # def before_next_page(player, timeout_happened):
    #     player.IntroductionGeneral_TS = time.time()

class IntroductionDecisionTrees(Page):
    form_model = 'player'
    form_fields = ['familiarity_with_decision_trees','IntroductionDecisionTrees_SF']
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1
    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            svg_template='survey/Trees/Tree_Sample_1.html',
            Lexicon=Lexicon,
            **which_language)
    # @staticmethod
    # def before_next_page(player, timeout_happened):
    #     player.IntroductionDecisionTrees_TS = time.time()

class InstructionsSample(Page):
    form_model = 'player'
    form_fields = ['InstructionsSample_SF']
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1
    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            Lexicon=Lexicon,
            **which_language)
    # @staticmethod
    # def before_next_page(player, timeout_happened):
    #     player.IntroductionDecisionTrees_TS = time.time()

class SampleQuestion_1(Page):
    form_model = "player"
    form_fields = ["question_loan_sample1","confidence_level_sample1", 'SampleQuestion_1_SF']

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
        if values['question_loan_sample1'] != False or values['confidence_level_sample1'] < 89:
            return Lexicon.please_select_correct_answers
    # @staticmethod
    # def before_next_page(player, timeout_happened):
    #     player.SampleQuestion_1_TS = time.time()


class SampleQuestion_2(Page):
    form_model = "player"
    form_fields = ["question_loan_sample2", "confidence_level_sample2", 'SampleQuestion_2_SF']
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
        if values['question_loan_sample2'] != True or values['confidence_level_sample2'] > 30:
            return Lexicon.please_select_correct_answers
    # @staticmethod
    # def before_next_page(player, timeout_happened):
    #     player.SampleQuestion_2_TS = time.time()
class PreMainStudy(Page):
    form_model = "player"
    form_fields = ['PreMainStudy_SF']
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1
    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            Lexicon=Lexicon,
            **which_language)
    # @staticmethod
    # def before_next_page(player, timeout_happened):
    #     player.PreMainStudy_TS = time.time()
class Tree_Question(Page):
    form_model = "player"
    form_fields = ["question_loan", "confidence_level","Tree_Question_SF"]

    @staticmethod
    def vars_for_template(player: Player):
        round_number = player.round_number
        tree_number = player.participant.treeOrder[round_number-1]
        tree_template = C.TREE_ANSWERS[tree_number][0]
        number_of_rounds=C.NUM_ROUNDS
        print('tree number',tree_number,'round number',player.round_number,tree_template)
        return dict(
            svg_template=f'survey/Trees/{tree_template}',
            Lexicon=Lexicon,
            number_of_rounds=number_of_rounds,
            **which_language)
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # player.Tree_Question_TS = time.time()
        round_number = player.round_number
        tree_number = player.participant.treeOrder[round_number-1]
        player.is_correct = int(player.question_loan == C.TREE_ANSWERS[tree_number][1])
        player.payoff = player.is_correct * C.payment_for_correct_answer
        print(player.is_correct)
        print(C.payment_for_correct_answer)
        print(player.payoff)


class PostMainStudy(Page):
    form_model = 'player'
    form_fields = ["PostMainStudy_SF"]
    @staticmethod
    def is_displayed(player):
        return player.round_number == C.NUM_ROUNDS
    @staticmethod
    def vars_for_template(player: Player):
        player.participant.total_correct_answers = sum(p.is_correct for p in player.in_all_rounds())
        return dict(
            Lexicon=Lexicon,
            **which_language)

    # @staticmethod
    # def before_next_page(player: Player, timeout_happened):
    #     player.Survey_Demographics_TS = time.time()



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
page_sequence = [PreStudyInfo, IntroductionGeneral, IntroductionDecisionTrees, InstructionsSample,SampleQuestion_1, SampleQuestion_2, PreMainStudy, Tree_Question, PostMainStudy]



