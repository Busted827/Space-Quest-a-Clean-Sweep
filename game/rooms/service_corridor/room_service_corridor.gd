# @popochiu-docs-ignore-class
@tool
extends PopochiuRoom

const Data := preload('room_service_corridor_state.gd')

var state: Data = load("res://game/rooms/service_corridor/room_service_corridor.tres")


#region Virtual ####################################################################################
# Called when Popochiu loads the room. At this point the room is in the scene tree but not yet
# visible.
# Add any code you want to setup the stage before the room is shown to the player (e.g. setting
# character position and facing direction, active walkable area, props visibility, etc.).
func _on_room_entered() -> void:
	C.player.teleport_to_marker("FromCloset")
	C.player.face_right()
	if state.puddle_mopped:
		get_prop("Puddle").disable()
	set_active_walkable_area("Floor" if state.puddle_mopped else "FloorLeft")


# Called after the room transition completes; the room is now visible.
# Implement this to start cutscenes, play sounds, etc.
# NOTE: this is NOT called when loading a saved game. Use [_on_restore_from_savegame] for that.
func _on_room_transition_finished() -> void:
	if not state.visited_first_time:
		return
	await G.show_system_text("The Service Deck corridor. The passengers never see it, which is the nicest thing anyone can say about it.")


# Called before Popochiu unloads the room.
# At this point the screen is black, processing is disabled, and characters
# have been removed from the $Characters node.
# Implement cleanup code, handle custom data or states before leaving the room, etc. if needed.
func _on_room_exited() -> void:
	pass


# Called after loading a saved game. The state of the room and all its objects is
# completely restored at this point. Use this to resume ongoing events,
# re-establish connections, or restart ambient audio.
# NOTE: `_on_room_transition_finished()` is NOT called when loading a savegame.
# If you need to run its code when loading a savegame, you can call it explicitly from this method.
func _on_restore_from_savegame() -> void:
	pass


#endregion

#region Public #####################################################################################
# Everything past the puddle: until it's mopped, trying to get there means walking through it.
func reach_far_side() -> bool:
	if state.puddle_mopped:
		return true
	await slip()
	return false


func puddle_mopped() -> void:
	state.puddle_mopped = true
	await get_prop("Puddle").disable()
	set_active_walkable_area("Floor")
	await I.Bucket.add_filth(1)


# The room's death: Roger walks into the puddle and slides out the waste chute.
func slip() -> void:
	await C.player.walk_to(Vector2(300, 300))
	await G.show_system_text("Roger strides boldly into the puddle. His feet go one way. The rest of him goes the other way, then down the corridor, then into the waste chute.")
	await G.show_system_text("Next time, try the mop. It's the long thing you're paid to hold.")
	await G.show_system_text("Thanks for playing Clean Sweep. As usual, you've been a real pantload!")
	await G.show_system_text("Click to rewind time and try again.")
	C.player.teleport_to_marker("FromCloset")
	C.player.face_right()


#endregion
