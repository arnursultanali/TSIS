import psycopg2
import sys

class Database:
    
    def __init__(self, config):
        try:
            self.conn = psycopg2.connect(**config)
            self.cur = self.conn.cursor() # Добавили курсор как атрибут для удобства
            self.create_tables()
            print("Successfully connected to PostgreSQL")
        except psycopg2.OperationalError as e:
            print(f"Database connection error: {e}")
            print("\nCheck your password in config.py!")
            sys.exit()

    def create_tables(self):
        with self.conn.cursor() as cur:
            # Создаем таблицы для игроков 
            cur.execute("""
                CREATE TABLE IF NOT EXISTS snake_users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    score INTEGER DEFAULT 0,
                    level INTEGER DEFAULT 1
                );
            """)
        self.conn.commit()

    def get_user(self, username):
        """Получает текущий счет и уровень игрока (нужно для main.py)."""
        query = "SELECT score, level FROM snake_users WHERE username = %s"
        self.cur.execute(query, (username,))
        return self.cur.fetchone()

    def create_user(self, username):
        """Создает нового пользователя, если его нет в базе."""
        query = "INSERT INTO snake_users (username, score, level) VALUES (%s, 0, 1) ON CONFLICT DO NOTHING"
        self.cur.execute(query, (username,))
        self.conn.commit()

    def update_user_progress(self, username, score, level):
        """Обновляет прогресс игрока (вызывается при проигрыше или выходе)."""
        query = "UPDATE snake_users SET score = %s, level = %s WHERE username = %s"
        self.cur.execute(query, (score, level, username))
        self.conn.commit()


    def save_result(self, username, score, level):
        self.create_user(username)
        self.update_user_progress(username, score, level)

    def __del__(self):
        # Закрываем соединение при удалении объекта
        if hasattr(self, 'conn'):
            self.conn.close()