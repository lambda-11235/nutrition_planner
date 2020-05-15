
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
parser.add_argument('--json', action='store_true',
    help="output data in json format instead of as human readable")
parser.add_argument('--json-indent', type=int, default=2,
    help="indent on JSON blocks (default %(default)s)")
parser.add_argument('--gen-blank-data', metavar='food_name', type=str,
    help="generate a blank data table for an ingredient (implies --json)")
args = parser.parse_args()

if args.gen_blank_data is not None:
    d = Data()
    d.name = args.gen_blank_data
    print(json.dumps(d.encode(), indent=args.json_indent))
    exit(0)


ingredients = {}
for f in glob.iglob(args.data_dir + "/*.json"):
    with open(f, 'r') as inp:
        ing = Data.decode(json.load(inp))
        ingredients[ing.name] = ing


recipe = Data()
with open(args.recipe, 'r') as inp:
    for name, amount in json.load(inp).items():
        if name not in ingredients:
            print(f"Error: Ingredient '{name}' could not be found in path '{args.data_dir}'")
            exit(1)

        amount = Mass.decode(amount)
        ing = ingredients[name].asAmount(amount)
        recipe = recipe.combine(ing)


def printMeas(sformat, meas, unit, optional=False):
    amount = meas.asUnit(unit)
    if not optional or amount > 0:
        print(sformat.format(f"{amount:.3f} {unit}"))

if args.json:
    print(json.dumps(recipe.encode(), indent=args.json_indent))
