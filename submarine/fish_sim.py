"""Lantern Fish simulation"""
import logging
import pytest

import numpy as np

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



def sim_v2(start_pop, duration):
    puzzle_input = start_pop
    for i in range(0, duration):
        puzzle_input += [7 for x in puzzle_input if x == 0] # reset countdown for old fishprint(puzzle_input)
        puzzle_input += [9 for x in puzzle_input if x == 0] # spawn new fish
        puzzle_input = [x for x in puzzle_input if x>0] # cleanup
        
        # logger.debug(f"Pos 1: {puzzle_input}")
        puzzle_input = [x-1 for x in puzzle_input] # step day forward

        
        logger.debug(f"After Day {i}: {puzzle_input}")

    return len(puzzle_input)    



def sim_v3(start_pop, duration):
    puzzle_input = np.array(start_pop, np.uint8)
    for i in range(0, duration):
            spawn_fish_number = np.sum(puzzle_input == 0)  # count fish that need to be spawned
            puzzle_input[puzzle_input == 0] = 7  # reset countdown for old fishprint(puzzle_input)
            spawn_fish_array = np.full(shape=spawn_fish_number, fill_value=9)  # spawn new fish in another array
            puzzle_input = np.append(puzzle_input, spawn_fish_array)  # merge old and new fish population

            puzzle_input = puzzle_input - 1  # step day forward

            logger.debug(f"After Day {i}: {puzzle_input}")

    return len(puzzle_input)

def sim_v5(start_pop, duration):
    puzzle_input = np.bincount(start_pop, minlength=9)  # count fish states of start population
    for i in range(0, duration):
        puzzle_input = np.roll(puzzle_input, -1)  # step day forward
        puzzle_input[6] += puzzle_input[8]  # add refreshed fish

    return np.sum(puzzle_input)


@pytest.mark.parametrize("duration, exp_population",[(18,26),(80,5934)]) # , (256,26984457539)])
def test_FishSim(duration, exp_population):
    sim = FishSim([3,4,3,1,2,], duration)
    sim.run()
    assert sim.number_of_fish() == exp_population

def test_FishSim_with_large_start_pop():
    puzzle_input =[5,4,3,5,1,1,2,1,2,1,3,2,3,4,5,1,2,4,3,2,5,1,4,2,1,1,2,5,4,4,4,1,5,4,5,2,1,2,5,5,4,1,3,1,4,2,4,2,5,1,3,5,3,2,3,1,1,4,5,2,4,3,1,5,5,1,3,1,3,2,2,4,1,3,4,3,3,4,1,3,4,3,4,5,2,1,1,1,4,5,5,1,1,3,2,4,1,2,2,2,4,1,2,5,5,1,4,5,2,4,2,1,5,4,1,3,4,1,2,3,1,5,1,3,4,5,4,1,4,3,3,3,5,5,1,1,5,1,5,5,1,5,2,1,5,1,2,3,5,5,1,3,3,1,5,3,4,3,4,3,2,5,2,1,2,5,1,1,1,1,5,1,1,4,3,3,5,1,1,1,4,4,1,3,3,5,5,4,3,2,1,2,2,3,4,1,5,4,3,1,1,5,1,4,2,3,2,2,3,4,1,3,4,1,4,3,4,3,1,3,3,1,1,4,1,1,1,4,5,3,1,1,2,5,2,5,1,5,3,3,1,3,5,5,1,5,4,3,1,5,1,1,5,5,1,1,2,5,5,5,1,1,3,2,2,3,4,5,5,2,5,4,2,1,5,1,4,4,5,4,4,1,2,1,1,2,3,5,5,1,3,1,4,2,3,3,1,4,1,1]
    sim = FishSim(puzzle_input, 80)
    sim.run()
    assert sim.number_of_fish() == 350917

@pytest.mark.parametrize("duration, exp_population",[(18,26),(80,5934)]) # , (256,26984457539)]) 
def test_sim_v2(duration, exp_population):
    assert sim_v2([3,4,3,1,2,], duration) == exp_population

