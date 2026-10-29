# @popochiu-docs-ignore-class
@tool
extends PopochiuHotspot
# Supply Closet 13-B: Roger's one and only award.

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
	await G.show_system_text("EMPLOYEE OF THE MONTH: (NEVER). Someone drew your face on it in marker. It's a good likeness. The nose is very accurate.")


func on_interact() -> void:
	await C.player.walk_to_clicked()
	await C.player.face_clicked()
	await C.player.say("I should take this down.")
	await G.show_system_text("Then again, it's the only award you have ever received. It stays.")


func on_talk() -> void:
	await C.player.say("Someday, buddy. Someday.")
