""" Created by srockx
A python script to convert plain, copied DnD beyond monster to homebrewery format

Currently does not support multi-paragraph action descriptions or Legendary actions
"""
from DnD5etools_parser import create_homebrewery_from_5etools_markdown_text
#TODO make it work for dnd wikidot / 5etools
from aidedd_and_dndbeyond_parser import create_homebrewery_from_text_aidedd_or_dndbeyond
from helpers import read_monster_text_file


# PATTERNS

if __name__ == '__main__':
    monster_text = read_monster_text_file()

    # this is markdown from 5etools
    print(monster_text[0:3])
    if monster_text[0:3] == '___':
        print('bla')
        text = create_homebrewery_from_5etools_markdown_text(monster_text)
    # assume aidedd or dndbeyond
    else:
        text = create_homebrewery_from_text_aidedd_or_dndbeyond(monster_text)
    print(text)