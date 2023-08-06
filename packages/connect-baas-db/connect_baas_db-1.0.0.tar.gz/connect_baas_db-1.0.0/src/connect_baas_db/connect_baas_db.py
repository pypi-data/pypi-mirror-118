import logging
import psycopg2 as pg
import time

logger = logging.getLogger(__name__)


class ConnectBaaSDB:

    def __init__(self, parameters):
        ''' Initialize the class '''
        self.parameters = parameters
        self.connection = None
        self.runtime = None

    def connect_to_db(self):
        ''' Connect to the Postgres database
            with a maximum of 3 attempts '''
        attempts = 1

        while attempts < 4:
            logger.info('Connecting to Postgres database: attempt {0} of 3'.format(attempts))
            try:
                self.connection = pg.connect(**self.parameters)
                logger.info('Connected to Postgres database')
                break
            except pg.Error as error:
                logger.error(error)
                time.sleep(3)
            finally:
                attempts += 1

    def close_connection_to_db(self):
        ''' Close the connection to the Postgres database '''
        attempts = 0

        while self.connection.closed == 0 and attempts < 3:
            logger.info('Closing connection to Postgres database')
            try:
                self.connection.close()
                logger.info('Connection to Postgres database is closed')
                break
            except pg.Error as error:
                logger.error(error)
                time.sleep(3)
            finally:
                attempts += 1

    def get_runtime_parameters(self, component):
        ''' Use this function to retrieve the parameters for each component of the Postgres Database '''
        logger.info('Retrieve runtime parameters for {}'.format(component))

        # Create a cursor object
        logger.debug('Creating cursor object')
        cursor = self.connection.cursor()

        try:
            logger.debug('Executing baas_own.baas_get_runtime_parameters')
            cursor.callproc('baas_own.baas_get_runtime_parameters', (component,))

            logger.debug('Fetching all results from query')
            all_rows = cursor.fetchall()
            self.runtime = dict(all_rows)

        except pg.DatabaseError as error:
            logger.error(error)

        finally:
            logger.debug('Closing cursor object')
            cursor.close()

    def update_runtime_parameters(self, component, parameter, input_variable):
        """ This function is used to update the config_runtime table in the Postgres database
        """
        logger.info('Start of updating the runtime parameters')

        # Define the query
        logger.debug('Defining the query')
        if input_variable == 'NULL':
            query = f"""UPDATE config_runtime SET "target_value" = {input_variable} WHERE "component" = '{component}'""" \
                    f""" AND "parameter" = '{parameter}';"""
        else:
            query = f"""UPDATE config_runtime SET "target_value" = '{input_variable}' WHERE "component" = '{component}'""" \
                    f""" AND "parameter" = '{parameter}';"""

        # Create a cursor
        logger.debug('Creating the cursor object')
        cursor = self.connection.cursor()

        try:
            # Execute the query using the cursor object
            logger.debug(f'Executing {query}')
            cursor.execute(query)

            # Commit the pending transaction to the database
            logger.debug(f'Committing the pending transaction {cursor.query}')
            self.connection.commit()

        except pg.Error as error:
            # Produce an error log
            logger.error(error)

            # Rollback the pending transaction to the database
            logger.debug(f'Rolling back the pending transaction {cursor.query}')
            self.connection.rollback()

        finally:
            # Close the cursor object
            logger.debug('Closing the cursor object')
            cursor.close()

        logger.info('End of updating the runtime parameters')


