"""
Export LibreLingo courses in the JSON format expected by the web app
"""

import itertools
from .types import *
from .utils import *
from .dictionary import *
from .challenge_types import *
from .module import *

__version__ = '0.1.0'


def get_course_data(course):
    """
    Format Course according to the JSON structure
    """

    return {
        "languageName": course.language_name,
        "languageCode": course.language_code,
        "specialCharacters": course.special_characters,
        "license": {
            "name": {
                "short": course.license.name,
                "full": course.license.full_name,

            },
            "link": course.license.link,
        },
        "modules": [
            get_module_summary(module) for module in course.modules
        ]
    }


def make_challenges_using(callback, data_source, course):
    return list(itertools.chain(
        *map(lambda item: callback(item, course), data_source)))


def get_challenges_data(skill, course):
    return sum([
        make_challenges_using(get_phrase_challenges, skill.phrases, course),
        make_challenges_using(get_word_challenges, skill.words, course),
    ], start=[])


def get_skill_data(skill, course):
    """
    Format Course according to the JSON structure
    """

    return {
        "id": get_opaque_id(skill, "Skill"),
        "levels": calculate_number_of_levels(
            len(skill.words), len(skill.phrases)),
        "challenges": get_challenges_data(skill, course),
    }