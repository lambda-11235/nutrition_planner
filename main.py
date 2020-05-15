
import argparse
import glob
import json

from data import *

parser = argparse.ArgumentParser(
    description='calculate nutrients for recipes')
parser.add_argument('data_dir', type=str,
    help="")
parser.add_argument('recipe', type=str,
    help="")
parser.add_argument('--exclude-zero', action='store_true',
    help="don't report nutrients that aren't present")
parser.add_argument('--exclude-micro', action='store_true',
    help="don't report micro-nutrients")
parser.add_argument('--json', action='store_true',
    help="output data in json format instead of as human readable")
parser.add_argument('--json-indent', type=int, default=2,
    help="indent on JSON blocks (default %(default)s)")
args = parser.parse_args()


CAL_GRAM_FAT = 9
CAL_GRAM_CARB = 4
CAL_GRAM_PROTEIN = 4


ingredients = {}
for f in glob.iglob(args.data_dir + "/*.json"):
    with open(f, 'r') as inp:
        ing = Data.decode(json.load(inp))
        ingredients[ing.name] = ing

if 'daily_value' in ingredients:
    dailyValue = ingredients['daily_value']
else:
    dailyValue = None


recipe = Data()
with open(args.recipe, 'r') as inp:
    for name, amount in json.load(inp).items():
        if name not in ingredients:
            print(f"Error: Ingredient '{name}' could not be found in path '{args.data_dir}'")
            exit(1)

        amount = Mass.decode(amount)
        ing = ingredients[name].asAmount(amount)
        recipe = recipe.combine(ing)


def printNut(label, category, nut, unit, optional=False):
    meas = recipe.nuts[category][nut]
    amount = meas.asUnit(unit)
    output = f"{label} - {amount:.3f} {unit}"

    if dailyValue is not None:
        dv = dailyValue.nuts[category][nut]

        if not dv.isZero():
            pdv = meas.div(dv)*100
            output += f" - {pdv:.1f}% DV"

    if not optional or amount > 0:
        print(output)

if args.json:
    print(json.dumps(recipe.encode(), indent=args.json_indent))
