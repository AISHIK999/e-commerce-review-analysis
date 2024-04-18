from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime

import re
import os
import pandas as pd


option = webdriver.ChromeOptions()
# option.binary_location = chrome_path
# option.add_argument("--headless=new")
driver = webdriver.Chrome(options=option)


def amazon(ASIN):
    cwd = os.getcwd()
    if not os.path.exists(os.path.join(cwd, "reviews")):
        os.makedirs(os.path.join(cwd, "reviews"))
    reviews_dir = os.path.join(cwd, "reviews")
    ASIN = str(ASIN)
    url = f"https://www.amazon.in/dp/{ASIN}"

    driver.get(url)

    # WebDriverWait(driver, 30).until(
    #     EC.presence_of_element_located((By.CSS_SELECTOR, 'link[rel="canonical"]'))
    # )

    # Get the actual product name for the respective ASIN
    # We need to use this to navigate to the reviews page, since the URL is dynamic
    canonical_link = driver.find_element(By.CSS_SELECTOR, 'link[rel="canonical"]')
    canonical_url = canonical_link.get_attribute("href")
    start_index = canonical_url.find("amazon.in/") + len("amazon.in/")
    end_index = canonical_url.find("/dp")
    text_between = canonical_url[start_index:end_index]

    # Amazon limits every review section to 10 pages
    # To go beyond this limit, we need to filter reviews by star rating
    # We get a max of 100 reviews per star rating
    # So in the below case, we would get a max of 700 reviews ideally
    # Then we filter duplicate reviews and save the final output
    start_url = [
        f"https://www.amazon.in/{text_between}/product-reviews/{ASIN}/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews&sortBy=recent&filterByStar=five_star",
        f"https://www.amazon.in/{text_between}/product-reviews/{ASIN}/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews&sortBy=recent&filterByStar=four_star",
        f"https://www.amazon.in/{text_between}/product-reviews/{ASIN}/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews&sortBy=recent&filterByStar=three_star",
        f"https://www.amazon.in/{text_between}/product-reviews/{ASIN}/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews&sortBy=recent&filterByStar=two_star",
        f"https://www.amazon.in/{text_between}/product-reviews/{ASIN}/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews&sortBy=recent&filterByStar=one_star",
        f"https://www.amazon.in/{text_between}/product-reviews/{ASIN}/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews&sortBy=recent&filterByStar=positive",
        f"https://www.amazon.in/{text_between}/product-reviews/{ASIN}/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews&sortBy=recent&filterByStar=critical",
    ]
    df = pd.DataFrame(columns=["USERNAME", "RATING", "REVIEW"])

    return reviews_dir, text_between, start_url, df


def scrape(reviews_dir, text_between, ASIN, start_url_list, df):
    for i in range(5):
        start_url = start_url_list[i]
        driver.get(start_url)

        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        pg = 0

        while True:
            review_list = soup.find("div", {"id": "cm_cr-review_list"})
            # Break if no reviews are posted
            if review_list and review_list.find(
                "span",
                string=re.compile(r"Sorry, no reviews match your current selections."),
            ):
                print("No more reviews found.")
                break

            pattern = re.compile(r"customer_review-\w+")
            review_divs = soup.find_all("div", {"id": pattern})

            data = []

            pg += 1
            # print(f"Getting reviews from page {pg}")

            for review_div in review_divs:
                review_text = review_div.find("span", {"data-hook": "review-body"})
                review_uname = review_div.find("span", {"class": "a-profile-name"})
                review_rating = review_div.find("span", {"class": "a-icon-alt"})
                review_date = review_div.find("span", {"data-hook": "review-date"})

                # Cleanup the reviews based on the following conditions
                # 1. Use only the text review if some media is attached
                # 2. Remove newline characters to avoid storing multiple blank paragraphs
                # 3. Extract the review date from the entire string and store it as a datetime object

                if review_text:
                    cleaned_review = re.sub(
                        r"The media could not be loaded\.", "", review_text.text.strip()
                    )
                    cleaned_review = re.sub(r"\n", "", cleaned_review)

                    review_date = review_date.text.strip()
                    review_date = re.sub(r"Reviewed in \w+ on ", "", review_date)
                    review_date = datetime.strptime(review_date, "%d %B %Y")

                    data.append(
                        {
                            "USERNAME": (
                                review_uname.text.strip() if review_uname else ""
                            ),
                            "RATING": (
                                review_rating.text.strip() if review_rating else ""
                            ),
                            "REVIEW": cleaned_review,
                            "DATE": review_date,
                        }
                    )

            df = pd.concat([df, pd.DataFrame(data, index=None)], ignore_index=True)

            # Manually navigate to the ext review page, since putting the page number directly onto the URL does not work
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "a-last"))
            )
            next_page_link = soup.find("li", {"class": "a-last"}).find("a", href=True)

            if next_page_link and "paging_btm_" in next_page_link["href"]:
                next_url = f"https://www.amazon.in{next_page_link['href']}"
                driver.get(next_url)
                html = driver.page_source
                soup = BeautifulSoup(html, "html.parser")
            else:
                break

    driver.quit()

    # Sort df by DATE column
    df = df.sort_values(by="DATE", ascending=False)
    df.to_excel(f"{reviews_dir}\\{text_between}-{ASIN}.xlsx", index=False)
    df.drop_duplicates(inplace=True)

    return f"{reviews_dir}\\{text_between}-{ASIN}.xlsx"
