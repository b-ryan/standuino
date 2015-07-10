import sqlite3


def create_table(cursor):
    cursor.execute('''
        CREATE TABLE standuino_states (
            id integer primary key,
            description text
        )
    ''')


def save_state(state):
    conn = sqlite3.connect('standuino.sqlite')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO standuino_states (description)
        VALUES (?)
    ''', (state.description,))
    state.id = cursor.lastrowid

    conn.commit()
    cursor.close()
    conn.close()

    return state
