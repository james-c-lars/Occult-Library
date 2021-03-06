from keywords import kw, con
from actions import Action, status_decorator
import log
import item_status



class WeaponAction(Action):
	def __init__(self, dmg_amount, dmg_type, /, *, name='Weapon Attack'):
		Action.__init__(self, None, name, {con.PHYSICAL, con.ATTACK, con.ITEM}, targeted=True)
		self.default = {kw.DMG_AMOUNT:dmg_amount, kw.DMG_TYPE:dmg_type}

	@status_decorator
	def __call__(self, target, /, *, dmg_amount, dmg_type):
		log.combat_log(f'{self.user} attacks {target} using {self.name}')
		target.damage_health(dmg_amount, dmg_type)

# A separate class so that the name field is consistent for item_status.Cursed
class CursedSlash(WeaponAction):
	def __init__(self, /):
		WeaponAction.__init__(self, 40, {con.SLASH}, name='Cursed Slash')



class Purify(Action):
	def __init__(self, /):
		Action.__init__(self, None, 'Purify', {con.PHYSICAL, con.UTILITY, con.ITEM}, targeted=True)

	@status_decorator
	def __call__(self, target, /):
		log.combat_log(f'{self.user} Purifies {target}')
		target.statuses.clear()