import unittest
from subprocess import Popen, PIPE
from cli import Pizza, Pepperoni, Margherita, Hawaiian


class TestPizza(unittest.TestCase):
    def test___init__(self):
        with self.assertRaises(AssertionError):
            Pizza('XXX')

        pizza_a = Pizza('X')
        pizza_b = Pizza('XL')
        self.assertEqual('X', pizza_a.size)
        self.assertEqual('XL', pizza_b.size)

    def test___eq__(self):
        pizza_a = Pizza('X')
        pizza_b = Pizza('X')
        pizza_c = Pizza('XL')
        self.assertTrue(pizza_a == pizza_b)
        self.assertFalse(pizza_a == pizza_c)


class TestMargherita(unittest.TestCase):
    def test___init__(self):
        with self.assertRaises(AssertionError):
            Margherita('XXX')

        pizza_a = Margherita('X')
        pizza_b = Margherita('XL')
        self.assertEqual('X', pizza_a.size)
        self.assertEqual('XL', pizza_b.size)

    def test___eq__(self):
        pizza_a = Margherita('X')
        pizza_b = Margherita('X')
        pizza_c = Margherita('XL')
        pizza_d = Pepperoni()
        self.assertTrue(pizza_a == pizza_b)
        self.assertFalse(pizza_a == pizza_c)
        self.assertFalse(pizza_a == pizza_d)

    def test_dict(self):
        pizza = Margherita()
        key, value = list(pizza.dict().items())[0]
        self.assertEqual('Margherita \U0001F9C0', key)
        self.assertEqual(['tomato sauce', 'mozzarella', 'tomatoes'], value)


class TestPepperoni(unittest.TestCase):
    def test___init__(self):
        with self.assertRaises(AssertionError):
            Pepperoni('XXX')

        pizza_a = Pepperoni('X')
        pizza_b = Pepperoni('XL')
        self.assertEqual('X', pizza_a.size)
        self.assertEqual('XL', pizza_b.size)

    def test___eq__(self):
        pizza_a = Pepperoni('X')
        pizza_b = Pepperoni('X')
        pizza_c = Pepperoni('XL')
        pizza_d = Margherita()
        self.assertTrue(pizza_a == pizza_b)
        self.assertFalse(pizza_a == pizza_c)
        self.assertFalse(pizza_a == pizza_d)

    def test_dict(self):
        pizza = Pepperoni()
        key, value = list(pizza.dict().items())[0]
        self.assertEqual('Pepperoni \U0001F355', key)
        self.assertEqual(['tomato sauce', 'mozzarella', 'pepperoni'], value)


class TestHawaiian(unittest.TestCase):
    def test___init__(self):
        with self.assertRaises(AssertionError):
            Hawaiian('XXX')

        pizza_a = Hawaiian('X')
        pizza_b = Hawaiian('XL')
        self.assertEqual('X', pizza_a.size)
        self.assertEqual('XL', pizza_b.size)

    def test___eq__(self):
        pizza_a = Hawaiian('X')
        pizza_b = Hawaiian('X')
        pizza_c = Hawaiian('XL')
        pizza_d = Margherita()
        self.assertTrue(pizza_a == pizza_b)
        self.assertFalse(pizza_a == pizza_c)
        self.assertFalse(pizza_a == pizza_d)

    def test_dict(self):
        pizza = Hawaiian()
        key, value = list(pizza.dict().items())[0]
        self.assertEqual('Hawaiian \U0001F34D', key)
        self.assertEqual(['tomato sauce', 'mozzarella', 'chicken', 'pineapples'], value)


class TestCLI(unittest.TestCase):
    def test_menu(self):
        with Popen("python cli.py menu", shell=True, stdout=PIPE) as f:
            output = f.stdout.read().decode('utf-8').split('\r\n')

        expected_output = '- Margherita \U0001F9C0: tomato sauce, mozzarella, tomatoes\n' \
                          '- Pepperoni \U0001F355: tomato sauce, mozzarella, pepperoni\n' \
                          '- Hawaiian \U0001F34D: tomato sauce, mozzarella, chicken, pineapples\n'

        self.assertEqual('\n'.join(output), expected_output)

    def test_order(self):
        with Popen("python cli.py order Hawaiian", shell=True, stdout=PIPE) as f:
            output = f.stdout.read().decode('utf-8').split('\r\n')[:-1]  # убираем из списка ''

        self.assertTrue(len(output) == 2)
        self.assertTrue(output[0][:14] == 'Приготовили за')
        self.assertTrue(output[1][:10] == 'Забрали за')

    def test_order_delivery(self):
        with Popen("python cli.py order Hawaiian --delivery", shell=True, stdout=PIPE) as f:
            output = f.stdout.read().decode('utf-8').split('\r\n')[:-1]  # убираем из списка ''

        self.assertTrue(len(output) == 2)
        self.assertTrue(output[0][:14] == 'Приготовили за')
        self.assertTrue(output[1][:12] == 'Доставили за')

    def test_order_invalid(self):
        with Popen("python cli.py order Calzone --delivery", shell=True, stdout=PIPE) as f:
            output = f.stdout.read().decode('utf-8').split('\r\n')

        expected_output = 'Вы заказали: Calzone.\n' \
                          'Такой пиццы нет в меню.\n' \
                          'Запустите команду \'python cli.py menu\' чтоб вывести меню.\n'

        self.assertEqual('\n'.join(output), expected_output)
