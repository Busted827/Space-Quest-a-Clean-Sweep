# @popochiu-docs-ignore-class
@tool
extends PopochiuProp
# Service Corridor: the murky puddle (Filth Meter level 1). Walking into it is a death.

# Left click with the Walk command, or no command: walk over.
func _on_click() -> void:
	_walk_or_slip()


func _on_double_click() -> void:
	E.command_fallback()


func _on_right_click() -> void:
	E.command_fallback()


func _on_middle_click() -> void:
	E.command_fallback()


func on_look() -> void:
	await G.show_system_text("A murky puddle, fed by the drip from the pipe above. It's spread across the whole corridor. Somebody should really mop that. Oh, wait. That's you.")


func on_interact() -> void:
	await C.player.walk_to_clicked()
	await C.player.face_clicked()
	await G.show_system_text("You dip a finger in. It's slippery. And warm. Let's not think about why it's warm.")


func on_talk() -> void:
	await G.show_system_text("You consider tasting it. Even you have limits. Barely.")


func _on_item_used(item: PopochiuInventoryItem) -> void:
	match item:
		I.Mop:
			await C.player.walk_to_clicked()
			await C.player.face_clicked()
			await G.show_system_text("You mop up the puddle and wring it into your bucket. Squelch. The water turns a promising shade of grey.")
			await R.ServiceCorridor.puddle_mopped()
		I.Bucket:
			await G.show_system_text("Mop first, then wring into the bucket. It's called a system. You learned it in janitor school, in the one class you stayed awake for.")
		I.Keycard:
			await G.show_system_text("You swipe the keycard through the puddle. Access denied. Also, now it's sticky.")
		_:
			E.command_fallback()


# Walking into the puddle is the room's death (design doc, Death scenes).
func _walk_or_slip() -> void:
	if E.current_command == SierraCommands.Commands.WALK:
		await R.ServiceCorridor.slip()
		return

	E.command_fallback()
