from keywords import kw, con
from status import Status
import combat_actions
import spell
import log



# Mummy

class Entangled(Status):
	def __init__(self, time=-1, /):
		Status.__init__(self, 'Entangled', time, Status.HALT_PRIORITY)

	def affects(self, action, /):
		if action.name == kw.TICK:
			return True

		if con.SPELL in action.action_type and con.GESTURE in action.casting_reqs:
			return True
		return con.PHYSICAL in action.action_type

	def apply(self, action, /, *args, **kwargs):
		if action.name == kw.TICK:
			return self.tick(*args, **kwargs)

		kwargs[str(con.STOP)] = True
		log.combat_log(f"{self.target}'s {self.name} status prevents the action")

		return args, kwargs

	def tick(self, /):
		self.target.damage_focus(10, {con.PANIC})
		return Status.tick(self)

class Infected(Status):
	def __init__(self, time=-1, /):
		Status.__init__(self, 'Infected', time, Status.DAMAGE_PRIORITY, tick=self.tick)

	def tick(self, /):
		log.combat_log(f"{self.target}'s {self.name} status damages them")
		self.target.damage_health(5, {con.DISEASE})

		return Status.tick(self)

# Automaton

class Rewinding(Status):
	def __init__(self, time=-1, /):
		Status.__init__(self, 'Rewinding', time, Status.HALT_PRIORITY)

	def affects(self, action, /):
		if action.name == kw.TICK:
			return True

		return con.MECHANICAL in action.action_type

	def apply(self, action, /, *args, **kwargs):
		if action.name == kw.TICK:
			return self.tick(*args, **kwargs)

		kwargs[str(con.STOP)] = True
		log.combat_log(f"{self.target}'s {self.name} status prevents the action")

		return args, kwargs

# Siren

class Singing(Status):
	def __init__(self, afflicted, /):
		Status.__init__(self, 'Singing', -1, Status.ALTER_PRIORITY, tick=self.tick, damage_focus=self.damage_focus)
		self.afflicted = afflicted
		self.counter = 0

	def tick(self, /):
		self.counter += 1
		if self.counter > 2:
			log.combat_log(f"{self.target}'s {self.name} enchants {self.afflicted}")
			self.afflicted.add_status(Enchanted(3))
			self.target.remove_status(self)
		else:
			log.combat_log(f'{self.target} continues their song')

		return Status.tick(self)

	def damage_focus(self, f_dmg_amount, f_dmg_type, /):
		if f_dmg_amount > 20:
			log.combat_log(f'{self.target} loses focus and stops {self.name}')
			self.target.remove_status(self)

		return (f_dmg_amount, f_dmg_type), {}

class Enchanted(Status):
	def __init__(self, time=-1, /):
		Status.__init__(self, 'Enchanted', time, Status.HALT_PRIORITY)

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

class Flying(Status):
	def __init__(self, time=-1, /):
		Status.__init__(self, 'Flying', time, Status.MITIGATE_PRIORITY, tick=self.tick, damage_health=self.damage_health, damage_focus=self.damage_focus)

	def damage_health(self, dmg_amount, dmg_type, /):
		log.combat_log(f'The attack only grazes {self.target}')
		dmg_amount = int(dmg_amount * 0.5)

		return (dmg_amount, dmg_type), {}

	def damage_focus(self, f_dmg_amount, f_dmg_type, /):
		if f_dmg_amount > 20:
			log.combat_log(f'{self.target} loses focus and tumbles to the ground')
			self.target.remove_status(self)

		return (f_dmg_amount, f_dmg_type), {}

	def tick(self, /):
		return Status.tick(self)

# Gargoyle

