extends Node
# Takes interface screenshots: the icon bar dropped down, and a narrator text box.
# Run it as an autoload (Shots="*res://tools/ui_shots.gd") under a real display, then remove it.

func _ready() -> void:
	_run.call_deferred()


func _move_mouse(pos: Vector2) -> void:
	get_viewport().warp_mouse(pos)
	var ev := InputEventMouseMotion.new()
	ev.position = pos
	ev.global_position = pos
	Input.parse_input_event(ev)


func _click() -> void:
	var ev := InputEventMouseButton.new()
	ev.button_index = MOUSE_BUTTON_LEFT
	ev.position = Vector2(320, 300)
	ev.pressed = true
	Input.parse_input_event(ev)
	var up := ev.duplicate()
	up.pressed = false
	Input.parse_input_event(up)


func _shot(path: String) -> void:
	await RenderingServer.frame_post_draw
	get_viewport().get_texture().get_image().save_png(path)
	print("[shots] saved ", path)


func _run() -> void:
	# Click through the intro until the game hands control to the player.
	while not (R.SupplyCloset.state.intro_done and not G.is_blocked):
		_click()
		await get_tree().create_timer(0.3).timeout
	await get_tree().create_timer(1.0).timeout
	_move_mouse(Vector2(320, 4))
	await get_tree().create_timer(0.5).timeout
	await _shot(OS.get_environment("SHOT_DIR") + "/menu_open.png")
	_move_mouse(Vector2(330, 200))
	await get_tree().create_timer(0.5).timeout
	await _shot(OS.get_environment("SHOT_DIR") + "/menu_closed.png")
	R.SupplyCloset.get_hotspot("CeilingTile").on_look()
	await get_tree().create_timer(1.0).timeout
	await _shot(OS.get_environment("SHOT_DIR") + "/text_box.png")
	get_tree().quit()
