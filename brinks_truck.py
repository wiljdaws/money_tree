import os
import random
import time
import numpy as np
import requests
from credit import credit

class BrinksTruckApp:
    def __init__(self):
        self.hook_url = 'https://hooks.slack.com/workflows/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'
        self.min_amount = 500
        self.max_pos_amount = 50000
        self.min_neg_amount = 200
        self.max_neg_amount = 10000
        self.amounts = np.arange(self.min_amount, self.max_pos_amount + 0.01, 0.01)
        self.neg_amounts = np.arange(self.min_neg_amount, self.max_neg_amount, 0.25)
        self.weights = self.pos_calculate_weights()
        self.neg_weights = self.neg_calculate_weights()

        if len(self.weights) != len(self.amounts):
            raise ValueError("The number of weights does not match the population.")

    def pos_calculate_weights(self):
        '''
        Range: 500 - 2000, Probability: High (80%)
        Range: 2000 - 5000, Probability: Medium (15%)
        Range: 5000 - 10000, Probability: Low (4.5%)
        Range: 10000 - 50000, Probability: Rare (0.5%)
        '''
        weights_mid = np.linspace(80, 0.01, int((2000 - 500) / 0.01))
        weights_high = np.linspace(10, 0.01, int((5000 - 2000) / 0.01))
        weights_severe = np.linspace(9, 0.01, int((10000 - 5000) / 0.01))
        weights_super_rare = np.linspace(1, 0.01, int((50000 - 10000) / 0.01))
        weights = np.concatenate((weights_mid, weights_high, weights_severe, weights_super_rare))
        pos_weights = np.resize(weights, len(self.amounts))
        
        return pos_weights
    
    def neg_calculate_weights(self):
        '''
        Range: 200 - 500, Probability: High (80%)
        Range: 500 - 1000, Probability: Medium (15%)
        Range: 1000 - 2000, Probability: Low (4.5%)
        Range: 2000 - 5000, Probability: Rare (0.5%)
        Range: 5000 - 10000, Probability: Severely rare (0.5%)
        '''
        weights_low = np.linspace(80, 0.01, int((500 - 200) / 0.01))
        weights_mid = np.linspace(15, 0.01, int((1000 - 500) / 0.01))
        weights_high = np.linspace(4.5, 0.01, int((2000 - 1000) / 0.01))
        weights_severe = np.linspace(0.5, 0.01, int((5000 - 2000) / 0.01))
        weights_super_rare = np.linspace(0.01, 0.001, int((10000 - 5000) / 0.01))
        weights = np.concatenate((weights_low, weights_mid, weights_high, weights_severe, weights_super_rare))
        neg_weights = np.resize(weights, len(self.neg_amounts))
        
        return neg_weights
    
    def calculate_weights(self):
        '''
        if self amount is positive use pos_calculate weights, else use neg_calculate_weights
        '''
        if self.generate_money_amount() > 0:
            return self.pos_calculate_weights()
        else:
            return self.neg_calculate_weights()

    def generate_money_amount(self):
        if random.randint(1, 4) == 1:
            amount = random.choices(self.neg_amounts, weights=self.neg_weights, k=1)[0] * -1
        else:
            amount = random.choices(self.amounts, weights=self.weights, k=1)[0]
        return round(amount, 2)
        
def send_webhook(webhook_url, payload):
    for keys in payload:
        payload[keys] = str(payload[keys])
    req = requests.Session()
    header = {"Content-Type": "application/json"}
    req.post(webhook_url, json=payload, headers=header)

if __name__ == "__main__":
    app = BrinksTruckApp()
    content = 'A Brinks truck has arrived in front of you, the rookie employee does not close the back door completely, leaving an oppurtunity of enormous fortune...'
    content2 = app.generate_money_amount()
    outcome = {
        '1': f'is able to loot the truck without anyone noticing. Total take ${content2}.',
        '2': f'attempts to loot the truck, someone has called the cops...  they seem about 2 minutes out; you start to load your trunk with as much cash as you can grab the cops are closing in... you get greedy grabbing more and more cash. You step out of the truck and you trip on your shoelaces! The cops are closing in you go to start your 1989 Geo Tracker and it wont start... Games over you have been jailed and bail was set you post bail and lose ${content2}.',
        '3': f'attempts to loot the truck, someone has called the cops...  they seem about 2 minutes out; you start to load your trunk with as much cash as you can grab the cops are closing in... you get greedy grabbing more and more cash. '
    }
    if content2 > 0:
        outcome = outcome['1']
    else:
        outcome = outcome['2']
    str(content2)
    
    payload = {"content": content, "content2": content2, "outcome": outcome}
    send_webhook(app.hook_url, payload)



