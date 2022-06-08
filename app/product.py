# not using
class Product:
    def __init__(self,name,price) -> None:
        self.__name = name
        self.__price = price

    def set_name(self,name):
        self.__name = name
    def set_price(self,price):
        self.__price = price
    def get_name(self):
        return self.__name
    def get_price(self):
        return self.__price
 
    def __str__(self):
        return f"{self.get_name()} has been added to the database with a price of {self.get_price()}"


# db = shelve.open('test.db')
# info = {'McSpicy': {'price': 8, 'quantity': 31}}
# db['test1'] = info
# sub = db['test1']
# print(sub)
# db.close()
# a = Price('lol', 32,123,'hi')
# print(a)