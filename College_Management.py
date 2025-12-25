import pandas as pd
from sqlalchemy import create_engine, text

# 1. Setup Connection
engine = create_engine("mysql+mysqlconnector://root:tiger@localhost/project_3")

def main():
    # --- Login System (Safety Lock) ---
    VALID_CREDENTIALS = {"sam": "Sam123"}
    max_attempts, attempts = 3, 0
    logged_in = False

    while attempts < max_attempts:
        username = input("Username: ").strip()
        password = input("Password: ")
        if VALID_CREDENTIALS.get(username) == password:
            print(f"Access Granted. Welcome {username}!")
            logged_in = True
            break
        attempts += 1
        print(f"Invalid! {max_attempts - attempts} left.")

    if not logged_in: return

    # --- Main Menu (Matching Demo Features) ---
    while True:
        print("\n--- COLLEGE MANAGEMENT SYSTEM ---")
        print("1. View Data\n2. Add Data\n3. Update Data\n4. Delete Data\n5. Manage Enrollments\n6. Exit")
        choice = input("Enter choice: ")

        if choice == '1':
            submenu("VIEW")
        elif choice == '2':
            submenu("ADD")
        elif choice == '3':
            update_data()
        elif choice == '4':
            delete_data()
        elif choice == '5':
            manage_enrollments()
        elif choice == '6':
            print("Goodbye!"); break

def submenu(mode):
    print(f"\nSelect Table to {mode}:")
    print("1. Course\n2. Enrollments\n3. Professors\n4. Student\n5. Back")
    ch = input("Enter (1-5): ")
    if ch == '5': return
    
    if mode == "VIEW": view_data(int(ch))
    else: add_data(int(ch))

def view_data(ch):
    tables = {1: "course", 2: "enrollments", 3: "proffessors", 4: "student"}
    t_name = tables.get(ch)
    if t_name:
        df = pd.read_sql(f"SELECT * FROM {t_name}", engine)
        print(f"\n--- {t_name.upper()} ---")
        print(df.to_string(index=False) if not df.empty else "Table is empty.")

def add_data(ch):
    config = {
        1: ("course", ["c_id", "C_name", "credits", "Department"]),
        2: ("enrollments", ["enrollment_id", "s_id", "c_id", "grade"]),
        3: ("proffessors", ["P_id", "p_name", "Department"]),
        4: ("student", ["S_id", "First_Name", "Last_Name", "Email", "Enrollement_date"])
    }
    t_name, cols = config[ch]
    all_entries = []
    print(f"Adding to {t_name}. Type 'stop' to finish.")

    while True:
        user_data = {}
        val = input(f"Enter {cols[0]}: ")
        if val.lower() == "stop": break
        user_data[cols[0]] = val
        for col in cols[1:]:
            user_data[col] = input(f"Enter {col}: ")
        all_entries.append(user_data)

    if all_entries:
        pd.DataFrame(all_entries).to_sql(t_name, engine, if_exists="append", index=False)
        print("Data Saved!")

def update_data():
    # Basic Update logic: Update Student Email by ID
    sid = input("Enter Student ID to update: ")
    new_email = input("Enter new Email: ")
    with engine.connect() as conn:
        conn.execute(text(f"UPDATE student SET Email = '{new_email}' WHERE S_id = {sid}"))
        conn.commit()
    print("Update Successful!")

def delete_data():
    # Basic Delete logic: Delete a record by ID
    table = input("Enter table name (student/course/proffessors): ")
    col_id = "S_id" if table == "student" else "c_id" if table == "course" else "P_id"
    val_id = input(f"Enter {col_id} to delete: ")
    with engine.connect() as conn:
        conn.execute(text(f"DELETE FROM {table} WHERE {col_id} = {val_id}"))
        conn.commit()
    print("Record Deleted!")

def manage_enrollments():
    # Join query to see which student is in which course
    query = """
    SELECT student.First_Name, course.C_name, enrollments.grade 
    FROM enrollments 
    JOIN student ON enrollments.s_id = student.S_id 
    JOIN course ON enrollments.c_id = course.c_id
    """
    df = pd.read_sql(query, engine)
    print("\n--- ENROLLMENT MANAGEMENT ---")
    print(df.to_string(index=False))

if __name__ == "__main__":
    main()