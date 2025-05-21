from abc import ABC
import enum
import math

# Třída označující lokalitu, kde se nemovitost nachází
class Locality:
    def __init__(self, name: str, locality_coefficient: float) -> None:
        self.name = name
        self.locality_coefficient = locality_coefficient


# Abstraktní třída, která reprezentuje nemovitost
class Property(ABC):
    def __init__(self, locality: Locality) -> None:
        self.locality = locality


# Enum třída pro typy pozemků
class EstateType(enum.Enum):
    LAND = 0.85
    BUILDING_SITE = 9
    FORREST = 0.35
    GARDEN = 2


# Třída reprezentující pozemek, potomek třídy Property
class Estate(Property):
    def __init__(self, locality: Locality, estate_type: EstateType, area: float) -> None:
        super().__init__(locality)
        self.estate_type = estate_type
        self.area = area

    def __str__(self) -> str:
        return f"Estate type: {self.estate_type}\nLocality: {self.locality.name} (coefficient {self.locality.locality_coefficient})\nArea: {self.area} square meters\nTax: {self.calculate_tax()} CZK\n"

    # Metoda spočítá výši daně pro pozemek
    def calculate_tax(self) -> int:
        return math.ceil(self.area * self.estate_type.value * self.locality.locality_coefficient)


# Třída reprezentující byt, dům nebo jinou stavbu
class Residence(Property):
    def __init__(self, locality: Locality, area: float, commercial: bool) -> None:
        super().__init__(locality)
        self.area = area
        self.commercial = commercial

    def __str__(self) -> str:
        if self.commercial == True:
            commercial_str = "commercial"
        else:
            commercial_str = "private"

        return f"Locality: {self.locality.name} (coefficient {self.locality.locality_coefficient})\nType: {commercial_str}\nArea: {self.area} square meters\nTax: {self.calculate_tax()} CZK\n"

    # Metoda spočítá výši daně pro byt, dům nebo jinou stavbu; jestli jde o stavbu komerční, daň se násobí *2
    def calculate_tax(self) -> int:
        if self.commercial == True:
            return math.ceil((self.area * self.locality.locality_coefficient * 15) * 2)
        else:
            return math.ceil(self.area * self.locality.locality_coefficient * 15)

# Třída reprezentující daňové přiznání
class TaxReport:
    def __init__(self, name: str) -> None:
        self.name = name
        self.property_list = []

    def __str__(self) -> str:
        return f"Name: {self.name}\nNumber of properties: {len(self.property_list)}\nTotal tax: {self.calculate_tax()} CZK\n"

    # Přidání nemovitosti do listu nemovitostí
    def add_property(self, property: Property) -> None:
        self.property_list.append(property)

    # Kalkulace dani ze všech nemovitostí v listu property_list
    def calculate_tax(self) -> int:
        total_tax = 0
        for property in self.property_list:
            total_tax += property.calculate_tax()
        return total_tax


estate = Estate(Locality("Manětín", 0.8), EstateType.LAND, 900)
print(estate)
dum = Residence(Locality("Manětín", 0.8), 120, False)
print(dum)
office = Residence(Locality("Brno", 3), 90, True)
print(office)


tax_report = TaxReport("Jan Černý")
tax_report.add_property(Estate(Locality("Ořešín", 1.5), EstateType.LAND, 500))
tax_report.add_property(Residence(Locality("Praha", 5), 80, commercial=True))
print(tax_report)
