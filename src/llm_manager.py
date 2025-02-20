from llama_cpp import Llama

class LLMManager:
    def __init__(self, model_config):
        self.llm = Llama(
            model_path=model_config['model_path'],
            n_ctx=2048,  # Context window
            n_threads=4   # Adjust based on your CPU
        )
    
    def generate_sql(self, question, context):
        """Generate SQL query from natural language question"""
        prompt = f"""
        Given the following database schema information:
        {context}
        
        Generate a SQL query for the following question:
        {question}
        
        Return only the SQL query without any explanation.
        """
        
        response = self.llm(
            prompt,
            max_tokens=500,
            temperature=0.1,
            stop=["--", "```"]
        )
        
        return response['choices'][0]['text'].strip()