else:
    printMeas("Calories: {}", recipe.calories, 'kcal')
    printMeas("Serving Size: {}", recipe.servingSize, 'g')

    print()

    printMeas("Total Fat: {}", recipe.fats['total'], 'g')
    printMeas("\tSaturated Fat: {}", recipe.fats['saturated'], 'g')
    printMeas("\tTrans Fat: {}", recipe.fats['trans'], 'g')
    printMeas("\tMonounsaturated Fat: {}", recipe.fats['monounsaturated'], 'g', optional=args.exclude_zero)
    printMeas("\tPolyunsaturated Fat: {}", recipe.fats['polyunsaturated'], 'g', optional=args.exclude_zero)

    printMeas("Cholesterol: {}", recipe.fats['cholesterol'], 'mg')
    printMeas("Sodium: {}", recipe.minerals['sodium'], 'mg')

    printMeas("Total Carbohydrate: {}", recipe.carbs['total'], 'g')
    printMeas("\tDietary Fiber: {}", recipe.carbs['dietary fiber'], 'g')
    printMeas("\tTotal Sugars: {}", recipe.carbs['total sugars'], 'g')
    printMeas("\t\tAdded Sugars: {}", recipe.carbs['added sugars'], 'g', optional=args.exclude_zero)
    printMeas("\t\tSugar Alcohol: {}", recipe.carbs['sugar alcohol'], 'g', optional=args.exclude_zero)

    printMeas("Protein: {}", recipe.proteins['total'], 'g')

    print()

    print("Minerals")
    printMeas("\tCalcium: {}", recipe.minerals['calcium'], 'mg', optional=args.exclude_zero)
    printMeas("\tChloride: {}", recipe.minerals['chloride'], 'mg', optional=args.exclude_zero)
    printMeas("\tChromium: {}", recipe.minerals['chromium'], 'mcg', optional=args.exclude_zero)
    printMeas("\tCopper: {}", recipe.minerals['copper'], 'mg', optional=args.exclude_zero)
    printMeas("\tIodine: {}", recipe.minerals['iodine'], 'mcg', optional=args.exclude_zero)
    printMeas("\tIron: {}", recipe.minerals['iron'], 'mg', optional=args.exclude_zero)
    printMeas("\tMagnesium: {}", recipe.minerals['magnesium'], 'mg', optional=args.exclude_zero)
    printMeas("\tManganese: {}", recipe.minerals['manganese'], 'mg', optional=args.exclude_zero)
    printMeas("\tMolybdenum: {}", recipe.minerals['molybdenum'], 'mcg', optional=args.exclude_zero)
    printMeas("\tPhosphorus: {}", recipe.minerals['phosphorus'], 'mg', optional=args.exclude_zero)
    printMeas("\tPotassium: {}", recipe.minerals['potassium'], 'mg', optional=args.exclude_zero)
    printMeas("\tSelenium: {}", recipe.minerals['selenium'], 'mcg', optional=args.exclude_zero)
    #printMeas("\tSodium: {}", recipe.minerals['sodium'], 'mg', optional=args.exclude_zero)
    printMeas("\tZinc: {}", recipe.minerals['zinc'], 'mg', optional=args.exclude_zero)

    print("Vitamins")
    printMeas("\tBiotin: {}", recipe.vitamins['biotin'], 'mcg', optional=args.exclude_zero)
    printMeas("\tCholine: {}", recipe.vitamins['choline'], 'mg', optional=args.exclude_zero)
    printMeas("\tFolic Acid: {}", recipe.vitamins['folic acid'], 'mcg', optional=args.exclude_zero)
    printMeas("\tNiacin: {}", recipe.vitamins['niacin'], 'mg', optional=args.exclude_zero)
    printMeas("\tPantothenic Acid: {}", recipe.vitamins['pantothenic acid'], 'mg', optional=args.exclude_zero)
    printMeas("\tRiboflavin: {}", recipe.vitamins['riboflavin'], 'mg', optional=args.exclude_zero)
    printMeas("\tThiamin: {}", recipe.vitamins['thiamin'], 'mg', optional=args.exclude_zero)
    printMeas("\tVitamin A: {}", recipe.vitamins['vitamin a'], 'mcg', optional=args.exclude_zero)
    printMeas("\tVitamin B-6: {}", recipe.vitamins['vitamin b-6'], 'mg', optional=args.exclude_zero)
    printMeas("\tVitamin B-12: {}", recipe.vitamins['vitamin b-12'], 'mcg', optional=args.exclude_zero)
    printMeas("\tVitamin C: {}", recipe.vitamins['vitamin c'], 'mg', optional=args.exclude_zero)
    printMeas("\tVitamin D: {}", recipe.vitamins['vitamin d'], 'mcg', optional=args.exclude_zero)
    printMeas("\tVitamin E: {}", recipe.vitamins['vitamin e'], 'mg', optional=args.exclude_zero)
    printMeas("\tVitamin K: {}", recipe.vitamins['vitamin k'], 'mcg', optional=args.exclude_zero)

    print("Essential Amino Acids")
    printMeas("\tHistidine: {}", recipe.essAminoAcids['histidine'], 'mg', optional=args.exclude_zero)
    printMeas("\tIsoleucine: {}", recipe.essAminoAcids['isoleucine'], 'mg', optional=args.exclude_zero)
    printMeas("\tLeucine: {}", recipe.essAminoAcids['leucine'], 'mg', optional=args.exclude_zero)
    printMeas("\tLysine: {}", recipe.essAminoAcids['lysine'], 'mg', optional=args.exclude_zero)
    printMeas("\tMethionine: {}", recipe.essAminoAcids['methionine'], 'mg', optional=args.exclude_zero)
    printMeas("\tPhenylalanine: {}", recipe.essAminoAcids['phenylalanine'], 'mg', optional=args.exclude_zero)
    printMeas("\tThreonine: {}", recipe.essAminoAcids['threonine'], 'mg', optional=args.exclude_zero)
    printMeas("\tTryptophan: {}", recipe.essAminoAcids['tryptophan'], 'mg', optional=args.exclude_zero)
    printMeas("\tValine: {}", recipe.essAminoAcids['valine'], 'mg', optional=args.exclude_zero)

    print("Nonessential Amino Acids")
    printMeas("\tAlanine: {}", recipe.nonessAminoAcids['alanine'], 'mg', optional=args.exclude_zero)
    printMeas("\tArginine: {}", recipe.nonessAminoAcids['arginine'], 'mg', optional=args.exclude_zero)
    printMeas("\tAsparagine: {}", recipe.nonessAminoAcids['asparagine'], 'mg', optional=args.exclude_zero)
    printMeas("\tAspartic Acid: {}", recipe.nonessAminoAcids['aspartic acid'], 'mg', optional=args.exclude_zero)
    printMeas("\tCysteine: {}", recipe.nonessAminoAcids['cysteine'], 'mg', optional=args.exclude_zero)
    printMeas("\tGlutamic Acid: {}", recipe.nonessAminoAcids['glutamic acid'], 'mg', optional=args.exclude_zero)
    printMeas("\tGlutamine: {}", recipe.nonessAminoAcids['glutamine'], 'mg', optional=args.exclude_zero)
    printMeas("\tGlycine: {}", recipe.nonessAminoAcids['glycine'], 'mg', optional=args.exclude_zero)
    printMeas("\tProline: {}", recipe.nonessAminoAcids['proline'], 'mg', optional=args.exclude_zero)
    printMeas("\tSerine: {}", recipe.nonessAminoAcids['serine'], 'mg', optional=args.exclude_zero)
    printMeas("\tTyrosine: {}", recipe.nonessAminoAcids['tyrosine'], 'mg', optional=args.exclude_zero)
