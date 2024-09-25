from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

def login_to_linkedin(driver, email, password):
    driver.get('https://www.linkedin.com/login')
    time.sleep(2)
   
    email_input = driver.find_element(By.ID, 'username')
    password_input = driver.find_element(By.ID, 'password')
   
    email_input.send_keys(email)
    password_input.send_keys(password)
   
    login_button = driver.find_element(By.XPATH, '//button[@type="submit"]')
    login_button.click()
    time.sleep(20)

def go_to_next_page(driver, max_scroll=5):
    try:
        next_button = driver.find_element(By.XPATH, '//button[contains(@class, "artdeco-pagination__button--next")]')
        next_button.click()
        time.sleep(5)  # wait for the next page to load
        for _ in range(max_scroll):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)
        return True
    except Exception as e:
        print(f"Error going to the next page: {e}")
        return False

def scrape_linkedin_hashtag(email, password, hashtag, max_scroll=5, max_pages=5):
    # Set up the WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    
    try:
        # Log in to LinkedIn
        login_to_linkedin(driver, email, password)
        
        # Navigate to the hashtag page
        hashtag_url = f'https://www.linkedin.com/feed/hashtag/?keywords={hashtag}'
        driver.get(hashtag_url)
        
        # Wait for the page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'scaffold-finite-scroll__content'))
        )
        
        post_data = []
        profile_links = set()

        for _ in range(max_pages):
            # Infinite scroll: scroll down several times to load more posts
            for _ in range(max_scroll):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(7)  # Adjust sleep time based on your network speed and page load speed
            
            # Extract posts
            posts = driver.find_elements(By.CLASS_NAME, 'relative')

            for post in posts:
                try:
                    author_element = post.find_element(By.CLASS_NAME, 'update-components-actor__name')
                    profile_link_element = post.find_element(By.CLASS_NAME, 'app-aware-link')
                    
                    author = author_element.text if author_element else 'Unknown'
                    profile_link = profile_link_element.get_attribute('href') if profile_link_element else 'No link'
                    
                    if profile_link not in profile_links:
                        profile_links.add(profile_link)
                        post_data.append({'author': author, 'profile_link': profile_link})
                except Exception as e:
                    print(f"Error extracting post: {e}")

            if not go_to_next_page(driver, max_scroll):
                break

        # Write data to a structured text file
        output_file = f'{hashtag}_linkedin_hashtag.txt'
        with open(output_file, 'w', encoding='utf-8') as file:
            for post in post_data:
                file.write(f"Author: {post['author']}\nProfile Link: {post['profile_link']}\n\n")

        print(f"Scraped {len(post_data)} authors and saved to {output_file}")

    finally:
        # Close the WebDriver
        driver.quit()

# Example usage:
scrape_linkedin_hashtag('heatpubg281q@gmail.com', 'Pratham_1234', 'ai4conference', max_scroll=5, max_pages=5)
