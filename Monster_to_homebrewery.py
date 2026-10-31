""" Created by srockx
A python script to convert plain, copied DnD beyond monster to homebrewery format

Currently does not support multi-paragraph action descriptions or Legendary actions
"""

#TODO make it work for dnd wikidot / 5etools
import regex as re

# PATTERNS
name_pattern = r'^([^\s]+)'
line_pattern = r'([^\n]+)'
ac_pattern = r'Armor Class ([0-9]+)'
hp_pattern = r'Hit Points ([^\n]+)'
speed_pattern = r'Speed ([^\n]+)'

CATEGORIES_TO_USE = ["Saving Throws", "Skills", 'Condition Immunities', 'Damage Resistances',
              'Damage Immunities', 'Senses', 'Languages', 'Proficiency Bonus']



def create_homebrewery_from_text():
    with open('monster_text.txt', 'r') as f:
        monster_text = f.read()

    name = re.findall(name_pattern, monster_text)[0]
    creature_type = re.findall(line_pattern, monster_text)[1] # second line
    # link if link is copied in on third line
    picture_link = re.findall(line_pattern, monster_text)[2]  # second line
    if not picture_link.startswith('https'):
        picture_link = '' # don't put in link if not provided
    ac = re.findall(ac_pattern, monster_text)[0]
    hp_and_hitdice = re.findall(hp_pattern, monster_text)[0]
    speed = re.findall(speed_pattern, monster_text)[0]

    skill_string = create_skills_string(monster_text)
    skills_etc_string = create_skills_etc_string(monster_text)

    # get traits and action section separately
    # TODO traits are not mentioned on aidedd, othewise could work
    traits_start = monster_text.find('Traits\n')
    actions_start = monster_text.index('Actions\n')

    if traits_start != -1:
        # only search trait section
        traits_string = create_traits_string(monster_text[traits_start+7:actions_start])
    else:
        traits_string = ''

    # TODO deal with legendary actions

    actions_string = create_actions_string(monster_text[actions_start+8:])

    text = f"""monster,frame,wide
## {name}
*{creature_type}*

![{name}_picture]({picture_link}) {{width:200px,wrapRight}}
___
**Armor Class** :: {ac} 
**Hit Points**  :: {hp_and_hitdice}
**Speed**       :: {speed}
___
|  STR  |  DEX  |  CON  |  INT  |  WIS  |  CHA  |
|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|
{skill_string}
___
{skills_etc_string}
___
### Traits
{traits_string}
:

### Actions
{actions_string}
: 
"""
    with open(f'output_homebrewery.txt', 'w') as f:
            f.write('{{' + text + '}}')

    return '{{' + text + '}}'

def create_skills_etc_string(monster_text):
    skills_etc_string = ''
    for c in CATEGORIES_TO_USE:
        pattern = f'{c} ([^\n]+)'
        match = re.findall(pattern, monster_text)
        if match:
            text = match[0]
            skills_etc_string += f"**{c}** :: {text}\n"
    return skills_etc_string[0:-1] # remove last new line

def create_traits_string(traits_text):
    "***Ability.*** {abilities_string}"
    traits_string = ''
    pattern = r'([^\.\n]+)\.([^\n]+)'
    matches = re.findall(pattern, traits_text)
    for match in matches:
        trait_name = match[0]
        trait_description = match[1]
        traits_string += f"***{trait_name}.*** {trait_description}\n\n"

    return traits_string[0:-1]# remove last new line


def create_actions_string(actions_text):
    # TODO deal with actions that have more than one paragraph (kinda hard?)
    action_string = ''
    pattern = r'([^\.\n]+)\.([^\n]+)'
    matches = re.findall(pattern, actions_text)
    for match in matches:
        action_name = match[0]
        action_description = match[1]

        action_description = action_description.replace('Hit:', '*Hit:*')
        action_description = re.sub(r'^([^\.]+)\. ([^:]+)Attack:', r'\g<1>. *\g<2> Attack:*', action_description)
        action_description = re.sub(r'DC ([0-9]{1,2})', r'*DC \g<1>*', action_description)
        action_string += f"***{action_name}.*** {action_description}\n\n"

    return action_string[0:-1] # remove last newline

def create_skills_string(monster_text):
    "|{strength} ({mod(strength)})|{dex} ({mod(dex)|{con} ({mod(cond)})|{intelligence} ({mod(intelligence)})|{wis} ({mod(wis)})|{cha} ({mod(cha)})|"
    skill_string = '|'
    for skill in ['STR', 'DEX', 'CON', 'INT', 'WIS', 'CHA']:
        pattern = f'{skill}\n([0-9]+)'
        match = re.findall(pattern, monster_text)
        skill_modifier = match[0] if match else 10
        skill_string += f"{skill_modifier} {mod(int(skill_modifier))}|"
    return skill_string

def modifier(number):
    return int((number - 10)/2)

def mod(skill) -> str:
    m = modifier(skill) #
    if m >= 0:
        return f'+{m}'
    else:
        return f'-{m}'

if __name__ == '__main__':
    text = create_homebrewery_from_text()
    print(text)