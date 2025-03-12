import tkinter as tk
import threading
import time
import random
from tkinter import ttk  # Für den Progressbar

# Spielvariablen
points = 0
click_power = 1
passive_income = 0
xp = 0  # Erfahrungspunkte für das Level
level = 1
running = True
multiplier_active = False
multiplier_duration = 0
prestige_level = 0
prestige_bonus = 0
achievements = []
shop_items = {"Klick-Multiplikator": 50, "Passives Einkommen Boost": 100}
quest = {"name": "Sammle 1000 Punkte", "completed": False}

# Upgradekosten
click_upgrade_cost = 10
passive_income_upgrade_cost = 20
company_upgrade_cost = 100
prestige_cost = 5000  # Prestigekosten

# XP benötigt, um zum nächsten Level aufzusteigen
xp_for_next_level = 100

# GUI initialisieren
def start_gui():
    global root, points_label, income_label, click_button, click_upgrade_button, passive_income_upgrade_button, company_upgrade_button, level_label, prestige_button, achievements_label, shop_button, quest_label, xp_bar

    root = tk.Tk()
    root.title("Idle Clicker Game")
    root.geometry("500x500")
    root.configure(bg="#282C34")  # Dunkler Hintergrund

    # Labels für Punkteanzeige und Level
    points_label = tk.Label(root, text=f"Punkte: {points}", font=("Arial", 16, "bold"), fg="white", bg="#282C34")
    points_label.pack(pady=10)

    income_label = tk.Label(root, text=f"+{passive_income} pro Sekunde", font=("Arial", 12), fg="lightgray", bg="#282C34")
    income_label.pack()

    level_label = tk.Label(root, text=f"Level: {level}", font=("Arial", 12), fg="lightgray", bg="#282C34")
    level_label.pack(pady=5)

    quest_label = tk.Label(root, text=f"Quest: {quest['name']}", font=("Arial", 12), fg="lightgray", bg="#282C34")
    quest_label.pack(pady=5)

    # XP Progress Bar (rot)
    xp_bar = ttk.Progressbar(root, length=200, mode="determinate", maximum=xp_for_next_level, style="TProgressbar")
    xp_bar.pack(pady=5)
    style = ttk.Style()
    style.configure("TProgressbar", thickness=30, troughcolor="#282C34", background="red")

    # Buttons
    click_button = tk.Button(root, text="Klick mich!", font=("Arial", 16), width=15, height=2, command=click, bg="white")
    click_button.pack(pady=10)

    click_upgrade_button = tk.Button(root, text=f"Klick-Upgrade ({click_upgrade_cost}P)", font=("Arial", 12), command=buy_click_upgrade)
    click_upgrade_button.pack(pady=5)

    passive_income_upgrade_button = tk.Button(root, text=f"Auto-Upgrade ({passive_income_upgrade_cost}P)", font=("Arial", 12), command=buy_passive_income_upgrade)
    passive_income_upgrade_button.pack(pady=5)

    company_upgrade_button = tk.Button(root, text=f"Firma-Upgrade ({company_upgrade_cost}P)", font=("Arial", 12), command=buy_company_upgrade)
    company_upgrade_button.pack(pady=5)

    prestige_button = tk.Button(root, text=f"Prestige (Kosten: {prestige_cost}P)", font=("Arial", 12), command=prestige)
    prestige_button.pack(pady=5)

    achievements_label = tk.Label(root, text=f"Erfolge: {', '.join(achievements)}", font=("Arial", 12), fg="lightgray", bg="#282C34")
    achievements_label.pack(pady=5)

    shop_button = tk.Button(root, text="Shop", font=("Arial", 12), command=open_shop)
    shop_button.pack(pady=5)

    # Starte passives Einkommen in einem separaten Thread
    threading.Thread(target=generate_passive_income, daemon=True).start()

    # Starte zufällige Ereignisse in einem separaten Thread
    threading.Thread(target=random_events, daemon=True).start()

    # Starte das Tkinter-Hauptloop
    root.mainloop()
    global running
    running = False  # Beende Hintergrundprozess, wenn Fenster geschlossen wird

# Klick-Funktion
def click():
    global points, xp
    points += click_power
    xp += 10  # XP für jeden Klick
    update_labels()
    # Quest-Überprüfung
    if points >= 1000 and not quest["completed"]:
        quest["completed"] = True
        achievements.append("Quest abgeschlossen: Sammle 1000 Punkte!")
    # Animation: Button kurz grün färben
    click_button.config(bg="#50C878")
    root.after(100, lambda: click_button.config(bg="white"))

