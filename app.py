from bs4 import BeautifulSoup
import requests

# Fetch the HTML content of the T-Mobile plans page
source = requests.get('https://www.t-mobile.com/cell-phone-plans').text

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(source, 'lxml')
plan_list = []

# Print header information
print("\nT-Mobile Available Plans:")
print("(Check latest prices at: https://www.t-mobile.com/cell-phone-plans)\n")
counter = 0

# Loop through each plan card on the page
for plan in soup.find_all('li', class_="upf-planCard--border-shadow"):
    # Skip hidden plan cards (that are duplicates)
    if plan.get('data-upf-plan-card-hide') is not None:
        continue

    # Extract the plan name and benefits
    name = plan.find('h3', class_='upf-planCard__plan-name').text
    benefits = plan.find('div', class_='upf-planCard__feature-list').text
    
    # Add the plan to the list if it's not already included
    if name not in plan_list:
        plan_list.append({name, benefits})

# Print each plan's details
for single, benefits in plan_list:
    counter += 1
    print(f"{counter}. {single}\n{benefits}")