def test_sim_v2_large_start_pop():
    puzzle_input =[5,4,3,5,1,1,2,1,2,1,3,2,3,4,5,1,2,4,3,2,5,1,4,2,1,1,2,5,4,4,4,1,5,4,5,2,1,2,5,5,4,1,3,1,4,2,4,2,5,1,3,5,3,2,3,1,1,4,5,2,4,3,1,5,5,1,3,1,3,2,2,4,1,3,4,3,3,4,1,3,4,3,4,5,2,1,1,1,4,5,5,1,1,3,2,4,1,2,2,2,4,1,2,5,5,1,4,5,2,4,2,1,5,4,1,3,4,1,2,3,1,5,1,3,4,5,4,1,4,3,3,3,5,5,1,1,5,1,5,5,1,5,2,1,5,1,2,3,5,5,1,3,3,1,5,3,4,3,4,3,2,5,2,1,2,5,1,1,1,1,5,1,1,4,3,3,5,1,1,1,4,4,1,3,3,5,5,4,3,2,1,2,2,3,4,1,5,4,3,1,1,5,1,4,2,3,2,2,3,4,1,3,4,1,4,3,4,3,1,3,3,1,1,4,1,1,1,4,5,3,1,1,2,5,2,5,1,5,3,3,1,3,5,5,1,5,4,3,1,5,1,1,5,5,1,1,2,5,5,5,1,1,3,2,2,3,4,5,5,2,5,4,2,1,5,1,4,4,5,4,4,1,2,1,1,2,3,5,5,1,3,1,4,2,3,3,1,4,1,1]
    assert sim_v2(puzzle_input, 80) == 350917

@pytest.mark.parametrize("duration, exp_population",[(18,26),(80,5934), (256,26984457539)]) 
def test_sim_v5(duration, exp_population):
    assert sim_v5([3,4,3,1,2,], duration) == exp_population

def test_sim_v5_large_start_pop():
    puzzle_input =[5,4,3,5,1,1,2,1,2,1,3,2,3,4,5,1,2,4,3,2,5,1,4,2,1,1,2,5,4,4,4,1,5,4,5,2,1,2,5,5,4,1,3,1,4,2,4,2,5,1,3,5,3,2,3,1,1,4,5,2,4,3,1,5,5,1,3,1,3,2,2,4,1,3,4,3,3,4,1,3,4,3,4,5,2,1,1,1,4,5,5,1,1,3,2,4,1,2,2,2,4,1,2,5,5,1,4,5,2,4,2,1,5,4,1,3,4,1,2,3,1,5,1,3,4,5,4,1,4,3,3,3,5,5,1,1,5,1,5,5,1,5,2,1,5,1,2,3,5,5,1,3,3,1,5,3,4,3,4,3,2,5,2,1,2,5,1,1,1,1,5,1,1,4,3,3,5,1,1,1,4,4,1,3,3,5,5,4,3,2,1,2,2,3,4,1,5,4,3,1,1,5,1,4,2,3,2,2,3,4,1,3,4,1,4,3,4,3,1,3,3,1,1,4,1,1,1,4,5,3,1,1,2,5,2,5,1,5,3,3,1,3,5,5,1,5,4,3,1,5,1,1,5,5,1,1,2,5,5,5,1,1,3,2,2,3,4,5,5,2,5,4,2,1,5,1,4,4,5,4,4,1,2,1,1,2,3,5,5,1,3,1,4,2,3,3,1,4,1,1]
    assert sim_v5(puzzle_input, 80) == 350917

if __name__ == "__main__":
    puzzle_input =[5,4,3,5,1,1,2,1,2,1,3,2,3,4,5,1,2,4,3,2,5,1,4,2,1,1,2,5,4,4,4,1,5,4,5,2,1,2,5,5,4,1,3,1,4,2,4,2,5,1,3,5,3,2,3,1,1,4,5,2,4,3,1,5,5,1,3,1,3,2,2,4,1,3,4,3,3,4,1,3,4,3,4,5,2,1,1,1,4,5,5,1,1,3,2,4,1,2,2,2,4,1,2,5,5,1,4,5,2,4,2,1,5,4,1,3,4,1,2,3,1,5,1,3,4,5,4,1,4,3,3,3,5,5,1,1,5,1,5,5,1,5,2,1,5,1,2,3,5,5,1,3,3,1,5,3,4,3,4,3,2,5,2,1,2,5,1,1,1,1,5,1,1,4,3,3,5,1,1,1,4,4,1,3,3,5,5,4,3,2,1,2,2,3,4,1,5,4,3,1,1,5,1,4,2,3,2,2,3,4,1,3,4,1,4,3,4,3,1,3,3,1,1,4,1,1,1,4,5,3,1,1,2,5,2,5,1,5,3,3,1,3,5,5,1,5,4,3,1,5,1,1,5,5,1,1,2,5,5,5,1,1,3,2,2,3,4,5,5,2,5,4,2,1,5,1,4,4,5,4,4,1,2,1,1,2,3,5,5,1,3,1,4,2,3,3,1,4,1,1]
    # puzzle_input=[3,4,3,1,2,]
    solution = 350917
    logging.basicConfig(level="INFO")
    # sim = FishSim(puzzle_input, 80)
    # sim.run()
    # print(sim.number_of_fish())
    # print(len(puzzle_input))
    
    logger.debug(f"start: {puzzle_input}")

    print(sim_v5(puzzle_input, 256))
    