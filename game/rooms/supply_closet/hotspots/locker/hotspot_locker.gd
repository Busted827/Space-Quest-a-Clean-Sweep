# @popochiu-docs-ignore-class
@tool
extends PopochiuHotspot
# Supply Closet 13-B: Roger's locker. Looking at the ceiling tile reveals the combination.

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
	var room_state = R.SupplyCloset.state
	if room_state.locker_open:
		await G.show_system_text("Your open locker. It smells like old socks and older dreams.")
		return

	await G.show_system_text("Your locker. WILCO is stenciled on it, spelled correctly for once. A combination lock keeps out thieves, and you.")


func on_interact() -> void:
	await C.player.walk_to_clicked()
	await C.player.face_clicked()
	var room_state = R.SupplyCloset.state
	if room_state.locker_open:
		await G.show_system_text("Nothing left but a sock of uncertain age. You leave it for science.")
		return

	if not room_state.combo_known:
		await C.player.say("Combination lock. I knew the combination once. I wrote it down somewhere I'd see it every day.")
		return

	await G.show_system_text("Roger spins 4-8-15. The locker opens on the first try, a personal record.")
	await G.show_system_text("Inside: your crew keycard, one sock, and a half-eaten Hyper-Jello cup from the Tuesday before last.")
	room_state.locker_open = true
	await I.Keycard.add()
	await C.player.say("Keycard. Check. Sock and jello stay here. They've earned it.")


func on_talk() -> void:
	await C.player.say("Open sesame?")
	await G.show_system_text("The locker is unimpressed.")


func _on_item_used(item: PopochiuInventoryItem) -> void:
	if item == I.Keycard:
		await G.show_system_text("It's a combination lock, not a card reader. Even the locker knows that.")
		return

	E.command_fallback()
