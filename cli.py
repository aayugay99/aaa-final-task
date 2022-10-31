import click
from random import randint
import time


class Pizza:
    def __init__(self, size: str = 'X'):
        assert size in ['X', 'XL']
        self.size = size
        self.max_bake_time = 10 if size == 'XL' else 5

    @staticmethod
    def dict():
        pass

    def __eq__(self, other):
        if self.dict() == other.dict() and self.size == other.size:
            return True
        return False


class Margherita(Pizza):
    @staticmethod
    def dict():
        return {'Margherita \U0001F9C0': ['tomato sauce', 'mozzarella', 'tomatoes']}


class Pepperoni(Pizza):
    def __init__(self, size: str = 'X'):
        super().__init__(size)
        self.max_bake_time = 6 if size == 'XL' else 3

    @staticmethod
    def dict():
        return {'Pepperoni \U0001F355': ['tomato sauce', 'mozzarella', 'pepperoni']}


class Hawaiian(Pizza):
    def __init__(self, size: str = 'X'):
        super().__init__(size)
        self.max_bake_time = 12 if size == 'XL' else 6

    @staticmethod
    def dict():
        return {'Hawaiian \U0001F34D': ['tomato sauce', 'mozzarella', 'chicken', 'pineapples']}


# def log(func):
#     def wrapper(x):
#         start = time.time()
#         value = func(x)
#         end = time.time()
#         print(f'{func.__name__} - {end-start}')
#         return value
#     return wrapper


def log(template):
    def my_decorator(func):
        def wrapper(x):
            start = time.time()
            value = func(x)
            end = time.time()
            print(template.format(round(end-start, 3)))
            return value
        return wrapper
    return my_decorator


@log('Приготовили за {}c')
def bake(pizza):
    """Готовит пиццу"""
    time.sleep(randint(1, pizza.max_bake_time))
    return pizza


@log('Доставили за {}c')
def deliver(pizza):
    """Доставляет пиццу"""
    time.sleep(randint(1, 4))
    return pizza


@log('Забрали за {}c')
def pickup(pizza):
    """Самовывоз"""
    time.sleep(randint(1, 5))
    return pizza


@click.group()
def cli():
    pass


@cli.command()
@click.option('--delivery', default=False, is_flag=True)
@click.option('--size', default='X')
@click.argument('pizza', nargs=1)
def order(pizza: str, delivery: bool, size: str):
    """Готовит и доставляет пиццу"""

    if pizza in ['Hawaiian', 'Pepperoni', 'Margherita']:
        if pizza == 'Hawaiian':
            baked_pizza = bake(Hawaiian(size))
        elif pizza == 'Pepperoni':
            baked_pizza = bake(Pepperoni(size))
        else:
            baked_pizza = bake(Margherita(size))

        if delivery:
            deliver(baked_pizza)
        else:
            pickup(baked_pizza)
    else:
        print(f'Вы заказали: {pizza}.\nТакой пиццы нет в меню.\nЗапустите команду \'python cli.py menu\' чтоб вывести меню.')


@cli.command()
def menu():
    """Выводит меню"""
    for pizza in [Margherita, Pepperoni, Hawaiian]:
        key, rec = list(pizza.dict().items())[0]
        print(f"- {key}: {', '.join(rec)}")


if __name__ == '__main__' :
    cli()
