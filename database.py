import aiosqlite
import logging

logger = logging.getLogger(__name__)

class CatDataBase:

    def __init__(self, db_path : str = 'favourites.db'):
        self.db_path = db_path

    async def create_db(self):
        async with aiosqlite.connect(self.db_path) as conn:
            cursor = await conn.cursor()
            await cursor.execute('''
            CREATE TABLE IF NOT EXISTS favourites (
                id INTEGER PRIMARY KEY AUTOINCREMENT,       
                user_id INTEGER NOT NULL,
                file_id TEXT NOT NULL,
                UNIQUE(user_id, file_id)
) 
                                 ''')

            await conn.commit()
            logger.info('database initialized successfully')
    
    async def add_favourites(self, user_id, file_id):
        async with aiosqlite.connect(self.db_path) as conn:
            try:
                cursor = await conn.cursor()
                await cursor.execute(
                '''INSERT INTO favourites (user_id, file_id) VALUES (?, ?)''', 
                (user_id, file_id))
                await conn.commit()
                logger.info(f'cat added to favourites to user: {user_id}')
                return True
            except Exception as e:
                logger.error(f"error adding favourite: {e}")
                return False
