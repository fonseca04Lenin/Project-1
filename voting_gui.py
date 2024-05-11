import csv  # Importing the CSV module for reading and writing CSV files
import subprocess  # Importing the subprocess module for executing system commands
from tkinter import Tk, Label, Entry, Button, IntVar, Checkbutton, W  # Importing necessary components from the tkinter library

class VotingGUI:
    def __init__(self):
        # Initialsize the tkinter window
        self.root = Tk()
        self.root.title("Voting Application")  # Set window title
        self.root.resizable(False, False)  # Make window non-resizable
        # Variable to hold the selected candidate
        self.selected_candidate = IntVar(self.root)
        # Set to keep track of voted IDs
        self.voted_ids = set()
        # Dictionary to store candidate names and their votes
        self.votes = {"Jane": 0, "John": 0}
        # Call function to create GUI
        self.create_gui()

    def submit_vote(self):
        # Get IDs and selected candidate ID from entry and checkbox
        input_id = self.id_entry.get()
        selected_id = self.selected_candidate.get()

        # Check for missing input
        if not input_id:
            self.vote_sent_label.config(text="Please Input ID!", fg="red")
        elif not selected_id:
            self.vote_sent_label.config(text="Please Select a Candidate!", fg="red")
        else:
            try:
                input_id = int(input_id)
                # Check if ID has already voted
                if input_id in self.voted_ids:
                    self.vote_sent_label.config(text="This ID has Already Voted.", fg="red")
                else:
                    # Add ID to voted list, save vote, and update label
                    self.voted_ids.add(input_id)
                    self.save_vote(input_id, selected_id)
                    self.vote_sent_label.config(text="Vote Sent!", fg="black")
            except ValueError:
                self.vote_sent_label.config(text="Please Input a Valid ID!", fg="red")

    def save_vote(self, voter_id, candidate_id):
        # Write votse to CSV file
        with open('voting_history.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            # Write header if file is empty
            if file.tell() == 0:
                writer.writerow(["ID", "Candidate"])
            # Get candidate name based on candidate ID
            candidate_name = "Jane" if candidate_id == 2 else "John"
            writer.writerow([voter_id, candidate_name])
        # Increment vote count for the candidate
        self.votes[candidate_name] += 1

    def show_voting_history(self):
        # Read and display voting history, and open CSV file
        with open('voting_history.csv', mode='r') as file:
            reader = csv.reader(file)
            rows = list(reader)
        # Calculate total votes (excluding header)
        total_votes = len(rows) - 1 if len(rows) > 0 else 0
        # Append total votes to file
        with open('voting_history.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['', '', f'Total Votes: {total_votes}'])
        # Open CSV file
        subprocess.run(['open', 'voting_history.csv'])

    def create_gui(self):
        # Create GUI elements
        id_label = Label(self.root, text="ID:")
        id_label.grid(row=0, column=0, padx=10, pady=10, sticky=W)

        self.id_entry = Entry(self.root)
        self.id_entry.grid(row=0, column=1, padx=10, pady=10)

        candidates_label = Label(self.root, text="CANDIDATES")
        candidates_label.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        candidate_names = ["Jane", "John"]
        # Create checkboxes for each candidate
        for i, candidate_name in enumerate(candidate_names, start=2):
            candidate_checkbox = Checkbutton(self.root, text=candidate_name,
                                             variable=self.selected_candidate, onvalue=i, offvalue=0)
            candidate_checkbox.grid(row=i, column=0, columnspan=2, padx=(60, 10), pady=5, sticky=W)

        # Create submit vote button
        submit_button = Button(self.root, text="SUBMIT VOTE", command=self.submit_vote)
        submit_button.grid(row=len(candidate_names) + 2, column=0, columnspan=2, padx=10, pady=10)

        # Create button to view voting history
        voting_history_button = Button(self.root, text="Voting History", command=self.show_voting_history)
        voting_history_button.grid(row=len(candidate_names) + 3, column=0, columnspan=2, padx=10, pady=10)

        # Label to display status of vote submission
        self.vote_sent_label = Label(self.root, text="", fg="red")
        self.vote_sent_label.grid(row=len(candidate_names) + 4, column=0, columnspan=2, padx=10, pady=10)

        # Run the GUI main loop
        self.root.mainloop()

