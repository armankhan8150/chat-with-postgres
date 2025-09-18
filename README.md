# Chat with PostgreSQL 🗄️🤖

A Streamlit app that lets you **chat with your PostgreSQL database** using **LangChain** and **OpenAI GPT models**.  
Ask questions in plain English, and the app will translate them into SQL, run the queries, and explain the results.

---

## 🚀 Features
- 🔑 Securely connect to any PostgreSQL database with user-provided credentials.
- 🤖 Uses OpenAI GPT (via LangChain) to convert natural language into SQL.
- 📊 Displays query results as interactive tables.
- 📝 AI-generated explanations of results.
- 💬 Maintains a chat history for context-aware conversations.
- 📂 Explore database schema and table names in the sidebar.
- 🧹 Clear chat history and set maximum rows to display.
- 🔄 Fallback to conversational agent if SQL execution fails.

---

## ⚙️ Installation

1. Clone the repo:
   ```bash
   git clone https://github.com/your-username/chat-with-postgres.git
   cd chat-with-postgres

2. Create a virtual environment:
    ```bash
   python -m venv venv
   source venv/bin/activate     # on Mac/Linux
   venv\Scripts\activate  # On windows

3. Install dependencies:
    ```bash
   pip install -r requirements.txt

▶️ Usage
1. Run the Streamlit app:
    ```bash
   streamlit run app.py

2. Enter your PostgreSQL credentials and OpenAI API key in the sidebar.

3. Ask questions about your data in natural language!

📌 Example

Question: "Show me the top 5 customers by sales"
    The app will:

        Generate SQL
        Run the query
        Show results in a table
        Provide an explanation in plain English