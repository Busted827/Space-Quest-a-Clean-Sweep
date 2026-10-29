@tool
extends "res://addons/popochiu/engine/interfaces/i_inventory.gd"

# classes ----
const PIIMop := preload("res://game/inventory_items/mop/inventory_item_mop.gd")
const PIIBucket := preload("res://game/inventory_items/bucket/inventory_item_bucket.gd")
const PIIKeycard := preload("res://game/inventory_items/keycard/inventory_item_keycard.gd")
# ---- classes

# nodes ----
var Mop: PIIMop : get = get_Mop
var Bucket: PIIBucket : get = get_Bucket
var Keycard: PIIKeycard : get = get_Keycard
# ---- nodes

# functions ----
func get_Mop() -> PIIMop: return get_item_instance("Mop")
func get_Bucket() -> PIIBucket: return get_item_instance("Bucket")
func get_Keycard() -> PIIKeycard: return get_item_instance("Keycard")
# ---- functions

