from menu import Menu, MenuItem
from coffee_maker import CoffeeMaker
from money_machine import MoneyMachine


menu = Menu()
coffee_maker = CoffeeMaker()
money_machine = MoneyMachine()

while True:
    items = menu.get_items()
    selection = input('What would you like? ' + items)
    if selection == 'off':
        print('Turning machine off...')
        break
    if selection == 'report':
        coffee_maker.report()
        money_machine.report()
        continue
    drink = menu.find_drink(selection)
    if drink:
        if coffee_maker.is_resource_sufficient(drink):
            if money_machine.make_payment(drink.cost):
                coffee_maker.make_coffee(drink)



