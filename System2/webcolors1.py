import math
import re

def _reversedict(d):
    return dict(list(zip(list(d.values()), list(d.keys()))))

HEX_COLOR_RE = re.compile(r'^#([a-fA-F0-9]{3}|[a-fA-F0-9]{6})$')
SUPPORTED_SPECIFICATIONS = ('html4', 'css2', 'css21', 'css3')

# Mappings of color names to normalized hexadecimal color values.
#################################################################
html4_names_to_hex = {'blue34': '#00ffff',
                      'black1': '#000000',
                      'blue35': '#0000ff',
                      'pink1': '#ff00ff',
                      'green1': '#008000',
                      'gray1': '#808080',
                      'yellow1': '#00ff00',
                      'maroon': '#800000',
                      'blue36': '#000080',
                      'green2': '#808000',
                      'purple1': '#800080',
                      'red1': '#ff0000',
                      'gray2': '#c0c0c0',
                      'teal': '#008080',
                      'white1': '#ffffff',
                      'yellow2': '#ffff00'}

css2_names_to_hex = html4_names_to_hex

css21_names_to_hex = dict(html4_names_to_hex, orange1='#ffa500')
css3_names_to_hex = {'blue1': '#00ffff',
                     'blue2': '#f0f8ff',
                     'blue3': '#faebd7',
                     'blue4': '#00ffff',
                     'blue5': '#7fffd4',
                     'blue6': '#f0ffff',
                     'cream1': '#f5f5dc',
                     'cream2': '#ffe4c4',
                     'black2': '#000000',
                     'cream3': '#ffebcd',
                     'blue7': '#0000ff',
                     'blue8': '#8a2be2',
                     'brown1': '#a52a2a',
                     'cream4': '#deb887',
                     'blue9': '#5f9ea0',
                     'green3': '#7fff00',
                     'brown2': '#d2691e',
                     'coral': '#ff7f50',
                     'blue10': '#6495ed',
                     'white2': '#fff8dc',
                     'red2': '#dc143c',
                     'blue11': '#00ffff',
                     'blue12': '#00008b',
                     'blue13': '#008b8b',
                     'brown3': '#b8860b',
                     'gray3': '#a9a9a9',
                     'green4': '#006400',
                     'darkkhaki': '#bdb76b',
                     'pink2': '#8b008b',
                     'green5': '#556b2f',
                     'orange2': '#ff8c00',
                     'purple2': '#9932cc',
                     'red3': '#8b0000',
                     'darksalmon': '#e9967a',
                     'green6': '#8fbc8f',
                     'blue14': '#483d8b',
                     'gray4': '#2f4f4f',
                     'blue15': '#00ced1',
                     'violet3': '#9400d3',
                     'pink3': '#ff1493',
                     'blue16': '#00bfff',
                     'gray5': '#696969',
                     'blue17': '#1e90ff',
                     'red4': '#b22222',
                     'white3': '#fffaf0',
                     'green7': '#228b22',
                     'pink4': '#ff00ff',
                     'gray6': '#dcdcdc',
                     'white4': '#f8f8ff',
                     'yellow3': '#ffd700',
                     'yellow4': '#daa520',
                     'gray7': '#808080',
                     'green8': '#008000',
                     'green9': '#adff2f',
                     'green10': '#f0fff0',
                     'pink5': '#ff69b4',
                     'red5': '#cd5c5c',
                     'indigo': '#4b0082',
                     'white5': '#fffff0',
                     'yellow5': '#f0e68c',
                     'violet1': '#e6e6fa',
                     'pink6': '#fff0f5',
                     'green11': '#7cfc00',
                     'yellow6': '#fffacd',
                     'blue18': '#add8e6',
                     'lightcoral': '#f08080',
                     'blue19': '#e0ffff',
                     'yellow7': '#fafad2',
                     'gray8': '#d3d3d3',
                     'green12': '#90ee90',
                     'pink7': '#ffb6c1',
                     'orange3': '#ffa07a',
                     'green13': '#20b2aa',
                     'blue20': '#87cefa',
                     'gray9': '#778899',
                     'gray10': '#b0c4de',
                     'cream5': '#ffffe0',
                     'green14': '#00ff00',
                     'green15': '#32cd32',
                     'cream6': '#faf0e6',
                     'red6': '#ff00ff',
                     'maroon': '#800000',
                     'green16': '#66cdaa',
                     'blue21': '#0000cd',
                     'purple3': '#ba55d3',
                     'purple4': '#9370d8',
		             'purple5':'#9370db',
                     'green17': '#3cb371',
                     'blue22': '#7b68ee',
                     'green18': '#00fa9a',
                     'blue23': '#48d1cc',
                     'pink8': '#c71585',
                     'blue24': '#191970',
                     'green19': '#f5fffa',
                     'cream7': '#ffe4e1',
                     'cream8': '#ffe4b5',
                     'cream9': '#ffdead',
                     'blue25': '#000080',
                     'cream10': '#fdf5e6',
                     'green20': '#808000',
                     'green21': '#6b8e23',
                     'orange4': '#ffa500',
                     'orange5': '#ff4500',
                     'purple6': '#da70d6',
                     'yellow8': '#eee8aa',
                     'green22': '#98fb98',
                     'blue26': '#afeeee',
                     'pink9': '#d87093',
                     'cream11': '#ffefd5',
                     'cream12': '#ffdab9',
                     'brown4': '#cd853f',
                     'pink10': '#ffc0cb',
                     'purple7': '#dda0dd',
                     'blue27': '#b0e0e6',
                     'purple8': '#800080',
                     'red7': '#ff0000',
                     'brown5': '#bc8f8f',
                     'blue28': '#4169e1',
                     'brown6': '#8b4513',
                     'orange6': '#fa8072',
                     'brown7': '#f4a460',
                     'green23': '#2e8b57',
                     'cream13': '#fff5ee',
                     'brown8': '#a0522d',
                     'gray11': '#c0c0c0',
                     'blue29': '#87ceeb',
                     'blue30': '#6a5acd',
                     'gray12': '#708090',
                     'white6': '#fffafa',
                     'green24': '#00ff7f',
                     'blue31': '#4682b4',
                     'brown9': '#d2b48c',
                     'blue32': '#008080',
                     'purple9': '#d8bfd8',
                     'orange7': '#ff6347',
                     'blue33': '#40e0d0',
                     'violet2': '#ee82ee',
                     'cream14': '#f5deb3',
                     'white7': '#ffffff',
                     'white8': '#f5f5f5',
                     'yellow9': '#ffff00',
                     'green25': '#9acd32'}

