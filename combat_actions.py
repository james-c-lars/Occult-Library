from keywords import kw, con
from actions import Action, status_decorator
import status
import entity_status
import log



class TailCoil(Action):
	def __init__(self, user, /):
		Action.__init__(self, user, 'Tail Coil', {con.PHYSICAL, con.ATTACK, con.CONTROL, con.NATURAL}, targeted=True)
		self.default = {kw.DMG_AMOUNT:5, kw.DMG_TYPE:{con.CRUSH}, kw.STATUS_TIME:1}

	@status_decorator
	def __call__(self, target, /, *, dmg_amount, dmg_type, status_time):
		log.combat_log(f'{self.user} damages {target} and Entangles them with {self.name}')
		target.damage_health(dmg_amount, dmg_type)
		target.add_status(entity_status.Entangled(status_time))

# Mummy

class MummyWrap(Action):
	def __init__(self, user, /):
		Action.__init__(self, user, 'Mummy Wrap', {con.PHYSICAL, con.ATTACK, con.CONTROL}, targeted=True)
		self.default = {kw.F_DMG_AMOUNT:5, kw.F_DMG_TYPE:{con.PANIC}, kw.STATUS_TIME:1}

	@status_decorator
	def __call__(self, target, /, *, f_dmg_amount, f_dmg_type, status_time):
		log.combat_log(f"{self.user} damages {target}'s focus and Entangles them with {self.name}")
		target.damage_focus(f_dmg_amount, f_dmg_type)
		target.add_status(entity_status.Entangled(status_time))

		if entity_status.Infected() in target.statuses:
			log.combat_log(f"It furthers {target}'s Infection")
			target.add_status(entity_status.Infected(status_time))

class Grasp(Action):
	def __init__(self, user, /):
		Action.__init__(self, user, 'Grasp', {con.PHYSICAL, con.ATTACK, con.NATURAL}, targeted=True)
		self.default = {kw.DMG_AMOUNT:10, kw.DMG_TYPE:{con.CRUSH}, kw.F_DMG_AMOUNT:20, kw.F_DMG_TYPE:{con.PANIC}}

	@status_decorator
	def __call__(self, target, /, *, dmg_amount, dmg_type, f_dmg_amount, f_dmg_type):
		if entity_status.Entangled() in target.statuses:
			log.combat_log(f"Being Entangled means {target} can't escape {self.user}'s {self.name}")
			dmg_amount *= 2
			target.damage_focus(f_dmg_amount, f_dmg_type)
		else:
			log.combat_log(f"{self.user}'s {self.name} crushes {target}")

		target.damage_health(dmg_amount, dmg_type)

class PlagueBreath(Action):
	def __init__(self, user, /):
		Action.__init__(self, user, 'Plague Breath', {con.ATTACK, con.NATURAL}, targeted=True)
		self.default = {kw.STATUS_TIME:5}

	@status_decorator
	def __call__(self, target, /, *, status_time):
		log.combat_log(f"{self.user}'s {self.name} Infects {target}")
		target.add_status(entity_status.Infected(status_time))

# Automaton

class ClockworkPunch(Action):
	def __init__(self, user, /):
		Action.__init__(self, user, 'Clockwork Punch', {con.PHYSICAL, con.ATTACK, con.MECHANICAL}, targeted=True)
		self.default = {kw.DMG_AMOUNT:25, kw.DMG_TYPE:{con.CRUSH}, kw.STATUS_TIME:2}

	@status_decorator
	def __call__(self, target, /, *, dmg_amount, dmg_type, status_time):
		log.combat_log(f'{self.user} strikes {target} with {self.name} and begins to Rewind')
		target.damage_health(dmg_amount, dmg_type)
		self.user.add_status(entity_status.Rewinding(status_time))

class ClockworkRepair(Action):
	def __init__(self, user, /):
		Action.__init__(self, user, 'Clockwork Repair', {con.UTILITY, con.HEAL, con.MECHANICAL})
		self.default = {kw.GAIN_AMOUNT:25, kw.GAIN_TYPE:{con.REPAIR}, kw.STATUS_TIME:2}

	@status_decorator
	def __call__(self, /, *, gain_amount, gain_type, status_time):
		log.combat_log(f'{self.user} uses {self.name} and begins to Rewind')
		self.user.gain_health(gain_amount, gain_type)
		self.user.add_status(entity_status.Rewinding(status_time))

# Siren

class Claw(Action):
	def __init__(self, user, /):
		Action.__init__(self, user, 'Claw', {con.PHYSICAL, con.ATTACK, con.NATURAL}, targeted=True)
		self.default = {kw.DMG_AMOUNT:10, kw.DMG_TYPE:{con.SLASH}}

	@status_decorator
	def __call__(self, target, /, *, dmg_amount, dmg_type):
		if entity_status.Enchanted() in target.statuses:
			log.combat_log(f'{self.user} frantically {self.name}s the helpless {target}')
			dmg_amount *= 3
		else:
			log.combat_log(f'{self.user} {self.name}s {target}')

		target.damage_health(dmg_amount, dmg_type)

