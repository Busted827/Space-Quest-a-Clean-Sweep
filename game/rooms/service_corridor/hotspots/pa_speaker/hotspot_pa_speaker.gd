# @popochiu-docs-ignore-class
@tool
extends PopochiuHotspot
# Service Corridor: the PA speaker Sterilis broadcasts through.

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
	await G.show_system_text("A PA speaker. Ten minutes ago it played elevator music. Now it plays a madman.")


func on_interact() -> void:
	await G.show_system_text("It's bolted high on the wall, well out of reach. Which is where you'd put it too if your crew included Roger Wilco.")


func on_talk() -> void:
	await C.player.say("Hello? Dr. Sterilis? Can we talk about this?")
	await G.show_system_text("The speaker crackles: \"Your call is important to us. Please remain sanitary. Your estimated wait time is... forever.\"")
