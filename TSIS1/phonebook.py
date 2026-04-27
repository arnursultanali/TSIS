import json
import csv
import psycopg2
import os  
from config import db_params


def export_to_json():
    #Exports all contacts, their groups, and multiple phone numbers into a structured JSON file.

    conn = psycopg2.connect(**db_params)
    try:
        cur = conn.cursor()
        # Using JSON aggregation to fetch contacts with their nested phones
        cur.execute("""
            SELECT c.first_name, c.email, c.birthday, g.name, 
                   json_agg(json_build_object('number', p.phone, 'type', p.type)) FILTER (WHERE p.phone IS NOT NULL)
            FROM contacts c
            LEFT JOIN groups g ON c.group_id = g.id
            LEFT JOIN phones p ON c.id = p.contact_id
            GROUP BY c.id, g.name
        """)
        rows = cur.fetchall()

        data = []
        for r in rows:
            data.append({
                "name": r[0],
                "email": r[1],
                "birthday": str(r[2]) if r[2] else None,
                "group": r[3],
                "phones": r[4] if r[4] else []
            })

        with open('contacts.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        print("Data successfully exported to contacts.json")
    finally:
        conn.close()


def import_from_json():
    #Imports contacts from JSON.Handles duplicates by asking the user to skip or overwrite.

    try:
        with open('contacts.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Error: contacts.json not found.")
        return

    conn = psycopg2.connect(**db_params)
    try:
        cur = conn.cursor()
        for item in data:
            cur.execute("SELECT id FROM contacts WHERE first_name = %s", (item['name'],))
            exists = cur.fetchone()

            if exists:
                choice = input(f"Contact '{item['name']}' exists. Overwrite? (y/n): ")
                if choice.lower() != 'y':
                    continue
                cur.execute("DELETE FROM contacts WHERE first_name = %s", (item['name'],))

            # Handle group logic
            group_id = None
            if item.get('group'):
                cur.execute("INSERT INTO groups (name) VALUES (%s) ON CONFLICT (name) DO NOTHING", (item['group'],))
                cur.execute("SELECT id FROM groups WHERE name = %s", (item['group'],))
                group_id = cur.fetchone()[0]

            # Insert contact and phones
            cur.execute("""
                INSERT INTO contacts (first_name, email, birthday, group_id) 
                VALUES (%s, %s, %s, %s) RETURNING id
            """, (item['name'], item['email'], item['birthday'], group_id))
            c_id = cur.fetchone()[0]

            for p in item.get('phones', []):
                if p.get('number'):
                    cur.execute("INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s)",
                                (c_id, p['number'], p['type']))
        conn.commit()
        print("JSON Import completed!")
    finally:
        conn.close()

def import_from_csv(file_path='contacts.csv'):
    # Проверяем, есть ли файл в текущей папке. Если нет — ищем в TSIS1/
    if not os.path.exists(file_path):
        alt_path = os.path.join('TSIS1', file_path)
        if os.path.exists(alt_path):
            file_path = alt_path
        else:
            print(f"Error: {file_path} not found.")
            return

    conn = psycopg2.connect(**db_params)
    try:
        cur = conn.cursor()
        with open(file_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Handle Group
                group_id = None
                if row['group']:
                    cur.execute("INSERT INTO groups (name) VALUES (%s) ON CONFLICT (name) DO NOTHING", (row['group'],))
                    cur.execute("SELECT id FROM groups WHERE name = %s", (row['group'],))
                    group_id = cur.fetchone()[0]

                # Insert Contact
                cur.execute("""
                    INSERT INTO contacts (first_name, email, birthday, group_id)
                    VALUES (%s, %s, %s, %s) RETURNING id
                """, (row['first_name'], row['email'], row['birthday'] if row['birthday'] else None, group_id))
                c_id = cur.fetchone()[0]

                # Insert Phone
                if row['phone']:
                    cur.execute("INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s)",
                                (c_id, row['phone'], row['phone_type']))
        conn.commit()
        print(f"CSV Import from '{file_path}' completed!")
    finally:
        conn.close()
# --------------------------------

def console_pagination():
    #Console loop for paginated navigation (next/prev).

    page = 0
    limit = 5
    conn = psycopg2.connect(**db_params)
    try:
        while True:
            cur = conn.cursor()
            cur.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (limit, page * limit))
            results = cur.fetchall()

            if not results and page > 0:
                print("\nNo more records.")
                page -= 1
                continue

            print(f"\n--- Page {page + 1} ---")
            for r in results: print(r)

            move = input("\n[n] Next, [p] Prev, [q] Quit: ").lower()
            if move == 'n':
                page += 1
            elif move == 'p' and page > 0:
                page -= 1
            elif move == 'q':
                break
    finally:
        conn.close()


def main_menu():
    #Basic console interface to run the tasks.

    while True:
        print("\n--- PhoneBook Extended Menu ---")
        print("1. Export to JSON")
        print("2. Import from JSON")
        print("3. Import from CSV (KZ)")
        print("4. View Contacts (Pagination)")
        print("5. Exit")

        choice = input("Select an option: ")
        if choice == '1':
            export_to_json()
        elif choice == '2':
            import_from_json()
        elif choice == '3':
            import_from_csv()
        elif choice == '4':
            console_pagination()
        elif choice == '5':
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main_menu()