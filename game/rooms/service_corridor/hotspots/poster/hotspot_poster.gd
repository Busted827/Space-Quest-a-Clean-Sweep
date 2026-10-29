# @popochiu-docs-ignore-class
@tool
extends PopochiuHotspot
# Service Corridor: a hygiene poster signed by the ship doctor.

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
	await G.show_system_text("\"A CLEAN SHIP IS A HAPPY SHIP,\" signed Dr. P. Ure, Ship's Physician. Someone has drawn a mustache on him. That someone was you.")


func on_interact() -> void:
	await C.player.walk_to_clicked()
	await C.player.face_clicked()
	await G.show_system_text("The poster is laminated, sealed and disinfected. The mustache is permanent marker. You regret nothing.")


func on_talk() -> void:
	await C.player.say("P. Ure. Pure. Huh. Weird name for a doctor.")
	await G.show_system_text("Yes, Roger. Weird.")
