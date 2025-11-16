
# - Chromosome (63 genes, crossover, mutation)
# - Knight (move_forward, move_backward, check_moves, evaluate_fitness)
# - Population (tournament selection, new generation, evaluation)
# - Main loop 


import random
import pygame
import sys

# CLASS CHROMOSOME

class Chromosome:
    LENGTH = 63

    def __init__(self, genes=None):
        # Creates a chromosome of 63 moves in [1..8]
        if genes is None:
            self.genes = [random.randint(1, 8) for _ in range(self.LENGTH)]
        else:
            if len(genes) != self.LENGTH:
                raise ValueError("Chromosome must contain exactly 63 genes.")
            self.genes = genes[:]

    def crossover(self, partner):
        # Single-point crossover (PDF requirement)
        point = random.randint(1, self.LENGTH - 1)
        c1 = self.genes[:point] + partner.genes[point:]
        c2 = partner.genes[:point] + self.genes[point:]
        return Chromosome(c1), Chromosome(c2)

    def mutation(self, mutation_rate=0.01):
        # Mutate random gene → new random move
        for i in range(self.LENGTH):
            if random.random() < mutation_rate:
                self.genes[i] = random.randint(1, 8)

# CLASS KNIGHT
class Knight:
    # Direction mapping EXACTLY as in PDF
    MOVES = {
        1: (1, -2),   # up-right
        2: (2, -1),   # right-up
        3: (2, 1),    # right-down
        4: (1, 2),    # down-right
        5: (-1, 2),   # down-left
        6: (-2, 1),   # left-down
        7: (-2, -1),  # left-up
        8: (-1, -2),  # up-left
    }

    def __init__(self, chromosome=None):
        self.chromosome = chromosome if chromosome else Chromosome()
        self.position = (0, 0)
        self.path = [(0, 0)]
        self.fitness = 0

    def move_forward(self, direction):
        x, y = self.position
        dx, dy = Knight.MOVES[direction]
        new_pos = (x + dx, y + dy)
        self.position = new_pos
        return new_pos

    def move_backward(self, direction):
        # Undo a move by applying opposite vector
        x, y = self.position
        dx, dy = Knight.MOVES[direction]
        self.position = (x - dx, y - dy)

    def check_moves(self):
        # Reset path
        self.position = (0, 0)
        self.path = [(0, 0)]

        # Random cycle direction (forward/backward)
        cycle_forward = random.choice([True, False])

        for i, move in enumerate(self.chromosome.genes):
            original_move = move

            # Try original move
            new_pos = self.move_forward(original_move)
            x, y = new_pos

            if 0 <= x < 8 and 0 <= y < 8 and new_pos not in self.path:
                self.path.append(new_pos)
                continue

            # Cancel illegal
            self.move_backward(original_move)

            # Try cycling moves
            valid = False
            for k in range(1, 8):
                if cycle_forward:
                    new_move = ((original_move + k - 1) % 8) + 1
                else:
                    new_move = ((original_move - k - 1) % 8) + 1

                test_pos = self.move_forward(new_move)
                x, y = test_pos

                if 0 <= x < 8 and 0 <= y < 8 and test_pos not in self.path:
                    self.path.append(test_pos)
                    self.chromosome.genes[i] = new_move
                    valid = True
                    break
                else:
                    self.move_backward(new_move)

            # If none valid → keep last move as PDF says
            if not valid:
                final_pos = self.move_forward(original_move)
                self.path.append(final_pos)

    def evaluate_fitness(self):
        # Count valid visited squares exactly as PDF
        visited = set()
        self.fitness = 0

        for pos in self.path:
            x, y = pos
            if not (0 <= x < 8 and 0 <= y < 8):
                break
            if pos in visited:
                break
            visited.add(pos)
            self.fitness += 1
            if self.fitness == 64:
                break

        return self.fitness

# POPULATION CLASS

class Population:
    def __init__(self, population_size):
        self.population_size = population_size
        self.generation = 1
        self.knights = [Knight() for _ in range(population_size)]

    def check_population(self):
        for k in self.knights:
            k.check_moves()

    def evaluate(self):
        best = None
        maxFit = -1

        for k in self.knights:
            fit = k.evaluate_fitness()
            if fit > maxFit:
                maxFit = fit
                best = k

        return maxFit, best

    def tournament_selection(self, size=3):
        sample = random.sample(self.knights, size)
        sample.sort(key=lambda k: k.fitness, reverse=True)
        return sample[0], sample[1]

    def create_new_generation(self):
        new_pop = []

        while len(new_pop) < self.population_size:
            p1, p2 = self.tournament_selection()

            c1, c2 = p1.chromosome.crossover(p2.chromosome)
            c1.mutation()
            c2.mutation()

            new_pop.append(Knight(c1))
            if len(new_pop) < self.population_size:
                new_pop.append(Knight(c2))

        self.knights = new_pop
        self.generation += 1


# BEAUTIFUL PYGAME INTERFACE

def show_interface(knight):
    pygame.init()
    cell = 80
    size = 8 * cell
    screen = pygame.display.set_mode((size, size))
    pygame.display.set_caption("Knight's Tour - Genetic Algorithm")

    font = pygame.font.SysFont("Arial", 22, bold=True)
    small_font = pygame.font.SysFont("Arial", 18)
    clock = pygame.time.Clock()

    path = knight.path

    def center(pos):
        x, y = pos
        return x * cell + cell // 2, y * cell + cell // 2

    running = True
    step = 0
    max_steps = len(path)
    speed = 5  # frames per second

    while running:
        clock.tick(speed)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Draw chessboard
        for y in range(8):
            for x in range(8):
                color = (240, 217, 181) if (x + y) % 2 == 0 else (181, 136, 99)
                pygame.draw.rect(screen, color, (x * cell, y * cell, cell, cell))

        # Draw path up to current step
        for i in range(step):
            cx, cy = center(path[i])
            pygame.draw.circle(screen, (255, 0, 0), (cx, cy), cell // 3)
            txt = font.render(str(i + 1), True, (255, 255, 255))
            screen.blit(txt, txt.get_rect(center=(cx, cy)))

        # Draw connecting lines
        if step > 1:
            pts = [center(path[i]) for i in range(step)]
            pygame.draw.lines(screen, (0, 0, 255), False, pts, 4)

        # Highlight start and end
        start_x, start_y = path[0]
        pygame.draw.rect(screen, (0, 255, 0), (start_x * cell, start_y * cell, cell, cell), 4)
        if step > 0:
            end_x, end_y = path[step - 1]
            pygame.draw.rect(screen, (255, 215, 0), (end_x * cell, end_y * cell, cell, cell), 4)

        # Display fitness and steps
        info_text = f"Fitness: {knight.fitness} | Steps: {max_steps}"
        screen.blit(small_font.render(info_text, True, (0, 0, 0)), (10, 10))

        pygame.display.update()

        # Increment step for animation
        if step < max_steps:
            step += 1

    pygame.quit()



# ---------------------------------------------------
# MAIN FUNCTION (AS IN THE PDF)
# ---------------------------------------------------
def main():
    population_size = 50
    population = Population(population_size)

    while True:
        population.check_population()
        maxFit, best = population.evaluate()

        print(f"Generation {population.generation} | Best Fitness = {maxFit}")

        if maxFit == 64:
            print("Solution found!")
            break

        population.create_new_generation()

    show_interface(best)


if __name__ == "__main__":
    main()