# Passive Einkommen generieren
def generate_passive_income():
    global points
    while running:
        if passive_income > 0:
            points += passive_income
            xp += 5  # Kleinere XP für passives Einkommen
            update_labels()
        time.sleep(1)

# Zufällige Ereignisse
def random_events():
    global points, multiplier_active, multiplier_duration
    while running:
        if random.random() < 0.1:  # 10% Chance für ein Bonusereignis
            if not multiplier_active:
                multiplier_active = True
                multiplier_duration = 10  # 10 Sekunden
                print("Multiplikator aktiviert!")
        if multiplier_active:
            multiplier_duration -= 1
            if multiplier_duration <= 0:
                multiplier_active = False
                print("Multiplikator deaktiviert!")
        time.sleep(1)

# Upgrades kaufen
def buy_click_upgrade():
    global points, click_power, click_upgrade_cost
    if points >= click_upgrade_cost:
        points -= click_upgrade_cost
        click_power += 1
        click_upgrade_cost *= 2
        update_labels()
    else:
        print("Nicht genügend Punkte für Klick-Upgrade!")

def buy_passive_income_upgrade():
    global points, passive_income, passive_income_upgrade_cost
    if points >= passive_income_upgrade_cost:
        points -= passive_income_upgrade_cost
        passive_income += 1
        passive_income_upgrade_cost *= 2
        update_labels()
    else:
        print("Nicht genügend Punkte für Auto-Upgrade!")

def buy_company_upgrade():
    global points, passive_income, company_upgrade_cost
    if points >= company_upgrade_cost:
        points -= company_upgrade_cost
        passive_income += 5  # Erhöhe passives Einkommen durch Firmen-Upgrade
        company_upgrade_cost *= 2
        update_labels()
    else:
        print("Nicht genügend Punkte für Firmen-Upgrade!")

# Prestige-System
def prestige():
    global points, prestige_level, prestige_bonus
    if points >= prestige_cost:
        prestige_level += 1
        prestige_bonus += 0.1  # Beispiel: 10% Bonus auf Punkte pro Klick
        points = 0  # Punkte zurücksetzen
        update_labels()
    else:
        print("Nicht genügend Punkte für Prestige!")

# Shop-Funktion
def open_shop():
    global points
    if points >= shop_items["Klick-Multiplikator"]:
        points -= shop_items["Klick-Multiplikator"]
        global click_power
        click_power *= 2  # Temporärer Multiplikator
        print("Klick-Multiplikator aktiviert!")
    else:
        print("Nicht genügend Punkte für den Shop-Kauf!")
    update_labels()

# Labels & Buttons aktualisieren
def update_labels():
    points_label.config(text=f"Punkte: {points}")
    income_label.config(text=f"+{passive_income} pro Sekunde")
    level_label.config(text=f"Level: {level}")
    quest_label.config(text=f"Quest: {quest['name']} - {'Abgeschlossen' if quest['completed'] else 'Noch offen'}")
    achievements_label.config(text=f"Erfolge: {', '.join(achievements)}")
    click_upgrade_button.config(text=f"Klick-Upgrade ({click_upgrade_cost}P)")
    passive_income_upgrade_button.config(text=f"Auto-Upgrade ({passive_income_upgrade_cost}P)")
    company_upgrade_button.config(text=f"Firma-Upgrade ({company_upgrade_cost}P)")
    prestige_button.config(text=f"Prestige (Kosten: {prestige_cost}P)")
    shop_button.config(text=f"Shop (Klick-Multiplikator {shop_items['Klick-Multiplikator']}P)")

    # XP Fortschritt anzeigen
    update_xp_bar()

# XP Fortschritt-Balken aktualisieren
def update_xp_bar():
    global xp, xp_for_next_level, xp_bar
    progress = min(xp, xp_for_next_level)
    xp_bar["value"] = progress

    # Überprüfen auf Levelaufstieg
    level_up()

# Levelaufstieg
def level_up():
    global xp, level, xp_for_next_level
    if xp >= xp_for_next_level:  # XP erforderlich, um das nächste Level zu erreichen
        level += 1
        xp -= xp_for_next_level  # Abziehen der XP für den Levelaufstieg
        xp_for_next_level *= 1.2  # Erhöhe XP-Anforderungen für das nächste Level
        update_labels()

# Sicherstellen, dass Punkte nie negativ werden
def safe_subtract_points(amount):
    global points
    if points >= amount:
        points -= amount
    else:
        points = 0
    update_labels()

# GUI starten
start_gui()
