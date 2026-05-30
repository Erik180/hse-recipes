class Ingredient:
    def __init__(self, name: str, quantity: float, unit: str):
        self.name = name
        self.quantity = quantity
        self.unit = unit

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        if value <= 0:
            raise ValueError("Количество должно быть положительным")
        self._quantity = float(value)

    def __str__(self):
        return f"{self.name}: {self.quantity} {self.unit}"

    def __repr__(self):
        return f"Ingredient('{self.name}', {self.quantity}, '{self.unit}')"

    def __eq__(self, other):
        if not isinstance(other, Ingredient):
            return False
        return self.name == other.name and self.unit == other.unit
    

class Recipe:
    def __init__(self, title: str, ingredients: list = None):
        self.title = title
        self.ingredients = ingredients if ingredients is not None else []

    def add_ingredient(self, ingredient: Ingredient):
        for existing in self.ingredients:
            if existing == ingredient:
                existing.quantity += ingredient.quantity
                return
        self.ingredients.append(ingredient)

    @staticmethod
    def is_valid_ratio(ratio):
        if not isinstance(ratio, (int, float)):
            return False
        return ratio > 0

    def scale(self, ratio: float):
        if not self.is_valid_ratio(ratio):
            raise ValueError("Количество должно быть положительным")
        new_ingredients = []
        for ing in self.ingredients:
            new_ingredients.append(Ingredient(ing.name, ing.quantity * ratio, ing.unit))
        return Recipe(self.title, new_ingredients)

    def __len__(self):
        return len(self.ingredients)

    def __str__(self):
        result = f"Рецепт: {self.title}\n"
        for ing in self.ingredients:
            result += f"  - {ing}\n"
        return result
    
class DietaryRecipe(Recipe):
    def __init__(self, title: str, diet_type: str, ingredients: list = None):
        super().__init__(title, ingredients)
        self.diet_type = diet_type

    def scale(self, ratio: float):
        scaled = super().scale(ratio)
        return DietaryRecipe(self.title, self.diet_type, scaled.ingredients)

    def __str__(self):
        return f"[{self.diet_type}] " + super().__str__()
    

class ShoppingList:
    def __init__(self):
        self._items = []

    def add_recipe(self, recipe: Recipe, portions: float):
        if portions <= 0:
            raise ValueError("Количество порций должно быть положительным")
        scaled = recipe.scale(portions)
        for ingredient in scaled.ingredients:
            self._items.append((ingredient, recipe.title))

    def remove_recipe(self, title: str):
        self._items = [(ing, t) for ing, t in self._items if t != title]

    def get_list(self):
        totals = {}
        for ingredient, _ in self._items:
            key = (ingredient.name, ingredient.unit)
            if key in totals:
                totals[key] += ingredient.quantity
            else:
                totals[key] = ingredient.quantity
        result = []
        for (name, unit), quantity in totals.items():
            result.append(Ingredient(name, quantity, unit))
        return sorted(result, key=lambda x: x.name)

    def __add__(self, other: 'ShoppingList'):
        new_list = ShoppingList()
        new_list._items = self._items.copy() + other._items.copy()
        return new_list