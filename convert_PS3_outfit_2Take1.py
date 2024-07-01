import re


class IndexItem:
    def __init__(self, type_str: str, index_int: int, comment_str: str):
        self.type = type_str
        self.index = index_int
        self.comment = comment_str


# Map each component and property to their corresponding index in 2Take1 outfit .ini file.
INDEX_MAP = {
   7:  IndexItem('[COMPONENTS]',           0,   'Head -- face'),
   17: IndexItem('[COMPONENTS]',           5,   'Parachute -- hands'),
   9:  IndexItem('[COMPONENTS]',           1,   'Mask -- head'),
   15: IndexItem('[COMPONENTS]',           4,   'Legs -- legs'),
   11: IndexItem('[COMPONENTS]',           2,   'Hair -- hair'),
   21: IndexItem('[COMPONENTS]',           7,   'Accessory -- special 1'),
   13: IndexItem('[COMPONENTS]',           3,   'Gloves -- torso'),
   29: IndexItem('[COMPONENTS]',           11,  'Torso -- torso 2'),
   19: IndexItem('[COMPONENTS]',           6,   'Feet -- shoes'),
   23: IndexItem('[COMPONENTS]',           8,   'Torso 2 -- special 2 texture'),
   25: IndexItem('[COMPONENTS]',           9,   'Vest -- special 3'),
   27: IndexItem('[COMPONENTS]',           10,  'Decal -- textures'),
   8:  IndexItem('[COMPONENTS_TEXTURES]',  0,   'Head -- face texture'),
   18: IndexItem('[COMPONENTS_TEXTURES]',  5,   'Parachute -- hands texture'),
   10: IndexItem('[COMPONENTS_TEXTURES]',  1,   'Mask -- head texture'),
   22: IndexItem('[COMPONENTS_TEXTURES]',  7,   'Accessory -- special 1 texture'),
   16: IndexItem('[COMPONENTS_TEXTURES]',  4,   'Legs -- legs texture'),
   12: IndexItem('[COMPONENTS_TEXTURES]',  2,   'Hair -- hair texture'),
   14: IndexItem('[COMPONENTS_TEXTURES]',  3,   'Gloves -- torso texture'),
   20: IndexItem('[COMPONENTS_TEXTURES]',  6,   'Feet -- shoes texture'),
   24: IndexItem('[COMPONENTS_TEXTURES]',  8,   'Torso 2 -- special 2 texture'),
   26: IndexItem('[COMPONENTS_TEXTURES]',  9,   'Vest -- special 3 texture'),
   28: IndexItem('[COMPONENTS_TEXTURES]',  10,  'Decal -- textures texture'),
   30: IndexItem('[COMPONENTS_TEXTURES]',  11,  'Torso -- torso 2 texture'),
   1:  IndexItem('[PROPERTIES]',           0,   'Hat -- hat'),
   3:  IndexItem('[PROPERTIES]',           1,   'Glasses -- glasses'),
   5:  IndexItem('[PROPERTIES]',           2,   'Ears -- ear pieces'),
   2:  IndexItem('[PROPERTIES_TEXTURES]',  0,   'Hat -- hat texture'),
   6:  IndexItem('[PROPERTIES_TEXTURES]',  2,   'Ears -- ear pieces texture'),
   4:  IndexItem('[PROPERTIES_TEXTURES]',  1,   'Glasses -- glasses texture'),
}
RE_PUSH_PATTERN = re.compile(r'^\s*Push1?\s+(?P<int_value>-?\d{1,3})(?!\d)', re.MULTILINE)


def translate_outfit(input_data: str):
    categories: dict[str, list[str]] = {
        '[COMPONENTS]': [],
        '[COMPONENTS_TEXTURES]': [],
        '[PROPERTIES]': [],
        '[PROPERTIES_TEXTURES]': [],
    }

    for i, match in enumerate(RE_PUSH_PATTERN.finditer(input_data), start=1):
        int_value = int(match.group("int_value"))
        map_item = INDEX_MAP[i]

        categories[map_item.type].append(f'index{map_item.index}={int_value} ;; {map_item.comment}')

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
                    if line.startswith(f'index{map_item2.index}='):
                        sorted_categories[category].append(line)

    # Output the result
    return '\n'.join(
        f'{category}\n' +
        '\n'.join(sorted_categories[category])
        for category in sorted_categories
    ).removesuffix("\n")


# Input data
input_data = '''
Push 39//hat
Push 0//hat texture
Push -1//glasses
Push -1//glasses texture
Push -1//ear pieces
Push -1//ear pieces texture
Push 0//face
Push 0//face texture
Push 54//head
Push 7//head texture
Push 13//hair
Push 4//hair texture
Push 81//torso
Push 0//torso texture
Push 28//legs
Push 1//legs texture
Push 10//hands
Push 7//hands texture
Push 8//shoes
Push 2//shoes texture
Push 41//special 1
Push 0//special 1 texture
Push 58//special 2
Push 0//special 2 texture
Push 0//special 3
Push 0//special 3 texture
Push 8//textures
Push 0//textures texture
Push 0//torso 2
Push 0//torso 2 texture
'''

# Translate the input data
output_data = translate_outfit(input_data)
print(output_data)
