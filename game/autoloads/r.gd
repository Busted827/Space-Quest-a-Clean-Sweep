@tool
extends "res://addons/popochiu/engine/interfaces/i_room.gd"

# classes ----
const PRSupplyCloset := preload("res://game/rooms/supply_closet/room_supply_closet.gd")
const PRServiceCorridor := preload("res://game/rooms/service_corridor/room_service_corridor.gd")
# ---- classes

# nodes ----
var SupplyCloset: PRSupplyCloset : get = get_SupplyCloset
var ServiceCorridor: PRServiceCorridor : get = get_ServiceCorridor
# ---- nodes

# functions ----
func get_SupplyCloset() -> PRSupplyCloset: return get_runtime_room("SupplyCloset")
func get_ServiceCorridor() -> PRServiceCorridor: return get_runtime_room("ServiceCorridor")
# ---- functions

