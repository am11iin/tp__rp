import random

# Version temporaire de la classe Chromosome (pour tester en attendant le Membre 1)
class Chromosome:
    def __init__(self, genes=None):
        if genes is None:
            # Génère 63 mouvements aléatoires (1 à 8)
            self.genes = [random.randint(1, 8) for _ in range(63)]
        else:
            self.genes = genes.copy()
    
    def crossover(self, partner):
        # Single-point crossover temporaire
        point = random.randint(1, 62)
        child1_genes = self.genes[:point] + partner.genes[point:]
        child2_genes = partner.genes[:point] + self.genes[point:]
        return Chromosome(child1_genes), Chromosome(child2_genes)
    
    def mutation(self, mutation_rate=0.01):
        for i in range(len(self.genes)):
            if random.random() < mutation_rate:
                self.genes[i] = random.randint(1, 8)


# ==================== CLASSE KNIGHT (TON TRAVAIL) ====================
class Knight:
    def __init__(self, chromosome=None):
        """
        Initialise un nouveau chevalier.
        Si aucun chromosome n'est fourni, en crée un nouveau.
        Position initiale: (0, 0)
        Fitness initiale: 0
        Path: liste contenant la position initiale
        """
        if chromosome is None:
            self.chromosome = Chromosome()
        else:
            self.chromosome = chromosome
        
        # Position initiale du chevalier (x, y)
        self.position = (0, 0)
        
        # Fitness initial à 0
        self.fitness = 0
        
        # Chemin: liste des positions visitées, commence avec (0, 0)
        self.path = [(0, 0)]
    
    def move_forward(self, direction):
        """
        Déplace le chevalier dans une des 8 directions.
        Génère la nouvelle position après application du mouvement.
        
        Direction mapping:
        1: up-right    (x+1, y+2)
        2: right-up    (x+2, y+1)
        3: right-down  (x+2, y-1)
        4: down-right  (x+1, y-2)
        5: down-left   (x-1, y-2)
        6: left-down   (x-2, y-1)
        7: left-up     (x-2, y+1)
        8: up-left     (x-1, y+2)
        
        Retourne la nouvelle position (x, y)
        """
        x, y = self.position
        
        # Définir les 8 mouvements possibles du chevalier (mouvement en L)
        if direction == 1:      # up-right
            new_position = (x + 1, y + 2)
        elif direction == 2:    # right-up
            new_position = (x + 2, y + 1)
        elif direction == 3:    # right-down
            new_position = (x + 2, y - 1)
        elif direction == 4:    # down-right
            new_position = (x + 1, y - 2)
        elif direction == 5:    # down-left
            new_position = (x - 1, y - 2)
        elif direction == 6:    # left-down
            new_position = (x - 2, y - 1)
        elif direction == 7:    # left-up
            new_position = (x - 2, y + 1)
        elif direction == 8:    # up-left
            new_position = (x - 1, y + 2)
        
        # Mettre à jour la position actuelle
        self.position = new_position
        
        return new_position
    
    def move_backward(self, direction):
        """
        Permet au chevalier de revenir en arrière si le mouvement appliqué est illégal.
        Annule le dernier mouvement en appliquant le mouvement inverse.
        """
        x, y = self.position
        
        # Appliquer le mouvement inverse
        if direction == 1:      # inverse de up-right
            self.position = (x - 1, y - 2)
        elif direction == 2:    # inverse de right-up
            self.position = (x - 2, y - 1)
        elif direction == 3:    # inverse de right-down
            self.position = (x - 2, y + 1)
        elif direction == 4:    # inverse de down-right
            self.position = (x - 1, y + 2)
        elif direction == 5:    # inverse de down-left
            self.position = (x + 1, y + 2)
        elif direction == 6:    # inverse de left-down
            self.position = (x + 2, y + 1)
        elif direction == 7:    # inverse de left-up
            self.position = (x + 2, y - 1)
        elif direction == 8:    # inverse de up-left
            self.position = (x + 1, y - 2)
    
    def check_moves(self):
        """
        Vérifie la validité de chaque mouvement dans le chromosome.
        
        Un mouvement est invalide si:
        - Il place le chevalier en dehors de l'échiquier (0-7, 0-7)
        - Il place le chevalier sur une position déjà visitée
        
        Si un mouvement est illégal:
        1. Annuler le mouvement avec move_backward()
        2. Tester d'autres mouvements en cyclant forward ou backward
        3. La direction du cycle est déterminée aléatoirement (même pour tous les mouvements)
        4. Si aucun mouvement valide n'est trouvé, garder le dernier mouvement
        
        Cycle forward (si mouvement actuel = 4): 5, 6, 7, 8, 1, 2, 3
        Cycle backward (si mouvement actuel = 4): 3, 2, 1, 8, 7, 6, 5
        """
        # Réinitialiser la position et le chemin pour cette vérification
        self.position = (0, 0)
        self.path = [(0, 0)]
        
        # Déterminer aléatoirement la direction du cycle (même pour tous les mouvements)
        cycle_forward = random.choice([True, False])
        
        # Parcourir chaque gène (mouvement) dans le chromosome
        for i in range(len(self.chromosome.genes)):
            current_move = self.chromosome.genes[i]
            
            # Appliquer le mouvement actuel
            new_position = self.move_forward(current_move)
            
            # Vérifier si le mouvement est valide
            x, y = new_position
            is_valid = True
            
            # Vérifier si en dehors de l'échiquier
            if x < 0 or x > 7 or y < 0 or y > 7:
                is_valid = False
            # Vérifier si position déjà visitée
            elif new_position in self.path:
                is_valid = False
            
            if is_valid:
                # Mouvement valide: ajouter la position au chemin
                self.path.append(new_position)
            else:
                # Mouvement invalide: annuler avec move_backward
                self.move_backward(current_move)
                
                # Tester d'autres mouvements en cyclant
                valid_move_found = False
                
                if cycle_forward:
                    # Cycle forward: 5, 6, 7, 8, 1, 2, 3 (pour current_move = 4)
                    for offset in range(1, 8):
                        test_move = ((current_move - 1 + offset) % 8) + 1
                        
                        # Tester ce mouvement
                        test_position = self.move_forward(test_move)
                        tx, ty = test_position
                        
                        # Vérifier validité
                        if (0 <= tx <= 7 and 0 <= ty <= 7 and 
                            test_position not in self.path):
                            # Mouvement valide trouvé
                            self.path.append(test_position)
                            self.chromosome.genes[i] = test_move
                            valid_move_found = True
                            break
                        else:
                            # Mouvement invalide, annuler
                            self.move_backward(test_move)
                else:
                    # Cycle backward: 3, 2, 1, 8, 7, 6, 5 (pour current_move = 4)
                    for offset in range(1, 8):
                        test_move = ((current_move - 1 - offset) % 8) + 1
                        
                        # Tester ce mouvement
                        test_position = self.move_forward(test_move)
                        tx, ty = test_position
                        
                        # Vérifier validité
                        if (0 <= tx <= 7 and 0 <= ty <= 7 and 
                            test_position not in self.path):
                            # Mouvement valide trouvé
                            self.path.append(test_position)
                            self.chromosome.genes[i] = test_move
                            valid_move_found = True
                            break
                        else:
                            # Mouvement invalide, annuler
                            self.move_backward(test_move)
                
                # Si aucun mouvement valide n'est trouvé, garder le dernier mouvement
                # (ne rien ajouter au path, le chevalier reste bloqué)
    
    def evaluate_fitness(self):
        """
        Boucle à travers le chemin du chevalier (liste des positions visitées)
        et incrémente la valeur de fitness de 1 jusqu'à rencontrer un mouvement invalide.
        
        Si le chevalier a visité toutes les cases de l'échiquier, fitness = 64.
        
        Retourne la valeur de fitness.
        """
        # La fitness est simplement le nombre de positions visitées
        # (longueur du path)
        self.fitness = len(self.path)
        
        return self.fitness


