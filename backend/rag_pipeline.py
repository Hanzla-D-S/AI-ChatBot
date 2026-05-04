import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate

load_dotenv()

VECTOR_STORE_PATH = "./vector_store"

# Custom prompt
SYSTEM_PROMPT = """
You are a helpful and friendly customer support assistant for ShopEasy,
a Pakistani e-commerce store.

- If the customer sends a greeting like "hi", "hello", "hlo", "hey" etc,
  respond warmly and ask how you can help them today.
- If the question is related to ShopEasy, use the provided context to answer accurately.
- If the answer is not in the context, politely say:
  "I'm sorry, I don't have information on that. Please contact our support
  team at support@shopeasy.pk or WhatsApp 0300-1234567."

Never make up information. Always be polite and professional.

Context:
{context}

Chat History:
{chat_history}

Customer Question: {question}

Answer:
"""

prompt = PromptTemplate(
    input_variables=["context", "chat_history", "question"],
    template=SYSTEM_PROMPT
)


def load_rag_chain():
    if not os.path.exists(VECTOR_STORE_PATH):
        raise FileNotFoundError(
            "Vector store not found! Please run 'python backend/ingest.py' first."
        )

    embeddings = OpenAIEmbeddings()
    vector_store = FAISS.load_local(
        VECTOR_STORE_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )

    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.2 
    )

    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key="answer"
    )

    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vector_store.as_retriever(search_kwargs={"k": 4}),
        memory=memory,
        combine_docs_chain_kwargs={"prompt": prompt},
        return_source_documents=False,
        output_key="answer"
    )

    print("RAG chain loaded successfully")
    return chain


# Global chain instance (loaded once when backend starts)
rag_chain = None

def get_or_create_chain():
    global rag_chain
    if rag_chain is None:
        rag_chain = load_rag_chain()
    return rag_chain


def get_response(user_message: str) -> str:
    chain = get_or_create_chain()
    result = chain({"question": user_message})
    return result["answer"]