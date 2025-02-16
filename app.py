from bs4 import BeautifulSoup
import requests

def fetch_html(url):
    """Fetch the HTML content of the T-Mobile plans page"""
    # Error handling in case the request fails
    try:
        response = requests.get(url).text
        return response
    except:
        print("An error occurred while fetching the HTML content.")
        return None

def parse_html(html):
    """Parse the HTML content using BeautifulSoup and extract the plan names and benefits"""
    soup = BeautifulSoup(html, 'lxml')
    plan_list = []

    for plan in soup.find_all('li', class_="upf-planCard--border-shadow"):
        # Skip hidden plan cards (that are duplicates)
        if plan.get('data-upf-plan-card-hide') is not None:
            continue

        # Extract the plan name and benefits
        name = plan.find('h3', class_='upf-planCard__plan-name').text.strip()
        benefits = plan.find('div', class_='upf-planCard__feature-list').text.strip()
        
        # Add the plan to the list if it's not already included
        if (name, benefits) not in plan_list:
            plan_list.append((name, benefits))

    return plan_list

def print_plans(plan_list):
    """Print plan details"""

    # Print heading and link to latest prices
    print("\nT-Mobile Cell Phone Plans\n")
    print("(Check latest prices at: https://www.t-mobile.com/cell-phone-plans)\n")
    
    counter = 0

    # Print each plan's details
    for (name, benefits) in plan_list:
        counter += 1
        print(f"{counter}. {name}\n{benefits}\n")

def main():
    url = 'https://www.t-mobile.com/cell-phone-plans'
    html = fetch_html(url)
    if html:
        plan_list = parse_html(html)
        print_plans(plan_list)

if __name__ == '__main__':
    main()