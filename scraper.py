from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from datetime import datetime

def debug_page_state(driver, page_name="debug"):
    """Save page source and screenshot for debugging."""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save page source
        with open(f"debug_{page_name}_{timestamp}.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        
        # Take screenshot
        driver.save_screenshot(f"debug_{page_name}_{timestamp}.png")
        
        print(f"Debug files saved: debug_{page_name}_{timestamp}.html/.png")
        
    except Exception as e:
        print(f"Could not save debug files: {e}")
import os
from datetime import datetime

def setup_chrome_driver():
    """Setup and return a Chrome WebDriver instance."""
    chrome_options = Options()
    
    # Anti-detection options
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    # Additional options for stability
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-features=VizDisplayCompositor")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-plugins")
    chrome_options.add_argument("--disable-images")
    chrome_options.add_argument("--disable-javascript-harmony-shipping")
    chrome_options.add_argument("--disable-background-timer-throttling")
    chrome_options.add_argument("--disable-renderer-backgrounding")
    chrome_options.add_argument("--disable-backgrounding-occluded-windows")
    chrome_options.add_argument("--disable-ipc-flooding-protection")
    
    # Performance options
    chrome_options.add_argument("--memory-pressure-off")
    chrome_options.add_argument("--max_old_space_size=4096")
    
    # Window size
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--start-maximized")
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        
        # Execute anti-detection scripts
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        driver.execute_cdp_cmd('Network.setUserAgentOverride', {
            "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        })
        
        # Set timeouts
        driver.implicitly_wait(10)
        driver.set_page_load_timeout(30)
        
        print("Chrome driver setup completed successfully")
        return driver
        
    except Exception as e:
        print(f"Error setting up Chrome driver: {e}")
        raise

def perform_manual_login(driver):
    """Navigate to Upwork login and wait for manual login."""
    print("Navigating to Upwork login page...")
    driver.get("https://www.upwork.com/ab/account-security/login")
    
    print("\n" + "="*60)
    print("MANUEL GİRİŞ GEREKLİ - MANUAL LOGIN REQUIRED")
    print("="*60)
    print("1. Please login to Upwork in the browser window above")
    print("2. Complete username, password, and 2FA steps")
    print("3. You have 60 seconds to complete the login")
    print("4. The system will automatically continue after login")
    print("="*60)
    
    # Wait 60 seconds for manual login
    time.sleep(60)
    
    # Check if still on login page
    current_url = driver.current_url
    if "login" in current_url.lower():
        print("Warning: Still on login page. Waiting additional 30 seconds...")
        time.sleep(30)

def scrape_jobs_with_driver(driver, search_query="web development", max_pages=2):
    """Scrape Upwork jobs using provided WebDriver instance."""
    wait = WebDriverWait(driver, 15)  # Increased timeout
    
    try:
        # Navigate to job search
        search_url = f"https://www.upwork.com/nx/search/jobs/?q={search_query.replace(' ', '%20')}"
        print(f"Navigating to search: {search_query}")
        driver.get(search_url)
        time.sleep(5)  # Increased wait time
        
        all_jobs = []
        
        for page in range(max_pages):
            print(f"Scraping page {page + 1}...")
            
            try:
                # Multiple selectors to try for job listings
                job_selectors = [
                    "[data-test='job-tile']",
                    "article[data-test='job-tile']", 
                    ".job-tile",
                    "[data-cy='job-tile']",
                    "article"
                ]
                
                job_elements = []
                for selector in job_selectors:
                    try:
                        print(f"Trying selector: {selector}")
                        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
                        job_elements = driver.find_elements(By.CSS_SELECTOR, selector)
                        if job_elements:
                            print(f"Found {len(job_elements)} elements with selector: {selector}")
                            break
                    except Exception as e:
                        print(f"Selector {selector} failed: {e}")
                        continue
                
                if not job_elements:
                    print("No job elements found with any selector. Saving debug info...")
                    debug_page_state(driver, f"no_jobs_page_{page+1}")
                    # Fallback: look for any articles or divs that might contain jobs
                    fallback_elements = driver.find_elements(By.TAG_NAME, "article")
                    if not fallback_elements:
                        fallback_elements = driver.find_elements(By.CSS_SELECTOR, "div[class*='job']") 
                    job_elements = fallback_elements[:10]  # Limit to first 10 to avoid noise
                
                print(f"Processing {len(job_elements)} job elements on page {page + 1}")
                
                for i, job_element in enumerate(job_elements):
                    try:
                        print(f"Processing job element {i+1}...")
                        
                        # Multiple selectors for title and link
                        title_selectors = [
                            "h2 a", "h3 a", "h4 a", "h5 a",
                            "a[data-test*='job-title']",
                            "[data-test='job-title'] a",
                            "a[href*='/jobs/']",
                            "a[title]"
                        ]
                        
                        title_element = None
                        title = ""
                        link = ""
                        
                        for selector in title_selectors:
                            try:
                                title_element = job_element.find_element(By.CSS_SELECTOR, selector)
                                title = title_element.text.strip()
                                link = title_element.get_attribute("href")
                                if title and link:
                                    break
                            except:
                                continue
                        
                        if not title or not link:
                            print(f"Could not find title/link for job element {i+1}, skipping...")
                            continue
                        
                        # Multiple selectors for description
                        description_selectors = [
                            "[data-test='job-description']",
                            "[data-test*='description']",
                            ".job-description",
                            "p", "div p", "span"
                        ]
                        
                        description = ""
                        for selector in description_selectors:
                            try:
                                desc_element = job_element.find_element(By.CSS_SELECTOR, selector)
                                description = desc_element.text.strip()
                                if len(description) > 50:  # Only use if it's substantial
                                    break
                            except:
                                continue
                        
                        if not description:
                            description = "No description available"
                        
                        # Validate the job data
                        if title and link and "upwork.com/jobs/" in link:
                            all_jobs.append({
                                'title': title,
                                'link': link,
                                'description': description
                            })
                            print(f"✓ Successfully extracted: {title[:50]}...")
                        else:
                            print(f"Invalid job data, skipping: title={bool(title)}, link={bool(link)}")
                        
                    except Exception as e:
                        print(f"Error extracting job {i+1}: {e}")
                        continue
                
                print(f"Extracted {len(all_jobs)} valid jobs so far")
                
                # Try to go to next page
                if page < max_pages - 1 and len(all_jobs) > 0:  # Only continue if we found jobs
                    try:
                        print(f"Attempting to navigate to page {page + 2}...")
                        
                        # Multiple selectors for next button
                        next_selectors = [
                            "[data-test='pagination-next']",
                            "[aria-label='Next']", 
                            "button[aria-label*='Next']",
                            "a[aria-label*='Next']",
                            "[data-cy='pagination-next']",
                            "nav [data-test] button:last-child",
                            "nav button:last-child",
                            "[data-test*='next']",
                            "button:contains('Next')",
                            "a:contains('Next')"
                        ]
                        
                        next_clicked = False
                        current_url_before = driver.current_url
                        
                        for selector in next_selectors:
                            try:
                                next_buttons = driver.find_elements(By.CSS_SELECTOR, selector)
                                print(f"Found {len(next_buttons)} elements with selector: {selector}")
                                
                                for next_button in next_buttons:
                                    try:
                                        if next_button.is_enabled() and next_button.is_displayed():
                                            print(f"Clicking next button: {next_button.get_attribute('outerHTML')[:100]}...")
                                            
                                            # Scroll to button first
                                            driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
                                            time.sleep(1)
                                            
                                            # Try regular click first
                                            try:
                                                next_button.click()
                                            except:
                                                # Fallback to JavaScript click
                                                driver.execute_script("arguments[0].click();", next_button)
                                            
                                            # Wait for page to change
                                            time.sleep(5)
                                            
                                            # Check if URL changed or page updated
                                            current_url_after = driver.current_url
                                            if current_url_after != current_url_before or 'page=' in current_url_after:
                                                print(f"✓ Successfully navigated to page {page + 2}")
                                                print(f"URL changed from: {current_url_before}")
                                                print(f"URL changed to: {current_url_after}")
                                                next_clicked = True
                                                break
                                            else:
                                                print(f"URL did not change, trying next method...")
                                                
                                    except Exception as e:
                                        print(f"Error clicking button: {e}")
                                        continue
                                
                                if next_clicked:
                                    break
                                    
                            except Exception as e:
                                print(f"Error with selector {selector}: {e}")
                                continue
                        
                        if not next_clicked:
                            print("Could not find or click next button - probably last page")
                            print("Available pagination elements:")
                            try:
                                # Debug: show all possible pagination elements
                                pagination_elements = driver.find_elements(By.CSS_SELECTOR, "nav, [class*='pag'], [data-test*='pag']")
                                for elem in pagination_elements[:3]:  # Show first 3
                                    print(f"  - {elem.get_attribute('outerHTML')[:200]}...")
                            except:
                                pass
                            break
                            
                    except Exception as e:
                        print(f"Error navigating to next page: {e}")
                        break
                
            except Exception as e:
                print(f"Error on page {page + 1}: {e}")
                # If we have some jobs, continue; if not, break
                if len(all_jobs) == 0:
                    break
                else:
                    continue
        
        print(f"Total jobs found: {len(all_jobs)}")
        return all_jobs
        
    except Exception as e:
        print(f"Scraping error: {e}")
        return []

def scrape_upwork_jobs(search_query="web development", max_pages=2):
    """Convenience function for backward compatibility."""
    driver = setup_chrome_driver()
    try:
        perform_manual_login(driver)
        return scrape_jobs_with_driver(driver, search_query, max_pages)
    finally:
        driver.quit()