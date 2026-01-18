import json
import os
from datetime import datetime
import matplotlib.pyplot as plt

# ------------------ File paths ------------------
NGO_FILE = "ngos.json"
DONATION_FILE = "donations.json"

# ------------------ Default NGO data ------------------
default_ngos = [
    {"name": "Save the Earth", "cause": "Environment", "donations": 0},
    {"name": "Help Kids", "cause": "Education", "donations": 0},
    {"name": "Animal Care", "cause": "Animals", "donations": 0}
]

# ------------------ File operations ------------------

def load_ngos():
    if os.path.exists(NGO_FILE):
        with open(NGO_FILE, "r") as f:
            return json.load(f)
    return default_ngos.copy()

def save_ngos(ngos):
    with open(NGO_FILE, "w") as f:
        json.dump(ngos, f, indent=4)

def load_donations():
    if os.path.exists(DONATION_FILE):
        with open(DONATION_FILE, "r") as f:
            return json.load(f)
    return []

def save_donations(history):
    with open(DONATION_FILE, "w") as f:
        json.dump(history, f, indent=4)

# ------------------ NGO operations ------------------

def show_ngos(ngos):
    if not ngos:
        print("No NGOs available.")
        return

    ngos_sorted = sorted(ngos, key=lambda x: x["donations"], reverse=True)
    print("\n--- List of NGOs (Sorted by Donations) ---")
    for idx, ngo in enumerate(ngos_sorted, start=1):
        print(f"{idx}. {ngo['name']} | Cause: {ngo['cause']} | Donations: ${ngo['donations']}")

def add_ngo(ngos):
    name = input("Enter NGO name: ").strip()
    cause = input("Enter cause: ").strip()

    if name and cause:
        ngos.append({"name": name, "cause": cause, "donations": 0})
        save_ngos(ngos)
        print("NGO added successfully!")
    else:
        print("Name and cause cannot be empty.")

def delete_ngo(ngos):
    if not ngos:
        print("No NGOs to delete.")
        return

    print("\n--- NGOs ---")
    for i, ngo in enumerate(ngos, start=1):
        print(f"{i}. {ngo['name']}")

    try:
        choice = int(input("Enter NGO number to delete: "))
        if 1 <= choice <= len(ngos):
            removed = ngos.pop(choice - 1)
            save_ngos(ngos)
            print(f"NGO '{removed['name']}' deleted successfully!")
        else:
            print("Invalid choice.")
    except ValueError:
        print("Please enter a valid number.")

def search_by_cause(ngos):
    cause = input("Enter cause to search: ").strip().lower()
    results = [ngo for ngo in ngos if ngo["cause"].lower() == cause]

    if results:
        print("\n--- NGOs Found ---")
        for ngo in results:
            print(f"{ngo['name']} | Donations: ${ngo['donations']}")
    else:
        print("No NGOs found for this cause.")

# ------------------ Donation operations ------------------

def donate(ngos, history):
    if not ngos:
        print("No NGOs available.")
        return

    show_ngos(ngos)

    try:
        choice = int(input("Select NGO number: "))
        if not (1 <= choice <= len(ngos)):
            print("Invalid NGO selection.")
            return
    except ValueError:
        print("Enter a valid number.")
        return

    donor = input("Enter your name: ").strip()

    try:
        amount = float(input("Enter donation amount: $"))
        if amount <= 0:
            print("Amount must be greater than zero.")
            return
    except ValueError:
        print("Invalid amount.")
        return

    ngos[choice - 1]["donations"] += amount
    save_ngos(ngos)

    record = {
        "ngo": ngos[choice - 1]["name"],
        "donor": donor,
        "amount": amount,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    history.append(record)
    save_donations(history)

    print(f"\nThank you {donor}! Donation successful.")

    show_top_ngos_chart(ngos)

def show_top_ngos_chart(ngos):
    top_ngos = sorted(ngos, key=lambda x: x["donations"], reverse=True)[:3]
    names = [ngo["name"] for ngo in top_ngos]
    donations = [ngo["donations"] for ngo in top_ngos]

    plt.figure(figsize=(8, 5))
    plt.bar(names, donations, color="skyblue")
    plt.title("Top 3 NGOs by Donations")
    plt.xlabel("NGO")
    plt.ylabel("Total Donations ($)")
    plt.grid(axis="y", linestyle="--", alpha=0.6)

    plt.savefig("top_ngos.png")
    plt.show()

# ------------------ Donation History ------------------

def show_donations(history):
    if not history:
        print("No donation history.")
        return

    print("\n--- Donation History ---")
    for i, d in enumerate(history, start=1):
        print(f"{i}. {d['donor']} donated ${d['amount']} to {d['ngo']} on {d['date']}")

def search_donations(history):
    if not history:
        print("No donation history.")
        return

    print("1. Search by donor")
    print("2. Search by NGO")
    choice = input("Choose option: ")

    if choice == "1":
        name = input("Enter donor name: ").lower()
        results = [d for d in history if d["donor"].lower() == name]
    elif choice == "2":
        ngo = input("Enter NGO name: ").lower()
        results = [d for d in history if d["ngo"].lower() == ngo]
    else:
        print("Invalid choice.")
        return

    if results:
        for d in results:
            print(f"{d['donor']} donated ${d['amount']} to {d['ngo']} on {d['date']}")
    else:
        print("No records found.")

# ------------------ Main Menu ------------------

def main_menu():
    ngos = load_ngos()
    history = load_donations()

    while True:
        print("\n--- NGO Wizard ---")
        print("1. View NGOs")
        print("2. Donate")
        print("3. Add NGO")
        print("4. Delete NGO")
        print("5. Search NGOs by cause")
        print("6. View donation history")
        print("7. Search donation history")
        print("8. Exit")

        choice = input("Enter choice (1-8): ")

        if choice == "1":
            show_ngos(ngos)
        elif choice == "2":
            donate(ngos, history)
        elif choice == "3":
            add_ngo(ngos)
        elif choice == "4":
            delete_ngo(ngos)
        elif choice == "5":
            search_by_cause(ngos)
        elif choice == "6":
            show_donations(history)
        elif choice == "7":
            search_donations(history)
        elif choice == "8":
            print("Goodbye! 👋")
            break
        else:
            print("Invalid option.")

# ------------------ Run Program ------------------

if __name__ == "__main__":
    main_menu()
