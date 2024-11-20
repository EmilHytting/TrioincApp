import json

def load_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

#Level System (Backend)
def update_user_level(cursor, db, user_id):
    cursor.execute("SELECT message_count, level FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()

    if result:
        message_count, level = result
        message_count += 1
        new_level = level
        
        if message_count >= 100 * new_level:
            new_level += 1
            print(f"User {user_id} is increased to level {new_level}")
        
        cursor.execute("UPDATE users SET message_count = ?, level = ? WHERE user_id = ?", (message_count, new_level, user_id))
    else:
        cursor.execute("INSERT INTO users (user_id, message_count, level) VALUES (?, 1, 1)", (user_id,))
        print(f"New user {user_id} added with level 1")

    db.commit()

