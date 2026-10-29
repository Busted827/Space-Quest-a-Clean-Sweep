# @popochiu-docs-ignore-class
@tool
extends PopochiuHotspot
# Supply Closet 13-B: shelves of confiscated cleaning products.

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
	await G.show_system_text("Shelves of industrial cleaning products: Scrub-Ex, Grime-B-Gone, and Sterilis Brand Antiseptic, now with 40% more sting.")


func on_interact() -> void:
	await C.player.walk_to_clicked()
	await C.player.face_clicked()
	if not ever_invoked(SierraCommands.Commands.INTERACT):
		await G.show_system_text("You get the shelves and put them in your pocket. Ouch.")
		await G.show_system_text("Just kidding. They're bolted to the wall because of people like you.")
		return
	await G.show_system_text("Every bottle carries a seal: CONFISCATED BY ORDER OF DR. STERILIS. Even the empty ones.")


# Talk is the mouth: the first time Roger chats, the second time he drinks.
func on_talk() -> void:
	if not ever_invoked(SierraCommands.Commands.TALK):
		await C.player.say("Psst. Any of you know how to stop a madman?")
		await G.show_system_text("The bleach remains silent. Bleach always does.")
		return

	await C.player.walk_to_clicked()
	await C.player.face_clicked()
	await G.show_system_text("Parched from a hard day of not working, Roger takes a long swig of Kleen-Zor. It is lemon scented. It is also industrial strength.")
	await R.SupplyCloset.rewind_after_death("Life sucks... again.")
