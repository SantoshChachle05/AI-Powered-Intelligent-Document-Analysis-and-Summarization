# import re
# from word2number import w2n
# units = [
#     "minute", "min", "second", "sec", "hour", "day", "week", "month", "year", 
#     "gram", "kg", "kilogram", "milligram", "ton", "pound", "ounce", "mile", 
#     "meter", "meter", "cm", "inch", "foot", "yard", "mile", "liter", "gallon", 
#     "cubic", "fahrenheit", "celsius", "kelvin", "degree", "degree", "atm", "bar",
#     "hertz", "volt", "ampere", "watt", "joule", "newton"
# ]

# def extract_number_from_string(input_string):
#     input_string = re.sub(r'\b(?:' + '|'.join([r'\b' + word + r'\b' for word in ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]]) + r')\b', lambda match: str(w2n.word_to_num(match.group())), input_string)
#     match = re.match(r'([+-]?\d*\.\d+|\d+)', input_string)
#     if match:
#         return (match.group(0))
#     else:
#         return None

    
# def test_function():
#     test_cases = [
#         "5 minutes",          
#         "5 min",              
#         "five minutes",        
#         "27.39 degree",       
#         "45 seconds",          
#         "100 kg",              
#         "ten grams",           
#         "100.5 hour",          
#         "3.14 minute",         
#     ]
    
#     for case in test_cases:
#         print(f'Input: "{case}" => Extracted Number: {extract_number_from_string(case)}')

# test_function()

import re

def remove_units(value):
    # List of common units (can be extended)
    units = [
        "gm", "g", "gram", "grams", "kg", "kgs", "kilogram", "kilograms",
        "ml", "milliliter", "milliliters", "l", "litre", "litres", "m", "meter", "meters",
        "cm", "centimeter", "centimeters", "mm", "millimeter", "millimeters",
        "in", "inch", "inches", "ft", "feet", "oz", "ounce", "ounces", "lb", "pound", "pounds"
    ]
    
    # Create a regex pattern for units with optional plural 's'
    pattern = r'\b(?:' + '|'.join(re.escape(unit) for unit in units) + r')\b'
    
    # Remove units from the string
    cleaned = re.sub(pattern, '', value, flags=re.IGNORECASE)
    
    # Remove extra whitespace
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    
    return cleaned


output = remove_units("five kg")
print(output)