import sys, os
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

file_path = os.path.abspath('index.html').replace('\\', '/')
file_url = f'file:///{file_path}'

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    # iPhone 12/13/14 viewport (390 x 844)
    page = browser.new_page(viewport={'width': 390, 'height': 844}, device_scale_factor=3)
    page.goto(file_url, wait_until='networkidle')

    # 1. Cantabria check
    print("\n--- 1. Testing Cantabria Mobile KPIs ---")
    page.click('button[data-tab="cantabria"]')
    page.wait_for_timeout(500)

    ct_cards = page.locator('#tab-cantabria .portal-hero .kpi-card').all()
    print(f"Cantabria KPI cards count: {len(ct_cards)}")
    for i, c in enumerate(ct_cards):
        text = c.inner_text().replace('\n', ' | ')
        bg = c.evaluate("el => window.getComputedStyle(el).backgroundColor")
        color = c.evaluate("el => window.getComputedStyle(el).color")
        box = c.bounding_box()
        print(f"  CT Card {i}: text='{text}', bg={bg}, box={box}")
        # Ensure card is NOT plain white
        assert bg != 'rgb(255, 255, 255)', f"Card {i} should NOT have a white background!"

    ct_screenshot = 'C:/Users/ANAVARRO/.gemini/antigravity/brain/520f1cd2-1b21-4165-8006-9960d094228a/test_cantabria_kpis_fixed.png'
    page.screenshot(path=ct_screenshot)
    print(f"Saved Cantabria mobile screenshot: {ct_screenshot}")

    # 2. Granada check
    print("\n--- 2. Testing Granada Mobile KPIs ---")
    page.click('button[data-tab="granada"]')
    page.wait_for_timeout(500)

    gr_cards = page.locator('#tab-granada .portal-hero .kpi-card').all()
    print(f"Granada KPI cards count: {len(gr_cards)}")
    for i, c in enumerate(gr_cards):
        text = c.inner_text().replace('\n', ' | ')
        bg = c.evaluate("el => window.getComputedStyle(el).backgroundColor")
        box = c.bounding_box()
        print(f"  GR Card {i}: text='{text}', bg={bg}, box={box}")
        assert bg != 'rgb(255, 255, 255)', f"Card {i} should NOT have a white background!"

    gr_screenshot = 'C:/Users/ANAVARRO/.gemini/antigravity/brain/520f1cd2-1b21-4165-8006-9960d094228a/test_granada_kpis_fixed.png'
    page.screenshot(path=gr_screenshot)
    print(f"Saved Granada mobile screenshot: {gr_screenshot}")

    browser.close()

print("\n🎉 ALL CHECKS PASSED! No blank white boxes exist in mobile view!")
