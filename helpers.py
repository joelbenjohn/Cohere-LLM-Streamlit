import cohere

def conversation_query(conn, conversation, query):
    """
    The chat endpoint allows users to have conversations with a Large Language Model (LLM) from Cohere. 
    Users can send messages as part of a persisted conversation using the conversation_id parameter, 
    or they can pass in their own conversation history using the chat_history parameter.
    The endpoint features additional parameters such as connectors and documents that enable conversations
    enriched by external knowledge. We call this "Retrieval Augmented Generation", or "RAG".
    """
    response = conn.chat(
    chat_history= conversation,
    message= query,
    # perform web search before answering the question. You can also use your own custom connector.
    connectors=[{"id": "web-search"}] 
    )
    return response.text

def generate(conn, prompt, model, max_tokens):
    """
    This endpoint generates realistic text conditioned on a given input.
    """
    return conn.generate(
                    model=model,
                    prompt = prompt,
                    max_tokens = max_tokens
                    )
def detect_language(conn, texts):
    """
    This endpoint identifies which language each of the provided texts is written in.
    """
    return conn.detect_language(
                                texts=texts
                                ).results

def relevance_ranked(conn, docs, query):
    """
    This endpoint takes in a query and a list of texts and produces an ordered array with each text assigned a relevance score.
    """

    return conn.rerank(
            model = 'rerank-english-v2.0',
            query = query,
            documents = docs,
            top_n = 3,
            )

def tokenize(conn, text):
    """
    This endpoint splits input text into smaller units called tokens using byte-pair encoding (BPE).
    To learn more about tokenization and byte pair encoding, see the tokens page.
    """
    return conn.tokenize(
            text=text,
            model='command' 
            )

def detokenize(conn, tokens):
    """
    This endpoint takes tokens using byte-pair encoding and returns their text representation.
    To learn more about tokenization and byte pair encoding, see the tokens page.
    """
    return conn.detokenize(
            tokens=tokens,
            model="command"
            )




