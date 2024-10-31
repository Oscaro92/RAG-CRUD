# RAG-CRUD
![Python](https://img.shields.io/badge/Python-3670A0?style=flat&logo=python&logoColor=white) ![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=flat&logo=langchain&logoColor=white) ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)

A RAG that manages the restriction of access to documents for different role

## 🔧 Installation

Clone the repository
```shell
git clone https://github.com/Oscaro92/RAG-CRUD.git
cd RAG-CRUD
```

Create a virtual environment
```shell
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows
```

Install dependencies
```shell
pip install -r requirements.txt
```

## ⚙️ Configuration

Create a `.env` file with the following variables:
```
OPENAI_API_KEY=sk-proj-...
```

## 🚀 Usage

```shell
streamlit run chat.py
```

## 📁 Project Structure

```
mail-agent/
├── agent.py            # Agent 
├── chat.py             # Chat
├── docs.py             # Load documents in RAG
├── drive               # Simulation of a drive
│   └── ...
├── Chroma              # RAG
│   └── ...
├── requirements.txt    # Dependencies
├── .env                # Environment variables
└── README.md           # Documentation
```

## 📝 License

This project is licensed under the MIT License.