#!/usr/bin/env python3
"""
Debug script for Upwork scraping - helps identify correct selectors
"""

from scraper import setup_chrome_driver, perform_manual_login, debug_page_state
from selenium.webdriver.common.by import By
import time

def debug_upwork_structure():
    """Debug script to understand Upwork's current page structure."""
    driver = setup_chrome_driver()
    
    try:
        print("=== UPWORK STRUCTURE DEBUG ===")
        
        # Login
        print("1. Performing manual login...")
        perform_manual_login(driver)
        
        # Navigate to jobs page
        print("2. Navigating to jobs page...")
        driver.get("https://www.upwork.com/nx/search/jobs/?q=web%20development")
        time.sleep(5)
        
        print("3. Current URL:", driver.current_url)
        print("4. Page title:", driver.title)
        
        # Save debug info
        debug_page_state(driver, "upwork_jobs_page")
        
        # Try to find various elements
        print("5. Analyzing page structure...")
        
        # Check for common selectors
        selectors_to_test = [
            "[data-test='job-tile']",
            "article[data-test='job-tile']", 
            ".job-tile",
            "[data-cy='job-tile']",
            "article",
            "div[class*='job']",
            "h2", "h3", "h4",
            "a[href*='/jobs/']"
        ]
        
        for selector in selectors_to_test:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                print(f"   {selector}: {len(elements)} elements found")
                
                if elements and len(elements) > 0:
                    # Print first element's HTML for analysis
                    first_element = elements[0]
                    print(f"      First element HTML (truncated): {first_element.get_attribute('outerHTML')[:200]}...")
                    
            except Exception as e:
                print(f"   {selector}: Error - {e}")
        
        # Look for text that might indicate job listings
        page_text = driver.page_source.lower()
        job_indicators = ['job', 'freelance', 'project', 'hiring', 'budget', 'hourly']
        
        print("6. Text analysis:")
        for indicator in job_indicators:
            count = page_text.count(indicator)
            print(f"   '{indicator}' appears {count} times")
        
        # Check if we're on the right page
        if 'search' in driver.current_url and 'jobs' in driver.current_url:
            print("7. ✓ Successfully on jobs search page")
        else:
            print("7. ✗ Not on expected jobs page")
            print(f"   Current URL: {driver.current_url}")
        
        print("\n=== DEBUG COMPLETE ===")
        print("Check the generated debug files for more details:")
        print("- debug_upwork_jobs_page_TIMESTAMP.html")
        print("- debug_upwork_jobs_page_TIMESTAMP.png")
        
        input("Press Enter to close browser...")
        
    except Exception as e:
        print(f"Debug error: {e}")
        debug_page_state(driver, "error_state")
        
    finally:
        driver.quit()

if __name__ == "__main__":
    debug_upwork_structure()