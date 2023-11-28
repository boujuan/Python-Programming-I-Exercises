import random

people = ["Juan", "Jiah", "Julia"]
exercises = ["E1", "E2", "E3", "E4", "E5", "E6", "E7"]

assignments = {}

for exercise in exercises:
    random_person = random.choice(people)
    assignments[exercise] = random_person
    people.remove(random_person)

for exercise, person in assignments.items():
    print(f"{exercise} is assigned to {person}")
    
input("Press Enter to exit...")