import aiomysql
import asyncio


from yoyo import read_migrations
from yoyo import get_backend

from logging import getLogger
_log = getLogger(__name__)


def setup(app=None, options=None):
    db = Db(app=app, options=options)
    return db.setup()


class Db:
    def __init__(self, app=None, options=None):
        self.conn = None
        self._app = app
        self._options = options

    def setup(self, app=None, options=None):
        try:
            backend = get_backend(
                'mysql://{}:{}@localhost/{}'.format(self._options.db_user,
                                                    self._options.db_password,
                                                    self._options.db_name)
            )
        except Exception as e:
            _log.error(f'Unable to open database: {e}')
            return None

        migrations = read_migrations(self._options.db_migrations_dir)

        try:
            with backend.lock():
                backend.apply_migrations(backend.to_apply(migrations))
        except Exception as e:
            _log.error(f'Database Migration went wrong: {e}')
            return None

        loop = asyncio.get_event_loop()
        try:
            self.conn = loop.run_until_complete(aiomysql.connect(
                user=self._options.db_user,
                password=self._options.db_password,
                db=self._options.db_name,
                cursorclass=aiomysql.DictCursor))
        except Exception as e:
            _log.error(f'Unable to connect to database: {e}')
            return None
        self._app.on_shutdown.append(self._on_shutdown)
        return self

    async def _on_shutdown(self, app):
        self.conn.close()
