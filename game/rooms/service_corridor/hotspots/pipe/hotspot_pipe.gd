# @popochiu-docs-ignore-class
@tool
extends PopochiuHotspot
# Service Corridor: the leaky pipe that feeds the puddle.

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
	await G.show_system_text("The pipe drips. And drips. It has dripped for three years. You filed a work order. Somebody filed it down the chute.")


func on_interact() -> void:
	await C.player.walk_to_clicked()
	await C.player.face_clicked()
	await G.show_system_text("You tighten the valve. It squeaks, sprays you in the face, then goes back to dripping. A classic.")


func on_talk() -> void:
	await C.player.say("Hang in there, buddy. We're both leaking on the job.")


func _on_item_used(item: PopochiuInventoryItem) -> void:
	if item == I.Bucket:
		await G.show_system_text("You'd catch about a cup a day. At that rate the bucket fills sometime after the ship hits the sun.")
		return

	E.command_fallback()
