import click
from random import randint
import time
from pizza import Hawaiian, Margherita, Pepperoni


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
