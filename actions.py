from keywords import kw, con
import status
import log



# This decorator used to do the status logic
def status_decorator(action_call, /):
	def status_altered_call(self, /, *args, **kwargs):
		for key in self.default:
			if key not in kwargs:
				kwargs[key] = self.default[key]

		args, kwargs = self.user.apply_statuses(self, *args, **kwargs)
		
		if str(con.STOP) not in kwargs:
			action_call(self, *args, **kwargs)

	return status_altered_call



class Action:
	def __init__(self, user, name, action_type, /, *, targeted=False):
		self.user = user
		self.name = name
		self.action_type = action_type
		self.targeted = targeted
		self.default = {}

	def __repr__(self, /):
		return f'<Action name:{self.name}, user:{self.user.name}, action_type:{self.action_type}>'
	def __str__(self, /):
		return self.name

	def __hash__(self, /):
		return hash(self.name)
	def __eq__(self, value, /):
		if not isinstance(value, Action):
			return False
		return self.name == value.name
	def __ne__(self, value, /):
		if not isinstance(value, Action):
			return True
		return self.name != value.name



# Base actions

class Tick(Action):
	def __init__(self, user, /):
		Action.__init__(self, user, kw.TICK, {con.BASE})

	@status_decorator
	def __call__(self, /):
		pass

class DamageHealth(Action):
	def __init__(self, user, /):
		Action.__init__(self, user, kw.DAMAGE_HEALTH, {con.BASE})

	@status_decorator
	def __call__(self, dmg_amount, dmg_type, /):
		log.combat_log(f'{self.user} takes {dmg_amount} {con.multi_str(dmg_type)} damage!')
		self.user.health -= dmg_amount

class DamageFocus(Action):
	def __init__(self, user, /):
		Action.__init__(self, user, kw.DAMAGE_FOCUS, {con.BASE})

	@status_decorator
	def __call__(self, f_dmg_amount, f_dmg_type, /):
		log.combat_log(f'{self.user} takes {f_dmg_amount} {con.multi_str(f_dmg_type)} focus damage!')
		self.user.focus -= f_dmg_amount

		if self.user.focus < 0:
			log.combat_log(f'The mental instability damages {self.user}')
			self.user.damage_health(-self.user.focus, {con.WOUND})
			self.user.focus = 25
			self.user.add_status(status.FocusRebound())

class GainHealth(Action):
	def __init__(self, user, /):
		Action.__init__(self, user, kw.GAIN_HEALTH, {con.BASE})

	@status_decorator
	def __call__(self, gain_amount, gain_type, /):
		log.combat_log(f'{self.user} gains {gain_amount} {con.multi_str(gain_type)} health!')
		self.user.health += gain_amount

class GainFocus(Action):
	def __init__(self, user, /):
		Action.__init__(self, user, kw.GAIN_FOCUS, {con.BASE})

	@status_decorator
	def __call__(self, f_gain_amount, f_gain_type, /):
		log.combat_log(f'{self.user} gains {f_gain_amount} {con.multi_str(f_gain_type)} focus!')
		self.user.focus += f_gain_amount
