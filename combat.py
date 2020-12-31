from random import randint
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