import sqlite3


class Database:
    def __init__(self):
        self.conn = sqlite3.connect('/database/database.db')
        self.cur = self.conn.cursor()

        if not self.is_setup():
            self.setup()

    def setup(self):
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS songs (
                video_id TEXT,
                name TEXT,
                artist TEXT,
                album TEXT
            )
        ''')

        self.cur.execute('''CREATE UNIQUE INDEX IF NOT EXISTS video_id_index ON songs (video_id)''')

        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS view (
                video_id TEXT,
                date TEXT
            )
        ''')

        self.cur.execute('''CREATE UNIQUE INDEX IF NOT EXISTS video_id_date_index ON view (video_id, date)''')

    def is_setup(self) -> bool:
        self.cur.execute('''SELECT name FROM sqlite_master WHERE type='table' AND name='songs' ''')
        return self.cur.fetchone() is not None

    def add_song(self, video_id: str, name: str, artist: str, album: str) -> bool:
        try:
            self.cur.execute('''INSERT INTO songs VALUES (?, ?, ?, ?)''', (video_id, name, artist, album))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def add_view(self, video_id: str, date: str):
        try:
            self.cur.execute('''INSERT INTO view VALUES (?, ?)''', (video_id, date))
            self.conn.commit()
        except sqlite3.IntegrityError:
            pass

    def get_stats(self):
        self.cur.execute('''SELECT COUNT(*) FROM songs''')
        song_count = self.cur.fetchone()[0]

        self.cur.execute('''SELECT COUNT(*) FROM view''')
        view_count = self.cur.fetchone()[0]

        return song_count, view_count
