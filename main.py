import os
import datetime

# ---------------- FILE SETUP ----------------
FILES = [
    "parking_spaces.txt",
    "vehicles.txt",
    "permits.txt",
    "entries.txt",
    "logs.txt",
    "passes.txt",
    "permit_types.txt"
]

def initialize_files():
    for file in FILES:
        if not os.path.exists(file):
            open(file, "w").close()

# ---------------- FILE FUNCTIONS ----------------
def read_file(file):
    data = []
    try:
        with open(file, "r") as f:
            for line in f:
                data.append(line.strip())
    except:
        print("Error reading file:", file)
    return data

def write_file(file, data):
    try:
        with open(file, "a") as f:
            f.write(data + "\n")
    except:
        print("Error writing to file:", file)

# ---------------- ADMIN FUNCTIONS ----------------
def add_parking_space():
    sid = input("Space ID: ").strip()
    stype = input("Type (Regular/Reserved/Electric): ").strip()
    if not sid:
        print("Invalid ID")
        return
    spaces = read_file("parking_spaces.txt")
    for s in spaces:
        if s.startswith(sid + ","):
            print("Space already exists")
            return
    write_file("parking_spaces.txt", f"{sid},{stype},free")
    print("Space added")

def remove_parking_space():
    sid = input("Enter Space ID to remove: ").strip()
    confirm = input("Are you sure? (y/n): ").lower()
    if confirm != "y":
        print("Cancelled")
        return
    spaces = read_file("parking_spaces.txt")
    new_spaces = [s for s in spaces if not s.startswith(sid + ",")]
    with open("parking_spaces.txt", "w") as f:
        for s in new_spaces: f.write(s + "\n")
    print("Space removed")

def update_parking_space():
    sid = input("Space ID: ").strip()
    new_type = input("New Type: ").strip()
    new_status = input("Status (free/occupied): ").strip()
    spaces = read_file("parking_spaces.txt")
    new_spaces = []
    for s in spaces:
        id, typ, status = s.split(",")
        if id == sid:
            new_spaces.append(f"{sid},{new_type},{new_status}")
        else:
            new_spaces.append(s)
    with open("parking_spaces.txt", "w") as f:
        for s in new_spaces: f.write(s + "\n")
    print("Space updated")

def add_permit_type():
    ptype = input("Permit type (daily/monthly/annual): ").strip()
    price = input("Price: ").strip()
    write_file("permit_types.txt", f"{ptype},{price}")
    print("Permit type added")

def update_permit_price():
    ptype = input("Permit type to update: ").strip()
    price = input("New price: ").strip()
    types = read_file("permit_types.txt")
    new_types = []
    for t in types:
        typ, pr = t.split(",")
        if typ == ptype:
            new_types.append(f"{ptype},{price}")
        else:
            new_types.append(t)
    with open("permit_types.txt", "w") as f:
        for t in new_types: f.write(t + "\n")
    print("Price updated")

def generate_report():
    spaces = read_file("parking_spaces.txt")
    permits = read_file("permits.txt")
    total = len(spaces)
    free = sum(1 for s in spaces if s.split(",")[2] == "free")
    print("\n--- REPORT ---")
    print("Total spaces:", total)
    print("Available:", free)
    print("Occupied:", total - free)
    print("Total permits:", len(permits))

def view_all_records():
    print("\n--- Parking Spaces ---")
    for s in read_file("parking_spaces.txt"): print(s)
    print("\n--- Vehicles ---")
    for v in read_file("vehicles.txt"): print(v)
    print("\n--- Permits ---")
    for p in read_file("permits.txt"): print(p)
    print("\n--- Logs ---")
    for l in read_file("logs.txt"): print(l)

# ---------------- STAFF FUNCTIONS ----------------
def check_availability():
    spaces = read_file("parking_spaces.txt")
    print("\nAvailable Spaces:")
    for s in spaces:
        sid, typ, status = s.split(",")
        if status == "free": print(sid, typ)

