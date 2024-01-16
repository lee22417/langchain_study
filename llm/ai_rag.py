from langchain.prompts import ChatPromptTemplate
from langchain.document_loaders import UnstructuredFileLoader
from langchain.embeddings import CacheBackedEmbeddings, OpenAIEmbeddings
from langchain.schema.runnable import RunnableLambda, RunnablePassthrough
from langchain.storage import LocalFileStore
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores.faiss import FAISS
from langchain.chat_models import ChatOpenAI

class ai_file:
    def __init__(self):
        self.llm = ChatOpenAI(
            temperature=0.1,
            streaming=True,
            callbacks=[
                # ChatCallbackHandler(),
            ],
        )
        
    def upload_file(self, file): 
        file_content = file.read()
        self.file_path = f"./.cache/files/{file.name}"
        print(f"{self.file_path}")
        with open(self.file_path, "wb") as f:
            f.write(file_content)
        
    def embed_file(self, file):
        cache_dir = LocalFileStore(f"./.cache/embeddings/{file.name}")
        splitter = CharacterTextSplitter.from_tiktoken_encoder(
            # separator="\n",
            chunk_size=600,
            chunk_overlap=100,
        )
        
        loader = UnstructuredFileLoader(self.file_path)
        docs = loader.load_and_split(text_splitter=splitter)
        
        embeddings = OpenAIEmbeddings()
        cached_embeddings = CacheBackedEmbeddings.from_bytes_store(embeddings, cache_dir)
        vectorstore = FAISS.from_documents(docs, cached_embeddings)
        retriever = vectorstore.as_retriever()
        return retriever
    
    def format_docs(self, docs):
        return "\n\n".join(document.page_content for document in docs)
    
    def answer (self, file, ask):      
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
                    Answer the question using ONLY the following context. If you don't know the answer just say you don't know. DON'T make anything up.
                    
                    Context: {context}
                    """,
                ),
                ("human", "{question}"),
            ]
        )
        
        retriever = self.embed_file(file)
        
        chain = (
            {
                "context": retriever | RunnableLambda(self.format_docs),
                "question": RunnablePassthrough(),
            }
            | prompt
            | self.llm
        )
        
        return chain.invoke(ask).content
        
        