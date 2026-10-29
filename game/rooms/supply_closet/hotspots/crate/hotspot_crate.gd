# @popochiu-docs-ignore-class
@tool
extends PopochiuHotspot
# Supply Closet 13-B: the crate Roger naps on.

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
	await G.show_system_text("Your crate. Your desk, your office, your bed. The drool stain on top is shaped like the Kerona system.")


func on_interact() -> void:
	await C.player.walk_to_clicked()
	await C.player.face_clicked()
	if not ever_invoked(SierraCommands.Commands.INTERACT):
		await C.player.say("Maybe just a quick nap. The sun can wait five minutes.")
		await G.show_system_text("Tempting. Very tempting. But the sun is not known for its patience.")
		return

	await G.show_system_text("Roger curls up on the crate for just a minute. He sleeps peacefully through the end of the ship.")
	await G.show_system_text("You've earned your rest. Permanently.")
	await R.SupplyCloset.rewind_after_death()


func on_talk() -> void:
	await C.player.say("You and me, crate. We've been through a lot.")
	await G.show_system_text("You have had deeper conversations with this crate than with most of the crew.")


func _on_item_used(item: PopochiuInventoryItem) -> void:
	if item == I.Mop:
		await G.show_system_text("You mop the crate. It is now the cleanest piece of furniture on the Service Deck. Nobody will ever know.")
		return

	E.command_fallback()