else:
    cals = recipe.calories.asUnit('kcal')
    percFats = 100*CAL_GRAM_FAT*recipe.nuts['fats']['total'].asUnit('g')/cals
    percCarbs = 100*CAL_GRAM_CARB*recipe.nuts['carbs']['total'].asUnit('g')/cals
    percProtein = 100*CAL_GRAM_PROTEIN*recipe.nuts['proteins']['total'].asUnit('g')/cals
    print(f"Calories - {cals} kcal - {percFats:.1f}% Fat, {percCarbs:.1f}% Carbs, {percProtein:.1f}% Protein")

    print(f"Serving Size - {recipe.servingSize.asUnit('g')} g")

    print()

    printNut("Total Fat", 'fats', 'total', 'g')
    printNut("\tSaturated Fat", 'fats', 'saturated', 'g')
    printNut("\tTrans Fat", 'fats', 'trans', 'g')
    printNut("\tMonounsaturated Fat", 'fats', 'monounsaturated', 'g', optional=args.exclude_zero)
    printNut("\tPolyunsaturated Fat", 'fats', 'polyunsaturated', 'g', optional=args.exclude_zero)

    printNut("Cholesterol", 'fats', 'cholesterol', 'mg')
    printNut("Sodium", 'minerals', 'sodium', 'mg')

    printNut("Total Carbohydrate", 'carbs', 'total', 'g')
    printNut("\tDietary Fiber", 'carbs', 'dietary fiber', 'g')
    printNut("\tTotal Sugars", 'carbs', 'total sugars', 'g')
    printNut("\t\tAdded Sugars", 'carbs', 'added sugars', 'g', optional=args.exclude_zero)
    printNut("\t\tSugar Alcohol", 'carbs', 'sugar alcohol', 'g', optional=args.exclude_zero)

    printNut("Protein", 'proteins', 'total', 'g')

    if args.exclude_micro:
        exit(0)

    print()

    print("Minerals")
    printNut("\tCalcium", 'minerals', 'calcium', 'mg', optional=args.exclude_zero)
    printNut("\tChloride", 'minerals', 'chloride', 'mg', optional=args.exclude_zero)
    printNut("\tChromium", 'minerals', 'chromium', 'mcg', optional=args.exclude_zero)
    printNut("\tCopper", 'minerals', 'copper', 'mg', optional=args.exclude_zero)
    printNut("\tIodine", 'minerals', 'iodine', 'mcg', optional=args.exclude_zero)
    printNut("\tIron", 'minerals', 'iron', 'mg', optional=args.exclude_zero)
    printNut("\tMagnesium", 'minerals', 'magnesium', 'mg', optional=args.exclude_zero)
    printNut("\tManganese", 'minerals', 'manganese', 'mg', optional=args.exclude_zero)
    printNut("\tMolybdenum", 'minerals', 'molybdenum', 'mcg', optional=args.exclude_zero)
    printNut("\tPhosphorus", 'minerals', 'phosphorus', 'mg', optional=args.exclude_zero)
    printNut("\tPotassium", 'minerals', 'potassium', 'mg', optional=args.exclude_zero)
    printNut("\tSelenium", 'minerals', 'selenium', 'mcg', optional=args.exclude_zero)
    #printNut("\tSodium", 'minerals', 'sodium', 'mg', optional=args.exclude_zero)
    printNut("\tZinc", 'minerals', 'zinc', 'mg', optional=args.exclude_zero)

    print("Vitamins")
    printNut("\tBiotin", 'vitamins', 'biotin', 'mcg', optional=args.exclude_zero)
    printNut("\tCholine", 'vitamins', 'choline', 'mg', optional=args.exclude_zero)
    printNut("\tFolic Acid", 'vitamins', 'folic acid', 'mcg', optional=args.exclude_zero)
    printNut("\tNiacin", 'vitamins', 'niacin', 'mg', optional=args.exclude_zero)
    printNut("\tPantothenic Acid", 'vitamins', 'pantothenic acid', 'mg', optional=args.exclude_zero)
    printNut("\tRiboflavin", 'vitamins', 'riboflavin', 'mg', optional=args.exclude_zero)
    printNut("\tThiamin", 'vitamins', 'thiamin', 'mg', optional=args.exclude_zero)
    printNut("\tVitamin A", 'vitamins', 'vitamin a', 'mcg', optional=args.exclude_zero)
    printNut("\tVitamin B-6", 'vitamins', 'vitamin b-6', 'mg', optional=args.exclude_zero)
    printNut("\tVitamin B-12", 'vitamins', 'vitamin b-12', 'mcg', optional=args.exclude_zero)
    printNut("\tVitamin C", 'vitamins', 'vitamin c', 'mg', optional=args.exclude_zero)
    printNut("\tVitamin D", 'vitamins', 'vitamin d', 'mcg', optional=args.exclude_zero)
    printNut("\tVitamin E", 'vitamins', 'vitamin e', 'mg', optional=args.exclude_zero)
    printNut("\tVitamin K", 'vitamins', 'vitamin k', 'mcg', optional=args.exclude_zero)

    print("Essential Amino Acids")
    printNut("\tHistidine", 'essAminoAcids', 'histidine', 'mg', optional=args.exclude_zero)
    printNut("\tIsoleucine", 'essAminoAcids', 'isoleucine', 'mg', optional=args.exclude_zero)
    printNut("\tLeucine", 'essAminoAcids', 'leucine', 'mg', optional=args.exclude_zero)
    printNut("\tLysine", 'essAminoAcids', 'lysine', 'mg', optional=args.exclude_zero)
    printNut("\tMethionine", 'essAminoAcids', 'methionine', 'mg', optional=args.exclude_zero)
    printNut("\tPhenylalanine", 'essAminoAcids', 'phenylalanine', 'mg', optional=args.exclude_zero)
    printNut("\tThreonine", 'essAminoAcids', 'threonine', 'mg', optional=args.exclude_zero)
    printNut("\tTryptophan", 'essAminoAcids', 'tryptophan', 'mg', optional=args.exclude_zero)
    printNut("\tValine", 'essAminoAcids', 'valine', 'mg', optional=args.exclude_zero)

    print("Nonessential Amino Acids")
    printNut("\tAlanine", 'nonessAminoAcids', 'alanine', 'mg', optional=args.exclude_zero)
    printNut("\tArginine", 'nonessAminoAcids', 'arginine', 'mg', optional=args.exclude_zero)
    printNut("\tAsparagine", 'nonessAminoAcids', 'asparagine', 'mg', optional=args.exclude_zero)
    printNut("\tAspartic Acid", 'nonessAminoAcids', 'aspartic acid', 'mg', optional=args.exclude_zero)
    printNut("\tCysteine", 'nonessAminoAcids', 'cysteine', 'mg', optional=args.exclude_zero)
    printNut("\tGlutamic Acid", 'nonessAminoAcids', 'glutamic acid', 'mg', optional=args.exclude_zero)
    printNut("\tGlutamine", 'nonessAminoAcids', 'glutamine', 'mg', optional=args.exclude_zero)
    printNut("\tGlycine", 'nonessAminoAcids', 'glycine', 'mg', optional=args.exclude_zero)
    printNut("\tProline", 'nonessAminoAcids', 'proline', 'mg', optional=args.exclude_zero)
    printNut("\tSerine", 'nonessAminoAcids', 'serine', 'mg', optional=args.exclude_zero)
    printNut("\tTyrosine", 'nonessAminoAcids', 'tyrosine', 'mg', optional=args.exclude_zero)
