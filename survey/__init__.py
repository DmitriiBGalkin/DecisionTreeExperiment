from otree.api import *

from onlySurveyAndResults import page_sequence
from settings import LANGUAGE_CODE
import random
import math
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
    group_distribution = [0.125, 0.2, 0.175, 0.125, 0.2, 0.175] #Change this to affect how the sample is collected: 0: no education <44, 1: some education... 5th - high age high education
class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
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
        min=1,
        max=100
    )
    prescreener_group = models.IntegerField()
    education_level_prescreener = models.IntegerField(
        choices=[
            (1, Lexicon.no_education),
            (2, Lexicon.vocational_education),
            (3, Lexicon.higher_education),
        ],
        label=Lexicon.education_label
    )

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
    interaction_times = models.LongStringField(blank=True)

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
        subsession.session.prescreener_groups_dict = {i: 0 for i in range(6)}

        easy_trees = list(range(11))         # Tree_1 to Tree_11
        hard_trees = list(range(11, 21))     # Tree_12 to Tree_21
        subsession.session.current_participants = 0
        subsession.session.participants_needed = subsession.session.config.get('participants_needed')
        #print(subsession.session.participants_needed)
        subsession.session.prescreener_groups_distr = {
            group_id: round(prop * subsession.session.participants_needed)
            for group_id, prop in enumerate(C.group_distribution)
        }
        # print(subsession.session.prescreener_groups_distr)
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
            # print(f'Random Order: {use_random} | EasyFirst: {participant.vars["easyFirst"]} | Tree Order: {full_order}')
def vars_for_admin_report(subsession):
    session = subsession.session

    group_counts = session.prescreener_groups_dict
    group_maxes = session.prescreener_groups_distr
    current_participants = session.current_participants

    # Define readable labels for each group
    group_labels = {
        0: "Low education, age < 45",
        1: "Mid education, age < 45",
        2: "High education, age < 45",
        3: "Low education, age ≥ 45",
        4: "Mid education, age ≥ 45",
        5: "High education, age ≥ 45",
    }

    display_data = []
    all_group_ids = sorted(set(group_counts.keys()) | set(group_maxes.keys()))

    for group_id in all_group_ids:
        current = group_counts.get(group_id, 0)
        max_allowed = group_maxes.get(group_id, 'N/A')
        label = group_labels.get(group_id, f"Group {group_id}")
        status = '✅ OK' if max_allowed == 'N/A' or current <= max_allowed else '⚠️ Exceeded'

        display_data.append(dict(
            group_id=group_id,
            label=label,
            current=current,
            max_allowed=max_allowed,
            status=status
        ))

    return dict(
        round_number=subsession.round_number,
        group_data=display_data,
        current_participants=current_participants,
    )



class Prescreener(Page):
    form_model = 'player'
    form_fields = ['age','education_level_prescreener']

    @staticmethod
    def is_displayed(player):
        #print('current',player.session.current_participants)
        return player.round_number == 1

    @staticmethod
    def vars_for_template(player: Player):
        #print('max', player.session.participants_needed, 'True?',player.session.current_participants<player.session.participants_needed)
        return dict(
            Lexicon=Lexicon,
            **which_language)
    @staticmethod
    def before_next_page(player, timeout_happened):
        age_group = 0 if player.age < 45 else 1
        player.prescreener_group = age_group * 3 + (player.education_level_prescreener - 1)


class ScreenOutPage(Page):
    @staticmethod
    def is_displayed(player):
        if player.round_number != 1:
            return False
        group = player.prescreener_group
        max_total = player.session.participants_needed - 1
        group_count = player.session.prescreener_groups_dict.get(group, None)
        group_count_max = player.session.prescreener_groups_distr.get(group, None)
        current_participants = player.session.current_participants
        # print("group", group)
        # print("round_number == 1:", player.round_number == 1)
        # print("group_count:", group_count)
        # print("group_count_max:", group_count_max)
        # print("group count > group_count_max:", group_count, group_count_max, group_count > group_count_max, )
        # print("current_participants > max_total:", current_participants, ">", max_total, current_participants > max_total)
        return (
            player.round_number == 1
            and
            (group_count > group_count_max or player.age < 18 or current_participants>max_total)
        )
    def js_vars(player):
        bilendi_id = player.participant.label
        if player.age < 18:
            redirect_url = f"https://survey.maximiles.com/screenout?p=98327_69cadaeb&m={bilendi_id}"
        else:
            redirect_url = f"https://survey.maximiles.com/quotasfull?p=98327_21a4610c&m={bilendi_id}"
            # print(redirect_url)
        return dict(redirect_url=redirect_url)


class IntroductionGeneral(Page):
    form_model = 'player'
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
            svg_template_model='survey/Trees/naked_model.html',
            svg_template='survey/Trees/Tree_Sample_Desc.html',
            Lexicon=Lexicon,
            **which_language)
    # @staticmethod
    # def before_next_page(player, timeout_happened):
    #     player.IntroductionDecisionTrees_TS = time.time()

class InstructionsSample(Page):
    form_model = 'player'
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
        if values['question_loan_sample1'] != False:
            return Lexicon.please_select_correct_answers
    # @staticmethod
    # def before_next_page(player, timeout_happened):
    #     player.SampleQuestion_1_TS = time.time()


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
        if values['question_loan_sample2'] != True:
            return Lexicon.please_select_correct_answers
    # @staticmethod
    # def before_next_page(player, timeout_happened):
    #     player.SampleQuestion_2_TS = time.time()
class PreMainStudy(Page):
    form_model = "player"
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1
    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            Lexicon=Lexicon,
            **which_language)
    @staticmethod
    def before_next_page(player, timeout_happened):
        group_dict = player.session.prescreener_groups_dict
        group = player.prescreener_group
        group_dict[group] += 1
        player.session.prescreener_groups_dict = group_dict  # save it back (not strictly necessary)

class Tree_Question(Page):
    form_model = "player"
    form_fields = ["question_loan", "confidence_level","interaction_times"]

    @staticmethod
    def vars_for_template(player: Player):
        round_number = player.round_number
        tree_number = player.participant.treeOrder[round_number-1]
        tree_template = C.TREE_ANSWERS[tree_number][0]
        number_of_rounds=C.NUM_ROUNDS
        # print('tree number',tree_number,'round number',player.round_number,tree_template)
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
        # print(player.is_correct)
        # print(C.payment_for_correct_answer)
        # print(player.payoff)

class PostMainStudy(Page):
    form_model = 'player'
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



# class TEST_Tree_Question(Page):
#     form_model = "player"
#     form_fields = ["question_loan", "confidence_level"]
#     @staticmethod
#     def vars_for_template(player: Player):
#         round_index = player.round_number - 1  # zero-indexed
#         tree_template = C.TREE_ANSWERS[round_index][0]
#         number_of_rounds=C.NUM_ROUNDS
#         return dict(
#             svg_template='survey/Trees/TREE_TEST.html',
#             Lexicon=Lexicon,
#             number_of_rounds=number_of_rounds,
#             **which_language)



#Actual sequence
page_sequence = [Prescreener, ScreenOutPage,  IntroductionGeneral, IntroductionDecisionTrees, InstructionsSample,SampleQuestion_1, SampleQuestion_2, PreMainStudy, Tree_Question, PostMainStudy]

#Testing
#page_sequence = [Prescreener, ScreenOutPage,  IntroductionGeneral]

