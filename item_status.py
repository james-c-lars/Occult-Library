from keywords import kw, con
from status import Status
import item_actions



class Cursed(Status):
	def __init__(self, time=-1, /):
		Status.__init__(self, 'Cursed', time, Status.DAMAGE_PRIORITY, non_combat=True, tick=self.tick)
		self.effects[item_actions.CursedSlash().name] = self.cursed_slash

	def cursed_slash(self, target, /, *, dmg_amount, dmg_type):
		self.user.damage_health(int(dmg_amount * 0.25), {con.SACRIFICE})

		return (target), {kw.DMG_AMOUNT:dmg_amount, kw.DMG_TYPE:dmg_type}