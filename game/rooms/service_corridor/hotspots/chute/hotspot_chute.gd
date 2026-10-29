# @popochiu-docs-ignore-class
@tool
extends PopochiuHotspot
# Service Corridor: the waste chute hatch.

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
	await G.show_system_text("The waste chute. Everything on the Service Deck goes down there eventually. Including, someday, you.")


func on_interact() -> void:
	if not await R.ServiceCorridor.reach_far_side():
		return
	await C.player.walk_to_clicked()
	await C.player.face_clicked()
	await G.show_system_text("You open the hatch. A smell climbs out, looks around, and files a complaint. You close the hatch.")


func on_talk() -> void:
	await C.player.say("Hellooo down there!")
	await G.show_system_text("Something down there says hello back. You decide not to think about it.")
