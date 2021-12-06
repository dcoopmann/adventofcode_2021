"""Lantern Fish simulation"""
import logging
import pytest

logger = logging.getLogger(__name__)

class LanternFish():
    def __init__(self, age):
        self.current_age = age
    
    def __repr__(self) -> str:
        return f"{self.current_age}"

    def spawn_offspring(self):
        return LanternFish(8)

    def pass_a_day(self):
        if self.current_age == 0:
            self.current_age=6
            
            b = self.spawn_offspring()
            logger.debug(f"new fish: {b} of type: {type(b)}")
            return b
        self.current_age -= 1
        
class FishSim():
    def __init__(self, start_ages, duration) -> None:
        self.population = self.populate(start_ages)
        self.duration = duration
    
    def populate(self, start_ages):
        population = []
        for age in start_ages:
            population.append(LanternFish(age))
        return population

    def run(self):
        for i in range(0, self.duration):
            tmp = []
            logger.info(f"Day {i}: Fishes total: {len(self.population)} Fishes: {self.population}")
            for fish in self.population:
                b = fish.pass_a_day()
                if type(b) == LanternFish:
                    tmp.append(b)
            logger.debug(len(tmp))
            if len(tmp) >0:
                self.population += tmp

    def number_of_fish(self):
        return len(self.population)

@pytest.mark.parametrize("duration, exp_population",[(80,5934), (256,26984457539)])
def test_FishSim(duration, exp_population):
    sim = FishSim([3,4,3,1,2,], duration)
    sim.run()
    assert sim.number_of_fish() == exp_population

if __name__ == "__main__":
    puzzle_input =[5,4,3,5,1,1,2,1,2,1,3,2,3,4,5,1,2,4,3,2,5,1,4,2,1,1,2,5,4,4,4,1,5,4,5,2,1,2,5,5,4,1,3,1,4,2,4,2,5,1,3,5,3,2,3,1,1,4,5,2,4,3,1,5,5,1,3,1,3,2,2,4,1,3,4,3,3,4,1,3,4,3,4,5,2,1,1,1,4,5,5,1,1,3,2,4,1,2,2,2,4,1,2,5,5,1,4,5,2,4,2,1,5,4,1,3,4,1,2,3,1,5,1,3,4,5,4,1,4,3,3,3,5,5,1,1,5,1,5,5,1,5,2,1,5,1,2,3,5,5,1,3,3,1,5,3,4,3,4,3,2,5,2,1,2,5,1,1,1,1,5,1,1,4,3,3,5,1,1,1,4,4,1,3,3,5,5,4,3,2,1,2,2,3,4,1,5,4,3,1,1,5,1,4,2,3,2,2,3,4,1,3,4,1,4,3,4,3,1,3,3,1,1,4,1,1,1,4,5,3,1,1,2,5,2,5,1,5,3,3,1,3,5,5,1,5,4,3,1,5,1,1,5,5,1,1,2,5,5,5,1,1,3,2,2,3,4,5,5,2,5,4,2,1,5,1,4,4,5,4,4,1,2,1,1,2,3,5,5,1,3,1,4,2,3,3,1,4,1,1]
    # logging.basicConfig(level="INFO")
    sim = FishSim(puzzle_input, 80)
    sim.run()
    print(sim.number_of_fish())
    