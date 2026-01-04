import random
import pandas as pd

# -----------------------------
# Message templates
# -----------------------------

scam_messages = [
    "Your UPI account is temporarily blocked. Verify immediately",
    "Refund failed. Click the link to re-initiate UPI payment",
    "Unauthorized transaction detected. Confirm now",
    "KYC expired. Update details to avoid UPI suspension",
    "You have received cashback. Claim now",
    "UPI reward pending. Click to receive",
    "Payment reversal failed. Act immediately"
]

safe_messages = [
    "₹{amount} received via UPI",
    "Paid ₹{amount} to merchant successfully",
    "UPI payment of ₹{amount} completed",
    "Transaction successful. Ref ID generated",
    "Money received from {name}",
    "Payment of ₹{amount} debited from account"
]

names = ["Rahul", "Amit", "Sneha", "Priya", "Ankit", "Rohit"]

sender_types = ["bank", "merchant", "unknown"]

# -----------------------------
# Data generation
# -----------------------------

data = []

for _ in range(1500):
    is_scam = random.choice([0, 1])

    if is_scam:
        message = random.choice(scam_messages)
        amount = random.randint(2000, 50000)
        sender = "unknown"
        label = "scam"
    else:
        template = random.choice(safe_messages)
        amount = random.randint(50, 5000)
        message = template.format(
            amount=amount,
            name=random.choice(names)
        )
        sender = random.choice(["bank", "merchant"])
        label = "safe"

    data.append({
        "message": message,
        "amount": amount,
        "sender_type": sender,
        "label": label
    })

# -----------------------------
# Save to CSV
# -----------------------------

df = pd.DataFrame(data)
df.to_csv("../dataset/scam_messages.csv", index=False)

print("✅ Synthetic UPI scam dataset generated successfully!")
print(df.head())
