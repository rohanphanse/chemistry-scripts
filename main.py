import csv

def get_periodic_table():
    # Thanks to @GoodmanSciences for periodic table CSV file: https://gist.github.com/GoodmanSciences/c2dd862cd38f21b0ad36b8f96b4bf1ee
    with open("periodic_table.csv") as csv_file:
        csv_reader = csv.reader(csv_file)
        periodic_table = []
        for row in csv_reader:
            periodic_table.append(row)
    return periodic_table

def create_mass_dict(periodic_table):
    symbol_index = periodic_table[0].index("Symbol")
    mass_index = periodic_table[0].index("AtomicMass")
    mass_dict = {}
    for index in range(1, len(periodic_table)):
        mass_dict[periodic_table[index][symbol_index]] = float(periodic_table[index][mass_index])
    return mass_dict

def percent_composition(molecule, mass_dict):
    masses = {}
    total_mass = 0
    for (element, quantity) in molecule:
        mass = mass_dict[element] * quantity
        total_mass += mass
        if masses.get(element):
            masses[element] += mass
        else:
            masses[element] = mass
    composition = {element: mass / total_mass * 100 for element, mass in masses.items()}
    return composition

def parse_molecule(molecule_string):
    index = 0
    molecule = []
    while index < len(molecule_string):
        symbol = ""
        if molecule_string[index].isupper():
            if index + 1 < len(molecule_string) and molecule_string[index + 1].islower():
                symbol = molecule_string[index:index + 2]
            else:
                symbol = molecule_string[index]
        quantity_index = index + len(symbol)
        while quantity_index < len(molecule_string):
            if molecule_string[quantity_index].isnumeric():
                quantity_index += 1
            else:
                break
        quantity = 1
        if quantity_index > index + len(symbol):
            quantity = int(molecule_string[index + len(symbol):quantity_index])
        molecule.append((symbol, quantity))
        index = quantity_index
    return molecule


if __name__ == "__main__":
    periodic_table = get_periodic_table()
    mass_dict = create_mass_dict(periodic_table)
    # sodium_dichromate = [("Na", 2), ("Cr", 2), ("O", 7)]
    print("Percent Composition Calculator")
    print("Enter molecules (e.g. Na2Cr2O7):")
    while True:
        try:
            user_input = input(">>> ")
            if user_input == "quit":
                break
            molecule = parse_molecule(user_input)
            for element, percentage in percent_composition(molecule, mass_dict).items():
                print(f"{element}: {round(percentage, 3)}%")
        except:
            print("Error")