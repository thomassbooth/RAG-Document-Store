from dotenv import dotenv_values
from langchain_openai import ChatOpenAI
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from .embeddings import DocumentEmbedder
from .storage import VectorStore
from langchain.prompts import PromptTemplate
from guardrails import Guard
from guardrails.hub import ToxicLanguage
from langchain import hub


# Convert my user query into an embedding vector, this way we can match what we have in the vector database
# https://python.langchain.com/docs/tutorials/rag/#indexing-load
# https://python.langchain.com/docs/how_to/MultiQueryRetriever/
# https://www.guardrailsai.com/docs/integrations/langchain


class DocumentFormatter:
    """Join together all documents retrieved from the vector store and extract their metadata to use in the query prompt"""
    @staticmethod
    def _format_docs(docs):
        """Format retrieved documents into a single string, including metadata"""
        formatted_docs = []
        for doc in docs:
            # Include the metadata (like source or location) along with the page content
            metadata = doc.metadata
            source = metadata.get("source", "Unknown source")
            page = metadata.get("page_index", "Unknown location")
            paragraph = metadata.get("paragraph_index")
            formatted_docs.append(
                f"Source: {source}, Page: {page}, Paragraph: {paragraph}\nContent:\n{doc.page_content}")

        return "\n\n".join(formatted_docs)


class QueryProcessor:
    """Processes the user query and retrieves relevant documents"""

    def __init__(self, embedding_service: DocumentEmbedder, vector_store: VectorStore):
        self._embedding_service = embedding_service
        self._storage_service = vector_store
        self._llm = ChatOpenAI(
            model="gpt-4o-mini", api_key=dotenv_values("../.env").get("OPENAI_API_KEY"), max_tokens=1500)
        self.guard = Guard()

    @staticmethod
    def _create_prompt_template():
        """Creates and returns the prompt template."""
        return PromptTemplate.from_template("""
        You are a helpful assistant. Based on the documents provided, answer the question below while citing the source, page, and paragraph for any information you reference.
        
        Documents:
        {context}

        Question: {question}

        Response:
        If the documents provided aren't enough to answer the question, please return "I don't have enough information to answer this question."
        """)

    async def process_query(self, query: str):
        """Process and query the vector store based on the language and query"""
        self.guard.use_many(
            ToxicLanguage(on_fail="filter"),
        )
        # Select vector store based on the language
        vectorstore = self._storage_service.get_vectorstore(
            self._embedding_service.get_embedding_model())
        # Use a multiquery retriever to generate multiple prompts, grab docs then combine the result
        retriever = MultiQueryRetriever.from_llm(retriever=vectorstore.as_retriever(
            search_type="similarity", search_kwargs={"k": 10}), llm=self._llm)

        prompt = hub.pull("rlm/rag-prompt")
        print(prompt)
        # Create the RAG chain, this essentially pipes each part as its computed as it goes through the chain
        # Including the guard to filter out bad results
        rag_chain = (
            {"context": retriever | DocumentFormatter._format_docs,
                "question": RunnablePassthrough()}
            | self._create_prompt_template()
            | self._llm
            | self.guard.to_runnable()
            | StrOutputParser()
        )

        # Stream the results as they come in, this function is invoked as a Streaming result so use yield to return the results as they come in
        async for chunk in rag_chain.astream({"question": query}):
            yield chunk
