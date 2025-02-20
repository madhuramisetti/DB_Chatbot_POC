class DatabaseChatbot:
    def __init__(self, db_config, model_config):
        self.logger = logging.getLogger('app_logger')
        try:
            self.db = DatabaseManager(db_config)
            self.rag = RAGManager(model_config)
            self.llm = LLMManager(model_config)
            
            # Initialize RAG with schema information
            schema_info = self.db.get_schema_info()
            self.rag.initialize_knowledge_base(schema_info)
            self.logger.info("Chatbot initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize chatbot: {str(e)}")
            raise
    
    def process_query(self, user_question):
        """Process user question with enhanced error handling"""
        try:
            self.logger.info(f"Processing user question: {user_question}")
            
            # Get relevant schema context
            context = self.rag.get_relevant_context(user_question)
            self.logger.debug(f"Retrieved context: {context}")
            
            # Generate SQL query
            sql_query = self.llm.generate_sql(user_question, context)
            self.logger.debug(f"Generated SQL query: {sql_query}")
            
            # Execute query
            results = self.db.execute_query(sql_query)
            self.logger.info(
                f"Query processed successfully. "
                f"Results returned: {len(results)}"
            )
            
            return {
                'sql_query': sql_query,
                'results': results,
                'status': 'success'
            }
        except Exception as e:
            error_logger = logging.getLogger('error_logger')
            error_logger.error(
                f"Error processing query: {user_question}\n"
                f"Error: {str(e)}\n"
                f"Stack trace:", exc_info=True
            )
            return {
                'status': 'error',
                'message': str(e)
            }