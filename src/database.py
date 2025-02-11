from sqlalchemy.exc import SQLAlchemyError
import logging

class DatabaseManager:
    def __init__(self, config):
        self.config = config
        self.engine = self._create_engine()
        self.metadata = MetaData()
        self.SessionLocal = sessionmaker(bind=self.engine)
        self.logger = logging.getLogger('db_logger')
        
    def _create_engine(self):
        try:
            url = URL.create(
                "postgresql+psycopg2",
                username=self.config['user'],
                password=self.config['password'],
                host=self.config['host'],
                port=self.config['port'],
                database=self.config['database']
            )
            engine = create_engine(url)
            # Test connection
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            self.logger.info("Database connection established successfully")
            return engine
        except Exception as e:
            self.logger.error(f"Failed to create database engine: {str(e)}")
            raise
    
    def get_schema_info(self):
        """Returns database schema information with error handling"""
        try:
            schema_info = []
            with self.engine.connect() as conn:
                # Get all tables
                tables = conn.execute(text("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public'
                """))
                
                for table in tables:
                    # Get column information
                    columns = conn.execute(text(f"""
                        SELECT column_name, data_type 
                        FROM information_schema.columns 
                        WHERE table_name = '{table[0]}'
                    """))
                    
                    schema_info.append({
                        'table': table[0],
                        'columns': [{'name': col[0], 'type': col[1]} 
                                  for col in columns]
                    })
            
            self.logger.info(f"Successfully retrieved schema info for {len(schema_info)} tables")
            return schema_info
        except SQLAlchemyError as e:
            self.logger.error(f"Database error while getting schema info: {str(e)}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error while getting schema info: {str(e)}")
            raise
    
    def execute_query(self, query):
        """Executes SQL query with enhanced error handling and logging"""
        query_logger = logging.getLogger('query_logger')
        try:
            query_logger.info(f"Executing query: {query}")
            with self.engine.connect() as conn:
                start_time = datetime.now()
                result = conn.execute(text(query))
                execution_time = (datetime.now() - start_time).total_seconds()
                
                results = [dict(row._mapping) for row in result]
                query_logger.info(
                    f"Query executed successfully. "
                    f"Execution time: {execution_time:.2f}s. "
                    f"Results returned: {len(results)}"
                )
                return results
        except SQLAlchemyError as e:
            query_logger.error(f"Database error executing query: {str(e)}")
            self.logger.error(f"Query failed: {query}\nError: {str(e)}")
            raise
        except Exception as e:
            query_logger.error(f"Unexpected error executing query: {str(e)}")
            self.logger.error(f"Query failed: {query}\nError: {str(e)}")
            raise