import pytest
from recipes import Ingredient, Recipe, ShoppingList, DietaryRecipe




def test_ingredient_init():
    ing = Ingredient("Свёкла", 300, "г")
    assert ing.name == "Свёкла"
    assert ing.quantity == 300.0
    assert ing.unit == "г"

def test_ingredient_str():
    ing = Ingredient("Свёкла", 300, "г")
    assert str(ing) == "Свёкла: 300.0 г"

def test_ingredient_eq_same():
    ing1 = Ingredient("Свёкла", 300, "г")
    ing2 = Ingredient("Свёкла", 150, "г")
    assert ing1 == ing2

def test_ingredient_eq_different_name():
    ing1 = Ingredient("Свёкла", 300, "г")
    ing2 = Ingredient("Морковь", 300, "г")
    assert ing1 != ing2

def test_ingredient_eq_different_unit():
    ing1 = Ingredient("Свёкла", 300, "г")
    ing2 = Ingredient("Свёкла", 300, "кг")
    assert ing1 != ing2

def test_ingredient_negative_quantity():
    with pytest.raises(ValueError):
        Ingredient("Свёкла", -100, "г")



def test_recipe_init():
    recipe = Recipe("Борщ")
    assert recipe.title == "Борщ"
    assert recipe.ingredients == []

def test_recipe_add_ingredient():
    recipe = Recipe("Борщ")
    ing = Ingredient("Свёкла", 300, "г")
    recipe.add_ingredient(ing)
    assert len(recipe) == 1

def test_recipe_add_ingredient_duplicate():
    recipe = Recipe("Борщ")
    recipe.add_ingredient(Ingredient("Свёкла", 300, "г"))
    recipe.add_ingredient(Ingredient("Свёкла", 150, "г"))
    assert len(recipe) == 1
    assert recipe.ingredients[0].quantity == 450.0

def test_recipe_scale():
    recipe = Recipe("Болоньезе")
    recipe.add_ingredient(Ingredient("Фарш", 500, "г"))
    scaled = recipe.scale(2)
    assert scaled.ingredients[0].quantity == 1000.0
    assert recipe.ingredients[0].quantity == 500.0

def test_recipe_scale_invalid():
    recipe = Recipe("Болоньезе")
    recipe.add_ingredient(Ingredient("Фарш", 500, "г"))
    with pytest.raises(ValueError):
        recipe.scale(-1)

def test_recipe_len():
    recipe = Recipe("Борщ")
    recipe.add_ingredient(Ingredient("Свёкла", 300, "г"))
    recipe.add_ingredient(Ingredient("Капуста", 200, "г"))
    assert len(recipe) == 2



def test_shopping_list_add_recipe():
    recipe = Recipe("Болоньезе")
    recipe.add_ingredient(Ingredient("Фарш", 500, "г"))
    sl = ShoppingList()
    sl.add_recipe(recipe, 2)
    result = sl.get_list()
    assert len(result) == 1
    assert result[0].quantity == 1000.0

def test_shopping_list_add_recipe_invalid_portions():
    recipe = Recipe("Борщ")
    sl = ShoppingList()
    with pytest.raises(ValueError):
        sl.add_recipe(recipe, 0)

def test_shopping_list_remove_recipe():
    recipe = Recipe("Борщ")
    recipe.add_ingredient(Ingredient("Свёкла", 300, "г"))
    sl = ShoppingList()
    sl.add_recipe(recipe, 1)
    sl.remove_recipe("Борщ")
    assert sl.get_list() == []

def test_shopping_list_remove_nonexistent():
    sl = ShoppingList()
    sl.remove_recipe("Несуществующий")

def test_shopping_list_get_list_sorted():
    recipe = Recipe("Борщ")
    recipe.add_ingredient(Ingredient("Свёкла", 300, "г"))
    recipe.add_ingredient(Ingredient("Капуста", 200, "г"))
    sl = ShoppingList()
    sl.add_recipe(recipe, 1)
    result = sl.get_list()
    assert result[0].name == "Капуста"
    assert result[1].name == "Свёкла"

def test_shopping_list_get_list_combines():
    recipe1 = Recipe("Борщ")
    recipe1.add_ingredient(Ingredient("Морковь", 100, "г"))
    recipe2 = Recipe("Болоньезе")
    recipe2.add_ingredient(Ingredient("Морковь", 50, "г"))
    sl = ShoppingList()
    sl.add_recipe(recipe1, 1)
    sl.add_recipe(recipe2, 1)
    result = sl.get_list()
    assert result[0].quantity == 150.0

def test_shopping_list_add():
    recipe1 = Recipe("Борщ")
    recipe1.add_ingredient(Ingredient("Свёкла", 300, "г"))
    recipe2 = Recipe("Болоньезе")
    recipe2.add_ingredient(Ingredient("Фарш", 500, "г"))
    sl1 = ShoppingList()
    sl1.add_recipe(recipe1, 1)
    sl2 = ShoppingList()
    sl2.add_recipe(recipe2, 1)
    sl3 = sl1 + sl2
    assert len(sl3.get_list()) == 2
    assert len(sl1.get_list()) == 1
    assert len(sl2.get_list()) == 1