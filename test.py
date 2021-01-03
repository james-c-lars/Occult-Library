import entity
import combat
import item

#entity.Mummy(), entity.Automaton(), entity.Siren(), entity.Gargoyle(), entity.Bogeyman()

monsters = [combat.Player.make_player(entity.Bogeyman()), entity.Mummy(), entity.Automaton(), entity.Siren(), entity.Gargoyle()]

battle = combat.Battle(monsters)
battle.begin()

