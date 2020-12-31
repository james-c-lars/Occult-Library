import entity
import combat

# entity.Mummy(), entity.Automaton(), entity.Siren(), entity.Gargoyle(), entity.Bogeyman()

battle = combat.Battle([entity.Mummy(), entity.Automaton(), entity.Siren(), entity.Gargoyle(), entity.Bogeyman()])
battle.begin()