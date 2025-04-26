def generate_response(insights_df):
    bullets = "\n".join(
        f"- {row['Percent']}% of {row['Audience']} say that {row['Topic'].lower()} {row['Statement'].lower()}"
        for _, row in insights_df.iterrows()
    )

    prompt = f"""You are an insights assistant. Given the following positive data points from a YouGov dataset, summarize them into a client-ready insight list:\n\n{bullets}\n\nList these as top 10 positive insights."""

    # Mocked response (for testing purposes)
    response = {
        "response": f"Here are the top insights based on the data you provided:\n\n{bullets}"
    }
    return response["response"]
