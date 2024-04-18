from utils.amazon_reviews import amazon, scrape
from utils.llm_analyzer import analyse


def main():
    ASIN = input("Please enter the product ASIN: ")
    print("Fetching reviews")
    reviews_dir, text_between, start_url_list, df = amazon(ASIN)
    product_name = scrape(reviews_dir, text_between, ASIN, start_url_list, df)
    print(f"Reviews for product {ASIN} have been saved as {product_name}")
    analyse(product_name)
    print(f"Analysis has been saved as {product_name}.md")


if __name__ == "__main__":
    main()
