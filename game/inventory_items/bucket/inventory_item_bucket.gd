# @popochiu-docs-ignore-class
extends PopochiuInventoryItem

const Data := preload('inventory_item_bucket_state.gd')

var state: Data = load("res://game/inventory_items/bucket/inventory_item_bucket.tres")


#region Virtual ####################################################################################
# Called when the item is clicked in the inventory
func _on_click() -> void:
	# Replace the call to E.command_fallback() to implement your code.
	E.command_fallback()


# Called when the item is right-clicked in the inventory
func _on_right_click() -> void:
	# Replace the call to E.command_fallback() to implement your code.
	E.command_fallback()


# Called when the item is middle-clicked in the inventory
func _on_middle_click() -> void:
	# Replace the call to E.command_fallback() to implement your code.
	E.command_fallback()


# Called when the item is clicked while another inventory item is selected
func _on_item_used(_item: PopochiuInventoryItem) -> void:
	# Replace the call to E.command_fallback() with your own logic.
	E.command_fallback()
	# Example: if a Key is used on this item, make the player say something.
#	if _item == I.Key:
#		await C.player.say("This item has no lock!")


# Called when the item is added to the inventory
func _on_added_to_inventory() -> void:
	# Replace the call to `super()` to implement custom behavior.
	# Calling `super()` preserves default behavior as well.
	super()


# Called when the item is discarded from the inventory
func _on_discard() -> void:
	# Replace the call to `super()` to implement custom behavior.
	# Calling `super()` preserves default behavior as well.
	super()


#endregion

#region Public #####################################################################################
const FILTH_NAMES := ["Spotless", "Murky", "Greasy", "Sludgy", "Unspeakable", "Biohazard"]
const FILTH_LOOKS := [
	"Your bucket. Filth Meter: Spotless. Every mess you mop makes it grosser, and gross is exactly what you will need.",
	"Your bucket. Filth Meter: Murky. Grey water with things floating in it. A promising start.",
	"Your bucket. Filth Meter: Greasy. A rainbow sheen swirls on top. It's almost pretty, in a deeply wrong way.",
	"Your bucket. Filth Meter: Sludgy. The water has stopped sloshing. It now oozes.",
	"Your bucket. Filth Meter: Unspeakable. We will not speak of it.",
	"Your bucket. Filth Meter: BIOHAZARD. Somewhere, Dr. Sterilis just felt a chill and doesn't know why.",
]


func on_look() -> void:
	await G.show_system_text(FILTH_LOOKS[state.filth])


# Raises the Filth Meter. The inventory picture gets grosser at each level.
func add_filth(level: int) -> void:
	if level <= state.filth:
		return
	state.filth = level
	texture = load("res://game/placeholders/inv_bucket_%d.png" % level)
	await G.show_system_text("Filth Meter: %s." % FILTH_NAMES[level])


#endregion
