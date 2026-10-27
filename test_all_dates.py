import sys, os
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

file_path = os.path.abspath('index.html').replace('\\', '/')
file_url = f'file:///{file_path}'

print(f"Testing URL: {file_url}")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1400, 'height': 900})
    page.goto(file_url, wait_until='networkidle')

    destinations_to_test = ['cantabria', 'granada', 'francia', 'belgica', 'dinamarca', 'birmingham', 'grecia', 'sanseb', 'alsacia']

    for dest in destinations_to_test:
        print(f"\n--- Testing {dest} ---")
        tab_btn = page.locator(f'button[data-tab="{dest}"]')
        if not tab_btn.is_visible():
            print(f"Tab button for {dest} not directly visible, scrolling...")
            tab_btn.scroll_into_view_if_needed()
        tab_btn.click()
        page.wait_for_timeout(400)

        opt_box = page.locator(f'#ai-opt-{dest}')
        assert opt_box.is_visible(), f"Date optimizer box #ai-opt-{dest} should be visible"
        print(f"✓ #ai-opt-{dest} is visible")

        # Check verdict banner
        v_el = page.locator(f'#verdict-text-{dest}')
        assert v_el.is_visible(), f"Verdict text for {dest} should be visible"
        v_text = v_el.inner_text()
        print(f"  Verdict: {v_text[:75]}...")

        # Find first booking link in tab
        booking_links = page.locator(f'#tab-{dest} a[href*="booking.com"]')
        count = booking_links.count()
        print(f"  Booking.com links in tab: {count}")
        if count > 0:
            href_init = booking_links.first.get_attribute('href')
            print(f"  Sample checkin param: {[x for x in href_init.split('&') if 'checkin=' in x]}")

    browser.close()

print("\n🎉 ALL 9 DESTINATIONS VERIFIED SUCCESSFULLY!")
