import random
import tkinter as tk
from tkinter import Canvas


#   CLASS CHROMOSOME


class Chromosome:
    def __init__(self, genes=None):
        if genes is None:
            # Generate random chromosome of 63 moves (1..8)
            self.genes = [random.randint(1, 8) for _ in range(63)]
        else:
            self.genes = genes

    def crossover(self, partner):
        # Single-point crossover
        point = random.randint(1, len(self.genes) - 1)

        child1 = self.genes[:point] + partner.genes[point:]
        child2 = partner.genes[:point] + self.genes[point:]

        return Chromosome(child1), Chromosome(child2)

    def mutation(self, mutation_rate=0.02):
        for i in range(len(self.genes)):
            if random.random() < mutation_rate:
                self.genes[i] = random.randint(1, 8)



#   CLASS KNIGHT 


class Knight:
    def __init__(self, chromosome=None):
        if chromosome is None:
            self.chromosome = Chromosome()
        else:
            self.chromosome = chromosome
        
        self.position = (0, 0)
        self.fitness = 0
        self.path = [(0, 0)]
    
    def move_forward(self, direction):
        x, y = self.position
        
        if direction == 1:
            new_position = (x + 1, y + 2)
        elif direction == 2:
            new_position = (x + 2, y + 1)
        elif direction == 3:
            new_position = (x + 2, y - 1)
        elif direction == 4:
            new_position = (x + 1, y - 2)
        elif direction == 5:
            new_position = (x - 1, y - 2)
        elif direction == 6:
            new_position = (x - 2, y - 1)
        elif direction == 7:
            new_position = (x - 2, y + 1)
        elif direction == 8:
            new_position = (x - 1, y + 2)
        
        self.position = new_position
        return new_position
    
    def move_backward(self, direction):
        x, y = self.position
        
        if direction == 1:
            self.position = (x - 1, y - 2)
        elif direction == 2:
            self.position = (x - 2, y - 1)
        elif direction == 3:
            self.position = (x - 2, y + 1)
        elif direction == 4:
            self.position = (x - 1, y + 2)
        elif direction == 5:
            self.position = (x + 1, y + 2)
        elif direction == 6:
            self.position = (x + 2, y + 1)
        elif direction == 7:
            self.position = (x + 2, y - 1)
        elif direction == 8:
            self.position = (x + 1, y - 2)
    
    def check_moves(self):
        self.position = (0, 0)
        self.path = [(0, 0)]
        
        cycle_forward = random.choice([True, False])
        
        for i in range(len(self.chromosome.genes)):
            current_move = self.chromosome.genes[i]
            new_position = self.move_forward(current_move)
            x, y = new_position
            is_valid = True
            
            if x < 0 or x > 7 or y < 0 or y > 7:
                is_valid = False
            elif new_position in self.path:
                is_valid = False
            
            if is_valid:
                self.path.append(new_position)
            else:
                self.move_backward(current_move)
                valid_move_found = False
                
                if cycle_forward:
                    for offset in range(1, 8):
                        test_move = ((current_move - 1 + offset) % 8) + 1
                        test_position = self.move_forward(test_move)
                        tx, ty = test_position
                        
                        if (0 <= tx <= 7 and 0 <= ty <= 7 and 
                            test_position not in self.path):
                            self.path.append(test_position)
                            self.chromosome.genes[i] = test_move
                            valid_move_found = True
                            break
                        else:
                            self.move_backward(test_move)
                else:
                    for offset in range(1, 8):
                        test_move = ((current_move - 1 - offset) % 8) + 1
                        test_position = self.move_forward(test_move)
                        tx, ty = test_position
                        
                        if (0 <= tx <= 7 and 0 <= ty <= 7 and 
                            test_position not in self.path):
                            self.path.append(test_position)
                            self.chromosome.genes[i] = test_move
                            valid_move_found = True
                            break
                        else:
                            self.move_backward(test_move)
    
    def evaluate_fitness(self):
        self.fitness = len(self.path)
        return self.fitness



#   CLASS POPULATION 


class Population:
    def __init__(self, population_size):
        self.population_size = population_size
        self.generation = 1
        self.knights = [Knight() for _ in range(population_size)]

    def check_population(self):
        for knight in self.knights:
            knight.check_moves()

    def evaluate(self):
        best_knight = None
        maxFit = -1

        for knight in self.knights:
            fitness = knight.evaluate_fitness()
            if fitness > maxFit:
                maxFit = fitness
                best_knight = knight

        return maxFit, best_knight

    def tournament_selection(self, size=3):
        sample = random.sample(self.knights, size)
        sample.sort(key=lambda k: k.fitness, reverse=True)
        return sample[0], sample[1]

    def create_new_generation(self):
        new_knights = []

        while len(new_knights) < self.population_size:
            parent1, parent2 = self.tournament_selection()

            child1_chrom, child2_chrom = parent1.chromosome.crossover(
                parent2.chromosome
            )

            child1_chrom.mutation()
            child2_chrom.mutation()

            new_knights.append(Knight(child1_chrom))

            if len(new_knights) < self.population_size:
                new_knights.append(Knight(child2_chrom))

        self.knights = new_knights
        self.generation += 1




#   INTERFACE TKINTER (PDF)


def show_solution(best_knight):
    window = tk.Tk()
    window.title("Knight's Tour Solution - Genetic Algorithm")

    cell_size = 60
    board_size = 8 * cell_size

    canvas = Canvas(window, width=board_size, height=board_size)
    canvas.pack()

    # Map positions to order index
    order_map = {}
    for i, pos in enumerate(best_knight.path):
        order_map[pos] = i + 1

    # Draw board
    for row in range(8):
        for col in range(8):
            x1 = col * cell_size
            y1 = row * cell_size
            x2 = x1 + cell_size
            y2 = y1 + cell_size

            # Chessboard colors
            fill_color = "#EEE" if (row + col) % 2 == 0 else "#999"
            canvas.create_rectangle(x1, y1, x2, y2, fill=fill_color)

            pos = (col, row)
            if pos in order_map:
                canvas.create_text(
                    x1 + cell_size / 2,
                    y1 + cell_size / 2,
                    text=str(order_map[pos]),
                    font=("Arial", 16, "bold"),
                    fill="red"
                )

    window.mainloop()




#   MAIN (PDF)


def main():
    population_size = 50
    population = Population(population_size)

    while True:
        population.check_population()

        maxFit, bestSolution = population.evaluate()

        print(f"Generation {population.generation} - Best fitness = {maxFit}")

        if maxFit == 64:
            print("Solution found!")
            break

        population.create_new_generation()

    # Show final solution
    show_solution(bestSolution)



if __name__ == "__main__":
    main()
