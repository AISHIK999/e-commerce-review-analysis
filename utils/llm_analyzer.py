import textwrap
import google.generativeai as genai
import pandas as pd

from IPython.display import Markdown


def to_markdown(text):
    text = text.replace("•", "  *")
    return Markdown(textwrap.indent(text, "> ", predicate=lambda _: True))


def analyse(report_path):
    genai.configure(api_key="YOUR_API_KEY")
    # for m in genai.list_models():
    #     if "generateContent" in m.supported_generation_methods:
    #         print(m.name)

    model = genai.GenerativeModel("gemini-pro")

    df = pd.read_excel(report_path)
    # Incase of token limitation, uncomment the below line to limit the reviews to the past year
    # df = df[df["DATE"] >= pd.Timestamp.now() - pd.DateOffset(years=1)]

    reviews_values = df["REVIEW"].values

    print("Generating analysis report")

    # Use below prompt or write a better prompt for analysis. I tried to keep it short due to token limitation
    response = model.generate_content(
        f"Consider that you are a market analyst, given a list of customer reviews for a product. These reviews contain both positive and negative experience reviews. Your job is to list what the customers like and dislike about the product in bullet points, without repeating a point more than once and state only the most valuable 5-7 points. Perform such analysis upon the list of reviews given below:\n{reviews_values}"
    )

    with open(f"{report_path}.md", "w", encoding="utf-8") as f:
        f.write(response.text)
