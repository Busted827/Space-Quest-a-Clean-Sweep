# @popochiu-docs-ignore-class
@tool
extends PopochiuHotspot
# Supply Closet 13-B: the way out to the Service Corridor.

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
	await G.show_system_text("The door to the Service Corridor. Through the window you can see a puddle. A big one. It's practically a lake.")


func on_interact() -> void:
	await C.player.walk_to_clicked()
	await C.player.face_clicked()
	if not (I.Mop.in_inventory and I.Bucket.in_inventory):
		await C.player.say("I'm not going out there without my mop and bucket. A janitor without a mop is just a guy.")
		return

	if not R.SupplyCloset.state.left_once:
		R.SupplyCloset.state.left_once = true
		await C.player.say("Okay, Wilco. Mop, bucket, keycard. Time to be a hero. Or at least a janitor.")
	R.goto_room("ServiceCorridor")


func on_talk() -> void:
	await C.player.say("Knock knock.")
	await G.show_system_text("Nobody answers. Everyone out there is tied up, hiding, or being sterilized.")
