import sqlite3
from datetime import datetime
import re

class VideoCommentTracker:
    def __init__(self, db_path='video_comments.db'):
        self.conn = sqlite3.connect(db_path)
        self._init_db()

    def _init_db(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS commented_videos (
                video_id TEXT PRIMARY KEY,
                comment_text TEXT,
                timestamp DATETIME,
                username TEXT
            )
        ''')
        self.conn.commit()

    def extract_video_id(self, input_str):
        """Извлекает ID видео из строки или URL"""
        if not input_str:
            return None

        # Для формата "id 7446335094186446122?q=axis"
        match = re.search(r'(?:id|video)[/\s](\d+)', input_str)
        if match:
            return match.group(1)

        # Для URL типа https://www.tiktok.com/@user/video/123456789
        if '/video/' in input_str:
            return input_str.split('/video/')[1].split('?')[0]

        return None

    def already_commented(self, video_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT 1 FROM commented_videos WHERE video_id = ?', (video_id,))
        return cursor.fetchone() is not None

    def mark_as_commented(self, video_id, comment_text, username):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO commented_videos 
                (video_id, comment_text, timestamp, username)
                VALUES (?, ?, ?, ?)
            ''', (video_id, comment_text, datetime.now(), username))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def close(self):
        self.conn.close()