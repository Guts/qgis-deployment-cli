# Python program to demonstrate
# issubclass()
  
  
# Defining Parent class
class Vehicles:
  
    # Constructor
    def __init__(vehicleType):
        print('Vehicles is a ', vehicleType)
  
# Defining Child class
class Car(Vehicles):
  
    # Constructor
    def __init__(self):
        Vehicles.__init__('Car')
  
# Driver's code   
# print(issubclass(Car, Vehicles))
# print(issubclass(Car, list))
# print(issubclass(Car, Car))
# print(issubclass(Car, (list, Vehicles)))
print(issubclass(Vehicles, Vehicles))
print(isinstance(Vehicles, Vehicles))
