from keywords import kw, con
from combat import Fight_AI
import actions as acts
import combat_actions
import item
import status
import entity_status



class Entity():
	def __init__(self, name, /, *, health=100, focus=100, action_map={}, statuses=[], slots={}):
		self.name = name
		self.health = health
		self.focus = focus

		self.action_map = action_map
		self.actions = [action for action in action_map]
		self.slots = slots

		self.statuses = []
		for status in statuses:
			self.add_status(status)

		# Base actions
		self.tick = acts.Tick(self)
		self.damage_health = acts.DamageHealth(self)
		self.damage_focus = acts.DamageFocus(self)
		self.gain_health = acts.GainHealth(self)
		self.gain_focus = acts.GainFocus(self)

	def __repr__(self, /):
		return f'<Entity name:{self.name}, health:{self.health}, focus:{self.focus}>'
	def __str__(self, /):
		return self.name

	# Status logic

	def add_status(self, status, /):
		if status not in self.statuses:
			status.target = self
			self.statuses.append(status)
			self.statuses = sorted(self.statuses, key=lambda k: k.priority)
		else:
			old_status = self.statuses[self.statuses.index(status)]
			old_status.time = max(old_status.time, status.time)

	def remove_status(self, status, /):
		self.statuses.remove(status)

	def apply_statuses(self, action, /, *args, **kwargs):
		for status in self.statuses:
			if status.affects(action) and str(con.STOP) not in kwargs:
				args, kwargs = status.apply(action, *args, **kwargs)
		return args, kwargs

	# Action logic

	def add_action(self, action, source, /):
		if action not in self.action_map:
			self.action_map[action] = {source}
			self.actions.append(action)
		else:
			self.action_map[action].add(source)

	def remove_action(self, action, source, /):
		self.action_map[action].remove(source)
		if len(self.action_map[action]) == 0:
			del self.action_map[action]
			self.actions.remove(action)



class Mummy(Entity, Fight_AI):
	def __init__(self):
		Entity.__init__(self, 'Mummy', health=150, focus=50, \
			action_map={combat_actions.MummyWrap(self):{self}, combat_actions.Grasp(self):{self}, combat_actions.PlagueBreath(self):{self}}, \
			statuses=[status.Vulnerability('Flammable', {con.FIRE}), status.Vulnerability('Crumbling', {con.CRUSH}), status.Resistance('Embalmed', {con.DISEASE, con.WOUND})], \
			slots={slot:None for slot in item.Slot} \
			)

		Fight_AI.__init__(self, {combat_actions.Grasp(None):2})

class Automaton(Entity, Fight_AI):
	def __init__(self):
		Entity.__init__(self, 'Automaton', health=200, focus=1, \
			action_map={combat_actions.ClockworkPunch(self):{self}, combat_actions.ClockworkRepair(self):{self}}, \
			statuses=[status.Resistance('Mechanical', {con.MAGIC, con.DISEASE, con.WOUND}), status.Resistance('Metal', {con.SLASH})], \
			slots={slot:None for slot in item.Slot} \
			)

		self.damage_focus = lambda *args, **kwargs: None
		self.gain_focus = self.damage_focus

		Fight_AI.__init__(self, {combat_actions.ClockworkPunch(None):2})

class Siren(Entity, Fight_AI):
	def __init__(self):
		Entity.__init__(self, 'Siren', health=75, focus=50, \
			action_map={combat_actions.Claw(self):{self}, combat_actions.Fly(self):{self}, combat_actions.BeginSong(self):{self}}, \
			statuses=[status.Vulnerability('Hollow Bones', {con.CRUSH}), status.FocusVulnerability('Flighty', {con.PANIC})], \
			slots={item.Slot.HEAD:None, item.Slot.NECK:None, item.Slot.BODY:None} \
			)

		Fight_AI.__init__(self, {})

	def act(self, entities, /):
		target = Fight_AI.choose_target(self, entities)

		if entity_status.Enchanted() in target.statuses:
			self.priorities[combat_actions.Claw(None)] = 100
			self.priorities[combat_actions.BeginSong(None)] = 0
			self.priorities[combat_actions.Fly(None)] = 0

		elif entity_status.Singing(None) not in self.statuses:
			self.priorities[combat_actions.BeginSong(None)] = 100
			self.priorities[combat_actions.Claw(None)] = 0
			self.priorities[combat_actions.Fly(None)] = 0

		elif entity_status.Flying() not in self.statuses:
			self.priorities[combat_actions.Fly(None)] = 100
			self.priorities[combat_actions.Claw(None)] = 0
			self.priorities[combat_actions.BeginSong(None)] = 0

		else:
			self.priorities[combat_actions.Claw(None)] = 1
			self.priorities[combat_actions.BeginSong(None)] = 0
			self.priorities[combat_actions.Fly(None)] = 0
		
		Fight_AI.act(self, [target])

class Gargoyle(Entity, Fight_AI):
	def __init__(self):
		Entity.__init__(self, 'Gargoyle', health=200, focus=100, \
			action_map={combat_actions.TakeFlight(self):{self}, combat_actions.Pounce(self):{self}}, \
			statuses=[status.Resistance('Stone', {con.SLASH, con.DISEASE, con.WOUND}), status.Vulnerability('Brittle', {con.CRUSH, con.FIRE}), status.FocusResistance('Indomitable', {con.PANIC, con.TERROR, con.PAIN})], \
			slots={item.Slot.HEAD:None, item.Slot.NECK:None, item.Slot.BODY:None, item.Slot.ARMS:None, item.Slot.HAND:None, item.Slot.RING:None}  \
			)

		# Plummet action given by the Lifting status
		Fight_AI.__init__(self, {combat_actions.Plummet(None):100, combat_actions.Pounce(None):2})

	def act(self, target, /):
		if entity_status.Flying() in self.statuses:
			self.priorities[combat_actions.TakeFlight(None)] = 0
		else:
			self.priorities[combat_actions.TakeFlight(None)] = 1

		Fight_AI.act(self, target)

class Bogeyman(Entity, Fight_AI):
	def __init__(self):
		Entity.__init__(self, 'Bogeyman', health=100, focus=100, \
			action_map={combat_actions.Terrorize(self):{self}, combat_actions.Slice(self):{self}, combat_actions.Stalk(self):{self}}, \
			statuses=[status.Resistance('Twisted', {con.WOUND}), status.FocusResistance('Psychopathic', {con.TERROR})], \
			slots={slot:None for slot in item.Slot} \
			)

		Fight_AI.__init__(self, {combat_actions.Stalk(None):100})