def record_entry():
    plate = input("Vehicle plate: ").strip()
    spaces = read_file("parking_spaces.txt")
    assigned = None
    new_spaces = []
    for s in spaces:
        sid, typ, status = s.split(",")
        if status == "free" and assigned is None:
            assigned = sid
            new_spaces.append(f"{sid},{typ},occupied")
        else:
            new_spaces.append(s)
    if assigned is None:
        print("No space available")
        return
    with open("parking_spaces.txt", "w") as f:
        for s in new_spaces: f.write(s + "\n")
    entry_time = str(datetime.datetime.now())
    write_file("entries.txt", f"{plate},{assigned},{entry_time}")
    print("Vehicle parked at", assigned)

def record_exit():
    plate = input("Plate number: ").strip()
    entries = read_file("entries.txt")
    new_entries = []
    sid = entry_time = None
    for e in entries:
        p, s, t = e.split(",")
        if p == plate:
            sid = s
            entry_time = t
        else:
            new_entries.append(e)
    with open("entries.txt", "w") as f:
        for e in new_entries: f.write(e + "\n")
    spaces = read_file("parking_spaces.txt")
    new_spaces = []
    for s in spaces:
        id, typ, status = s.split(",")
        if id == sid: new_spaces.append(f"{id},{typ},free")
        else: new_spaces.append(s)
    with open("parking_spaces.txt", "w") as f:
        for s in new_spaces: f.write(s + "\n")
    exit_time = str(datetime.datetime.now())
    write_file("logs.txt", f"{plate},{sid},{entry_time},{exit_time}")
    print("Vehicle exited")

def issue_temporary_pass():
    plate = input("Plate: ").strip()
    fee = input("Fee: ").strip()
    validity = input("Valid until: ").strip()
    write_file("passes.txt", f"{plate},{fee},{validity}")
    print("Temporary pass issued")

def view_daily_logs():
    today = str(datetime.date.today())
    print("\nToday's Logs:")
    for l in read_file("logs.txt"):
        if today in l: print(l)

# ---------------- VEHICLE OWNER ----------------
def register_vehicle():
    plate = input("Plate: ").strip()
    model = input("Model: ").strip()
    color = input("Color: ").strip()
    write_file("vehicles.txt", f"{plate},{model},{color}")
    print("Vehicle registered")

def request_permit():
    plate = input("Plate: ").strip()
    owner = input("Owner: ").strip()
    ptype = input("Permit type: ").strip()
    expiry = input("Expiry date: ").strip()
    write_file("permits.txt", f"{plate},{owner},{ptype},{expiry},pending")
    print("Permit request submitted")

def view_permit_status():
    plate = input("Plate: ").strip()
    found = False
    for p in read_file("permits.txt"):
        data = p.split(",")
        if data[0] == plate:
            print("Owner:", data[1])
            print("Permit:", data[2])
            print("Expiry:", data[3])
            print("Status:", data[4])
            found = True
            break
    if not found: print("No permit found")

def view_parking_history():
    plate = input("Plate: ").strip()
    for l in read_file("logs.txt"):
        if l.startswith(plate): print(l)

# ---------------- PERMIT OFFICER ----------------
def issue_permit():
    plate = input("Plate: ").strip()
    owner = input("Owner: ").strip()
    ptype = input("Permit type: ").strip()
    expiry = input("Expiry date: ").strip()
    write_file("permits.txt", f"{plate},{owner},{ptype},{expiry},approved")
    print("Permit issued")

def renew_permit():
    plate = input("Plate: ").strip()
    new_expiry = input("New expiry: ").strip()
    permits = read_file("permits.txt")
    new_permits = []
    for p in permits:
        data = p.split(",")
        if data[0] == plate:
            new_permits.append(f"{data[0]},{data[1]},{data[2]},{new_expiry},{data[4]}")
        else:
            new_permits.append(p)
    with open("permits.txt", "w") as f:
        for p in new_permits: f.write(p + "\n")
    print("Permit renewed")

