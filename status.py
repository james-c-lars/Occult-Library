from functools import partial

from keywords import kw, con
import log



class Status():
	MISC_PRIORITY = 5000
	DAMAGE_PRIORITY = 1000
	MITIGATE_PRIORITY = 500
	ALTER_PRIORITY = 250
	HALT_PRIORITY = 100

	def __init__(self, name, time, priority, /, *, non_combat=False, **kwargs):
		self.target = None		# self.target should be set by entity.add_status
		self.name = name
		self.time = time
		self.priority = priority
		self.non_combat = non_combat
		self.effects = kwargs

	def __repr__(self, /):
		return f'<Status name:{self.name}, time:{self.time}, priority:{self.priority}, effects:{self.effects}>'
	def __str__(self, /):
		return self.name

	def __hash__(self, /):
		return hash(self.name)
	def __eq__(self, value, /):
		if not isinstance(value, Status):
			return False
		return self.name == value.name
	def __ne__(self, value, /):
		if not isinstance(value, Status):
			return True
		return self.name != value.name

	def affects(self, action, /):
		return action.name in self.effects

	def apply(self, action, /, *args, **kwargs):
		return self.effects[action.name](*args, **kwargs)

	def change_effect(self, kw_name, new_func, /):
		self.effects[kw_name] = partial(new_func, self)

	def tick(self ,/):
		self.time -= 1
		if self.time == 0:
			self.target.remove_status(self)
			log.combat_log(f'{self.name} ends')
		return (), {}



class FocusRebound(Status):
	def __init__(self, /):
		Status.__init__(self, 'Focus Rebound', 1, Status.HALT_PRIORITY)

	def affects(self, action, /):
		if action.name == kw.TICK:
			return True

		return con.BASE not in action.action_type

	def apply(self, action, /, *args, **kwargs):
		if action.name == kw.TICK:
			return self.tick(*args, **kwargs)

		kwargs[str(con.STOP)] = True
		log.combat_log(f"{self.target}'s {self.name} status prevents the action")

		return args, kwargs



# Vulnerability

class Vulnerability(Status):
	def __init__(self, name, dmg_type, time=-1, /):
		Status.__init__(self, name, time, Status.MITIGATE_PRIORITY, tick=self.tick, damage_health=self.damage_health)
		self.dmg_type = dmg_type

	def damage_health(self, dmg_amount, dmg_type, /):
		for dmg in self.dmg_type:
			if dmg in dmg_type:
				dmg_amount = dmg_amount * 2
				log.combat_log(f"{self.target}'s {self.name} status increases damage dealt!")

		return (dmg_amount, dmg_type), {}

class FocusVulnerability(Status):
	def __init__(self, name, f_dmg_type, time=-1, /):
		Status.__init__(self, name, time, Status.MITIGATE_PRIORITY, tick=self.tick, damage_focus=self.damage_focus)
		self.f_dmg_type = f_dmg_type

	def damage_focus(self, f_dmg_amount, f_dmg_type, /):
		for f_dmg in self.f_dmg_type:
			if f_dmg in f_dmg_type:
				f_dmg_amount = f_dmg_amount * 2
				log.combat_log(f"{self.target}'s {self.name} status increases focus damage dealt!")

		return (f_dmg_amount, f_dmg_type), {}



# Resistances

class Resistance(Status):
	def __init__(self, name, dmg_type, time=-1, /):
		Status.__init__(self, name, time, Status.MITIGATE_PRIORITY, tick=self.tick, damage_health=self.damage_health)
		self.dmg_type = dmg_type

	def damage_health(self, dmg_amount, dmg_type, /):
		for dmg in self.dmg_type:
			if dmg in dmg_type:
				dmg_amount = int(dmg_amount * 0.5)
				log.combat_log(f"{self.target}'s {self.name} status decreases damage dealt!")

		return (dmg_amount, dmg_type), {}

class FocusResistance(Status):
	def __init__(self, name, f_dmg_type, time=-1, /):
		Status.__init__(self, name, time, Status.MITIGATE_PRIORITY, tick=self.tick, damage_focus=self.damage_focus)
		self.f_dmg_type = f_dmg_type

	def damage_focus(self, f_dmg_amount, f_dmg_type, /):
		for f_dmg in self.f_dmg_type:
			if f_dmg in f_dmg_type:
				f_dmg_amount = int(f_dmg_amount * 0.5)
				log.combat_log(f"{self.target}'s {self.name} status decreases focus damage dealt!")

		return (f_dmg_amount, f_dmg_type), {}