# ==================== CODE DE TEST ====================
if __name__ == "__main__":
    print("=" * 60)
    print("TEST DE LA CLASSE KNIGHT")
    print("=" * 60)
    print()
    
    # Test 1: Création d'un chevalier
    print("Test 1: Création d'un chevalier")
    print("-" * 40)
    knight = Knight()
    print(f"Position initiale: {knight.position}")
    print(f"Fitness initiale: {knight.fitness}")
    print(f"Path initial: {knight.path}")
    print(f"Longueur du chromosome: {len(knight.chromosome.genes)} gènes")
    print()
    
    # Test 2: Test de move_forward
    print("Test 2: Test de move_forward")
    print("-" * 40)
    knight2 = Knight()
    print(f"Position de départ: {knight2.position}")
    
    # Tester direction 1 (up-right)
    new_pos = knight2.move_forward(1)
    print(f"Après move_forward(1) [up-right]: {new_pos}")
    
    # Tester direction 2 (right-up)
    new_pos = knight2.move_forward(2)
    print(f"Après move_forward(2) [right-up]: {new_pos}")
    print()
    
    # Test 3: Test de move_backward
    print("Test 3: Test de move_backward")
    print("-" * 40)
    knight3 = Knight()
    print(f"Position initiale: {knight3.position}")
    knight3.move_forward(1)
    print(f"Après move_forward(1): {knight3.position}")
    knight3.move_backward(1)
    print(f"Après move_backward(1): {knight3.position}")
    print()
    
    # Test 4: Test complet avec check_moves et evaluate_fitness
    print("Test 4: Check moves et évaluation de fitness")
    print("-" * 40)
    knight4 = Knight()
    print(f"Avant check_moves - Path: {knight4.path[:3]}...")
    
    knight4.check_moves()
    print(f"Après check_moves - Longueur du path: {len(knight4.path)}")
    
    fitness = knight4.evaluate_fitness()
    print(f"Fitness calculée: {fitness}")
    print(f"Premières 5 positions du path: {knight4.path[:5]}")
    print()
    
    # Test 5: Statistiques sur plusieurs chevaliers
    print("Test 5: Statistiques sur 20 chevaliers")
    print("-" * 40)
    fitness_list = []
    
    for i in range(20):
        k = Knight()
        k.check_moves()
        f = k.evaluate_fitness()
        fitness_list.append(f)
    
    print(f"Fitness minimum: {min(fitness_list)}")
    print(f"Fitness maximum: {max(fitness_list)}")
    print(f"Fitness moyenne: {sum(fitness_list) / len(fitness_list):.2f}")
    print(f"Liste des fitness: {fitness_list}")
    print()
    
    # Test 6: Afficher un exemple de chemin complet
    print("Test 6: Exemple de chemin d'un chevalier")
    print("-" * 40)
    knight5 = Knight()
    knight5.check_moves()
    knight5.evaluate_fitness()
    
    print(f"Fitness: {knight5.fitness}")
    print(f"Chemin complet ({len(knight5.path)} positions):")
    
    # Afficher le chemin par groupes de 8
    for i in range(0, len(knight5.path), 8):
        print(f"  {knight5.path[i:i+8]}")
    
    print()
    print("=" * 60)
    print("FIN DES TESTS")
    print("=" * 60)