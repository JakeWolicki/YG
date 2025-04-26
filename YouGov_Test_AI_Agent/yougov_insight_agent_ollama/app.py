# cd /Users/jakewolicki/Documents/YouGov_Test_AI_Agent/yougov_insight_agent_ollama
# streamlit run app.py

import streamlit as st
from insights.generate_insights import load_data, get_relevant_rows
from llm.ask_agent import generate_response

st.set_page_config(page_title="Arizona Cardinals Data Story", layout="wide")

# Load logo
st.image("logo.png", width=120)

st.title("Arizona Cardinals Data Story")

# Load the data once at the start
df = load_data()

# --- Sidebar (Optional) ---
with st.sidebar:
    st.header("ℹ️ About This App")
    st.write("Explore insights from the Arizona Cardinals fan data. Search by audience, topic, and ask your own questions!")

# --- EXPLORE SECTION (collapsible) ---
with st.expander("📚 Explore Available Data", expanded=False):
    st.subheader("📋 View Available Audiences")
    search_audience = st.text_input("🔎 Search Audiences", key="audience_search")
    filtered_audiences = [aud for aud in sorted(df['Audience'].unique()) if search_audience.lower() in aud.lower()]
    for audience in filtered_audiences:
        st.markdown(f"- {audience}")

    st.subheader("🎯 View Available Topics")
    search_topic = st.text_input("🔎 Search Topics", key="topic_search")
    filtered_topics = [top for top in sorted(df['Topic'].unique()) if search_topic.lower() in top.lower()]
    for topic in filtered_topics:
        st.markdown(f"- {topic}")

    st.subheader("🔍 Explore Topics by Audience")
    selected_audience_explore = st.selectbox(
        "Select an Audience to view their available Topics:",
        options=sorted(df['Audience'].unique()),
        index=0,
        key="audience_explore"
    )

    if selected_audience_explore:
        related_topics = sorted(df[df['Audience'] == selected_audience_explore]['Topic'].unique())
        st.markdown(f"**Topics for {selected_audience_explore}:**")
        for topic in related_topics:
            st.markdown(f"- {topic}")

# --- MAIN SECTION ---
st.header("💬 Ask a Question")
query = st.text_input("Example: 'What are some positives about NFL fans and tequila?'", key="user_query")

if query:
    # Dynamically detect audience and topic
    audiences = df['Audience'].unique()
    topics = df['Topic'].unique()

    selected_audience = None
    selected_topic = None

    for audience in audiences:
        if audience.lower() in query.lower():
            selected_audience = audience
            break

    for topic in topics:
        if topic.lower() in query.lower():
            selected_topic = topic
            break

    insights = get_relevant_rows(df, audience=selected_audience, topic=selected_topic)

    if insights.empty:
        st.warning("⚠️ No matching insights found.")
    else:
        response = generate_response(insights)
        st.markdown(response)
