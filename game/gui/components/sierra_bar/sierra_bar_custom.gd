extends "sierra_bar.gd"

# SQ5's status bar: dark letters on slate, no outline.
const INK := Color(0.0941176, 0.12549, 0.12549)


func _ready() -> void:
	var hover_label: RichTextLabel = $PanelContainer/HBoxContainer/HoverText/RichTextLabel
	hover_label.add_theme_color_override("default_color", INK)
	hover_label.add_theme_constant_override("outline_size", 0)


func _update_text() -> void:
	lbl_score.text = "Score: %d of %d" % [score, max_score]
