import logging.handlers
import logging
import json
import psycopg2 as pg
import uuid

from connect_baas_db.connect_baas_db import ConnectBaaSDB


class PostgresHandler(logging.Handler, ConnectBaaSDB):
    '''
    Customized logging handler that puts logs to the database.
    '''

    def __init__(self, parameters):
        logging.Handler.__init__(self)
        ConnectBaaSDB.__init__(self, parameters)
        self.connect_to_db()
        self.reference_id = str(uuid.uuid4())
        self.name = 'PostgresHandler'

    def emit(self, record):
        if self.connection:
            cursor = self.connection.cursor()

            log_msg = str(record.msg)
            log_msg = log_msg.strip()
            log_msg = log_msg.replace('\'', '\'\'')
            message = str(log_msg)

            application = str(record.name)
            module = str(record.module)
            func = str(record.funcName)
            severity = str(record.levelname)

            json_message = json.dumps({'referenceid': self.reference_id,
                                       'application': application,
                                       'module': module,
                                       'function': func,
                                       'severity': severity,
                                       'message': message})

            query = f"CALL baas_own.baas_logger('{self.reference_id}', '{application}', '{module}.{func}', '{severity}', '{message}', '{json_message}');"

            attempts = 0
            while attempts < 3:
                try:
                    cursor.execute(query)
                    self.connection.commit()
                    cursor.close()
                    break
                except pg.DatabaseError:
                    self.connection.rollback()
                finally:
                    attempts += 1
            else:
                cursor.close()
                self.close_connection_to_db()
