@tool
extends "res://addons/popochiu/engine/interfaces/i_room.gd"

# classes ----
const PRSupplyCloset := preload("res://game/rooms/supply_closet/room_supply_closet.gd")
# ---- classes

# nodes ----
var SupplyCloset: PRSupplyCloset : get = get_SupplyCloset
# ---- nodes

# functions ----
func get_SupplyCloset() -> PRSupplyCloset: return get_runtime_room("SupplyCloset")
# ---- functions

