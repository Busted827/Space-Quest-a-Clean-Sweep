@tool
extends "res://addons/popochiu/engine/interfaces/i_character.gd"

# classes ----
const PCRoger := preload("res://game/characters/roger/character_roger.gd")
# ---- classes

# nodes ----
var Roger: PCRoger : get = get_Roger
# ---- nodes

# functions ----
func get_Roger() -> PCRoger: return get_runtime_character("Roger")
# ---- functions

