# Get token
## Get client_id and client_secret - [here](https://www.donationalerts.com/application/clients)
```python
import donationalerts

auth = donationalerts.Authorization("CLIENT_ID", "CLIENT_SECRET")
auth.start_authorization()
```

# Test application
## Donation notifer
```python
import donationalerts
import win10toast

token = "YOUR_TOKEN_HERE"
donation = donationalerts.DonationAlerts(token)
notify = win10toast.ToastNotifier()


@donation.handler
def on_donate(donation_data):
    notify.show_toast(
        title=f"{donation_data['username']} donated {donation_data['amount']}{donation_data['currency']}!",
        msg=donation_data["message"],
        duration=10
    )


if __name__ == "__main__":
    donation.polling()
```

> by @cxldxice with ♥