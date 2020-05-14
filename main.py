
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
parser.add_argument('--gen-blank-data', metavar='food_name', type=str,
    help="generate a blank data table for an ingredient")
args = parser.parse_args()

if args.gen_blank_data is not None:
    d = Data()
    d.name = args.gen_blank_data
    print(json.dumps(d.encode(), indent=4))
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

print(recipe)
