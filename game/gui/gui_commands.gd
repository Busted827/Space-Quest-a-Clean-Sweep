# @popochiu-docs-ignore-class
extends SierraCommands
# Default replies when an object has no line of its own. Most are riffs on the
# narrator's lines from SQ1 to SQ6 (see the design doc's Easter eggs section).

const LOOK_LINES := [
	"Excellent guess, Kreskin. Wrong, but excellent.",
	"You stare at it. It does not stare back. Small victories.",
	"It looks exactly like something you'll be asked to clean later.",
]
const HAND_LINES := [
	"Don't touch that. We know exactly where you've been. We clean up after you.",
	"Excellent guess, Kreskin. Wrong, but excellent.",
	"You'd need a work order for that. In triplicate.",
]
const TALK_LINES := [
	"You drool in that general direction, but no one notices.",
	"It has nothing to say. It's been listening to you all shift.",
]
const COMBINE_LINES := [
	"Careful! Combining those items might cause a rip in the space-time continuum... (Or not.)",
	"Those two things have never been introduced, and they'd like to keep it that way.",
	"Excellent guess, Kreskin. Wrong, but excellent.",
]
const MOP_LINE := "You mop it. It is now slightly wetter and no cleaner. Story of your career."

var _turns := {}


func _init() -> void:
	super()


static func get_script_name() -> String:
	return "SierraCommands"


# Called when a registered command has no Callable defined.
# By default this calls `walk()`. Override to implement a different fallback behavior.
func fallback() -> void:
	super()


# Called when `E.current_command == Commands.WALK` and `E.command_fallback()` is triggered.
# By default makes the character walk to the clicked `PopochiuClickable`.
func walk() -> void:
	super()


# Called when `E.current_command == Commands.LOOK` and `E.command_fallback()` is triggered.
func look() -> void:
	await G.show_system_text(_next("look", LOOK_LINES))


# Called when `E.current_command == Commands.INTERACT` and `E.command_fallback()` is triggered.
func interact() -> void:
	if I.active and (I.clicked or E.clicked) and I.active != I.clicked:
		if I.active == I.Mop:
			await G.show_system_text(MOP_LINE)
		else:
			await G.show_system_text(_next("combine", COMBINE_LINES))
	elif I.clicked:
		I.clicked.set_active()
	else:
		await G.show_system_text(_next("hand", HAND_LINES))


# Called when `E.current_command == Commands.TALK` and `E.command_fallback()` is triggered.
func talk() -> void:
	await G.show_system_text(_next("talk", TALK_LINES))


# Cycles through a set of lines so repeat clicks get a new joke.
func _next(key: String, lines: Array) -> String:
	var turn: int = _turns.get(key, 0)
	_turns[key] = turn + 1
	return lines[turn % lines.size()]
