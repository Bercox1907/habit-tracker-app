import json
from datetime import datetime
from habit import Habit

class HabitTracker:
    def __init__(self):
        self.habits = []

    def create_habit(self, name, periodicity):
        habit = Habit(name, periodicity)
        habit.creation_date = datetime.now()
        self.habits.append(habit)

    def complete_habit(self, habit_index):
        date = datetime.now()
        self.habits[habit_index].mark_completed(date)

    def save_data(self, filename):
        data = []
        for habit in self.habits:
            data.append({
                "name": habit.name,
                "periodicity": habit.periodicity,
                "creation_date": str(habit.creation_date),
                "completion_history": [str(date) for date in habit.completion_history]
            })
        
        with open(filename, 'w') as f:
            json.dump(data, f)

    def load_data(self, filename):
        with open(filename, 'r') as f:
            data = json.load(f)
            for item in data:
                habit = Habit(item["name"], item["periodicity"])
                habit.creation_date = datetime.strptime(item["creation_date"], '%Y-%m-%d %H:%M:%S.%f')
                habit.completion_history = [datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f') for date in item["completion_history"]]
                self.habits.append(habit)

if __name__ == "__main__":
    tracker = HabitTracker()

    # Example usage
    tracker.create_habit("Exercise", 7)
    tracker.create_habit("Read", 14)

    tracker.complete_habit(0)
    tracker.complete_habit(0)
    tracker.complete_habit(1)

    tracker.save_data("habit_data.json")
    tracker.load_data("habit_data.json")

    for habit in tracker.habits:
        print(habit)
        print("Completion History:", habit.completion_history)
