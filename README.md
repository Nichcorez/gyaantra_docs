# 📚 Gyaantra: Chat with Your PDFs 

Gyaantra is your intelligent document assistant. Upload multiple PDFs and start asking questions instantly. Powered by LLMs, embeddings, and Streamlit, it gives contextual answers straight from your documents.
[Live link](https://gyaantra-docs.onrender.com)

## Screenshots
![image](https://github.com/user-attachments/assets/6b07e989-f310-454b-a3b6-4e082199cf3c)
![image](https://github.com/user-attachments/assets/69964897-023b-4a53-8870-6aa67d5d35aa)
![image](https://github.com/user-attachments/assets/509046a5-1bbd-4bad-8ef1-dcae87ca5731)
![image](https://github.com/user-attachments/assets/617a851f-154c-46d2-bf60-1300187f9cbc)

## Features

- Upload and process multiple PDFs
-  Ask natural language questions
-  Context-aware responses using RAG (Retrieval Augmented Generation)
-  Conversation memory with follow-up handling
-  LLM integration via [Groq’s LLaMA 3](https://groq.com/)
-  Answer length options (Short, Medium, Long)
-  Clear chat option
-  Avatar UI with chat bubbles
-  Sidebar tips and credits

## Working  
1. Document Processing: PDFs are parsed and split into manageable chunks
2. Embedding Generation: Text chunks are converted to vector embeddings using HuggingFace models
3. Vector Storage: Embeddings are stored in FAISS for fast similarity search
4. Query Processing: User questions are embedded and matched against document chunks
5. Context Retrieval: Relevant chunks are retrieved and passed to the LLM
6. Response Generation: Groq's Llama3 model generates contextual answers
    
![Gyaantra-Working](https://github.com/user-attachments/assets/c8f7131a-e9ed-47d1-bf44-4ab933c3ff07)

##  Tech Stack

- [Python](https://www.python.org/)
- [Streamlit](https://streamlit.io/)
- [LangChain](https://www.langchain.com/)
- [FAISS](https://github.com/facebookresearch/faiss)
- [HuggingFace Embeddings](https://huggingface.co/)
- [LLaMA 3 via Groq API](https://groq.com/)
- [PyPDF2](https://pypi.org/project/PyPDF2/)


##  Project Structure

  - Gyaantra Docs/  
  ├── assets/   
  ├── app.py   
  ├── answer_length.py   
  ├── htmlTemplates.py  
  ├── .env   
  ├── .gitignore  
  ├── requirements.txt  
  └── README.md  

## Steps
  1. Clone repository
     ```bash
     git clone https://github.com/your-username/gyaantra.git
     cd gyaantra
     ```
  2. Create a Virtual Environment
     ```bash
     python -m venv venv  
     source venv/bin/activate  # or venv\Scripts\activate on Windows
     ```
  3. Install Dependencies
     ```bash
     pip install -r requirements.txt
     ```
  4. Add Environment Variables ```.env```
     ```bash
     GROQ_API_KEY="your_groq_api_key_here"
     HUGGINGFACEHUB_API_TOKEN="your_huggingface_api"
     ```
  5. Run the app
     ```bash
     streamlit run app.py
     ```

## ⚠️ Warning

> **LangChain updates rapidly**: The LangChain library frequently changes its APIs, class names, and functions.  
> This version of Gyaantra is up to date **as of the day it was developed**.  
> You may encounter breaking changes in future versions of LangChain.  
> Always check the [official LangChain docs](https://docs.langchain.com) and pin your package versions to avoid compatibility issues.

---
## License 
[MIT License](LICENSE) © 2025 Kalpesh Gajare