# Mappings of normalized hexadecimal color values to color names.
#################################################################
html4_hex_to_names = _reversedict(html4_names_to_hex)

css2_hex_to_names = html4_hex_to_names

css21_hex_to_names = _reversedict(css21_names_to_hex)

css3_hex_to_names = _reversedict(css3_names_to_hex)

# Normalization routines.
#################################################################
def normalize_hex(hex_value):
    try:
        hex_digits = HEX_COLOR_RE.match(hex_value).groups()[0]
    except AttributeError:
        raise ValueError("'%s' is not a valid hexadecimal color value." % hex_value)
    if len(hex_digits) == 3:
        hex_digits = ''.join([2 * s for s in hex_digits])
    return '#%s' % hex_digits.lower()

def normalize_integer_triplet(rgb_triplet):
    return tuple([_normalize_integer_rgb(value) for value in rgb_triplet])

def _normalize_integer_rgb(value):
    if 0 <= value <= 255:
        return value
    if value < 0:
        return 0
    if value > 255:
        return 255

def normalize_percent_triplet(rgb_triplet):
    return tuple([_normalize_percent_rgb(value) for value in rgb_triplet])

def _normalize_percent_rgb(value):
    percent = value.split('%')[0]
    percent = float(percent) if '.' in percent else int(percent)
    
    if 0 <= percent <= 100:
        return '%s%%' % percent
    if percent < 0:
        return '0%'
    if percent > 100:
        return '100%'   

