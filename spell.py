from keywords import kw, con
from actions import Action, status_decorator
import status
import spell_status



class Spell(Action):
	def __init__(self, user, name, action_type, casting_reqs, /):
		Action.__init__(self, user, name, action_type)
		self.casting_reqs = casting_reqs




class Fireball(Spell):
	def __init__(self, user, /):
		Spell.__init__(self, user, 'Fireball', {con.SPELL, con.ATTACK}, {con.GESTURE, con.INVOCATION})
		self.default = {kw.DMG_AMOUNT:15, kw.DMG_TYPE:{con.FIRE, con.MAGIC}, kw.F_DMG_AMOUNT:20, kw.F_DMG_TYPE:{con.PANIC}, kw.STATUS_TIME:3}

	@status_decorator
	def __call__(self, target, /, *, dmg_amount, dmg_type, f_dmg_amount, f_dmg_type, status_time):
		target.damage_health(dmg_amount, dmg_type)
		target.damage_focus(f_dmg_amount, f_dmg_type)

		target.add_status(spell_status.Aflame(status_time))

class FireProtection(Spell):
	def __init__(self, user, /):
		Spell.__init__(self, user, 'Fire Protection', {con.SPELL, con.PROTECTION}, {con.CHANT})
		self.default = {kw.STATUS_TIME:5}

	@status_decorator
	def __call__(self, /, *, status_time):
		self.user.add_status(spell_status.FireResistance(status_time))

class FireEnhancement(Spell):
	def __init__(self, user, /):
		Spell.__init__(self, user, 'Fire Enhancement', {con.SPELL, con.ENHANCEMENT}, {con.CHANT})
		self.default = {kw.STATUS_TIME:5}

	@status_decorator
	def __call__(self, /, *, status_time):
		self.user.add_status(spell_status.FireEnhancement(status_time))

class LambOfTime(Spell):
	def __init__(self, user, /):
		Spell.__init__(self, user, 'Lamb of Time', {con.SPELL, con.UTILITY}, {con.RITUAL})
		self.default = {kw.DMG_AMOUNT:25, kw.DMG_TYPE:{con.SACRIFICE}, kw.STATUS_TIME:5}

	@status_decorator
	def __call__(self, /, *, dmg_amount, dmg_type, status_time):
		self.user.damage_health(dmg_amount, dmg_type)
		self.user.add_status(spell_status.LaminarTimeFlow(status_time))