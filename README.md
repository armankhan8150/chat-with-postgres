# Chat with Postgres: Natural Language SQL Agent

A conversational Text-to-SQL assistant that translates plain English questions into PostgreSQL queries and returns structured results, powered by LangChain, OpenAI, and Streamlit.

---

## How It Works

```
User: "Show me the top 5 customers by total orders last month"
    │
    ▼
┌──────────────────────┐
│   LangChain Agent     │  ──→  Inspects schema, understands table relationships
└──────────────────────┘
    │
    ▼
┌──────────────────────┐
│   OpenAI LLM          │  ──→  Generates valid PostgreSQL query from intent
└──────────────────────┘
    │
    ▼
┌──────────────────────┐
│   PostgreSQL          │  ──→  Executes query safely against your database
└──────────────────────┘
    │
    ▼
┌──────────────────────┐
│   Streamlit UI        │  ──→  Displays results as formatted table + raw SQL
└──────────────────────┘
```

### Key Design Decisions
- **Schema-aware generation**: LangChain SQL Agent introspects the database schema before generating queries, reducing hallucinated column/table names
- **SQL transparency**: the generated SQL is always shown alongside results so users can verify and trust the output
- **Conversational context**: multi-turn conversation history lets users refine queries naturally ("now filter only active ones")
- **Safe execution**: read-only query enforcement prevents accidental data modification

---

## Tech Stack

| Component | Technology |
|---|---|
| LLM | OpenAI GPT-4o-mini |
| Agent Framework | LangChain SQL Agent |
| Database | PostgreSQL |
| DB Connector | SQLAlchemy |
| Web UI | Streamlit |
| Language | Python 3.10+ |

---

## Features

- 💬 **Natural language to SQL**: ask questions in plain English, get SQL + results
- 🔍 **Schema introspection**: automatically reads your database structure
- 📊 **Formatted results**: query output displayed as clean interactive tables
- 🔎 **SQL visibility**: generated SQL always shown for transparency
- 🧠 **Multi-turn conversation**: refine queries across multiple messages
- 🖥 **Streamlit interface**: simple web UI, no SQL knowledge needed

---

## Getting Started

### Prerequisites
- Python 3.10+
- PostgreSQL database (local or remote)
- OpenAI API key → [platform.openai.com](https://platform.openai.com)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/armankhan8150/chat-with-postgres.git
cd chat-with-postgres

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
cp .env.example .env
# Add your credentials to .env
```

### Environment Variables

```env
OPENAI_API_KEY=your_openai_api_key
DATABASE_URL=postgresql://user:password@localhost:5432/your_database
```

### Run

```bash
streamlit run app.py
```

---

## Example Queries

| You Ask | Generated SQL |
|---|---|
| "How many users registered this week?" | `SELECT COUNT(*) FROM users WHERE created_at >= NOW() - INTERVAL '7 days'` |
| "Top 5 products by revenue" | `SELECT name, SUM(price * quantity) AS revenue FROM orders GROUP BY name ORDER BY revenue DESC LIMIT 5` |
| "Show all orders with status pending" | `SELECT * FROM orders WHERE status = 'pending'` |

---

## 🗺 Roadmap

- [ ] Support for multiple database schemas
- [ ] Query history and export to CSV
- [ ] Chart generation from query results
- [ ] MySQL and SQLite support

---

## Author

**Arman Malik**: AI Engineer
[LinkedIn](https://linkedin.com/in/arman-malik) · [GitHub](https://github.com/armankhan8150)

---

## License

MIT License: see [LICENSE](LICENSE) for details.
