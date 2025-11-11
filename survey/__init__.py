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
    # # List of tree filenames and correct answers
    # TREE_ANSWERS = [
    #     ['Tree_1.html', True],
    #     ['Tree_2.html', True],
    #     ['Tree_3.html', False],
    #     ['Tree_4.html', True],
    #     ['Tree_5.html', True],
    #     ['Tree_6.html', False],
    #     ['Tree_7.html', False],
    #     ['Tree_8.html', True],
    #     ['Tree_9.html', True],
    #     ['Tree_10.html', False],
    #     ['Tree_11.html', False],
    #     ['Tree_12.html', True],
    #     ['Tree_13.html', False],
    #     ['Tree_14.html', True],
    #     ['Tree_15.html', False],
    #     ['Tree_16.html', True],
    #     ['Tree_17.html', True],
    #     ['Tree_18.html', True],
    #     ['Tree_19.html', True],
    #     ['Tree_20.html', False],
    #     ['Tree_21.html', True]
    # ]
    payment_for_correct_answer = 0.30
    total_possible = payment_for_correct_answer*(NUM_ROUNDS)
    #tree_order=list(range(1, 22))
    group_distribution = [0.166, 0.166, 0.166, 0.166, 0.166, 0.166] #Change this to affect how the sample is collected: 0: no education <44, 1: some education... 5th - high age high education
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
    education_currently_a_student_label = models.BooleanField(
        choices=[
            (True, Lexicon.yes),
            (False, Lexicon.no),
        ],
        label=Lexicon.education_currently_a_student_label,
        widget=widgets.RadioSelectHorizontal
    )

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
    per_page_time=models.IntegerField(blank=True)

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
        subsession.session.speeder_counter = 0   # 👈 initialize here
        easy_trees = list(range(1,12))         # Tree_1 to Tree_11
        hard_trees = list(range(12, 22))     # Tree_12 to Tree_21
        subsession.session.participants_needed = subsession.session.config.get('participants_needed')
        #print(subsession.session.participants_needed)
        subsession.session.prescreener_groups_dict = {
            group_id: {
                'current': 0,
                'max_allowed': round(prop * subsession.session.participants_needed)
            }
            for group_id, prop in enumerate(C.group_distribution)
        }
        # print(subsession.session.prescreener_groups_distr)
        for player in subsession.get_players():
            participant = player.participant
            use_random_block = subsession.session.config.get('random_order_block', False)

            if use_random_block:
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
                # Fixed order from 1 to 21 (Tree_1.html to Tree_21.html)
                participant.easyFirst = False  # or set to None if not used
                full_order = list(range(1, 22))
                random.shuffle(full_order)
            full_order = [(n, random.choice(['a', 'r'])) for n in full_order]
            participant.treeOrder = full_order
            participant.prescreener_group=0
            #print(f'Random Order: {use_random_block} | EasyFirst: {participant.vars["easyFirst"]} | Tree Order: {full_order}')


def vars_for_admin_report(subsession):
    groups = subsession.session.prescreener_groups_dict or {}

    group_labels = {
        0: "Low education, age < 45",
        1: "Mid education, age < 45",
        2: "High education, age < 45",
        3: "Low education, age ≥ 45",
        4: "Mid education, age ≥ 45",
        5: "High education, age ≥ 45",
    }

    display_data = []
    for group_id in sorted(groups.keys()):
        g = groups[group_id]
        current = g['current']
        max_allowed = g['max_allowed']
        label = group_labels.get(group_id, f"Group {group_id}")
        status = '✅ OK' if current <= max_allowed else '⚠️ Exceeded'
        display_data.append(dict(
            group_id=group_id,
            label=label,
            current=current,
            max_allowed=max_allowed,
            status=status,
        ))

    current_total = sum(x['current'] for x in groups.values())
    max_total     = sum(x['max_allowed'] for x in groups.values())

    threshold = subsession.session.config.get('min_total_time_sec')

    # 👉 Use the session variable directly (fallback to 0 if missing)
    speeder_count = getattr(subsession.session, 'speeder_counter', 0)

    return dict(
        round_number=subsession.round_number,
        group_data=display_data,
        current_participants=current_total,
        participants_needed=max_total,
        speeder_threshold=threshold,
        speeder_count=speeder_count,
    )



class Prescreener(Page):
    form_model = 'player'
    form_fields = ['age','education_level_prescreener','education_currently_a_student_label']

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
        age_group = 0 if player.age < 45 else 1
        player.participant.prescreener_group = age_group * 3 + (player.education_level_prescreener - 1)


