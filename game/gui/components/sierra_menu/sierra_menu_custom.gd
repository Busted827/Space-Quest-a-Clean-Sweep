extends "sierra_menu.gd"


# SQ6's empty-pockets joke instead of an empty inventory window.
func _on_inventory_pressed() -> void:
	if C.player.inventory.is_empty():
		hide()
		G.show_system_text("You have nothing. Nada. Zip. Zero. Zilch. Not even lint. You're a professional.")
		return

	super()
