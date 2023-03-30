import sqlite3

from app import *

conn = sqlite3.connect('warnings.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS warnings (
    user_id INTEGER PRIMARY KEY,
    first_name TEXT,
    count INTEGER,
    last_warned TIMESTAMP DEFAULT NULL,
    message_text TEXT
)
''')
conn.commit()


WARNING_LIMIT = 3
MUTE_DURATION = 1


def get_warning_count(user_id):
    cursor.execute('SELECT count FROM warnings WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        return 0

def increment_warning_count(first_name, user_id, message_text):
    current_time = datetime.now()
    warning_count = get_warning_count(user_id) + 1
    cursor.execute('SELECT message_text FROM warnings WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    if result is not None:
        # If the user already has a message, append the new message to it
        message_text = result[0] + "\n" + message_text
        cursor.execute('''
            UPDATE warnings
            SET count = ?, last_warned = ?, message_text = ?
            WHERE user_id = ?
        ''', (warning_count, current_time, message_text, user_id))
    if result is None:
        # If the user doesn't have a message yet, insert a new record
        cursor.execute('''
            INSERT INTO warnings (user_id, first_name, count, last_warned, message_text)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, first_name, warning_count, current_time, message_text))
    conn.commit()

async def mute_user(chat_id, user_id):
    mute_time = datetime.now() + timedelta(days=MUTE_DURATION)
    await bot.restrict_chat_member(chat_id, user_id,
                                   types.ChatPermissions(can_send_messages=False),
                                   until_date=mute_time.timestamp())

async def warning_to_zero(user_id):
    cursor.execute('''
        UPDATE warnings
        SET count = 0
        WHERE user_id = ?
        ''', (user_id,))
    conn.commit()

async def update_sheet():
    cursor.execute("SELECT user_id, first_name, count, last_warned, message_text FROM warnings")
    rows = cursor.fetchall()
    # Iterate through the rows and insert the values into the worksheet
    for row_index, row in enumerate(rows):
        for col_index, value in enumerate(row):
            cell = worksheet.cell((row_index + 1, col_index + 1))
            cell.value = value