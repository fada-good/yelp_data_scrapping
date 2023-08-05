from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd
import time

print("Enter the details to get the data:")
service = input("Enter the Type of Service (e.g., Restaurants, Hotels): ")
location = input("Enter the Location (e.g., San Francisco): ")
pages = int(input("Enter the Number of Pages to Scrape: "))

data = []
columns = ["Name", "Star Rating", "Total Reviews", "Location", "Review", "Phone Number"]
df = pd.DataFrame(data, columns=columns)

print("Scrapping data ....")

for page in range(1, pages + 1):
    time.sleep(1)
    url = f"https://www.yelp.com/search?find_desc={service}&find_loc={location}&start={page * 10}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    business_list = soup.find_all("div", class_="padding-t3__09f24__TMrIW padding-r3__09f24__eaF7p padding-b3__09f24__S8R2d padding-l3__09f24__IOjKY border-color--default__09f24__NPAKY")
    print(len(business_list))
    for business in business_list:
        name_element = business.find("a", class_="css-19v1rkv")
        name = name_element.get_text(strip=True) if name_element else None
        totalReviews_element = business.find("span", class_="css-chan6m")
        totalReviews = totalReviews_element.get_text(strip=True) if totalReviews_element else None
        location_element = business.find("p", class_="css-dzq7l1")
        location = location_element.get_text(strip=True).strip('$') if location_element else None
        stars_elem = business.find("div", class_="five-stars__09f24__mBKym")
        stars = stars_elem['aria-label'] if stars_elem else None
        review_element = business.find("p", class_="css-16lklrv")
        review = review_element.get_text(strip=True) if review_element else None

        phone_numbers = []
        span_elements = business.find_all("span", class_="css-1wayfxy")
        for span_element in span_elements:
            href = span_element.find("a")["href"]
            phone_response = requests.get("https://www.yelp.com" + href)
            phone_soup = BeautifulSoup(phone_response.text, "html.parser")
            phone_element = phone_soup.find("p", class_="css-14qygu0") or phone_soup.find("p", class_="css-1p9ibgf")
            print(phone_element)
            phone_number = phone_element.get_text(strip=True) if phone_element else None
            phone_numbers.append(phone_number)

        df_row = pd.DataFrame([{"Name": name, "Star Rating": stars, "Total Reviews": totalReviews,
                                "Location": location, "Review": review, "Phone Number": phone_numbers}])
        df = pd.concat([df, df_row], axis=0)

filename = "scraped_data.csv"
df.to_csv(filename, index=False, encoding="utf-8")

print("Done..")
