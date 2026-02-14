import os
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace,HuggingFaceEndpointEmbeddings
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel,RunnablePassthrough,RunnableLambda
from langchain_core.output_parsers import StrOutputParser


from dotenv import load_dotenv

load_dotenv()   
hf_token = os.getenv("HUGGINGFACE_API_KEY")
llm = HuggingFaceEndpoint(
    repo_id="google/gemma-3-27b-it",
    task="conversational", 
    max_new_tokens=512,
    huggingfacehub_api_token=hf_token
)

model = ChatHuggingFace(llm=llm)


# step 1a indexing

video_id = "Rni7Fz7208c"  # Replace with your YouTube video ID
try:
    # transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
    ytt_api=YouTubeTranscriptApi()
    transcript=ytt_api.fetch(video_id, languages=["en","hi"])
    transcript_text = " ".join([entry.text for entry in transcript])
    # print(transcript_text)
except TranscriptsDisabled:
    print("Transcripts are disabled for this video.")

# transcript loaded

# step 1b textsplitter

spiltter=RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks=spiltter.create_documents([transcript_text])
print(len(chunks))


# step 1c and 1d embeddings and vectorstore

embeddings=HuggingFaceEndpointEmbeddings(model="sentence-transformers/all-MiniLM-L6-v2",huggingfacehub_api_token=hf_token)


vectorstore=FAISS.from_documents(chunks, embeddings)


# Step 2: Retrieval 

retriver=vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 3})

# result= retriver.invoke("What is the video about?")

# print("retrieved result is:", result[0].page_content)

# Step 3: Generate answer

prompt=PromptTemplate(
    input_variables=["retrieved_content","question"],
    template="Based on the following retrieved content, answer the question{retrieved_content}.If you dont know about ans,just say i dont know\n\nQuestion:\n{question}\n\nAnswer:"
)

# 71 to 81 lines are runned by chain in line 89

# question="What is the video about?"

# retrieved_content= retriver.invoke(question)
# # print("retrieved content is:", retrieved_content)

def format_doc(retrieved_content):
    context_text="\n".join([doc.page_content for doc in retrieved_content])
    return context_text



# final_prompt=prompt.invoke({"retrieved_content": format_doc, "question": question})

# # print("final prompt is:", final_prompt)
# # step 4: generate answer
# answer=model.invoke(final_prompt)
# print("Answer is:", answer.content)

# Running through chains
parallel_chain=RunnableParallel({
    "retrieved_content":retriver | RunnableLambda(format_doc),
    "question":RunnablePassthrough()
})

parallelchainresult=parallel_chain.invoke("wht is the video about?")

# print("parallel chain result is:", parallelchainresult)
parser=StrOutputParser()


main_chain=parallel_chain | prompt | model | parser

final_answer=main_chain.invoke("What is the video about?")

print("final answer is:", final_answer)