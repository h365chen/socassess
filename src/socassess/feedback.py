from pathlib import Path

import xmltodict

from . import feedback_helper
from .display import formatter, no_auto_feedback
from .exception import SocAssessException
from .level import FeedbackLevel


def generate_feedback(ansdir, artifacts, *, config):
    """Parse test outcomes then produce feedback messages."""
    outcomes = test_outcomes(artifacts)
    fb_dict = automated_feedback(outcomes.keys(), ansdir, artifacts)

    need_expert = fb_dict.pop('need_expert', None)
    if need_expert is not None:
        # prepare the default feedback
        fb_dict |= no_auto_feedback(need_expert,
                                    template=config.feedback_template)

        # overwrite feedback afterwards
        enabled_features: dict[str, bool]
        enabled_features = config.feature_dict

        if enabled_features["ai"] is True:
            from .ai import ai_feedback
            fb_dict |= ai_feedback(need_expert, config=config)

        # email has to be after ai so that ai feedback is observable at this
        # point
        if enabled_features["email"] is True:
            from .email import email_feedback

            # a "_hidden_email_" key will be added
            fb_dict |= email_feedback(need_expert,
                                      fb_dict,
                                      ansdir,
                                      artifacts,
                                      config=config)

    # format feedback dict into text
    # this step has to be the last step
    current_automated_feedback = formatter(fb_dict,
                                           template=config.feedback_template)
    return current_automated_feedback


def test_outcomes(artifacts: Path):
    """Convert xml test outputs into a list of test outcomes.

    test_it::test_a::passed
    test_it::test_b::failed
    ...

    """
    xml = artifacts / 'report.xml'
    outcomes = xmltodict.parse(xml.read_text(encoding='utf-8'))
    testcases = outcomes['testsuites']['testsuite']['testcase']
    if isinstance(testcases, dict):  # if there is only one test outcome
        testcases = [testcases]
    res = {}
    for t in testcases:
        name = t['@classname'] + "::" + t['@name']
        if 'failure' in t:
            outcome = 'failed'
            res[f"{name}::{outcome}"] = t['failure']['@message']
        elif 'error' in t:
            outcome = 'failed'
            res[f"{name}::{outcome}"] = t['error']['@message']
        elif 'skipped' in t:
            continue
        else:
            outcome = 'passed'
            res[f"{name}::{outcome}"] = None
    return res


def automated_feedback(
        outcomes: list,
        ansdir: Path,
        artifacts: Path) -> dict:
    """Map test outcomes into automated feedback messages automatically.

    If automated feedback cannot be found for some questions, then a dict
    containing the context of those questions will be linked with key
    `need_expert`. One can pop that out and handle it afterwards.

    """
    fb_dict = map_feedback(outcomes, ansdir, artifacts)
    return fb_dict


def map_feedback(outcomes: list, ansdir: Path, artifacts: Path):
    """Invoke _map_feedback to generate feedback."""
    try:
        import maps  # dynamically load `maps` under folder `args.feedback`
        fb = _map_feedback(maps, outcomes, ansdir, artifacts)
    except Exception as e:
        raise SocAssessException(e)
    return fb


def _map_feedback(maps,
                  outcomes: list, ansdir: Path, artifacts: Path):
    """Provide mappings between test outcomes and feedback messages.

    Additional content can be provided using `{content}`.

    Variables
    ---------
    mappings: dict[set, tuple[function, str, bool]]
        The key is the test outcomes. The value is a dict, containing the
        feedback string. Optionally, it can contain a function to fill
        `{content}` inside the feedback string. Also, a level indicator

    """
    feedback_dict = {}
    for qn in maps.selected:
        cur_mapping = maps.selected[qn]
        qn_dict = {}
        for oneset in cur_mapping:
            if oneset.issubset(frozenset(outcomes)):
                feedback, fb_level = \
                    feedback_helper.extract(cur_mapping[oneset])
                if fb_level == FeedbackLevel.SINGLE:
                    # stop early in this case
                    return {"_single_feedback_only": [feedback]}
                if fb_level not in qn_dict:
                    qn_dict |= {fb_level: [feedback]}
                else:
                    qn_dict[fb_level].append(feedback)

        if len(qn_dict) == 0:  # if no mapping was found
            if 'need_expert' not in feedback_dict:
                feedback_dict |= {'need_expert': {}}
            qn_context = feedback_helper.context(qn, maps)
            feedback_dict['need_expert'] |= {
                qn: qn_context
            }
        else:
            # only retain the highest feedback level for each question
            qn_highest = qn_dict[sorted(qn_dict.keys(), reverse=True)[0]]
            feedback_dict |= {qn: qn_highest}
    return feedback_dict
