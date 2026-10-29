# @popochiu-docs-ignore-class
@tool
extends PopochiuHotspot
# Service Corridor: the door back to Supply Closet 13-B.

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
	await G.show_system_text("Supply Closet 13-B. Home sweet broom closet.")


func on_interact() -> void:
	await C.player.walk_to_clicked()
	await C.player.face_clicked()
	R.goto_room("SupplyCloset")


func on_talk() -> void:
	await C.player.say("Don't wait up, crate.")
