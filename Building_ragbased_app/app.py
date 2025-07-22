import streamlit as st
import os
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.prompts import PromptTemplate

os.environ["OPENAI_API_KEY"] = ""  
os.environ["OPENAI_PROJECT"] = ""      

st.title("🎥 YouTube Videos Q&A")
st.write("Ask your questions based on a YouTube video")

video_id = st.text_input("Enter YouTube Video ID (e.g., LCEmiRjPEtQ)")

if st.button("Load Transcript"):
    try:
        with st.spinner("Fetching transcript..."):
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=["en"])
            transcript = " ".join(chunk["text"] for chunk in transcript_list)
            st.session_state.transcript = transcript
            st.success("✅ Transcript loaded successfully!")
    except TranscriptsDisabled:
        st.error("❌ No captions available for this video.")
    except Exception as e:
        st.error(f"⚠️ Error: {e}")

if "transcript" in st.session_state:
    transcript_text = st.session_state.transcript

    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=50)
    chunks = splitter.create_documents([transcript_text])

    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vector_store = Chroma.from_documents(chunks, embeddings)
    retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k":4})

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)

    prompt = PromptTemplate(
        template="""Answer ONLY from the provided transcript context.
        If the context is insufficient, say you don't know.
        
        Context:
        {context}
        
        Question: {question}""",
        input_variables=['context', 'question']
    )

    user_question = st.text_input("Ask a question about the video:")

    if st.button("Get Answer"):
        with st.spinner("Thinking..."):
            retrieved_docs = retriever.invoke(user_question)
            context_text = "\n\n".join(doc.page_content for doc in retrieved_docs)

            final_prompt = prompt.format(context=context_text, question=user_question)

            answer = llm.invoke(final_prompt)
            st.subheader("Answer")
            st.write(answer.content)
