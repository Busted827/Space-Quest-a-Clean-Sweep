# @popochiu-docs-ignore-class
@tool
extends PopochiuRoom

const Data := preload('room_supply_closet_state.gd')

var state: Data = load("res://game/rooms/supply_closet/room_supply_closet.tres")


#region Virtual ####################################################################################
# Called when Popochiu loads the room. At this point the room is in the scene tree but not yet
# visible.
# Add any code you want to setup the stage before the room is shown to the player (e.g. setting
# character position and facing direction, active walkable area, props visibility, etc.).
func _on_room_entered() -> void:
	if state.mop_taken:
		get_prop("Mop").disable()
	if state.bucket_taken:
		get_prop("Bucket").disable()

	if not state.intro_done:
		C.player.teleport_to_marker("Start")
		C.player.face_right()


# Called after the room transition completes; the room is now visible.
# Implement this to start cutscenes, play sounds, etc.
# NOTE: this is NOT called when loading a saved game. Use [_on_restore_from_savegame] for that.
func _on_room_transition_finished() -> void:
	if state.intro_done:
		return

	state.intro_done = true
	await E.queue([
		G.queue_show_system_text(
			"Supply Closet 13-B, Service Deck, SCS Lavish Excess. Roger Wilco is doing what he does best."
		),
		C.player.queue_say("Zzzz... five more minutes... the mop can wait..."),
		G.queue_show_system_text(
			"ATTENTION, PASSENGERS AND CREW. This is Dr. Purity Sterilis. I have taken command of this filthy vessel."
		),
		G.queue_show_system_text(
			"In approximately one hour we will fly into the sun for the ultimate deep clean. Please remain calm and wash your hands."
		),
		G.queue_show_system_text(
			"And Wilco... I know you are down there. I can smell you."
		),
		C.player.queue_say("Uh oh."),
	])


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
# Sierra-style death, with a modern rewind: Roger is put back on his feet in this room.
func rewind_after_death(title := "") -> void:
	if title:
		await G.show_system_text(title)
	await G.show_system_text("Thanks for playing Clean Sweep. As usual, you've been a real pantload!")
	await G.show_system_text("Click to rewind time and try again.")
	C.player.teleport_to_marker("Start")
	C.player.face_right()


#endregion
