from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter

class RAGManager:
    def __init__(self, model_config):
        self.embeddings = HuggingFaceEmbeddings(
            model_name=model_config['embeddings_model']
        )
        self.vector_store = None
        
    def initialize_knowledge_base(self, schema_info):
        """Initialize vector store with schema information"""
        # Convert schema info to documents
        documents = self._create_schema_documents(schema_info)
        
        # Create vector store
        self.vector_store = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            persist_directory="./data/chroma"
        )
    
    def _create_schema_documents(self, schema_info):
        """Convert schema information to document format"""
        documents = []
        text_splitter = CharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        
        for table in schema_info:
            # Create detailed schema description
            schema_text = f"Table: {table['table']}\n"
            schema_text += "Columns:\n"
            for col in table['columns']:
                schema_text += f"- {col['name']} ({col['type']})\n"
            
            # Split into chunks if needed
            chunks = text_splitter.split_text(schema_text)
            documents.extend(chunks)
        
        return documents
    
    def get_relevant_context(self, query):
        """Retrieve relevant schema context for a query"""
        if not self.vector_store:
            raise Exception("Knowledge base not initialized")
        
        results = self.vector_store.similarity_search(query, k=3)
        return "\n".join([doc.page_content for doc in results])