extends Node
# Smoke test: clicks through text boxes and plays the Supply Closet puzzle chain.
# Run it by adding it as an autoload (Smoke="*res://tools/smoke_test.gd"), then remove it.

func _ready() -> void:
	_run.call_deferred()


func _click() -> void:
	var ev := InputEventMouseButton.new()
	ev.button_index = MOUSE_BUTTON_LEFT
	ev.position = Vector2(320, 180)
	ev.pressed = true
	Input.parse_input_event(ev)
	var up := ev.duplicate()
	up.pressed = false
	Input.parse_input_event(up)


func _process(_delta: float) -> void:
	if Engine.get_process_frames() % 8 == 0:
		_click()


func _run() -> void:
	await get_tree().create_timer(8.0).timeout
	var room = R.SupplyCloset
	print("[smoke] intro_done=", room.state.intro_done)
	await C.player.on_look()
	await C.player.on_interact()
	await C.player.on_talk()
	await E.command_fallback()
	await room.get_hotspot("Shelves").on_talk()
	await room.get_prop("Mop").on_look()
	await room.rewind_after_death("Life sucks... again.")
	print("[smoke] quotes ok")
	await room.get_hotspot("Locker").on_interact()
	print("[smoke] locker without combo, open=", room.state.locker_open)
	await room.get_hotspot("CeilingTile").on_look()
	print("[smoke] combo_known=", room.state.combo_known)
	await room.get_hotspot("Locker").on_interact()
	print("[smoke] locker open=", room.state.locker_open, " keycard=", I.Keycard.in_inventory)
	await room.get_hotspot("Door").on_interact()
	await room.get_prop("Mop").on_interact()
	await room.get_prop("Bucket").on_interact()
	print("[smoke] mop=", I.Mop.in_inventory, " bucket=", I.Bucket.in_inventory)
	await room.get_hotspot("Crate").on_interact()
	await room.get_hotspot("Crate").on_interact()
	await room.get_hotspot("Door").on_interact()
	await get_tree().create_timer(3.0).timeout
	var hall = R.ServiceCorridor
	print("[smoke] in corridor=", R.current == hall)
	await hall.get_prop("Puddle").on_look()
	await hall.get_hotspot("Lifts").on_interact()
	print("[smoke] slipped, mopped=", hall.state.puddle_mopped)
	await hall.get_prop("Puddle").on_item_used(I.Mop)
	print("[smoke] mopped=", hall.state.puddle_mopped, " filth=", I.Bucket.state.filth)
	await hall.get_hotspot("Lifts").on_item_used(I.Keycard)
	await hall.get_hotspot("StaffDoor").on_item_used(I.Keycard)
	await I.Bucket.on_look()
	await hall.get_hotspot("ClosetDoor").on_interact()
	await get_tree().create_timer(3.0).timeout
	print("[smoke] back in closet=", R.current == R.SupplyCloset, " roger at ", C.player.position)
	print("[smoke] done")
	get_tree().quit()
