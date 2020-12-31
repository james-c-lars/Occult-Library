from keywords import kw, con
from status import Status



class Aflame(Status):
	def __init__(self, time=-1, /):
		Status.__init__(self, 'Aflame', time, Status.DAMAGE_PRIORITY, tick=self.tick)

	def tick(self, /):
		self.target.damage_health(5, {con.FIRE})
		self.target.damage_focus(10, {con.PANIC})

		return Status.tick(self)

class FireEnhancement(Status):
	def __init__(self, time=-1, /):
		Status.__init__(self, 'Fire Enhancement', time, Status.DAMAGE_PRIORITY)

	def affects(self, action, /):
		if action.name == kw.TICK:
			return True

		return con.ATTACK in action.action_type

	def apply(self, action, /, *args, **kwargs):
		if action.name == kw.TICK:
			return self.tick(*args, **kwargs)

		return self.fire_attack(*args, **kwargs)

	def fire_attack(self, /, *args, **kwargs):
		if con.FIRE in kwargs[kw.DMG_TYPE]:
			kwargs[kw.DMG_AMOUNT] = int(kwargs[kw.DMG_AMOUNT] * 1.5)
		return args, kwargs

class LaminarTimeFlow(Status):
	def __init__(self, time=-1, /):
		Status.__init__(self, 'Laminar Time Flow', time, Status.MISC_PRIORITY, tick=self.tick)

	def tick(self, /):
		for status in self.target.statuses:
			if status != self and kw.TICK in status.effects:
				status.time += 1

		return Status.tick(self)