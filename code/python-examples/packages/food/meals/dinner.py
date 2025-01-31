from food.actions.eat import eat
from food.actions.drink import drink
from food.actions import eat_more

def dinner():
	eat('appetizer')
	drink('red wine')
	eat('main dish')
	eat('desert')
	eat_more('desert')
