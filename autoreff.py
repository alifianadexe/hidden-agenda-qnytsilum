from seleniumbase import SB
import time
import csv
import names
import random
import string

# Function to generate a random filename
def generate_random_filename(length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length)) + '.csv'

def extract_email_password(csv_file):
    emails_passwords = []
    with open(csv_file, 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) >= 2:  # Assuming email is in first column and password in second
                email = row[0]
                password = row[1]
                emails_passwords.append((email, password))
    return emails_passwords

csv_file = 'emails.csv' # Max 5 email per 30 minute, coz hash rate limit
reff_link = "https://multisynq.io/auth?referral=83b94818d4342fcf" # Change your reff link

emails_passwords = extract_email_password(csv_file)

list_email_error = []

for email, password in emails_passwords:
    with SB(uc=True, headed=True) as driver:
        try:
            print(f"Email: {email}, Password: {password}")

            driver.get("https://accounts.google.com/signin")
            driver.type("#identifierId", email)
            driver.click("#identifierNext > div > button")

            driver.sleep(2)
            
            checkPassword = driver.is_element_present("#password")
            if(not checkPassword):
                driver.refresh()
                driver.sleep(1)

                driver.type("#identifierId", email)
                driver.click("#identifierNext > div > button")

                driver.sleep(1)

            driver.type("#password > div.aCsJod.oJeWuf > div > div.Xb9hP > input", password)
            driver.click("#passwordNext > div > button")
            
            driver.sleep(10)  # Do nothing for the given amount of time.
            url =""
            driver.get(url)

            # Double Check 
            driver.driver.uc_open_with_reconnect(url, 3)
            if not driver.is_text_visible("Sign Up", 'h4'):
                driver.sleep(1)
                driver.driver.uc_open_with_reconnect(url, 4)
            
            if not driver.is_text_visible("Sign Up", 'h4'):
                driver.refresh()
                driver.sleep(2)
                driver.driver.uc_open_with_reconnect(url, 4)

            driver.type('[name="email"]', email)
            driver.type('[name="password"]', password)
            driver.type('[name="confirmPassword"]', password)

            driver.click(".css-17wg8y7")

            driver.sleep(15)
            driver.get("https://gmail.com")

            driver.sleep(1)
            driver.click('table td div[role="link"]')

            driver.sleep(1)
            driver.click_link('Verify')

            driver.click('[name="firstName"]')
            driver.sleep(1)
            driver.type('[name="firstName"]', names.get_first_name())
            driver.sleep(1)
            driver.click('[name="lastName"]')
            driver.sleep(1)
            driver.type('[name="lastName"]', names.get_last_name())
            driver.sleep(1)

            driver.click(".css-12sr1n0")
            driver.sleep(15)

        except Exception as e:
            print("This Email Have Exception ", email)
            list_email_error.append((email,password))
            
    time.sleep(3)

filename = "error_email_" + generate_random_filename()

with open(filename, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['email', 'pass'])  # Write header
    csvwriter.writerows(list_email_error)  # Write data