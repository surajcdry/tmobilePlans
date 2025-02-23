from bs4 import BeautifulSoup
import requests
import csv
import datetime # for logging
import pytz # to convert time from Universal to EST

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

def save_to_csv(plan_list):
    """Save the plans to a CSV file"""
    csv_file = 'plans.csv'
    
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write header
        writer.writerow(['Name', 'Benefits'])
        
        # Write plan data
        for name, benefits in plan_list:
            writer.writerow([name, benefits])

def save_log(success, message):
    """Save execution log with timestamp"""
    est = pytz.timezone('America/New_York') # timezone change
    timestamp = datetime.datetime.now(est).strftime("%Y-%m-%d %H:%M:%S %Z")
    with open('crawler.log', 'a', encoding='utf-8') as file:
        log_entry = f"[{timestamp}] {'SUCCESS' if success else 'FAILED'}: {message}\n"
        file.write(log_entry)

def main():
    try:
        url = 'https://www.t-mobile.com/cell-phone-plans'
        html = fetch_html(url)
        
        if html is None:
            save_log(False, "Failed to fetch HTML content")
            print("No plans found")
            return
            
        plan_list = parse_html(html)
        if not plan_list:
            save_log(False, "No plans found in the HTML content")
            print("No plans found")
            return
            
        print_plans(plan_list)
        save_to_csv(plan_list)
        save_log(True, f"Successfully scraped {len(plan_list)} plans")
        print("\nPlans have been saved to plans.csv")
    except Exception as e:
        save_log(False, f"Error occurred: {str(e)}")
        raise e

if __name__ == '__main__':
    main()