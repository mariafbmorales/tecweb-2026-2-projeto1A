import sqlite3
from dataclasses import dataclass


@dataclass
class Note:
    id: int = None
    title: str = None
    content: str = ''
    favorite: int = 0

class Database():
    def __init__(self, nome):
        self.conn = sqlite3.connect(nome + '.db')
        self.conn.execute(
            '''
            CREATE TABLE IF NOT EXISTS note (
                id INTEGER PRIMARY KEY,
                title TEXT,
                content TEXT NOT NULL
            );
            '''
        )
        try:
            self.conn.execute('ALTER TABLE note ADD COLUMN favorite INTEGER NOT NULL DEFAULT 0;')
            self.conn.commit()
        except sqlite3.OperationalError:
            pass

    def add(self, note):
        self.conn.execute(
            '''
            INSERT INTO note (title, content)
            VALUES (?, ?);
            ''',
            (note.title, note.content)
        )
        self.conn.commit()

    def get_all(self):
        cursor = self.conn.execute(
            '''
            SELECT id, title, content, favorite FROM note
            ORDER BY favorite DESC, id ASC
            '''
        )

        notes = []

        for linha in cursor:
            note = Note(
                id=linha[0],
                title=linha[1],
                content=linha[2],
                favorite=linha[3]
            )
            notes.append(note)

        return notes

    def get_by_id(self, note_id):
        cursor = self.conn.execute(
            '''
            SELECT id, title, content, favorite FROM note
            WHERE id = ?;
            ''',
            (note_id,)
        )

        linha = cursor.fetchone()

        if linha is None:
            return None

        return Note(
            id=linha[0],
            title=linha[1],
            content=linha[2],
            favorite=linha[3]
        )


    def update(self, entry):
        self.conn.execute(
            '''
            UPDATE note
            SET title = ?, content = ?
            WHERE id = ?;
            ''',
            (entry.title, entry.content, entry.id)
        )
        self.conn.commit()
    
    def delete(self, note_id):
        self.conn.execute(
            '''
            DELETE FROM note
            WHERE id = ?;
            ''',
            (note_id,)
        )
        self.conn.commit()

    def toggle_favorite(self, note_id):
        self.conn.execute(
            '''
            UPDATE note
            SET favorite = 1 - favorite
            WHERE id = ?;
            ''',
            (note_id,)
        )
        self.conn.commit()