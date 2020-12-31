from enum import Enum, auto



class kw():

	### INTEGRAL KEYWORDS
	# Strings so that they can correctly compare to parameters in a kwarg dictionary

	# Base actions
	TICK = 'tick'
	DAMAGE_HEALTH = 'damage_health'
	DAMAGE_FOCUS = 'damage_focus'
	GAIN_HEALTH = 'gain_health'
	GAIN_FOCUS = 'gain_focus'

	# Parameter keywords
	DMG_TYPE = 'dmg_type'
	DMG_AMOUNT = 'dmg_amount'
	GAIN_AMOUNT = 'gain_amount'
	GAIN_TYPE = 'gain_type'
	F_DMG_TYPE = 'f_dmg_type'
	F_DMG_AMOUNT = 'f_dmg_amount'
	F_GAIN_AMOUNT = 'f_gain_amount'
	F_GAIN_TYPE = 'f_gain_type'
	STATUS_TIME = 'status_time'



class con(Enum):

	### NON-INTEGRAL KEYWORDS
	# Enum, because they just need to be unique constants

	# Utility
	STOP = auto()

	# Action types
	BASE = auto()
	ATTACK = auto()
	SPELL = auto()
	PHYSICAL = auto()
	NATURAL = auto()
	PROTECTION = auto()
	ENHANCEMENT = auto()
	UTILITY = auto()
	CONTROL = auto()
	ITEM = auto()
	HEAL = auto()
	MECHANICAL = auto()
	MENTAL = auto()

	# dmg_type
	MAGIC = auto()
	FIRE = auto()
	SLASH = auto()
	SACRIFICE = auto()
	CRUSH = auto()
	DISEASE = auto()
	WOUND = auto()

	# gain_type
	REPAIR = auto()
	SIPHON = auto()

	# f_dmg_type
	PANIC = auto()
	TERROR = auto()
	INSANITY = auto()
	PAIN = auto()

	# f_gain_type
	GLEE = auto()

	# Spell parameter values
	GESTURE = auto()
	INVOCATION = auto()
	CHANT = auto()
	RITUAL = auto()

	def __repr__(self):
		return '<con.' +  self.name + '>'

	def __str__(self):
		return self.name[0] + self.name[1:].lower()

	def multi_str(dmg_type):
		to_return = ''
		for dmg in dmg_type:
			to_return += f', {dmg}'

		return to_return[2:]