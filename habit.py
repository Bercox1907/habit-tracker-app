class Habit:
    def __init__(self, name, periodicity):
        self.name = name
        self.periodicity = periodicity
        self.creation_date = None
        self.completion_history = []

    def mark_completed(self, date):
        self.completion_history.append(date)

    def __str__(self):
        return f"Habit: {self.name} (Periodicity: {self.periodicity} days)"
