
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from openai import OpenAI
from langchain.prompts import ChatPromptTemplate



def mock_rag_model(question: str, retriever) -> str:
    # Set up prompt

    template = """
    Context: {context}

    Question: {question}
    """

    local_prompt = ChatPromptTemplate.from_template(template)

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)
    
    response = invoke_LLMServer(question,retriever,format_docs,local_prompt)
    return response
    

def chatGPT_llm(prompt_text):
    # Point to the local server
    client = OpenAI()

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
        {"role": "system", "content": "You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise. Don't state your role and task. Avoid using prefaces"},
        {"role": "user", "content": str(prompt_text)}
    ],
    temperature=0.8,
    )
    return str(completion.choices[0].message.content)

def local_llm(prompt_text):
    # Point to the local server
    client = OpenAI(base_url="http://192.168.68.78:8080/v1")

    completion = client.chat.completions.create(
    model="Meta-Llama-3-8B-Instruct-GGUF",
    messages=[
        {"role": "system", "content": "You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise. Don't state your role and task. Avoid using preface like According to the provided context."},
        {"role": "user", "content": str(prompt_text)}
    ],
    temperature=0.8,
    )
    return str(completion.choices[0].message.content)

    # Update the chain to use the local LLM server
def invoke_LLMServer(prompt_text,retriever,format_docs,local_prompt):
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | local_prompt
        | local_llm
        | StrOutputParser()
    )
    llama_response = rag_chain.invoke("What is this program?")
    return llama_response[:-10]
