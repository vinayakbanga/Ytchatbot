import os
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace, HuggingFaceEndpointEmbeddings
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from operator import itemgetter

# Load environment variables
load_dotenv()
hf_token = os.getenv("HUGGINGFACE_API_KEY")

# Initialize LLM
llm = HuggingFaceEndpoint(
    repo_id="google/gemma-3-27b-it",
    task="conversational",
    max_new_tokens=768,  # Increased for longer, more detailed responses
    huggingfacehub_api_token=hf_token
)
model = ChatHuggingFace(llm=llm)

# Initialize embeddings
embeddings = HuggingFaceEndpointEmbeddings(
    model="sentence-transformers/all-MiniLM-L6-v2",
    huggingfacehub_api_token=hf_token
)


def get_transcript(video_id):
    """
    Fetch YouTube transcript for a given video ID.
    
    Args:
        video_id (str): YouTube video ID
        
    Returns:
        str: Transcript text
        
    Raises:
        TranscriptsDisabled: If transcripts are disabled for the video
        Exception: For other errors
    """
    try:
        ytt_api = YouTubeTranscriptApi()
        transcript = ytt_api.fetch(video_id, languages=["en", "hi"])
        transcript_text = " ".join([entry.text for entry in transcript])
        return transcript_text
    except TranscriptsDisabled:
        raise Exception("Transcripts are disabled for this video.")
    except Exception as e:
        raise Exception(f"Error fetching transcript: {str(e)}")


def create_vectorstore(transcript_text):
    """
    Create FAISS vectorstore from transcript text.
    
    Args:
        transcript_text (str): The transcript text to process
        
    Returns:
        FAISS: Vector store containing the transcript chunks
    """
    # Split text into chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=300)  # Larger chunks for more context
    chunks = splitter.create_documents([transcript_text])
    
    # Create and return vectorstore
    vectorstore = FAISS.from_documents(chunks, embeddings)
    return vectorstore


def create_rag_chain(vectorstore):
    """
    Create RAG chain from vectorstore.
    
    Args:
        vectorstore (FAISS): Vector store to use for retrieval
        
    Returns:
        RunnableSequence: The complete RAG chain
    """
    # Create retriever
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 5})  # Retrieve 5 chunks for broader context
    
    # Create prompt template
    prompt = PromptTemplate(
        input_variables=["retrieved_content", "chat_history", "question"],
        template="""You are a helpful AI assistant answering questions based on a YouTube video transcript.
        
Using the transcript context and previous conversation history provided below, answer the user's question.
If the answer isn't in the transcript, use the conversation history to maintain context (e.g., if the user asks 'who is he?' referring to someone mentioned earlier).

Transcript Context:
{retrieved_content}

Previous Conversation:
{chat_history}

Question: {question}
Answer:"""
    )
    
    # Helper function to format documents
    def format_doc(retrieved_content):
        context_text = "\n".join([doc.page_content for doc in retrieved_content])
        return context_text
    
    # Create parallel chain for retrieval
    parallel_chain = RunnableParallel({
        "retrieved_content": itemgetter("question") | retriever | RunnableLambda(format_doc),
        "chat_history": itemgetter("chat_history"),
        "question": itemgetter("question")
    })
    
    # Create output parser
    parser = StrOutputParser()
    
    # Create and return main chain
    main_chain = parallel_chain | prompt | model | parser
    return main_chain


def answer_question(chain, question, chat_history_str):
    """
    Get answer from RAG chain.
    
    Args:
        chain: The RAG chain
        question (str): User's question
        chat_history_str (str): Formatted chat history
        
    Returns:
        str: AI-generated answer
    """
    answer = chain.invoke({"question": question, "chat_history": chat_history_str})
    return answer


def format_chat_history(history_list):
    """Format history list into a string for the prompt."""
    if not history_list:
        return "No previous conversation."
    
    formatted = ""
    # Only take last 5 turns to avoid context overflow
    for msg in history_list[-10:]: 
        role = "User" if msg.get('role') == 'user' else "AI"
        content = msg.get('content', '')
        formatted += f"{role}: {content}\n"
    return formatted


# Cache for vectorstores (video_id -> vectorstore)
_vectorstore_cache = {}


def get_or_create_vectorstore(video_id):
    """
    Get cached vectorstore or create a new one.
    
    Args:
        video_id (str): YouTube video ID
        
    Returns:
        FAISS: Vector store for the video
    """
    if video_id not in _vectorstore_cache:
        transcript_text = get_transcript(video_id)
        vectorstore = create_vectorstore(transcript_text)
        _vectorstore_cache[video_id] = vectorstore
    
    return _vectorstore_cache[video_id]


def chat_with_video(video_id, question, chat_history=None):
    """
    Main function to chat with a YouTube video.
    
    Args:
        video_id (str): YouTube video ID
        question (str): User's question
        chat_history (list): List of previous messages
        
    Returns:
        str: AI-generated answer
    """
    if chat_history is None:
        chat_history = []

    # Get or create vectorstore
    vectorstore = get_or_create_vectorstore(video_id)
    
    # Create RAG chain
    chain = create_rag_chain(vectorstore)
    
    # Format history
    chat_history_str = format_chat_history(chat_history)
    
    # Get answer
    answer = answer_question(chain, question, chat_history_str)
    
    return answer
