# @popochiu-docs-ignore-class
@tool
extends PopochiuHotspot
# Service Corridor: the door to the Galley.

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
	await G.show_system_text("The Galley, where Chef-O-Matic serves the crew whatever the passengers sent back.")


func on_interact() -> void:
	await C.player.walk_to_clicked()
	await C.player.face_clicked()
	await G.show_system_text("(This room isn't built yet. It arrives in a later build.)")


func on_talk() -> void:
	await C.player.say("Chef? You in there?")
	await G.show_system_text("No answer. Chef-O-Matic has been unplugged, which is the happiest he's ever been.")
