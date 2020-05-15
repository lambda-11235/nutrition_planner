

import argparse
import json
import pandas as pd

from data import *

parser = argparse.ArgumentParser(
    description='calculate nutrients for recipes')
parser.add_argument('data_dir', type=str,
    help="")
parser.add_argument('fdc_id', type=int,
    help="")
parser.add_argument('name', type=str,
    help="")
parser.add_argument('--json-indent', type=int, default=2,
    help="indent on JSON blocks (default %(default)s)")
args = parser.parse_args()

foodData = pd.read_csv(args.data_dir + "/food.csv", index_col="fdc_id")
foodData = foodData.loc[args.fdc_id]

foodNutData = pd.read_csv(args.data_dir + "/food_nutrient.csv")
foodNutData = foodNutData.loc[foodNutData.fdc_id == args.fdc_id]

nutData = pd.read_csv(args.data_dir + "/nutrient.csv", index_col="id")


def hasNutrient(nutID):
    nuts = list(foodNutData['nutrient_id'])
    return nutID in nutData.index and nutID in nuts

def getNutrientAmount(nutID):
    amount = foodNutData.loc[foodNutData['nutrient_id'] == nutID].iloc[0]['amount']

    fcUnit = nutData.loc[nutID]['unit_name']
    if fcUnit == 'KCAL':
        return Energy(amount, 'kcal')
    if fcUnit == 'kJ':
        return Energy(amount, 'kj')
    if fcUnit == 'G':
        return Mass(amount, 'g')
    elif fcUnit == 'MG':
        return Mass(amount, 'mg')
    elif fcUnit == 'UG':
        return Mass(amount, 'mcg')
    else:
        raise RuntimeError(f"unit {fcUnit} unrecognized for nutrient id {nutID}")


d = Data()
d.name = args.name
d.desc = foodData['description']

if hasNutrient(1008):
    d.calories = getNutrientAmount(1008)
elif hasNutrient(1062):
    d.calories = getNutrientAmount(1062)

# All nutrients are given per 100g in FoodCentral's database, so use
# that.
d.servingSize = Mass(100, 'g')


def assignNutrients(category, idMap):
    for name, ids in idMap.items():
        for i in ids:
            if hasNutrient(i):
                d.nuts[category][name] = getNutrientAmount(i)
                break

assignNutrients('fats',
                {'total': [1004, 1085],
                 'cholesterol': [1253],
                 'saturated': [1258],
                 'trans': [1257],
                 'monounsaturated': [1292],
                 'polyunsaturated': [1293]})

assignNutrients('carbs',
                {'total': [1005, 1050],
                 'dietary fiber': [1079, 2033],
                 'total sugars': [1063, 2000],
                 'added sugars': [1235],
                 'sugar alcohol': [1086]})

assignNutrients('proteins', {'total': [1003]})

assignNutrients('essAminoAcids',
                {'histidine': [1221],
                 'isoleucine': [1212],
                 'leucine': [1213],
                 'lysine': [1214],
                 'methionine': [1215],
                 'phenylalanine': [1217],
                 'threonine': [1211],
                 'tryptophan': [1210],
                 'valine': [1219]})

assignNutrients('nonessAminoAcids',
                {'alanine': [1222],
                 'arginine': [1220],
                 'asparagine': [], # Not in database
                 'aspartic acid': [1223],
                 'cysteine': [1232],
                 'glutamic acid': [1224],
                 'glutamine': [1233],
                 'glycine': [1225],
                 'proline': [1226],
                 'serine': [1227],
                 'tyrosine': [1218]})

assignNutrients('minerals',
                {'calcium': [1087],
                 'chloride': [1088],
                 'chromium': [1096],
                 'copper': [1098],
                 'iodine': [1100],
                 'iron': [1089],
                 'magnesium': [1090],
                 'manganese': [1101],
                 'molybdenum': [1102],
                 'phosphorus': [1091],
                 'potassium': [1092],
                 'selenium': [1103],
                 'sodium': [1093],
                 'zinc': [1095]})

assignNutrients('vitamins',
                {'biotin': [1176],
                 'choline': [1180],
                 'folic acid': [1186],
                 'niacin': [1167],
                 'pantothenic acid': [1170],
                 'riboflavin': [1166],
                 'thiamin': [1165],
                 'vitamin a': [1106],
                 'vitamin b-6': [1175],
                 'vitamin b-12': [1178],
                 'vitamin c': [1162],
                 'vitamin d': [1114],
                 'vitamin e': [1109]})

# Vitamin K has 3 entries (3 types), so add them together
d.nuts['vitamins']['vitamin k'] = Mass.zero()
for nutID in [1183, 1184, 1185]:
    if hasNutrient(nutID):
        amount = getNutrientAmount(nutID)
        d.nuts['vitamins']['vitamin k'] = d.nuts['vitamins']['vitamin k'].add(amount)

print(json.dumps(d.encode(), indent=args.json_indent))
