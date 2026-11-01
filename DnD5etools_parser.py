""" Created by srockx
parser for 5e tools monsters
"""

#TODO make it work for dnd wikidot / 5etools
import regex as re

from helpers import create_homebrewery_string, read_monster_text_file

# PATTERNS
line_pattern = r'([^\n]+)'
ac_pattern = r'AC ([0-9]+)'
hp_pattern = r'HP ([^\n]+)'
speed_pattern = r'Speed ([^\n]+)'

CATEGORIES_TO_USE = ["Saving Throws", "Skills", 'Condition Immunities', 'Damage Resistances',
              'Damage Immunities', 'Senses', 'Languages', 'Proficiency Bonus']



def create_homebrewery_from_5etools_markdown_text(monster_text):

    monster_text = monster_text.replace('>', '')
    monster_text = monster_text.replace('___', 'monster,frame,wide', 1)
    with open(f'output_homebrewery.txt', 'w') as f:
            f.write('{{' + monster_text + '}}')

    return '{{' + monster_text + '}}'
