"""Streamlit app for Snowflake Cortex Analyst integration"""
import pandas as pd
import os
from dotenv import load_dotenv
from snowflake.snowpark import Session
from streamlit_data import CortexAnalystClient
import streamlit as st

load_dotenv()

# Snowflake connection
@st.cache_resource
def create_session():
    """Create Snowflake session"""
    connection_parameters = {
        "account": os.getenv("SNOWFLAKE_ACCOUNT"),
        "user": os.getenv("SNOWFLAKE_USER"),
        "password": os.getenv("SNOWFLAKE_PAT"),
        "role": os.getenv("SNOWFLAKE_ROLE"),
        "warehouse": os.getenv("SNOWFLAKE_WAREHOUSE"),
        "database": "DEMO",
        "schema": "DEMO_BVPRJG"
    }

    return Session.builder.configs(connection_parameters).create()

@st.cache_resource
def create_analyst_client():
    """Create Cortex Analyst client"""
    return CortexAnalystClient(
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        user=os.getenv("SNOWFLAKE_USER"),
        pat=os.getenv("SNOWFLAKE_PAT")
    )

# Main application
def main():
    st.title("💬 Snowflake Cortex Analyst")
    st.markdown("Ask questions about your sales data in natural language")

    # Create session and client
    try:
        session = create_session()
        analyst_client = create_analyst_client()
    except Exception as e:
        st.error(f"❌ Snowflake connection error: {str(e)}")
        st.info("💡 Check your .env file with connection settings")
        return

    # Semantic view
    semantic_view = "DEMO.DEMO_BVPRJG.SALES"
    st.info(f"📊 Semantic View: **{semantic_view}**")

    # Question input
    st.markdown("---")
    st.subheader("💬 Your Question")
    question = st.text_area(
        "Enter your question:",
        height=100,
        placeholder="For example: What are the top 5 products by sales?",
        help="Enter your question in natural language"
    )

    # Execute button
    if st.button("🚀 Get Answer", type="primary"):
        if not question.strip():
            st.warning("⚠️ Please enter a question")
        else:
            try:
                with st.spinner("🤖 Generating SQL query..."):
                    # Call Cortex Analyst REST API
                    response = analyst_client.send_message(question, semantic_view)
                    
                    # Extract data from response
                    generated_sql = analyst_client.extract_sql(response)
                    text_response = analyst_client.extract_text(response)
                    suggestions = analyst_client.extract_suggestions(response)
                    
                    # Show interpretation
                    if text_response:
                        st.info(f"📝 {text_response}")
                    
                    # If there are suggestions - question is ambiguous
                    if suggestions:
                        st.warning("💡 Question is ambiguous. Try:")
                        for i, suggestion in enumerate(suggestions, 1):
                            st.write(f"{i}. {suggestion}")
                    
                    # Show and execute SQL
                    elif generated_sql:
                        with st.expander("🔍 Generated SQL", expanded=False):
                            st.code(generated_sql, language='sql')
                        
                        # Execute query
                        with st.spinner("🔄 Executing query..."):
                            result = session.sql(generated_sql).collect()
                            
                            if result:
                                df = pd.DataFrame([row.asDict() for row in result])
                                
                                st.subheader("📊 Results")
                                st.dataframe(df, use_container_width=True)
                                st.success(f"✅ Query executed successfully! Rows returned: {len(df)}")
                            else:
                                st.info("ℹ️ Query executed but returned no results")
                    else:
                        st.error("❌ SQL was not generated")
                        
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                with st.expander("🔍 Error Details"):
                    import traceback
                    st.code(traceback.format_exc())

    # Information
    with st.expander("ℹ️ About"):
        st.markdown("""
        **How to use:**
        1. Enter your question in natural language
        2. Click "Get Answer"
        3. View the results
        
        **Example questions:**
        - "What are the top 10 products by sales?"
        - "Show sales by month for the last year"
        - "What is the average order value by category?"
        - "Which customers generated the most revenue?"
        
        **Semantic View:** DEMO.DEMO_BVPRJG.SALES
        """)

if __name__ == "__main__":
    main()
