# @popochiu-docs-ignore-class
@tool
extends PopochiuProp
# Supply Closet 13-B: Roger's bucket. Later it carries the Filth Meter.

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
	await G.show_system_text("Your bucket. Empty for now. Filth Meter: Spotless. Don't worry, that won't last.")


func on_interact() -> void:
	await C.player.walk_to_clicked()
	await C.player.face_clicked()
	var room_state = R.SupplyCloset.state
	room_state.bucket_taken = true
	await disable()
	await I.Bucket.add()
	await G.show_system_text("Roger takes the bucket. Its handle squeaks a little welcome.")


func on_talk() -> void:
	await C.player.say("You're looking very clean today.")
	await G.show_system_text("The bucket blushes. Buckets can't blush. Something is very wrong on this ship.")
