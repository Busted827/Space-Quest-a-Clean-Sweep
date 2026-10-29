# @popochiu-docs-ignore-class
@tool
extends PopochiuHotspot
# Service Corridor: the lifts up to the Passenger Deck.

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
	await G.show_system_text("The lifts to the Passenger Deck, where the carpet is thicker and the passengers are thinner.")


func on_interact() -> void:
	if not await R.ServiceCorridor.reach_far_side():
		return
	await C.player.walk_to_clicked()
	await C.player.face_clicked()
	await G.show_system_text("The panel lights up: STAFF ACCESS REVOKED BY ORDER OF DR. STERILIS. GUESTS ONLY. HAVE A SPOTLESS DAY.")


func on_talk() -> void:
	await C.player.say("Going up?")
	await G.show_system_text("The lift says nothing. Lifts never do. They just judge you.")


func _on_item_used(item: PopochiuInventoryItem) -> void:
	if item == I.Keycard:
		if not await R.ServiceCorridor.reach_far_side():
			return
		await C.player.walk_to_clicked()
		await C.player.face_clicked()
		await G.show_system_text("BZZT. \"Staff card rejected. Guests only.\" You'll need a guest keycard. Rich people lose those all the time. Usually in the trash.")
		return

	E.command_fallback()