# Conversions from color names to various formats.
#################################################################
def name_to_hex(name, spec='css3'):
    if spec not in SUPPORTED_SPECIFICATIONS:
        raise TypeError("'%s' is not a supported specification for color name lookups; supported specifications are: %s." % (spec,
                                                                                                                             ', '.join(SUPPORTED_SPECIFICATIONS)))
    normalized = name.lower()
    try:
        hex_value = globals()['%s_names_to_hex' % spec][normalized]
    except KeyError:
        raise ValueError("'%s' is not defined as a named color in %s." % (name, spec))
    return hex_value

def name_to_rgb(name, spec='css3'):
    return hex_to_rgb(name_to_hex(name, spec=spec))

def name_to_rgb_percent(name, spec='css3'):
    return rgb_to_rgb_percent(name_to_rgb(name, spec=spec))

# Conversions from hexadecimal color values to various formats.
#################################################################
def hex_to_name(hex_value, spec='css3'):
    if spec not in SUPPORTED_SPECIFICATIONS:
        raise TypeError("'%s' is not a supported specification for color name lookups; supported specifications are: %s." % (spec,
                                                                                                                             ', '.join(SUPPORTED_SPECIFICATIONS)))
    normalized = normalize_hex(hex_value)
    try:
        name = globals()['%s_hex_to_names' % spec][normalized]
    except KeyError:
        raise ValueError("'%s' has no defined color name in %s." % (hex_value, spec))
    return name

def hex_to_rgb(hex_value):
    hex_digits = normalize_hex(hex_value)
    return tuple([int(s, 16) for s in (hex_digits[1:3], hex_digits[3:5], hex_digits[5:7])])

def hex_to_rgb_percent(hex_value):
    return rgb_to_rgb_percent(hex_to_rgb(hex_value))

# Conversions from  integer rgb() triplets to various formats.
#################################################################
def rgb_to_name(rgb_triplet, spec='css3'):
    return hex_to_name(rgb_to_hex(normalize_integer_triplet(rgb_triplet)), spec=spec)

def rgb_to_hex(rgb_triplet):
    return '#%02x%02x%02x' % normalize_integer_triplet(rgb_triplet)

def rgb_to_rgb_percent(rgb_triplet):
    # In order to maintain precision for common values,
    # 256 / 2**n is special-cased for values of n
    # from 0 through 4, as well as 0 itself.
    specials = {255: '100%', 128: '50%', 64: '25%',
                 32: '12.5%', 16: '6.25%', 0: '0%'}
    return tuple([specials.get(d, '%.02f%%' % ((d / 255.0) * 100)) \
                  for d in normalize_integer_triplet(rgb_triplet)])

# Conversions from percentage rgb() triplets to various formats.
#################################################################
def rgb_percent_to_name(rgb_percent_triplet, spec='css3'):
    return rgb_to_name(rgb_percent_to_rgb(normalize_percent_triplet(rgb_percent_triplet)), spec=spec)

def rgb_percent_to_hex(rgb_percent_triplet):
    return rgb_to_hex(rgb_percent_to_rgb(normalize_percent_triplet(rgb_percent_triplet)))

def _percent_to_integer(percent):
    num = float(percent.split('%')[0]) / 100.0 * 255
    e = num - math.floor(num)
    return e < 0.5 and int(math.floor(num)) or int(math.ceil(num))

def rgb_percent_to_rgb(rgb_percent_triplet):
    return tuple(map(_percent_to_integer, normalize_percent_triplet(rgb_percent_triplet)))

'''if __name__ == '__main__':
    import doctest
    doctest.testmod()
'''