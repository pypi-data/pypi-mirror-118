from vinca.lib import classes

def generate():
	# initialize card
	new_card = classes.Card(create=True)
	# initialize card metadata
	new_card.editor, new_card.reviewer, new_card.scheduler = 'media', 'media', 'base'
	# initialize card data files
	for side in ('front', 'back'):
		(new_card.path / side).touch()
	new_card.edit()  
	return [new_card]
