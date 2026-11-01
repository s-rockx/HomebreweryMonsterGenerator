def create_homebrewery_string(ac,
                              actions_string: str,
                              creature_type,
                              hp_and_hitdice,
                              name,
                              picture_link: str,
                              skill_string: str,
                              skills_etc_string: str,
                              speed,
                              traits_string: str) -> str:
    # TODO implement reactions/ bonus actions / Legendary actions
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
    return text


def read_monster_text_file():
    with open('monster_text.txt', 'r') as f:
        monster_text = f.read()
    return monster_text