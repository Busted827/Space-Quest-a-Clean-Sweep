# @popochiu-docs-ignore-class
@tool
extends PopochiuProp
# Supply Closet 13-B: Roger's mop, the first item to pick up.

# Left click with the Walk command, or no command: walk over.
func _on_click() -> void:
	E.command_fallback()


func _on_double_click() -> void:
	E.command_fallback()


func _on_right_click() -> void:
	E.command_fallback()


func _on_middle_click() -> void:
	E.command_fallback()


func on_look() -> void:
	await C.player.walk_to_clicked()
	await C.player.face_clicked()
	await G.show_system_text("Your trusty mop. Standard issue, model M-1 Swabbie. It smells like every floor on this ship.")
	await C.player.say("All the other janitors get new mops...")


func on_interact() -> void:
	await C.player.walk_to_clicked()
	await C.player.face_clicked()
	var room_state = R.SupplyCloset.state
	room_state.mop_taken = true
	await disable()
	await I.Mop.add()
	await G.show_system_text("Roger takes the mop. It feels right in his hands. Like Excalibur, if Excalibur were damp.")


func on_talk() -> void:
	await C.player.say("Ready for one more shift, old friend?")
