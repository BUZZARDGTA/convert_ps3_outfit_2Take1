import re

RE_PUSH_PATTERN = re.compile(r'Push1?\s+(?P<int_value>-?\d+)')

class IndexItem:
    def __init__(self, type_str: str, index_int: int, comment_str: str):
        self.type = type_str
        self.index = index_int
        self.comment = comment_str

# Map each component and property to their corresponding index in 2Take1 outfit .ini file.
index_map = {
   7:  IndexItem('[COMPONENTS]',           0,   'Head -- face'),
   23: IndexItem('[COMPONENTS]',           5,   'Parachute -- special 2'),
   9:  IndexItem('[COMPONENTS]',           1,   'Mask -- head'),
   15: IndexItem('[COMPONENTS]',           4,   'Legs -- legs'),
   11: IndexItem('[COMPONENTS]',           2,   'Hair -- hair'),
   21: IndexItem('[COMPONENTS]',           7,   'Accessory -- special 1'),
   17: IndexItem('[COMPONENTS]',           3,   'Gloves -- hands'),
   13: IndexItem('[COMPONENTS]',           11,  'Torso -- torso'),
   19: IndexItem('[COMPONENTS]',           6,   'Feet -- shoes'),
   29: IndexItem('[COMPONENTS]',           8,   'Torso 2 -- torso 2'),
   25: IndexItem('[COMPONENTS]',           9,   'Vest -- special 3'),
   27: IndexItem('[COMPONENTS]',           10,  'Decal -- textures'),
   8:  IndexItem('[COMPONENTS_TEXTURES]',  0,   'Head -- face texture'),
   24: IndexItem('[COMPONENTS_TEXTURES]',  5,   'Parachute -- special 2 texture'),
   10: IndexItem('[COMPONENTS_TEXTURES]',  1,   'Mask -- head texture'),
   22: IndexItem('[COMPONENTS_TEXTURES]',  7,   'Accessory -- special 1 texture'),
   16: IndexItem('[COMPONENTS_TEXTURES]',  4,   'Legs -- legs texture'),
   12: IndexItem('[COMPONENTS_TEXTURES]',  2,   'Hair -- hair texture'),
   18: IndexItem('[COMPONENTS_TEXTURES]',  3,   'Gloves -- hands texture'),
   20: IndexItem('[COMPONENTS_TEXTURES]',  6,   'Feet -- shoes texture'),
   30: IndexItem('[COMPONENTS_TEXTURES]',  8,   'Torso 2 -- torso 2 texture'),
   26: IndexItem('[COMPONENTS_TEXTURES]',  9,   'Vest -- special 3 texture'),
   28: IndexItem('[COMPONENTS_TEXTURES]',  10,  'Decal -- textures texture'),
   14: IndexItem('[COMPONENTS_TEXTURES]',  11,  'Torso -- torso texture'),
   1:  IndexItem('[PROPERTIES]',           0,   'Hat -- hat'),
   3:  IndexItem('[PROPERTIES]',           1,   'Glasses -- glasses'),
   5:  IndexItem('[PROPERTIES]',           2,   'Ears -- ear pieces'),
   2:  IndexItem('[PROPERTIES_TEXTURES]',  0,   'Hat -- hat texture'),
   6:  IndexItem('[PROPERTIES_TEXTURES]',  2,   'Ears -- ear pieces texture'),
   4:  IndexItem('[PROPERTIES_TEXTURES]',  1,   'Glasses -- glasses texture'),
}


def translate_outfit(input_data: str):
    categories: dict[str, list[str]] = {
        '[COMPONENTS]': [],
        '[COMPONENTS_TEXTURES]': [],
        '[PROPERTIES]': [],
        '[PROPERTIES_TEXTURES]': [],
    }

    i = 0
    for line in input_data.splitlines():
        if not line.startswith('Push '):
            continue

        match = RE_PUSH_PATTERN.search(line)
        if not match:
            continue
        int_value = int(match["int_value"])

        i += 1
        item = index_map[i]

        categories[item.type].append(f'index{item.index}={int_value} ;; {item.comment}')

    sorted_categories: dict[str, list[str]] = {
        '[COMPONENTS]': [],
        '[COMPONENTS_TEXTURES]': [],
        '[PROPERTIES]': [],
        '[PROPERTIES_TEXTURES]': [],
    }

    for map_item in index_map.values():
        for category in sorted_categories:
            if map_item.type == category:
                for item in categories[category]:
                    if item.startswith(f'index{map_item.index}='):
                        sorted_categories[category].append(item)

    # Output the result
    output_data = ''
    for category in sorted_categories:
        output_data += f'{category}\n'
        output_data += '\n'.join(sorted_categories[category]) + '\n'
    output_data = output_data.removesuffix("\n")

    return output_data


# Input data
input_data = '''
Push 38
Push 2
Push -1
Push -1
Push -1
Push -1
Push 0
Push 0
Push 36
Push 0
Push 10
Push 6
Push 18
Push 1
Push 30
Push 2
Push 38
Push 1
Push 1
Push 2
Push 23
Push 1
Push 35
Push 0
Push 2
Push 0
Push 0
Push 0
Push 46
Push 1
'''

# Translate the input data
output_data = translate_outfit(input_data)
print(output_data)
