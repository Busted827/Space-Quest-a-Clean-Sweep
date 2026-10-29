# @popochiu-docs-ignore-class
@tool
extends PopochiuHotspot
# Service Corridor: the staff-only door to Waste Reclamation.

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
	await G.show_system_text("STAFF ONLY: WASTE RECLAMATION. There is a card slot, and under it someone scratched \"abandon hope.\"")


func on_interact() -> void:
	if not await R.ServiceCorridor.reach_far_side():
		return
	await C.player.walk_to_clicked()
	await C.player.face_clicked()
	await G.show_system_text("Locked. The card slot blinks red at you, patiently, like a disappointed parent.")


func on_talk() -> void:
	await C.player.say("Open sesame?")
	await G.show_system_text("The door was not programmed by anybody with a sense of humor.")


func _on_item_used(item: PopochiuInventoryItem) -> void:
	if item == I.Keycard:
		if not await R.ServiceCorridor.reach_far_side():
			return
		await C.player.walk_to_clicked()
		await C.player.face_clicked()
		await G.show_system_text("You swipe your keycard. The light turns green. Somewhere behind the door, something gurgles.")
		await G.show_system_text("(This room isn't built yet. It arrives in a later build.)")
		return

	E.command_fallback()
