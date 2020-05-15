
import json

REPR_INDENT = 2


class Measure:
    baseUnit = 'unitless'
    conversions = {'unitless': 1}
    encodeUnitLevels = ['unitless']
    encodeUnitZero = 'unitless'

    def __init__(self, amount, unit):
        self.measure = amount*self.__class__.conversions[unit]

    @classmethod
    def zero(cls):
        return cls(0, cls.baseUnit)

    def asUnit(self, unit):
        return self.measure/self.__class__.conversions[unit]

    def add(self, other):
        return self.__class__(self.measure + other.measure, self.__class__.baseUnit)

    def div(self, other):
        return self.measure/other.measure

    def multNumber(self, num):
        return self.__class__(num*self.measure, self.__class__.baseUnit)

    @classmethod
    def decode(cls, obj):
        return cls(obj['amount'], obj['unit'])

    def encode(self):
        amount = self.measure
        unit = self.__class__.encodeUnitZero

        if self.measure != 0:
            for u in self.__class__.encodeUnitLevels:
                amount = self.measure/self.__class__.conversions[u]
                unit = u
                if amount >= 1:
                    break

        return {'amount': amount, 'unit': unit}

    def __repr__(self):
        return json.dumps(self.encode(), indent=REPR_INDENT)


class Energy(Measure):
    baseUnit = 'kcal'
    conversions = {'kcal': 1, 'kj': 4.184}
    encodeUnitLevels = ['kcal']
    encodeUnitZero = 'kcal'


class Mass(Measure):
    baseUnit = 'g'
    conversions = {'kg': 1000, 'g': 1, 'mg': 1e-3, 'mcg': 1e-6}
    encodeUnitLevels = ['kg', 'g', 'mg', 'mcg']
    encodeUnitZero = 'g'


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

        self.nuts = {'fats': {},
                     'carbs': {},
                     'proteins': {},
                     'essAminoAcids': {},
                     'nonessAminoAcids': {},
                     'minerals': {},
                     'vitamins': {}}

        for fat in Data.fats:
            self.nuts['fats'][fat] = Mass(0, 'g')

        for carb in Data.carbs:
            self.nuts['carbs'][carb] = Mass(0, 'g')

        for protein in Data.proteins:
            self.nuts['proteins'][protein] = Mass(0, 'g')

        for essAminoAcid in Data.essAminoAcids:
            self.nuts['essAminoAcids'][essAminoAcid] = Mass(0, 'g')

        for nonessAminoAcid in Data.nonessAminoAcids:
            self.nuts['nonessAminoAcids'][nonessAminoAcid] = Mass(0, 'g')

        for mineral in Data.minerals:
            self.nuts['minerals'][mineral] = Mass(0, 'g')

        for vitamin in Data.vitamins:
            self.nuts['vitamins'][vitamin] = Mass(0, 'g')


    def asAmount(self, amount):
        data = Data()
        factor = amount.div(self.servingSize)

        data.name = self.name
        data.desc = self.desc
        data.calories = self.calories.multNumber(factor)
        data.servingSize = self.servingSize.multNumber(factor)

        for category, series in self.nuts.items():
            data.nuts[category] = Data.__multSeries(series, factor)

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
        data.calories = self.calories.add(other.calories)
        data.servingSize = self.servingSize.add(other.servingSize)

        for category, series in self.nuts.items():
            data.nuts[category] = Data.__addSeries(series, other.nuts[category])

        return data

    def __addSeries(series1, series2):
        ret = {}
        for name, mass in series1.items():
            ret[name] = mass.add(series2[name])
        return ret


    def decode(obj):
        data = Data()

        data.name = obj['name']
        data.desc = obj['description']
        data.calories = Energy.decode(obj['calories'])
        data.servingSize = Mass.decode(obj['serving size'])

        for category, _ in data.nuts.items():
            data.nuts[category] = Data.__decodeSeries(obj[category])

        return data

    def __decodeSeries(series):
        ret = {}
        for name, mass in series.items():
            ret[name] = Mass.decode(mass)
        return ret


    def encode(self):
        enc = {'name': self.name,
               'description': self.desc,
               'calories': self.calories.encode(),
               'serving size': self.servingSize.encode()}

        for category, series in self.nuts.items():
            enc[category] = Data.__encodeSeries(series)

        return enc

    def __encodeSeries(series):
        ret = {}
        for name, mass in series.items():
            ret[name] = mass.encode()
        return ret


    def __repr__(self):
        return json.dumps(self.encode(), indent=REPR_INDENT)