def cancel_permit():
    plate = input("Plate: ").strip()
    permits = read_file("permits.txt")
    new_permits = []
    for p in permits:
        data = p.split(",")
        if data[0] == plate:
            data[4] = "cancelled"
            new_permits.append(",".join(data))
        else:
            new_permits.append(p)
    with open("permits.txt", "w") as f:
        for p in new_permits: f.write(p + "\n")
    print("Permit cancelled")

def update_permit():
    plate = input("Plate number to update: ").strip()
    permits = read_file("permits.txt")
    new_permits = []
    found = False
    for p in permits:
        data = p.split(",")
        if data[0] == plate:
            print("Current Permit Info:", data)
            new_owner = input(f"New Owner ({data[1]}): ").strip() or data[1]
            new_type = input(f"New Permit Type ({data[2]}): ").strip() or data[2]
            new_expiry = input(f"New Expiry ({data[3]}): ").strip() or data[3]
            new_status = input(f"New Status ({data[4]}): ").strip() or data[4]
            new_permits.append(f"{plate},{new_owner},{new_type},{new_expiry},{new_status}")
            found = True
        else:
            new_permits.append(p)
    if not found:
        print("No permit found with that plate number")
        return
    with open("permits.txt", "w") as f:
        for p in new_permits: f.write(p + "\n")
    print("Permit updated successfully")

def view_permit_list():
    for p in read_file("permits.txt"): print(p)

# ---------------- MENUS ----------------
def admin_menu():
    while True:
        print("\nADMIN MENU")
        print("1 Add Space")
        print("2 Remove Space")
        print("3 Update Space")
        print("4 Add Permit Type")
        print("5 Update Permit Price")
        print("6 Generate Report")
        print("7 View All Records")
        print("8 Back")
        c = input("Choice: ").strip()
        if c == "1": add_parking_space()
        elif c == "2": remove_parking_space()
        elif c == "3": update_parking_space()
        elif c == "4": add_permit_type()
        elif c == "5": update_permit_price()
        elif c == "6": generate_report()
        elif c == "7": view_all_records()
        elif c == "8": break

def staff_menu():
    while True:
        print("\nSTAFF MENU")
        print("1 Check Availability")
        print("2 Record Entry")
        print("3 Record Exit")
        print("4 Temporary Pass")
        print("5 View Daily Logs")
        print("6 Back")
        c = input("Choice: ").strip()
        if c == "1": check_availability()
        elif c == "2": record_entry()
        elif c == "3": record_exit()
        elif c == "4": issue_temporary_pass()
        elif c == "5": view_daily_logs()
        elif c == "6": break

def owner_menu():
    while True:
        print("\nOWNER MENU")
        print("1 Register Vehicle")
        print("2 Request Permit")
        print("3 View Permit Status")
        print("4 Parking History")
        print("5 Back")
        c = input("Choice: ").strip()
        if c == "1": register_vehicle()
        elif c == "2": request_permit()
        elif c == "3": view_permit_status()
        elif c == "4": view_parking_history()
        elif c == "5": break

def permit_officer_menu():
    while True:
        print("\nPERMIT OFFICER MENU")
        print("1 Issue Permit")
        print("2 Renew Permit")
        print("3 Cancel Permit")
        print("4 Update Permit")
        print("5 View Permit List")
        print("6 Back")
        c = input("Choice: ").strip()
        if c == "1": issue_permit()
        elif c == "2": renew_permit()
        elif c == "3": cancel_permit()
        elif c == "4": update_permit()
        elif c == "5": view_permit_list()
        elif c == "6": break

# ---------------- MAIN ----------------
def main():
    initialize_files()
    while True:
        print("\nPARKING LOT MANAGEMENT SYSTEM")
        print("1 Administrator")
        print("2 Parking Staff")
        print("3 Vehicle Owner")
        print("4 Permit Officer")
        print("5 Exit")
        c = input("Choice: ").strip()
        if c == "1": admin_menu()
        elif c == "2": staff_menu()
        elif c == "3": owner_menu()
        elif c == "4": permit_officer_menu()
        elif c == "5":
            print("System Closed")
            break

main()