class ScreenOutPage(Page):
    @staticmethod
    def is_displayed(player):
        if player.round_number != 1:
            return False
        group_id = player.participant.prescreener_group  # or player.participant.prescreener_group
        groups = player.session.prescreener_groups_dict or {}


        g = groups.get(group_id)
        current_total = sum(x['current'] for x in groups.values())
        max_total = sum(x['max_allowed'] for x in groups.values())

        reached_group_quota = g['current'] >= g['max_allowed']
        reached_total_quota = current_total >= max_total
        underage = player.age < 18
        # print("group_of_participant", group_id)
        # print("round_number == 1:", player.round_number == 1)
        # print("groups:", groups)
        # print("current_total:", current_total)
        # print("group count > group_count_max:", g['current'] ,'>', g['max_allowed'], reached_group_quota )
        # print("current_participants > max_total:", current_total, ">", max_total, current_total > max_total)
        return (
            player.round_number == 1
            and
            reached_group_quota or reached_total_quota or underage
        )
    def js_vars(player):
        bilendi_id = player.participant.label
        if player.age < 18:
            redirect_url = f"https://survey.maximiles.com/screenout?p=154054_5cb4a0e8&m={bilendi_id}"
        else:
            redirect_url = f"https://survey.maximiles.com/quotasfull?p=154054_9791854e&m={bilendi_id}"
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
    @staticmethod
    def before_next_page(player, timeout_happened):
        player.participant.server_timestamp_start = time.time()

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


class Tree_Question(Page):
    form_model = "player"
    form_fields = ["question_loan", "confidence_level","interaction_times","per_page_time"]

    @staticmethod
    def vars_for_template(player: Player):
        round_number = player.round_number
        num, variant = player.participant.treeOrder[round_number - 1]
        number_of_rounds=C.NUM_ROUNDS
        # print('tree number',tree_number_in_list,'round number',player.round_number,tree_template)
        return dict(
            svg_template=f'survey/updating_trees/Tree_{num}{variant}.html',
            Lexicon=Lexicon,
            number_of_rounds=number_of_rounds,
            **which_language)
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        round_number = player.round_number
        num, variant = player.participant.treeOrder[round_number - 1]
        expected = (variant == 'a')  # 'a' => accept/True, 'r' => reject/False
        player.is_correct = int(player.question_loan == expected)
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
        all_rounds_query=player.in_all_rounds()
        total_time_server=time.time() - player.participant.server_timestamp_start
        # print(all_rounds_query,"total_time_server",total_time_server)
        player.participant.total_correct_answers = sum(p.is_correct for p in all_rounds_query)
        total_time=sum(p.per_page_time for p in all_rounds_query)
        threshold = player.session.config.get('min_total_time_sec')
        player.participant.speeder=(total_time<threshold)
        # print('total time',total_time)
        # print('total_time_server',total_time_server)
        # print('threshold',threshold)
        # print('Speeder', player.participant.speeder)
        return dict(
            Lexicon=Lexicon,
            **which_language)

    # @staticmethod
    # def before_next_page(player, timeout_happened):
    #     group_dict = player.session.prescreener_groups_dict
    #     group = player.prescreener_group
    #     group_dict[group] += 1
    #     player.session.prescreener_groups_dict = group_dict  # save it back (not strictly necessary)
    # @staticmethod
    # def before_next_page(player: Player, timeout_happened):
    #     player.Survey_Demographics_TS = time.time()


class TestUpdatingTreesAB(Page):
    def vars_for_template(self):
        # Adjust the include path if your files live elsewhere
        rows = [
            {
                "i": i,
                "a_path": f"survey/updating_trees/Tree_{i}a.html",
                "r_path": f"survey/updating_trees/Tree_{i}r.html",
                "a_label": f"Tree_{i}a",
                "r_label": f"Tree_{i}r",
            }
            for i in range(1,22)
        ]
        return dict(
            rows=rows,
            Lexicon=Lexicon,
            **which_language
        )

class test_all_trees(Page):
    def vars_for_template(self):
        trees = [{'path': f'survey/Trees/Tree_{i}.html', 'label': f'Tree_{i}'} for i in range(1, 22)]
        first_six = trees[:6]
        next_fifteen = trees[6:]  # 3 rows of 5
        return dict(first_six=first_six, next_fifteen=next_fifteen,
                    Lexicon=Lexicon,
                    **which_language
                    )

class an_updating_trees(Page):
    def vars_for_template(self):
        return dict(Lexicon=Lexicon,
                    **which_language
                    )

#Actual sequence
page_sequence = [Prescreener, ScreenOutPage,  IntroductionGeneral, IntroductionDecisionTrees, InstructionsSample,SampleQuestion_1, SampleQuestion_2, PreMainStudy, Tree_Question, PostMainStudy]

#Testing
#page_sequence = [Prescreener, ScreenOutPage,  IntroductionGeneral]

#page_sequence=[test_all_trees]

#page_sequence=[an_updating_trees]

#page_sequence = [TestUpdatingTreesAB]

#page_sequence = [Tree_Question, PostMainStudy]