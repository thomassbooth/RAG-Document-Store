from qdrant_client import QdrantClient
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Qdrant
from dotenv import dotenv_values
from langchain_openai import ChatOpenAI
from langchain import hub
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain.memory import ConversationBufferMemory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from fastapi import WebSocket

# steps to take
# Convert my user query into an embedding vector, this way we can match what we have in the vector database
# https://python.langchain.com/docs/tutorials/rag/#indexing-load
# https://python.langchain.com/docs/how_to/MultiQueryRetriever/


class QueryProcessor:
    """Processes the user query and retrieves relevant documents"""

    def __init__(self, embedding_model_loader: EmbeddingModelLoader, vectorstore_manager: VectorStoreManager):
        self._embedding_model_loader = embedding_model_loader
        self._vectorstore_manager = vectorstore_manager
        self._llm = ChatOpenAI(
            model="gpt-4o-mini", api_key=dotenv_values("../.env").get("OPENAI_API_KEY"), max_tokens=1500)

    @staticmethod
    def _format_docs(docs):
        """Format retrieved documents into a single string"""
        return "\n\n".join(doc.page_content for doc in docs)

    async def process_query(self, query: str, userid: int, ws: WebSocket):
        """Process and query the vector store based on the language and query"""

        # Select vector store based on the language
        vectorstore = self._vectorstore_manager.get_vectorstore()
        # Use a multiquery retriever to generate multiple prompts, grab docs then combine the result
        retriever = MultiQueryRetriever.from_llm(retriever=vectorstore.as_retriever(
            search_type="similarity", search_kwargs={"k": 10}), llm=self._llm)

        # Load the prompt template from the hub
        prompt = hub.pull("rlm/rag-prompt")

        # Create the RAG chain, this essentially pipes each part as its computed as it goes through the chain
        ragChain = (
            # Adjusting to work with the chain
            {"context": retriever | self._format_docs,
                "question": RunnablePassthrough()}
            | prompt
            | self._llm
            | StrOutputParser()
        )

        # Stream the results using the formatted context and user query this is an async generator, so no need to use yield
        finalResponse = ""
        first = True
        async for chunk in ragChain.astream({"question": fullQuery}):
            if first:
                first = False
                await ws.send_text("start+")
            finalResponse += chunk
            await ws.send_text(chunk)
    
        # return finalResponse