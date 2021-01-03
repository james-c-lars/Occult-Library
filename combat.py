from random import randint
from functools import partial
import log



class Fight_AI:
	def __init__(self, priorities, /):
		self.priorities = priorities

	def act(self, entities, /):
		target = self.choose_target(entities)

		total = 0
		for action in self.actions:
			total += self.priorities.get(action, 1)

		selection = randint(0, total-1)
		for action in self.actions:
			selection -= self.priorities.get(action, 1)
			if selection < 0:
				chosen_action = action
				break

		if chosen_action.targeted:
			chosen_action(target)
			log.combat_log(f'{target.name} - health:{target.health}, focus:{target.focus}')
			return target

		else:
			chosen_action()
			log.combat_log(f'{self.name} - health:{self.health}, focus:{self.focus}')
			return False

	def choose_target(self, entities, /):
		target = self
		while target == self:
			target = entities[randint(0, len(entities)-1)]
		return target



class Player:
	def make_player(entity, name='Player', /):
		entity.act = partial(Player.act, entity)
		entity.prompt_action = partial(Player.prompt_action, entity)
		entity.prompt_target = partial(Player.prompt_target, entity)
		entity.name = f'{name} ({entity.name})'
		return entity

	def act(self, entities, /):
		action = self.prompt_action()

		if action.targeted:
			target = self.prompt_target(entities)
			action(target)
			return target

		else:
			action()
			return False

	def prompt_action(self, /):
		for i, action in enumerate(self.actions):
			log.combat_log(f'{i} - {action.name}')

		choice = None
		while choice == None:
			try:
				choice = self.actions[int(input('Enter your choice: '))]
			except ValueError:
				print('Not a number')
			except IndexError:
				print('Not a valid number')

		return choice

	def prompt_target(self, entities, /):
		for i, entity in enumerate(entities):
			log.combat_log(f'{i} - {entity.name}, health={entity.health}, focus={entity.focus}')

		choice = None
		while choice == None:
			try:
				choice = entities[int(input('Enter your choice: '))]
			except ValueError:
				print('Not a number')
			except IndexError:
				print('Not a valid number')

		return choice





class Battle:
	def __init__(self, entities, /):
		self.entities = entities

	def begin(self):
		while len(self.entities) > 1:
			for entity in self.entities:

				log.combat_log(f'{entity.name} - health:{entity.health}, focus:{entity.focus}')

				target = entity.act(self.entities)

				if target and target.health <= 0:
					self.entities.remove(target)
					log.combat_log(f'\n{target} is defeated!\n')

				entity.tick()

				if entity.health <= 0:
					self.entities.remove(entity)
					log.combat_log(f'\n{entity} is defeated!\n')

				log.combat_log('')