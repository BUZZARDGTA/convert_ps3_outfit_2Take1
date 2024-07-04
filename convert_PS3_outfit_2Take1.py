import re
from pathlib import Path


class IndexItem:
    def __init__(self, type: str, sorted_insert_pos: int, component_id: int, official_game_file__help_name: str, two_take_one__feature__help_name: str, notyourdope_rage_asm__code_comment__help_name: str):
        self.type = type
        self.sorted_insert_pos = sorted_insert_pos
        self.component_id = component_id
        self.official_game_file__help_name = official_game_file__help_name
        self.two_take_one__feature__help_name = two_take_one__feature__help_name
        self.notyourdope_rage_asm__code_comment__help_name = notyourdope_rage_asm__code_comment__help_name


# Map each component and property to their corresponding line index in 2Take1 outfit .ini files.
INDEX_MAP = {
   7:   IndexItem('[COMPONENTS]',           0,   0,   'head',  'Head',       'face'),
   17:  IndexItem('[COMPONENTS]',           1,   5,   'hand',  'Parachute',  'hands'),
   9:   IndexItem('[COMPONENTS]',           2,   1,   'berd',  'Mask',       'head'),
   15:  IndexItem('[COMPONENTS]',           3,   4,   'lowr',  'Legs',       'legs'),
   11:  IndexItem('[COMPONENTS]',           4,   2,   'hair',  'Hair',       'hair'),
   21:  IndexItem('[COMPONENTS]',           5,   7,   'teef',  'Accessory',  'special 1'),
   13:  IndexItem('[COMPONENTS]',           6,   3,   'uppr',  'Gloves',     'torso'),
   29:  IndexItem('[COMPONENTS]',           7,   11,  'jbib',  'Torso',      'torso 2'),
   19:  IndexItem('[COMPONENTS]',           8,   6,   'feet',  'Feet',       'shoes'),
   23:  IndexItem('[COMPONENTS]',           9,  8,   'accs',  'Torso 2',    'special 2'),
   25:  IndexItem('[COMPONENTS]',           10,  9,   'task',  'Vest',       'special 3'),
   27:  IndexItem('[COMPONENTS]',           11,  10,  'decl',  'Decal',      'textures'),
   8:   IndexItem('[COMPONENTS_TEXTURES]',  0,   0,   'head',  'Head',       'face texture'),
   18:  IndexItem('[COMPONENTS_TEXTURES]',  1,   5,   'hand',  'Parachute',  'hands texture'),
   10:  IndexItem('[COMPONENTS_TEXTURES]',  2,   1,   'berd',  'Mask',       'head texture'),
   22:  IndexItem('[COMPONENTS_TEXTURES]',  3,   7,   'teef',  'Accessory',  'special 1 texture'),
   16:  IndexItem('[COMPONENTS_TEXTURES]',  4,   4,   'lowr',  'Legs',       'legs texture'),
   12:  IndexItem('[COMPONENTS_TEXTURES]',  5,   2,   'hair',  'Hair',       'hair texture'),
   14:  IndexItem('[COMPONENTS_TEXTURES]',  6,   3,   'uppr',  'Gloves',     'torso texture'),
   20:  IndexItem('[COMPONENTS_TEXTURES]',  7,   6,   'feet',  'Feet',       'shoes texture'),
   24:  IndexItem('[COMPONENTS_TEXTURES]',  8,   8,   'accs',  'Torso 2',    'special 2 texture'),
   26:  IndexItem('[COMPONENTS_TEXTURES]',  9,  9,   'task',  'Vest',       'special 3 texture'),
   28:  IndexItem('[COMPONENTS_TEXTURES]',  10,  10,  'decl',  'Decal',      'textures texture'),
   30:  IndexItem('[COMPONENTS_TEXTURES]',  11,  11,  'jbib',  'Torso',      'torso 2 texture'),
   1:   IndexItem('[PROPERTIES]',           0,   0,   'head',  'Hat',        'hat'),
   3:   IndexItem('[PROPERTIES]',           1,   1,   'eyes',  'Glasses',    'glasses'),
   5:   IndexItem('[PROPERTIES]',           2,   2,   'ears',  'Ears',       'ear pieces'),
   2:   IndexItem('[PROPERTIES_TEXTURES]',  0,   0,   'head',  'Hat',        'hat texture'),
   6:   IndexItem('[PROPERTIES_TEXTURES]',  1,   2,   'ears',  'Ears',       'ear pieces texture'),
   4:   IndexItem('[PROPERTIES_TEXTURES]',  2,   1,   'eyes',  'Glasses',    'glasses texture'),
}
# User settings START
#MODLOADER_PATH = Path('D:/Downloads/GTA Stuff/PS3/2) MODLOADERS/BUZZARD v6.1 Private/source by JR/ModLoader.csa')
MODLOADER_PATH = Path('D:/Downloads/GTA Stuff/PS3/2) MODLOADERS/BUZZARD v6.1 Private/source by JR/BUZZARD_6_1_male_outfits.csa')
#MODLOADER_PATH = Path('D:/Downloads/GTA Stuff/PS3/2) MODLOADERS/BUZZARD v6.1 Private/source by JR/BUZZARD_6_1_female_outfits.csa')
FILENAME_MALE_OR_FEMALE = 'male' # male / female / mixed
FILENAME_SANITIZER = True
# User settings END
RE_OUTFIT_PATTERN = re.compile(
    r'^:(?P<outfit_label>[\w&\.-]+)(?: ?//.*)?$\n(?P<outfit_data>(?:Push1? (?:-1|\d{1,3})(?: ?//.*)?$(?:\n)){30})Call @[\w&\.-]+$(?:\nPushString "(?P<outfit_name>[^"]+)")?',
    re.MULTILINE
)
RE_OUTFIT_PUSH_VALUE_PATTERN = re.compile(r'^Push1? (?P<int_value>-1|\d{1,3})$')
RE_FILENAME_SANITIZER_PATTERN = re.compile(r'~b~|~n~|~p~|~r~|:')
INVALID_WINDOWS_FILENAME_CHARS = set('\\/:*?"<>|')


