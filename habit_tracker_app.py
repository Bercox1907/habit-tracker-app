import datetime
import json

# Habit Class
class Habit:
    def __init__(self, task, periodicity):
        self.task = task
        self.periodicity = periodicity
        self.created_date = datetime.datetime.now()
        self.completion_history = []

    def complete_task(self):
        self.completion_history.append(datetime.datetime.now())

    def is_completed_in_period(self, start_date, end_date):
        return any(start_date <= completion_date <= end_date for completion_date in self.completion_history)

    def get_streak(self):
        streak = 0
        today = datetime.datetime.now()
        for completion_date in reversed(self.completion_history):
            if (today - completion_date).days <= self.periodicity:
                streak += 1
                today = completion_date
            else:
                break
        return streak

# Habit Tracker Class
class HabitTracker:
    def __init__(self):
        self.habits = []

    def add_habit(self, habit):
        self.habits.append(habit)

    def get_all_habits(self):
        return self.habits

    def get_habits_by_periodicity(self, periodicity):
        return [habit for habit in self.habits if habit.periodicity == periodicity]

    def get_longest_streak(self):
        return max(habit.get_streak() for habit in self.habits)

    def get_longest_streak_for_habit(self, habit):
        return habit.get_streak()

    def save_data(self, filename):
        data = [{"task": habit.task,
                 "periodicity": habit.periodicity,
                 "created_date": habit.created_date.strftime('%Y-%m-%d %H:%M:%S'),
                 "completion_history": [date.strftime('%Y-%m-%d %H:%M:%S') for date in habit.completion_history]}
                for habit in self.habits]
        with open(filename, 'w') as f:
            json.dump(data, f)

    def load_data(self, filename):
        with open(filename, 'r') as f:
            data = json.load(f)
            for habit_data in data:
                habit = Habit(habit_data["task"], habit_data["periodicity"])
                habit.created_date = datetime.datetime.strptime(habit_data["created_date"], '%Y-%m-%d %H:%M:%S')
                habit.completion_history = [datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
                                           for date in habit_data["completion_history"]]
                self.add_habit(habit)

# CLI Interface
def create_habit():
    task = input("Enter habit task: ")
    periodicity = int(input("Enter periodicity (days): "))
    habit = Habit(task, periodicity)
    habit_tracker.add_habit(habit)

def complete_task():
    habit_idx = int(input("Enter habit index: "))
    habit = habit_tracker.habits[habit_idx]
    habit.complete_task()

def analyze_habits():
    print("1. List all habits")
    print("2. List habits by periodicity")
    print("3. Get longest streak for all habits")
    print("4. Get longest streak for a specific habit")
    choice = int(input("Enter your choice: "))

    if choice == 1:
        habits = habit_tracker.get_all_habits()
        for idx, habit in enumerate(habits):
            print(f"{idx}. {habit.task}")
    elif choice == 2:
        periodicity = int(input("Enter periodicity (days): "))
        habits = habit_tracker.get_habits_by_periodicity(periodicity)
        for idx, habit in enumerate(habits):
            print(f"{idx}. {habit.task}")
    elif choice == 3:
        longest_streak = habit_tracker.get_longest_streak()
        print(f"Longest streak for all habits: {longest_streak} days")
    elif choice == 4:
        habit_idx = int(input("Enter habit index: "))
        habit = habit_tracker.habits[habit_idx]
        longest_streak = habit_tracker.get_longest_streak_for_habit(habit)
        print(f"Longest streak for '{habit.task}': {longest_streak} days")

if __name__ == "__main__":
    habit_tracker = HabitTracker()

    # Predefined habits
    habit_tracker.add_habit(Habit("Brush teeth", 1))   # Daily habit
    habit_tracker.add_habit(Habit("Exercise", 7))      # Weekly habit
    habit_tracker.add_habit(Habit("Read", 2))          # Bi-weekly habit
    habit_tracker.add_habit(Habit("Meditate", 1))      # Daily habit
    habit_tracker.add_habit(Habit("Learn", 7))         # Weekly habit

    while True:
        print("\nHabit Tracker Menu:")
        print("1. Create a new habit")
        print("2. Complete a task")
        print("3. Analyze habits")
        print("4. Save data")
        print("5. Load data")
        print("6. Exit")
        choice = int(input("Enter your choice: "))

        if choice == 1:
            create_habit()
        elif choice == 2:
            complete_task()
        elif choice == 3:
            analyze_habits()
        elif choice == 4:
            filename = input("Enter filename to save data: ")
            habit_tracker.save_data(filename)
        elif choice == 5:
            filename = input("Enter filename to load data: ")
            habit_tracker.load_data(filename)
        elif choice == 6:
            break

