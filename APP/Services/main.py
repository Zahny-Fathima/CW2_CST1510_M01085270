from app.data.users import migrate_users_from_file

def main():
    conn = connect_database()
    create_tables(conn)

     
    migrate_users_from_file()

