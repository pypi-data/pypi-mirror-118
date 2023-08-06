#Donation Alerts v1.0.0
#by @cxldxice

from time import sleep
import threading
import requests

from .authorization import Authorization


class DonationAlerts(object):
    def __init__(self, token) -> None:
        self.handlers = []
        self.token = token

    def handler(self, func):
        self.handlers.append(func)
    
    def get(self, show_last=False):
        donations = []

        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        donate = requests.get(url="https://www.donationalerts.com/api/v1/alerts/donations", headers=headers).json()

        for data in donate["data"]:
            donations_data = {
                "id": data["id"],
                "username": data["username"],
                "message": data["message"],
                "amount": data["amount"],
                "currency": data["currency"],
                "amount_in_account_currency": data["amount_in_user_currency"],
                "date": data["created_at"]
            }

            donations.append(donations_data)

        if show_last:
            return donations[0]

        return donations

    def __polling(self):
        last_id = self.get(show_last=True)["id"]

        while True:
            donation = self.get(show_last=True)

            if donation["id"] != last_id:
                last_id = donation["id"]

                for handler in self.handlers:
                    handler(donation)
                
                
            

    def polling(self, in_this_thread=True):
        if not in_this_thread:
            threading.Thread(target=self.__polling).start()

            return

        self.__polling()