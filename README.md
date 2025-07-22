# 🎥 YouTube Video QA Chatbot  

This is a **Streamlit web app** that lets you:  

-Fetch a **YouTube video transcript**  
-Split it into chunks and create **vector embeddings**  
-Ask **questions** about the video  
-Get answers using **LangChain + OpenAI GPT models**  

---

##  Features  

- Paste a full **YouTube Video ID**  
- Automatically extracts the **video transcript**  
- Uses **FAISS / Chroma vector store** for efficient retrieval  
- **Retrieval-Augmented Generation (RAG)** for accurate answers  
- Clean **Streamlit UI** with loading spinners  
- Option to use **your own OpenAI API key** (no need to expose yours!)  

---

## Demo UI  

- **Input:** YouTube URL + Question  
- **Sidebar:** Enter your OpenAI API key & Project ID  
- **Output:**  
  - Answer from the transcript  
  - Expandable transcript context used  

---

##  Installation  

### Clone the repo  

```bash
git clone https://github.com/sharik31/Ragbsed-youtube-chatbot
```
---
## Install dependencies
```bash
pip install -r requirements.txt
```


---

## Usage
```bash
python -m streamlit run app.py
```




