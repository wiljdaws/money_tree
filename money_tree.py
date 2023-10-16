import os
import csv
import random
from time import sleep
import tkinter as tk
from tkinter import messagebox
import numpy as np
import getpass
import requests
import time

class MoneyTreeApp:
    def __init__(self):
        # self.window = tk.Tk()
        # self.window.title("Money Tree App")

        # self.label = tk.Label(self.window, text="Money dropped: $", font=("Arial", 24))
        # self.label.pack(pady=20)

        # self.claim_button = tk.Button(self.window, text="Claim Money", command=self.claim_money_drop, font=("Arial", 16), bg="#4CAF50", fg="white")
        # self.claim_button.pack(pady=10)

        # self.username = getpass.getuser()
        # self.username_label = tk.Label(self.window, text=f"Username: {self.username}", font=("Arial", 16))
        # self.username_label.pack(pady=10)

        # self.csv_file = "accounts.csv"
        self.min_amount = 0.01
        self.max_amount = 1000

        self.amounts = np.arange(self.min_amount, self.max_amount + 0.01, 0.01)
        self.weights = self.calculate_weights()

        if len(self.weights) != len(self.amounts):
            raise ValueError("The number of weights does not match the population.")

        # if not os.path.exists(self.csv_file):
        #     self.create_csv_file()

    def calculate_weights(self):
        # Range: 0.01 - 5, Probability: High (80%)
        weights_low = np.linspace(80, 0.01, int((5 - 0.01) / 0.01))
        # Range: 5 - 20, Probability: Medium (15%)
        weights_mid = np.linspace(15, 0.01, int((20 - 5) / 0.01))
        # Range: 20 - 50, Probability: Low (4.5%)
        weights_high = np.linspace(4.5, 0.01, int((50 - 20) / 0.01))
        # Range: 50 - 100, Probability: Severe (0.5%)
        weights_severe = np.linspace(0.5, 0.01, int((100 - 50) / 0.01))
        # Range: 100 - 1000, Probability: Super Rare (0.01%)
        weights_super_rare = np.linspace(0.01, 0.001, int((1000 - 100) / 0.01))

        weights = np.concatenate((weights_low, weights_mid, weights_high, weights_severe, weights_super_rare))
        weights = np.resize(weights, len(self.amounts))

        return weights

    # def create_csv_file(self):
    #     with open(self.csv_file, "w", newline="") as file:
    #         writer = csv.writer(file)
    #         writer.writerow(["User", "Amount", "Soul"])
    #         writer.writerow([self.username, 0.0, 100.0])  # Initialize user with 0 amount and 100% soul

    def generate_money_amount(self):
        amount = random.choices(self.amounts, weights=self.weights, k=1)[0]
        return round(amount, 2)

    # # def update_account(self, amount):
    # #     accounts = self.load_accounts()

    #     if self.username in accounts:
    #         accounts[self.username]["Amount"] += amount
    #     else:
    #         accounts[self.username] = {"Amount": amount, "Soul": 100.0}

    #     with open(self.csv_file, "w", newline="") as file:
    #         writer = csv.writer(file)
    #         writer.writerow(["User", "Amount", "Soul"])
    #         for user, data in accounts.items():
    #             writer.writerow([user, round(data["Amount"], 2), round(data["Soul"], 2)])

    def load_accounts(self):
        accounts = {}
        try:
            with open(self.csv_file, "r") as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    if len(row) == 3:
                        user = row[0]
                        amount = float(row[1])
                        soul = float(row[2])
                        accounts[user] = {"Amount": amount, "Soul": soul}
        except FileNotFoundError:
            pass

        return accounts

    # def claim_money_drop(self):
    #     amount = self.generate_money_amount()
    #     self.update_account(amount)



def send_webhook(webhook_url, payload):
    for keys in payload:
        payload[keys] = str(payload[keys])
    req = requests.Session()
    header = {"Content-Type": "application/json"}
    req.post(webhook_url, json=payload, headers=header)

            


if __name__ == "__main__":
    app = MoneyTreeApp()
    
    '''
    Content = The Money tree has dropped a Sack!
    Content2 = app.generatemoneyamount()
    '''
    content = 'The Money tree has dropped a Sack!'
    content2 = app.generate_money_amount()
    # print(content, content2)
    str(content2)
    hook_url = 'https://hooks.slack.com/workflows/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'
    payload = {"content": content, "content2": content2}
    send_webhook(hook_url, payload)



