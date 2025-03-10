from otree.api import *
from settings import LANGUAGE_CODE, SESSION_CONFIGS
if LANGUAGE_CODE == 'de':
    from .lexicon_de import Lexicon
else:
    from .lexicon_en import Lexicon
which_language = {'en': False, 'de': False}  # noqa
which_language[LANGUAGE_CODE[:2]] = True


class C(BaseConstants):
    NAME_IN_URL = "DecisionTreeExperiment"
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
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


# FUNCTIONS
# PAGES
class IntroductionGeneral(Page):
    def vars_for_template(player: Player):
        return dict(
            Lexicon=Lexicon,
            **which_language)

class IntroductionDecisionTrees(Page):
    form_model = 'player'
    form_fields = ['familiarity_with_decision_trees']
    def vars_for_template(player: Player):
        return dict(
            Lexicon=Lexicon,
            **which_language)

class Demographics(Page):
    form_model = 'player'
    form_fields = ['age', 'gender']


class CognitiveReflectionTest(Page):
    form_model = 'player'
    form_fields = ['crt_bat', 'crt_widget', 'crt_lake']


page_sequence = [IntroductionGeneral, IntroductionDecisionTrees, Demographics, CognitiveReflectionTest]
