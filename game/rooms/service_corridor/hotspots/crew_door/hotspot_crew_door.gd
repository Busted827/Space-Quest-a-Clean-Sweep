# @popochiu-docs-ignore-class
@tool
extends PopochiuHotspot
# Service Corridor: the door to Crew Quarters.

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
	await G.show_system_text("Crew Quarters. Forty bunks, one shower, and a smell that has its own crew badge.")


func on_interact() -> void:
	await C.player.walk_to_clicked()
	await C.player.face_clicked()
	await G.show_system_text("(This room isn't built yet. It arrives in a later build.)")


func on_talk() -> void:
	await C.player.say("Anybody in there? Sterilis just took over the ship. Hello?")
	await G.show_system_text("Somebody snores. Loudly. It's the most useful thing the crew has done all week.")
