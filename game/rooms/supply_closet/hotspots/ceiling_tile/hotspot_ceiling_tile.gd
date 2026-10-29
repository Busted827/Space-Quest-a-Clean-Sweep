# @popochiu-docs-ignore-class
@tool
extends PopochiuHotspot
# Supply Closet 13-B: the tile where Roger scratched his locker combination.

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
	await C.player.face_clicked()
	var room_state = R.SupplyCloset.state
	await G.show_system_text("The ceiling tile above your crate. You have stared at it every day for three years.")
	await G.show_system_text("Someone scratched 4-8-15 into it. Oh, right. You did. It's your locker combination.")
	room_state.combo_known = true


func on_interact() -> void:
	await C.player.say("I can't reach it. I can barely reach the crate.")


func on_talk() -> void:
	await C.player.say("Hello, ceiling. Still up there?")
	await G.show_system_text("The ceiling is, in fact, still up there.")


func _on_item_used(item: PopochiuInventoryItem) -> void:
	if item == I.Mop:
		await C.player.say("I could poke it with the mop... nah. Last time a tile fell on my head I was out for a week. Best week of my life, actually.")
		return

	E.command_fallback()
