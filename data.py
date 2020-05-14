
import json

REPR_INDENT = 2


class Energy:
    baseUnit = 'kcal'
    conversions = {'kcal': 1, 'kj': 4.184}

    def __init__(self, amount, unit):
        self.measure = amount*Energy.conversions[unit]

    def zero():
        return Energy(0, Energy.baseUnit)

    def asUnit(self, unit):
        return self.measure/Energy.conversions[unit]

    def addEnergy(self, other):
        return Energy(self.measure + other.measure, Energy.baseUnit)

    def divEnergy(self, other):
        return self.measure/other.measure

    def multNumber(self, num):
        return Energy(num*self.measure, Energy.baseUnit)

    def decode(obj):
        return Energy(obj['amount'], obj['unit'])

    def encode(self):
        return {'amount': self.measure/Energy.conversions['kcal'],
                'unit': 'kcal'}

    def __repr__(self):
        return json.dumps(self.encode(), indent=REPR_INDENT)


class Mass:
    baseUnit = 'g'
    conversions = {'kg': 1000, 'g': 1, 'mg': 1e-3, 'mcg': 1e-6}

    def __init__(self, amount, unit):
        self.measure = amount*Mass.conversions[unit]

    def zero():
        return Mass(0, Mass.baseUnit)

    def asUnit(self, unit):
        return self.measure/Mass.conversions[unit]

    def addMass(self, other):
        return Mass(self.measure + other.measure, Mass.baseUnit)

    def divMass(self, other):
        return self.measure/other.measure

    def multNumber(self, num):
        return Mass(num*self.measure, Mass.baseUnit)

    def decode(obj):
        return Mass(obj['amount'], obj['unit'])

    def encode(self):
        if self.measure >= Mass.conversions['kg']:
            unit = 'kg'
        elif self.measure >= Mass.conversions['g'] or self.measure == 0:
            unit = 'g'
        elif self.measure >= Mass.conversions['mg']:
            unit = 'mg'
        else:
            unit = 'mcg'

        return {'amount': self.measure/Mass.conversions[unit],
                'unit': unit}

    def __repr__(self):
        return json.dumps(self.encode(), indent=REPR_INDENT)


class Nutrient:
    types = ['fat', 'carbohydrate', 'protein',
             'essential amino acid',
             'nonessential amino acid',
             'mineral', 'vitamin']

    def __init__(self, name, typ):
        if typ not in Nutrient.types:
            raise RuntimeError(f"uknown nutrient type {typ}")

        self.name = name
        self.typ = typ

    def decode(obj):
        return Nutrient(obj['name'], obj['type'])

    def encode(self):
        return {'name': self.name, 'type': self.typ}

    def __repr__(self):
        return json.dumps(self.encode(), indent=REPR_INDENT)
        


