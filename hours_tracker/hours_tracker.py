import pandas as pd
from datetime import datetime as dt
import os

class TimeCard:
    def __init__(self, name):
        self.name = name
        self.hours = pd.DataFrame(columns=['date', 'in', 'out'])
        if os.path.exists(f'hours_{self.name}.csv'):
            self.hours = pd.read_csv(f'hours_{self.name}.csv')

    def punch_in(self, in_time: str) -> None:
        new_entry = pd.DataFrame(
            [{'date': str(dt.today().strftime('%m/%d/%Y')),
              'in': in_time,
              'out': ' '
              }]
        )
        self.hours = pd.concat([self.hours, new_entry], ignore_index=True)
        self.hours.to_csv(f'hours_{self.name}.csv', index=False)

    def punch_out(self, out_time: str) -> None:
        self.hours[self.hours['date'] == str(dt.today().strftime('%m/%d/%Y'))] = out_time
        self.hours.to_csv(f'hours_{self.name}.csv', index=False)

    def load(self):
        1 == 1

