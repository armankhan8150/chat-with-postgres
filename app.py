
"""A Streamlit app to chat with a PostgreSQL database using LangChain and OpenAI.

Features:
- Securely connect to any PostgreSQL database using user-provided credentials.
- Uses OpenAI's GPT models (via LangChain) to translate natural language questions into SQL queries.
- Executes generated SQL queries and displays results as interactive tables.
- Provides simple explanations of query results using AI.
- Maintains a chat history for context-aware conversations.
- Lets users explore database schema and table names in the sidebar.
- Allows clearing chat history and setting a maximum number of rows to display.
- Falls back to a conversational agent if direct SQL execution fails.
- Designed for ease of use with a modern Streamlit UI.

How it works:
1. Enter your database and OpenAI API credentials in the sidebar and apply the configuration.
2. The app connects to your PostgreSQL database and fetches schema information.
3. Ask questions about your data in plain English in the chat interface.
4. The app uses OpenAI (via LangChain) to generate SQL, runs the query, and shows the results.
5. For each result, an AI-generated explanation is provided.
6. All interactions are saved in the chat history for context and review.

"""




import os
import streamlit as st
from sqlalchemy import create_engine, text
import pandas as pd
from langchain_community.utilities import SQLDatabase
from langchain_community.tools.sql_database.tool import (
    QuerySQLDataBaseTool, InfoSQLDatabaseTool, ListSQLDatabaseTool
)
from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory

# --- Streamlit UI ---
st.set_page_config(page_title="Chat with PostgreSQL", page_icon="🗄️", layout="wide")

# ==============================================================================
# ====== START: Sidebar Configuration (Modified Code) ========================
# ==============================================================================

with st.sidebar:
    st.title("🛠️ Database Configuration")
    
    # --- Database Configuration Section ---
    # st.header("🔧 Database Configuration")
    
    # Database connection inputs
    db_host = st.text_input("Database Host", value="localhost", placeholder="e.g., localhost or your-db-host.com")
    db_port = st.text_input("Database Port", value="5432", placeholder="e.g., 5432")
    db_name = st.text_input("Database Name", placeholder="Enter your database name")
    db_user = st.text_input("Database User", placeholder="Enter your username")
    db_password = st.text_input("Database Password", type="password", placeholder="Enter your password")
    
    
    # Add a visual separator
    st.markdown("---")
    
    # --- API Configuration Section ---
    st.header("🤖 OpenAI Configuration")
    openai_api_key = st.text_input("OpenAI API Key", type="password", placeholder="Enter your OpenAI API key")
    
    # Save button to apply configuration
    if st.button("🔄 Apply Configuration", type="primary"):
        if all([db_host, db_port, db_name, db_user, db_password, openai_api_key]):
            st.session_state.config_applied = True
            st.success("✅ Configuration applied. You can now chat with your database.")
        else:
            st.session_state.config_applied = False
            st.warning("⚠️ Please fill in all configuration fields before applying.")


    # Add a visual separator
    st.markdown("---")
    
    # --- Connection Status and Database Info ---
    st.header("📊 Database Info")
    
    # Check if all required fields are filled
    config_complete = all([db_host, db_port, db_name, db_user, db_password, openai_api_key])
    
    # Only show warning and handle connection if config is complete
    if config_complete:
        # Try to establish database connection
        connection_str = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        
        try:
            engine = create_engine(connection_str)
            with engine.connect():  # Test the connection
                db_connected = True
                st.success("✅ Database Connected")
                
                # Initialize LangChain components
                db = SQLDatabase(engine)
                llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=openai_api_key)
                
                tools = [
                    QuerySQLDataBaseTool(db=db),
                    InfoSQLDatabaseTool(db=db),
                    ListSQLDatabaseTool(db=db),
                ]
                
                # Initialize memory if not exists
                if "memory" not in st.session_state:
                    st.session_state.memory = ConversationBufferMemory(
                        memory_key="chat_history",
                        return_messages=True
                    )
                
                agent_executor = initialize_agent(
                    tools=tools,
                    llm=llm,
                    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
                    verbose=True,
                    memory=st.session_state.memory,
                    handle_parsing_errors=True
                )
                
                # Display table information
                try:
                    table_names = db.get_table_names()
                    st.info(f"**Tables:** {len(table_names)}")
                    with st.expander("View Schema"):
                        for table_name in table_names:
                            st.markdown(f"• **{table_name}**")
                except Exception as e:
                    st.error(f"Could not fetch schema: {e}")
                    
        except Exception as e:
            st.error(f"❌ Database Connection Failed")
            st.error(f"Error: {str(e)}")
            db_connected = False
            db = None
            agent_executor = None
    else:
        # Set defaults when config is not complete
        db_connected = False
        db = None
        agent_executor = None
        # Don't show any warning here - let the user fill the form first
    
    # Add a visual separator
    st.markdown("---")
    
    # --- Settings Section ---
    st.header("⚙️ Settings")
    max_rows = st.number_input(
        label="Max rows to display", 
        min_value=1, 
        value=1000, 
        step=100,
        help="Set the maximum number of rows to show in the output table."
    )

    if st.button("Clear Chat History", type="primary"):
        if "messages" in st.session_state:
            st.session_state.messages = []
        if "memory" in st.session_state:
            st.session_state.memory.clear()
        st.rerun()  # Rerun to update the UI instantly

# ==============================================================================
# ====== END: Sidebar Configuration ===========================================
# ==============================================================================

# --- Main Chat Interface ---
st.title("🗄️ Chat with your PostgreSQL Database")
st.markdown("Ask questions about your data in natural language!")

# Check if configuration is complete and connection is successful
if not config_complete:
    st.info("👈 Please configure your database and OpenAI settings in the sidebar to get started.")
    st.stop()

if not db_connected:
    st.error("❌ Please check your database configuration. Connection failed.")
    st.stop()

# Initialize messages if not exists
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        # Check if content is a dataframe to render it correctly
        if isinstance(msg["content"], pd.DataFrame):
            st.dataframe(msg["content"])
            if "explanation" in msg:
                st.markdown("📌 **Explanation:**")
                st.markdown(msg["explanation"])
        else:
            st.markdown(msg["content"])

# Handle user input
if user_input := st.chat_input("Ask something about your database..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Process the query and get the response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # First, try to generate and execute SQL directly for efficiency
                sql_query_prompt = f"Translate the following request into a SQL query for PostgreSQL: {user_input}"
                sql_query = llm.invoke(sql_query_prompt).content
                
                df = None
                with engine.connect() as conn:
                    try:
                        result = conn.execute(text(sql_query))
                        rows = result.fetchall()
                        if rows:
                            df = pd.DataFrame(rows, columns=result.keys())
                    except Exception:
                        pass # Fallback to agent if direct SQL fails

                if df is not None:
                    # Display the dataframe limited by the sidebar setting
                    display_df = df.head(int(max_rows))
                    st.dataframe(display_df)

                    # Get and display the explanation
                    explanation_prompt = f"Explain the following table in simple terms:\n{display_df.to_markdown(index=False)}"
                    explanation = llm.invoke(explanation_prompt).content
                    st.markdown("📌 **Explanation:**")
                    st.markdown(explanation)
                    
                    # Store dataframe and explanation in chat history
                    st.session_state.messages.append(
                        {"role": "assistant", "content": display_df, "explanation": explanation}
                    )
                else:
                    # Fallback to the LangChain agent if direct SQL doesn't work
                    result = agent_executor.invoke({"input": user_input})
                    answer = result["output"]
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})

            except Exception as e:
                error_msg = f"⚠️ An error occurred: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})