class Fly(Action):
	def __init__(self, user, /):
		Action.__init__(self, user, 'Fly', {con.PHYSICAL, con.UTILITY, con.NATURAL})
		self.default = {kw.STATUS_TIME:3}

	@status_decorator
	def __call__(self, /, *, status_time):
		log.combat_log(f'{self.user} begins to {self.name}')
		self.user.add_status(entity_status.Flying(status_time))

class BeginSong(Action):
	def __init__(self, user, /):
		Action.__init__(self, user, 'Begin Song', {con.PHYSICAL, con.UTILITY, con.NATURAL}, targeted=True)

	@status_decorator
	def __call__(self, target, /):
		log.combat_log(f'{self.user} begins to Sing to {target}')
		self.user.add_status(entity_status.Singing(target))

# Gargoyle

class TakeFlight(Action):
	def __init__(self, user, /):
		Action.__init__(self, user, 'Take Flight', {con.PHYSICAL, con.UTILITY})
		self.default = {kw.STATUS_TIME:3}

	@status_decorator
	def __call__(self, /, *, status_time):
		if entity_status.Flying() not in self.user.statuses:
			log.combat_log(f'{self.user} struggles to lift off the ground')
			self.user.add_status(entity_status.Lifting(status_time))
		else:
			log.combat_log(f'{self.user} renews their Flying')
			self.user.add_status(entity_status.Flying(status_time))

class Plummet(Action):
	def __init__(self, user, /):
		Action.__init__(self, user, 'Plummet', {con.PHYSICAL, con.ATTACK, con.NATURAL}, targeted=True)
		self.default = {kw.DMG_AMOUNT:50, kw.DMG_TYPE:{con.CRUSH}, kw.F_DMG_AMOUNT:50, kw.F_DMG_TYPE:{con.TERROR}}

	@status_decorator
	def __call__(self, target, /, *, dmg_amount, dmg_type, f_dmg_amount, f_dmg_type):
		log.combat_log(f'{self.user} begins to {self.name} towards {target}, terrifying them!')
		self.user.add_status(entity_status.Plummeting(target, dmg_amount, dmg_type))
		target.damage_focus(f_dmg_amount, f_dmg_type)
		self.user.remove_status(entity_status.Flying())
		self.user.remove_action(self, entity_status.Lifting())

class Pounce(Action):
	def __init__(self, user, /):
		Action.__init__(self, user, 'Pounce', {con.PHYSICAL, con.ATTACK, con.NATURAL}, targeted=True)
		self.default = {kw.DMG_AMOUNT:20, kw.DMG_TYPE:{con.CRUSH}, kw.F_DMG_AMOUNT:10, kw.F_DMG_TYPE:{con.TERROR}}

	@status_decorator
	def __call__(self, target, /, *, dmg_amount, dmg_type, f_dmg_amount, f_dmg_type):
		log.combat_log(f'{self.user} {self.name}s at {target}, terrifying them')
		target.damage_health(dmg_amount, dmg_type)
		target.damage_focus(f_dmg_amount, f_dmg_type)

# Bogeyman

class Terrorize(Action):
	def __init__(self, user, /):
		Action.__init__(self, user, 'Terrorize', {con.ATTACK, con.MENTAL}, targeted=True)
		self.default = {kw.F_DMG_AMOUNT:10, kw.F_DMG_TYPE:{con.TERROR}}

	@status_decorator
	def __call__(self, target, /, *, f_dmg_amount, f_dmg_type):
		log.combat_log(f'{self.user} {self.name}s {target}')
		target.damage_focus(f_dmg_amount, f_dmg_type)

class Slice(Action):
	def __init__(self, user, /):
		Action.__init__(self, user, 'Slice', {con.PHYSICAL, con.ATTACK, con.NATURAL}, targeted=True)
		self.default = {kw.DMG_AMOUNT:10, kw.DMG_TYPE:{con.SLASH, con.WOUND}, kw.STATUS_TIME:5}

	@status_decorator
	def __call__(self, target, /, *, dmg_amount, dmg_type, status_time):
		log.combat_log(f'{self.user} {self.name}s {target}, drawing blood')
		target.damage_health(dmg_amount, dmg_type)
		target.add_status(entity_status.Bleeding(status_time))

class Stalk(Action):
	def __init__(self, user, /):
		Action.__init__(self, user, 'Stalk', {con.MENTAL, con.UTILITY}, targeted=True)

	@status_decorator
	def __call__(self, target, /):
		log.combat_log(f'{self.user} begins {self.name}ing {target}, putting them On Edge')
		self.user.add_status(entity_status.Stalking(target))

		self.user.remove_action(self, self.user)