def convert_invalid_windows_filename_chars_to_unicode(filename: str):
    return ''.join(f'U+{ord(char):04X}' if char in INVALID_WINDOWS_FILENAME_CHARS else char for char in filename)

def outfit_converter():
    outfit_categories: dict[str, list[str]] = {
        '[COMPONENTS]': [''] * 12,
        '[COMPONENTS_TEXTURES]': [''] * 12,
        '[PROPERTIES]': [''] * 3,
        '[PROPERTIES_TEXTURES]': [''] * 3,
    }

    for i, int_value in enumerate(outfit_int_values_list, start=1):
        map_item = INDEX_MAP[i]

        outfit_categories[map_item.type][map_item.sorted_insert_pos] = f'index{map_item.component_id}={int_value} ;; {map_item.two_take_one__feature__help_name}'

    return '\n'.join(
        f'{category}\n' +
        '\n'.join(outfit_categories[category])
        for category in outfit_categories
    ).removesuffix('\n')

def generate_outfit_filename():
    outfit_path = Path(f'PS3_{FILENAME_MALE_OR_FEMALE}_{str(i).zfill(max_generated_outfits__index_length)}.ini')
    extra_outfit_name = None

    if outfit_name:
        if FILENAME_SANITIZER:
            extra_outfit_name = RE_FILENAME_SANITIZER_PATTERN.sub('', outfit_name)
        else:
            extra_outfit_name = outfit_name
    elif outfit_label:
        extra_outfit_name = outfit_label

    if extra_outfit_name:
        extra_outfit_name = convert_invalid_windows_filename_chars_to_unicode(extra_outfit_name)
        outfit_path = outfit_path.with_stem(f'{outfit_path.stem}_{extra_outfit_name}')

    return outfit_path


matches = list(RE_OUTFIT_PATTERN.finditer(MODLOADER_PATH.read_text(encoding='utf-8')))
max_generated_outfits__index_length = len(str(len(matches)))

for i, match in enumerate(matches, start=1):
    outfit_label = match['outfit_label']
    outfit_data = match['outfit_data']
    outfit_name = match['outfit_name']

    outfit_int_values_list: list[int] = []
    for data in outfit_data.splitlines(keepends=False):
        match = RE_OUTFIT_PUSH_VALUE_PATTERN.search(data)
        outfit_int_values_list.append(int(match['int_value']))

    translated_outfit_data = outfit_converter()
    outfit_path = generate_outfit_filename()

    outfit_path.write_text(translated_outfit_data, encoding='utf-8')
    print(f'Created outfit: "{outfit_path}"')