class Data:
    fats = [
        'total',
        'cholesterol',
        'saturated', 'trans',
        'monounsaturated', 'polyunsaturated'
    ]

    carbs = [
        'total',
        'dietary fiber',
        'total sugars',
        'added sugars',
        'sugar alcohol'
    ]

    proteins = ['total']

    essAminoAcids = [
        'histidine',
        'isoleucine',
        'leucine',
        'lysine',
        'methionine',
        'phenylalanine',
        'threonine',
        'tryptophan',
        'valine'
    ]

    nonessAminoAcids = [
        'alanine',
        'arginine',
        'asparagine',
        'aspartic acid',
        'cysteine',
        'glutamic acid',
        'glutamine',
        'glycine',
        'proline',
        'serine',
        'tyrosine'
    ]

    minerals = [
        'calcium',
        'chloride',
        'chromium',
        'copper',
        'iodine',
        'iron',
        'magnesium',
        'manganese',
        'molybdenum',
        'phosphorus',
        'potassium',
        'selenium',
        'sodium',
        'zinc'
    ]

    vitamins = [
        'biotin',
        'choline',
        'folic acid',
        'niacin',
        'pantothenic acid',
        'riboflavin',
        'thiamin',
        'vitamin a',
        'vitamin b-6',
        'vitamin b-12',
        'vitamin c',
        'vitamin d',
        'vitamin e',
        'vitamin k'
    ]

    def __init__(self):
        self.name = "unknown"
        self.desc = ""
        self.calories = Energy(0, 'kcal')
        self.servingSize = Mass(0, 'g')

        self.fats = {}
        for fat in Data.fats:
            self.fats[fat] = Mass(0, 'g')

        self.carbs = {}
        for carb in Data.carbs:
            self.carbs[carb] = Mass(0, 'g')

        self.proteins = {}
        for protein in Data.proteins:
            self.proteins[protein] = Mass(0, 'g')

        self.essAminoAcids = {}
        for essAminoAcid in Data.essAminoAcids:
            self.essAminoAcids[essAminoAcid] = Mass(0, 'g')

        self.nonessAminoAcids = {}
        for nonessAminoAcid in Data.nonessAminoAcids:
            self.nonessAminoAcids[nonessAminoAcid] = Mass(0, 'g')

        self.minerals = {}
        for mineral in Data.minerals:
            self.minerals[mineral] = Mass(0, 'g')

        self.vitamins = {}
        for vitamin in Data.vitamins:
            self.vitamins[vitamin] = Mass(0, 'g')


    def asAmount(self, amount):
        data = Data()
        factor = amount.divMass(self.servingSize)

        data.name = self.name
        data.desc = self.desc
        data.calories = self.calories.multNumber(factor)
        data.servingSize = self.servingSize.multNumber(factor)

        data.fats = Data.__multSeries(self.fats, factor)
        data.carbs = Data.__multSeries(self.carbs, factor)
        data.proteins = Data.__multSeries(self.proteins, factor)
        data.essAminoAcids = Data.__multSeries(self.essAminoAcids, factor)
        data.nonessAminoAcids = Data.__multSeries(self.nonessAminoAcids, factor)
        data.minerals = Data.__multSeries(self.minerals, factor)
        data.vitamins = Data.__multSeries(self.vitamins, factor)

        return data

    def __multSeries(series, factor):
        ret = {}
        for name, mass in series.items():
            ret[name] = mass.multNumber(factor)
        return ret


    def combine(self, other):
        data = Data()

        data.name = self.name + ", " + other.name
        data.desc = self.desc + "\n" + other.desc
        data.calories = self.calories.addEnergy(other.calories)
        data.servingSize = self.servingSize.addMass(other.servingSize)

        data.fats = Data.__addSeries(self.fats, other.fats)
        data.carbs = Data.__addSeries(self.carbs, other.carbs)
        data.proteins = Data.__addSeries(self.proteins, other.proteins)
        data.essAminoAcids = Data.__addSeries(self.essAminoAcids, other.essAminoAcids)
        data.nonessAminoAcids = Data.__addSeries(self.nonessAminoAcids, other.nonessAminoAcids)
        data.minerals = Data.__addSeries(self.minerals, other.minerals)
        data.vitamins = Data.__addSeries(self.vitamins, other.vitamins)

        return data

    def __addSeries(series1, series2):
        ret = {}
        for name, mass in series1.items():
            ret[name] = mass.addMass(series2[name])
        return ret


    def decode(obj):
        data = Data()

        data.name = obj['name']
        data.desc = obj['description']
        data.calories = Energy.decode(obj['calories'])
        data.servingSize = Mass.decode(obj['serving size'])

        data.fats = Data.__decodeSeries(obj['fats'])
        data.carbs = Data.__decodeSeries(obj['carbohydrates'])
        data.proteins = Data.__decodeSeries(obj['proteins'])
        data.essAminoAcids = Data.__decodeSeries(obj['essential amino acids'])
        data.nonessAminoAcids = Data.__decodeSeries(obj['nonessential amino acids'])
        data.minerals = Data.__decodeSeries(obj['minerals'])
        data.vitamins = Data.__decodeSeries(obj['vitamins'])

        return data

    def __decodeSeries(series):
        ret = {}
        for name, mass in series.items():
            ret[name] = Mass.decode(mass)
        return ret


    def encode(self):
        nutEnc = []

        return {'name': self.name,
                'description': self.desc,
                'calories': self.calories.encode(),
                'serving size': self.servingSize.encode(),

                'fats': Data.__encodeSeries(self.fats),
                'carbohydrates': Data.__encodeSeries(self.carbs),
                'proteins': Data.__encodeSeries(self.proteins),
                'essential amino acids': Data.__encodeSeries(self.essAminoAcids),
                'nonessential amino acids': Data.__encodeSeries(self.nonessAminoAcids),
                'minerals': Data.__encodeSeries(self.minerals),
                'vitamins': Data.__encodeSeries(self.vitamins)}

    def __encodeSeries(series):
        ret = {}
        for name, mass in series.items():
            ret[name] = mass.encode()
        return ret


    def __repr__(self):
        return json.dumps(self.encode(), indent=REPR_INDENT)