class Lifting(Status):
	def __init__(self, time=-1, /):
		Status.__init__(self, 'Lifting', 1, Status.HALT_PRIORITY)
		self.flying_time = time

	def affects(self, action, /):
		if action.name == kw.TICK:
			return True

		return con.BASE not in action.action_type

	def apply(self, action, /, *args, **kwargs):
		if action.name == kw.TICK:
			return self.tick(*args, **kwargs)

		kwargs[str(con.STOP)] = True
		log.combat_log(f'{self.target} is in the middle of {self.name} off the ground')

		return args, kwargs

	def tick(self, /):
		Status.tick(self)

		if self.time == 0:
			log.combat_log(f'{self.target} is now Flying in the air')

			flying = Flying(self.flying_time)
			flying.change_effect(kw.TICK, Lifting.flying_tick)
			flying.change_effect(kw.DAMAGE_FOCUS, Lifting.flying_damage_focus)
			self.target.add_status(flying)

			self.target.add_action(combat_actions.Plummet(self.target), self)

		return (), {}

	def flying_tick(self, /):
		args, kwargs = self.tick()

		if self.time == 0:
			if combat_actions.Plummet(None) in self.target.actions:
				self.target.remove_action(combat_actions.Plummet(None), Lifting())

		return args, kwargs

	def flying_damage_focus(self, f_dmg_amount, f_dmg_type, /):
		args, kwargs = self.damage_focus(f_dmg_amount, f_dmg_type)

		if f_dmg_amount > 20:
			if combat_actions.Plummet(None) in self.target.actions:
				self.target.remove_action(combat_actions.Plummet(None), Lifting())

		return args, kwargs

class Plummeting(Status):
	def __init__(self, targeted, dmg_amount, dmg_type, /):
		Status.__init__(self, 'Plummeting', 2, Status.HALT_PRIORITY)
		self.targeted = targeted
		self.dmg_amount = dmg_amount
		self.dmg_type = dmg_type

	def affects(self, action, /):
		if action.name == kw.TICK:
			return True

		return con.BASE not in action.action_type

	def apply(self, action, /, *args, **kwargs):
		if action.name == kw.TICK:
			return self.tick(*args, **kwargs)

		kwargs[str(con.STOP)] = True
		log.combat_log(f'{self.target} is in the middle of {self.name} to the ground')

		return args, kwargs

	def tick(self, /):
		Status.tick(self)

		if self.time == 0 and Flying() not in self.targeted.statuses:
			log.combat_log(f'{self.target} lands! Devastating {self.targeted}')
			self.targeted.damage_health(self.dmg_amount, self.dmg_type)

		return (), {}

# Bogeyman

class OnEdge(Status):
	def __init__(self, /):
		Status.__init__(self, 'On Edge', -1, Status.MISC_PRIORITY, damage_focus=self.damage_focus)
		self.counter = 1

	def damage_focus(self, f_dmg_amount, f_dmg_type, /):
		self.counter += 1
		log.combat_log(f"{self.target}'s nerves build")

		if f_dmg_amount > 30:
			log.combat_log(f'It overcomes them, and they take damage!')
			self.target.damage_health(int(f_dmg_amount * 0.3), {con.WOUND})

		return (f_dmg_amount, f_dmg_type), {}


class Stalking(Status):
	def __init__(self, targeted, /):
		Status.__init__(self, 'Stalking', -1, Status.MISC_PRIORITY)
		self.targeted = targeted

		self.on_edge = OnEdge()
		self.targeted.add_status(self.on_edge)

	def get_counter(self, /):
		if self.on_edge in self.targeted.statuses:
			return self.on_edge.counter
		return 1

	def affects(self, action, /):
		return con.ATTACK in action.action_type

	def apply(self, action, /, *args, **kwargs):
		if action == combat_actions.Terrorize(None):
			return self.terrorize(*args, **kwargs)

		if len(args) > 0 and args[0] == self.targeted:
			log.combat_log(f"{self.target} feeds off of {self.targeted}'s terror")
			self.target.gain_health(5 * self.get_counter(), {con.SIPHON})
			self.target.gain_focus(5 * self.get_counter(), {con.GLEE})

		return args, kwargs

	def terrorize(self, target, /, *, f_dmg_amount, f_dmg_type):
		if target == self.targeted:
			log.combat_log(f"{self.targeted}'s nerves spike!")
			f_dmg_amount *= self.get_counter()

		return (target, ), {kw.F_DMG_AMOUNT:f_dmg_amount, kw.F_DMG_TYPE:f_dmg_type}

class Bleeding(Status):
	def __init__(self, time=-1, /):
		Status.__init__(self, 'Bleeding', time, Status.DAMAGE_PRIORITY, tick=self.tick, damage_focus=self.damage_focus)

	def tick(self, /):
		log.combat_log(f'%s is %s' % (self.target, self.name))
		self.target.damage_health(5, {con.WOUND})
		return Status.tick(self)

	def damage_focus(self, f_dmg_amount, f_dmg_type, /):
		log.combat_log(f"{self.target}'s {self.name} makes it easier for them to lose focus")
		f_dmg_amount += 5
		return (f_dmg_amount, f_dmg_type), {}