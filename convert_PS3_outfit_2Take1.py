import re
from pathlib import Path


class IndexItem:
    def __init__(self, type: str, component_id: int, official_game_file__help_name: str, two_take_one__feature__help_name: str, notyourdope_rage_asm__code_comment__help_name: str):
        self.type = type
        self.component_id = component_id
        self.official_game_file__help_name = official_game_file__help_name
        self.two_take_one__feature__help_name = two_take_one__feature__help_name
        self.notyourdope_rage_asm__code_comment__help_name = notyourdope_rage_asm__code_comment__help_name


# Map each component and property to their corresponding line index in 2Take1 outfit .ini files.
INDEX_MAP = {
   7:   IndexItem('[COMPONENTS]',           0,   'head',  'Head',       'face'),
   17:  IndexItem('[COMPONENTS]',           5,   'hand',  'Parachute',  'hands'),
   9:   IndexItem('[COMPONENTS]',           1,   'berd',  'Mask',       'head'),
   15:  IndexItem('[COMPONENTS]',           4,   'lowr',  'Legs',       'legs'),
   11:  IndexItem('[COMPONENTS]',           2,   'hair',  'Hair',       'hair'),
   21:  IndexItem('[COMPONENTS]',           7,   'teef',  'Accessory',  'special 1'),
   13:  IndexItem('[COMPONENTS]',           3,   'uppr',  'Gloves',     'torso'),
   29:  IndexItem('[COMPONENTS]',           11,  'jbib',  'Torso',      'torso 2'),
   19:  IndexItem('[COMPONENTS]',           6,   'feet',  'Feet',       'shoes'),
   23:  IndexItem('[COMPONENTS]',           8,   'accs',  'Torso 2',    'special 2'),
   25:  IndexItem('[COMPONENTS]',           9,   'task',  'Vest',       'special 3'),
   27:  IndexItem('[COMPONENTS]',           10,  'decl',  'Decal',      'textures'),
   8:   IndexItem('[COMPONENTS_TEXTURES]',  0,   'head',  'Head',       'face texture'),
   18:  IndexItem('[COMPONENTS_TEXTURES]',  5,   'hand',  'Parachute',  'hands texture'),
   10:  IndexItem('[COMPONENTS_TEXTURES]',  1,   'berd',  'Mask',       'head texture'),
   22:  IndexItem('[COMPONENTS_TEXTURES]',  7,   'teef',  'Accessory',  'special 1 texture'),
   16:  IndexItem('[COMPONENTS_TEXTURES]',  4,   'lowr',  'Legs',       'legs texture'),
   12:  IndexItem('[COMPONENTS_TEXTURES]',  2,   'hair',  'Hair',       'hair texture'),
   14:  IndexItem('[COMPONENTS_TEXTURES]',  3,   'uppr',  'Gloves',     'torso texture'),
   20:  IndexItem('[COMPONENTS_TEXTURES]',  6,   'feet',  'Feet',       'shoes texture'),
   24:  IndexItem('[COMPONENTS_TEXTURES]',  8,   'accs',  'Torso 2',    'special 2 texture'),
   26:  IndexItem('[COMPONENTS_TEXTURES]',  9,   'task',  'Vest',       'special 3 texture'),
   28:  IndexItem('[COMPONENTS_TEXTURES]',  10,  'decl',  'Decal',      'textures texture'),
   30:  IndexItem('[COMPONENTS_TEXTURES]',  11,  'jbib',  'Torso',      'torso 2 texture'),
   1:   IndexItem('[PROPERTIES]',           0,   'head',  'Hat',        'hat'),
   3:   IndexItem('[PROPERTIES]',           1,   'eyes',  'Glasses',    'glasses'),
   5:   IndexItem('[PROPERTIES]',           2,   'ears',  'Ears',       'ear pieces'),
   2:   IndexItem('[PROPERTIES_TEXTURES]',  0,   'head',  'Hat',        'hat texture'),
   6:   IndexItem('[PROPERTIES_TEXTURES]',  2,   'ears',  'Ears',       'ear pieces texture'),
   4:   IndexItem('[PROPERTIES_TEXTURES]',  1,   'eyes',  'Glasses',    'glasses texture'),
}
MODLOADER_PATH = Path('D:/Downloads/GTA Stuff/PS3/2) MODLOADERS/BUZZARD v6.1 Private/source by JR/ModLoader.csa')
RE_OUTFIT_PATTERN = re.compile(
    r'^:(?P<outfit_label>[\w&\.-]+)(?: ?//.*)?$\n(?P<outfit_data>(?:Push1? (?:-1|\d{1,3})(?: ?//.*)?$(?:\n)){30})Call @[\w&\.-]+$(?:\nPushString "(?P<outfit_name>[^"]+)")?',
    re.MULTILINE
)
RE_OUTFIT_PUSH_VALUE_PATTERN = re.compile(r'^Push1? (?P<int_value>-1|\d{1,3})$')
INVALID_WINDOWS_FILENAME_CHARS = set("\\/:*?\"<>|")


def translate_outfit(outfit_int_values_list: list[int]):
    categories: dict[str, list[str]] = {
        '[COMPONENTS]': [],
        '[COMPONENTS_TEXTURES]': [],
        '[PROPERTIES]': [],
        '[PROPERTIES_TEXTURES]': [],
    }

    for i, int_value in enumerate(outfit_int_values_list, start=1):
        map_item = INDEX_MAP[i]

        categories[map_item.type].append(f'index{map_item.component_id}={int_value} ;; {map_item.two_take_one__feature__help_name}')

    sorted_categories: dict[str, list[str]] = {
        '[COMPONENTS]': [],
        '[COMPONENTS_TEXTURES]': [],
        '[PROPERTIES]': [],
        '[PROPERTIES_TEXTURES]': [],
    }

    for map_item2 in INDEX_MAP.values():
        for category in sorted_categories:
            if map_item2.type == category:
                for line in categories[category]:
                    if line.startswith(f'index{map_item2.component_id}='):
                        sorted_categories[category].append(line)

    return '\n'.join(
        f'{category}\n' +
        '\n'.join(sorted_categories[category])
        for category in sorted_categories
    ).removesuffix('\n')

def convert_invalid_chars(filename: str):
    return ''.join(f"U+{ord(char):04X}" if char in INVALID_WINDOWS_FILENAME_CHARS else char for char in filename)


for i, match in enumerate(RE_OUTFIT_PATTERN.finditer(MODLOADER_PATH.read_text(encoding='utf-8')), start=1):
    outfit_label = match['outfit_label']
    outfit_data = match['outfit_data']
    outfit_name = match['outfit_name']

    outfit_int_values_list = []
    for data in outfit_data.splitlines(keepends=False):
        match = RE_OUTFIT_PUSH_VALUE_PATTERN.search(data)
        outfit_int_values_list.append(int(match['int_value']))

    translated_output_data = translate_outfit(outfit_int_values_list)

    outfit_filename = Path(f"PS3_outfit_{i}.ini")

    base_name_to_sanitize = None
    if outfit_name:
        base_name_to_sanitize = outfit_name
    elif outfit_label:
        base_name_to_sanitize = outfit_label

    if base_name_to_sanitize:
        sanitized_base_name = convert_invalid_chars(base_name_to_sanitize)
        outfit_filename = outfit_filename.with_name(f"{outfit_filename.stem}_{sanitized_base_name}").with_suffix(outfit_filename.suffix)

    outfit_filename.write_text(translated_output_data, encoding='utf-8')

    print(f"Created outfit: {outfit_filename}")
exit(0)
