import tkinter as tk
from tkinter import ttk
from Fenwick import FenwickTree

class SportsLeague:
    def __init__(self, team_scores):
        self.team_scores = team_scores
        self.fenwick_tree = FenwickTree(len(team_scores))
        for idx, score in enumerate(team_scores, start=1):
            self.fenwick_tree.update(idx, score)

    def update_team_score(self, team_index, new_score):
        delta = new_score - self.team_scores[team_index - 1]
        self.team_scores[team_index - 1] = new_score
        self.fenwick_tree.update(team_index, delta)

    def delete_team(self, team_index):
        score = self.team_scores[team_index - 1]
        self.team_scores.pop(team_index - 1)
        self.fenwick_tree.delete(team_index, score)

    def total_score_in_range(self, left_team, right_team):
        return self.fenwick_tree.range_sum(left_team, right_team)
    

class SportsLeagueUI(tk.Tk):
    def __init__(self, league):
        super().__init__()
        self.title("Sports League")

        self.league = league

        self.input_frame = ttk.Frame(self)
        self.input_frame.pack(padx=10, pady=10)

        self.result_frame = ttk.Frame(self)
        self.result_frame.pack(padx=10, pady=10)

        self.init_input_frame()
        self.init_result_frame()

    def init_input_frame(self):
        ttk.Label(self.input_frame, text="From Team Index:").grid(row=0, column=0)
        ttk.Label(self.input_frame, text="To Team Index:").grid(row=1, column=0)

        self.from_index = tk.StringVar()
        self.to_index = tk.StringVar()

        ttk.Entry(self.input_frame, textvariable=self.from_index).grid(row=0, column=1)
        ttk.Entry(self.input_frame, textvariable=self.to_index).grid(row=1, column=1)

        ttk.Button(self.input_frame, text="Get Total Score", command=self.get_total_score).grid(row=2, column=0, columnspan=2, pady=10)

    def init_result_frame(self):
        ttk.Label(self.result_frame, text="Total Score:").grid(row=0, column=0)

        self.result_var = tk.StringVar()
        ttk.Label(self.result_frame, textvariable=self.result_var).grid(row=0, column=1)

    def get_total_score(self):
        from_index = int(self.from_index.get())
        to_index = int(self.to_index.get())
        total_score = self.league.total_score_in_range(from_index, to_index)
        self.result_var.set(str(total_score))

if __name__ == "__main__":
    team_scores = [50, 40, 55, 60, 45, 70, 65, 80, 75, 90, 85]
    league = SportsLeague(team_scores)
    app = SportsLeagueUI(league)
    app.mainloop()