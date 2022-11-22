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
