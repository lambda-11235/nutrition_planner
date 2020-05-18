
# Nutrition Planner

This is a nutrition planner that lets one design recipes and calculate
their nutritional values.
It tracks calories, macros (carbs, fats, and proteins), the most
common vitamins and minerals, and the protein amino acid makeup.
To use the planner you must first create a data directory with
ingredient data, and a recipe file.
See `example/` for an example layout.
Basic usage is
```
> ./main.py example/data/ example/recipe.json --exclude-micro
Calories - 236.0 kcal - 2.5% Fat, 91.8% Carbs, 10.1% Protein
Serving Size - 400.0 g

Total Fat - 0.660 g - 1.0% DV
	Saturated Fat - 0.124 g - 0.6% DV
	Trans Fat - 0.000 g
	Monounsaturated Fat - 0.032 g
	Polyunsaturated Fat - 0.318 g
Cholesterol - 0.000 mg - 0.0% DV
Sodium - 150.000 mg - 6.3% DV
Total Carbohydrate - 54.140 g - 18.0% DV
	Dietary Fiber - 9.800 g - 39.2% DV
	Total Sugars - 11.120 g
		Added Sugars - 0.000 g
		Sugar Alcohol - 0.000 g
Protein - 5.960 g - 11.9% DV
```

To add new ingredients either copy and modify an existing file, or use
`gen_blank_data.py`.

## Daily Value

In order to correctly report nutritional data as a %DV, it is required
that the ingredient data directory contain an ingredient named
`daily_value`.
`examples/data/daily_value.json` contains DV data gathered from the
FDA's website.

## Importing FoodCentral Nutrition Data

Go to [FoodCentral](https://fdc.nal.usda.gov/) and retrieve their
current "Full Download of All Data Types" in CSV format.
As of this writing, to get the current data files do
```
> wget https://fdc.nal.usda.gov/fdc-datasets/FoodData_Central_csv_2020-04-29.zip
--2020-05-17 21:53:21--  https://fdc.nal.usda.gov/fdc-datasets/FoodData_Central_csv_2020-04-29.zip
Resolving fdc.nal.usda.gov (fdc.nal.usda.gov)... 52.227.222.192
Connecting to fdc.nal.usda.gov (fdc.nal.usda.gov)|52.227.222.192|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 88474019 (84M) [application/zip]
Saving to: ‘FoodData_Central_csv_2020-04-29.zip’

FoodData_Central_csv_2020-04-29.zip             100%[======================================================================================================>]  84.38M   227KB/s    in 8m 23s

2020-05-17 22:01:47 (172 KB/s) - ‘FoodData_Central_csv_2020-04-29.zip’ saved [88474019/88474019]

> mkdir FoodDataCentral
> cd FoodDataCentral/
> unzip ../FoodData_Central_csv_2020-04-29.zip
Archive:  ../FoodData_Central_csv_2020-04-29.zip
  inflating: wweia_food_category.csv
  inflating: food_category.csv
  inflating: retention_factor.csv
  inflating: food_attribute_type.csv
  inflating: nutrient.csv
  inflating: nutrient_incoming_name.csv
  inflating: measure_unit.csv
  inflating: food_nutrient_source.csv
  inflating: food_nutrient_derivation.csv
  inflating: lab_method.csv
  inflating: lab_method_code.csv
  inflating: lab_method_nutrient.csv
  inflating: fndds_derivation.csv
  inflating: fndds_ingredient_nutrient_value.csv
  inflating: food.csv
  inflating: food_nutrient.csv
  inflating: food_portion.csv
  inflating: food_component.csv
  inflating: agricultural_acquisition.csv
  inflating: survey_fndds_food.csv
  inflating: branded_food.csv
  inflating: food_update_log_entry.csv
  inflating: sr_legacy_food.csv
  inflating: foundation_food.csv
  inflating: sample_food.csv
  inflating: sub_sample_food.csv
  inflating: sub_sample_result.csv
  inflating: market_acquisition.csv
  inflating: acquisition_sample.csv
  inflating: input_food.csv
  inflating: food_attribute.csv
  inflating: food_calorie_conversion_factor.csv
  inflating: food_protein_conversion_factor.csv
  inflating: food_nutrient_conversion_factor.csv
  inflating: all_downloaded_table_record_counts.csv
  inflating: Download_Field_Descriptions_Apr2020.pdf
```

Now import data like so

```
> mkdir data
> ./fc_importer.py FoodDataCentral/ 170026 potato > data/potato.json
```

## Useful Sites

- For looking up food nutrient contents.
  https://fdc.nal.usda.gov/

- For what nutrients to look for.
  https://www.accessdata.fda.gov/scripts/interactivenutritionfactslabel/
