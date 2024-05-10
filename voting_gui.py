import csv
import subprocess
from tkinter import Tk, Label, Entry, Button, IntVar, Checkbutton, W

class VotingGUI:
    def __init__(self):
        self.root = Tk()
        self.root.title("Voting Application")
        self.root.resizable(False, False)  # Make window non-resizable
        self.selected_candidate = IntVar(self.root)
        self.voted_ids = set()
        self.votes = {"Jane": 0, "John": 0}
        self.create_gui()

    def submit_vote(self):
        input_id = self.id_entry.get()
        selected_id = self.selected_candidate.get()

        if not input_id:
            self.vote_sent_label.config(text="Please Input ID!", fg="red")
        elif not selected_id:
            self.vote_sent_label.config(text="Please Select a Candidate!", fg="red")
        else:
            try:
                input_id = int(input_id)
                if input_id in self.voted_ids:
                    self.vote_sent_label.config(text="This ID has Already Voted.", fg="red")
                else:
                    self.voted_ids.add(input_id)
                    self.save_vote(input_id, selected_id)
                    self.vote_sent_label.config(text="Vote Sent!", fg="black")
            except ValueError:
                self.vote_sent_label.config(text="Please Input a Valid ID!", fg="red")

    def save_vote(self, voter_id, candidate_id):
        with open('voting_history.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            if file.tell() == 0:  # If the file is empty, write header
                writer.writerow(["ID", "Candidate"])
            candidate_name = "Jane" if candidate_id == 2 else "John"
            writer.writerow([voter_id, candidate_name])
        self.votes[candidate_name] += 1

    def show_voting_history(self):
        with open('voting_history.csv', mode='r') as file:
            reader = csv.reader(file)
            rows = list(reader)
        total_votes = len(rows) - 1 if len(rows) > 0 else 0  # Subtract header row
        with open('voting_history.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['', '', f'Total Votes: {total_votes}'])
        subprocess.run(['open', 'voting_history.csv'])

    def create_gui(self):
        id_label = Label(self.root, text="ID:")
        id_label.grid(row=0, column=0, padx=10, pady=10, sticky=W)

        self.id_entry = Entry(self.root)
        self.id_entry.grid(row=0, column=1, padx=10, pady=10)

        candidates_label = Label(self.root, text="CANDIDATES")
        candidates_label.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        candidate_names = ["Jane", "John"]
        for i, candidate_name in enumerate(candidate_names, start=2):
            candidate_checkbox = Checkbutton(self.root, text=candidate_name,
                                             variable=self.selected_candidate, onvalue=i, offvalue=0)
            candidate_checkbox.grid(row=i, column=0, columnspan=2, padx=(60, 10), pady=5, sticky=W)

        submit_button = Button(self.root, text="SUBMIT VOTE", command=self.submit_vote)
        submit_button.grid(row=len(candidate_names) + 2, column=0, columnspan=2, padx=10, pady=10)

        voting_history_button = Button(self.root, text="Voting History", command=self.show_voting_history)
        voting_history_button.grid(row=len(candidate_names) + 3, column=0, columnspan=2, padx=10, pady=10)

        self.vote_sent_label = Label(self.root, text="", fg="red")
        self.vote_sent_label.grid(row=len(candidate_names) + 4, column=0, columnspan=2, padx=10, pady=10)

        self.root.mainloop()
