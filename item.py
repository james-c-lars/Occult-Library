from keywords import kw, con
from enum import Enum, auto
import item_actions
import item_status



class Slot(Enum):
	HEAD = auto()
	BODY = auto()
	LEGS = auto()
	ARMS = auto()
	CAPE = auto()
	NECK = auto()
	RING = auto()
	HAND = auto()

	def __repr__(self):
		return '<Slot.' +  self.name + '>'

class Item:
	def __init__(self, name, value, slot, actions, /):
		self.name = name
		self.value = value
		self.slot = slot
		self.actions = actions
		self.user = None

	def equip(self, user, /):
		if self.slot not in user.slots or user.slots[self.slot] != None:
			return False

		user.slots[self.slot] = self
		self.user = user

		for action in self.actions:
			user.add_action(action)
			action.user = user

		return True

	def dequip(self, /):
		for action in self.actions:
			self.user.actions[action].remove(self)
			if len(self.user.actions[action]) == 0:
				del self.user.actions[action]
			action.user = None

		self.user.slots[self.slot] = None
		self.user = None



class Sword(Item):
	def __init__(self, /):
		Item.__init__(self, 'Sword', 50, Slot.HAND, {item_actions.WeaponAction(self, 20, {con.SLASH}, name='Sword')})

class Mace(Item):
	def __init__(self, /):
		Item.__init__(self, 'Mace', 50, Slot.HAND, {item_actions.WeaponAction(self, 20, {con.SLASH}, name='Mace')})

class HolyWater(Item):
	def __init__(self, /):
		Item.__init__(self, 'Holy Water', 1000, None, {item_actions.Purify()})

class CursedSword(Item):
	def __init__(self, /):
		Item.__init__(self, 'Cursed Sword', 1000, Slot.HAND, {item_actions.CursedSlash()})

	def equip(self, user, /):
		if Item.equip(self, user):
			self.user.add_status(item_status.Cursed())
			return True

		return False

	def dequip(self, /):
		self.user.remove_status(item_status.Cursed())
		Item.dequip(self)