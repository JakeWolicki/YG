import pandas as pd

def load_data():
    # Load the CSV file containing insights
    df = pd.read_csv("data/yougov_data.csv")
    
    # Ensure Percent column is numeric
    df['Percent'] = pd.to_numeric(df['Percent'], errors='coerce')
    return df

def get_relevant_rows(df, audience=None, topic=None, tone="Positive"):
    # Start by filtering for tone
    filtered = df[df["Tone"].str.lower() == tone.lower()]

    # If audience is given, match exactly
    if audience:
        filtered = filtered[filtered["Audience"].str.lower() == audience.lower()]

    # If topic is given, match exactly
    if topic:
        filtered = filtered[filtered["Topic"].str.lower() == topic.lower()]

    # Return the top 10 relevant insights
    return filtered.head(10)

def generate_response(insights):
    # If no relevant insights were found, return a warning
    if insights.empty:
        return "⚠️ No matching insights found."

    responses = []
    for _, row in insights.iterrows():
        audience = row['Audience'].strip()
        topic = row['Topic'].strip()
        statement = row['Statement'].strip()
        percent = row['Percent']

        # Corrected sentence structure:
        formatted = f"**{percent}% of {audience} say that {topic.lower()} {statement.lower()}**."
        
        responses.append(formatted)

    return "\n\n".join(responses)
