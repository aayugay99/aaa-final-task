import click
from random import randint
import time


class Pizza:
    """Базовый класс для пиццы, который наследуется видами пиццы."""
    def __init__(self, size: str = 'X'):
        assert size in ['X', 'XL']
        self.size = size                                # размер пиццы
        self.max_bake_time = 10 if size == 'XL' else 5  # максимальное время готовки

    @staticmethod
    def dict():
        """Метод описывает рецепт пиццы. Определяется в наследниках."""
        pass

    def __eq__(self, other):
        """Метод для сравнения пицц. Пиццы сравниваются по размеру и рецепту"""
        if self.dict() == other.dict() and self.size == other.size:
            return True
        return False


class Margherita(Pizza):
    """Класс описывающий Маргариту."""
    @staticmethod
    def dict():
        """Метод описывает рецепт пиццы."""
        return {'Margherita \U0001F9C0': ['tomato sauce', 'mozzarella', 'tomatoes']}


class Pepperoni(Pizza):
    """Класс описывающий Пепперони. У данной пиццы отличается время готовки."""
    def __init__(self, size: str = 'X'):
        super().__init__(size)
        self.max_bake_time = 6 if size == 'XL' else 3

    @staticmethod
    def dict():
        """Метод описывает рецепт пиццы."""
        return {'Pepperoni \U0001F355': ['tomato sauce', 'mozzarella', 'pepperoni']}


class Hawaiian(Pizza):
    """Класс описывающий Гавайи. У данной пиццы отличается время готовки."""
    def __init__(self, size: str = 'X'):
        super().__init__(size)
        self.max_bake_time = 12 if size == 'XL' else 6

    @staticmethod
    def dict():
        """Метод описывает рецепт пиццы."""
        return {'Hawaiian \U0001F34D': ['tomato sauce', 'mozzarella', 'chicken', 'pineapples']}


def log(template):
    """
    Декоратор, выводящий время работы функции.
    Принимает в качестве аргумента шаблон,
    в который подставляется время работы декорируемой функции.
    """
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
    """
    Готовит и доставляет пиццу.
    При заказе несуществующей пиццы предлагает посмотреть меню.
    """

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
        print(
            f'Вы заказали: {pizza}.',
            'Такой пиццы нет в меню.',
            'Запустите команду \'python cli.py menu\' чтоб вывести меню.',
            sep='\n'
        )


@cli.command()
def menu():
    """Выводит меню"""
    for pizza in [Margherita, Pepperoni, Hawaiian]:
        key, rec = list(pizza.dict().items())[0]
        print(f"- {key}: {', '.join(rec)}")


if __name__ == '__main__':
    cli()
