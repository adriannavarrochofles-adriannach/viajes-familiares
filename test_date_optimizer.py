import sys, os, time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

file_path = os.path.abspath('index.html').replace('\\', '/')
file_url = f'file:///{file_path}'

print(f"Testing URL: {file_url}")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1400, 'height': 900})
    page.goto(file_url, wait_until='networkidle')

    # 1. Switch to Cantabria tab
    print("\n--- 1. Testing Cantabria Date Optimization ---")
    page.click('button[data-tab="cantabria"]')
    page.wait_for_timeout(600)

    # Check date box visibility
    opt_box = page.locator('#ai-opt-cantabria')
    assert opt_box.is_visible(), "Cantabria date optimizer box should be visible"
    print("✓ #ai-opt-cantabria is visible")

    # Initial booking link check on first hotel card
    first_hotel_btn = page.locator('#tab-cantabria a.btn-booking').first
    href_initial = first_hotel_btn.get_attribute('href')
    print("Initial Booking URL checkin/out:", [x for x in href_initial.split('&') if 'checkin=' in x or 'checkout=' in x])
    assert 'checkin=2026-12-05' in href_initial, "Initial checkin should be 2026-12-05"
    assert 'checkout=2026-12-08' in href_initial, "Initial checkout should be 2026-12-08"

    # Initial verdict
    v_text = page.locator('#verdict-text-cantabria').inner_text()
    print("Initial verdict preview:", v_text[:80])
    assert "Puente de Diciembre" in v_text, "Verdict should mention Puente de Diciembre"

    # Initial lodging price in table
    init_hotel_cost = page.locator('#ct-table-hotel-cost').inner_text()
    print(f"Initial hotel cost (4 adults): {init_hotel_cost}")

    # 2. Click Pre-Navidad Económica pill
    print("\n--- 2. Clicking Pre-Navidad Económica Pill ---")
    page.click('#pill-cantabria-prenav')
    page.wait_for_timeout(500)

    # Check active class
    prenav_pill = page.locator('#pill-cantabria-prenav')
    assert 'active' in prenav_pill.get_attribute('class'), "Pre-nav pill should be active"

    # Check updated verdict
    v_prenav = page.locator('#verdict-text-cantabria').inner_text()
    print("Pre-Nav verdict preview:", v_prenav[:90])
    assert "Pre-Navidad" in v_prenav or "Ahorro" in v_prenav, "Verdict should mention Pre-Navidad or Ahorro"

    # Check updated Booking URL
    href_prenav = first_hotel_btn.get_attribute('href')
    print("Updated Booking URL:", [x for x in href_prenav.split('&') if 'checkin=' in x or 'checkout=' in x])
    assert 'checkin=2026-11-27' in href_prenav, "Checkin should update to 2026-11-27"
    assert 'checkout=2026-11-30' in href_prenav, "Checkout should update to 2026-11-30"

    # Check lodging cost reduced
    prenav_hotel_cost = page.locator('#ct-table-hotel-cost').inner_text()
    print(f"Pre-nav hotel cost: {prenav_hotel_cost} (was {init_hotel_cost})")
    assert int(prenav_hotel_cost.replace('€', '').strip()) < int(init_hotel_cost.replace('€', '').strip()), "Lodging cost should decrease"

    # 3. Test Custom Date Picker in Cantabria (Autumn test)
    print("\n--- 3. Testing Custom Date Picker (Autumn Oct 15-19) ---")
    page.click('#pill-cantabria-custom')
    page.wait_for_timeout(300)
    assert page.locator('#custom-row-cantabria').is_visible(), "Custom row should be visible"

    page.fill('#input-cantabria-in', '2027-10-15')
    page.fill('#input-cantabria-out', '2027-10-19')
    page.click('#custom-row-cantabria .btn-apply-custom')
    page.wait_for_timeout(500)

    v_custom = page.locator('#verdict-text-cantabria').inner_text()
    print("Custom Autumn verdict:", v_custom[:100])
    assert "Otoño" in v_custom or "Secuoyas" in v_custom or "15/10/2027" in v_custom, "AI assessment should evaluate Autumn"

    href_custom = first_hotel_btn.get_attribute('href')
    print("Custom Booking URL:", [x for x in href_custom.split('&') if 'checkin=' in x or 'checkout=' in x])
    assert 'checkin=2027-10-15' in href_custom, "Checkin should be 2027-10-15"
    assert 'checkout=2027-10-19' in href_custom, "Checkout should be 2027-10-19"

    # Take screenshot of Cantabria Date Optimizer
    page.screenshot(path='C:/Users/ANAVARRO/.gemini/antigravity/brain/520f1cd2-1b21-4165-8006-9960d094228a/test_cantabria_date_opt.png')
    print("Saved test_cantabria_date_opt.png")

    # 4. Switch to Granada tab
    print("\n--- 4. Testing Granada Date Optimization ---")
    page.click('button[data-tab="granada"]')
    page.wait_for_timeout(600)

    opt_box_gr = page.locator('#ai-opt-granada')
    assert opt_box_gr.is_visible(), "Granada date optimizer box should be visible"
    print("✓ #ai-opt-granada is visible")

    first_gr_hotel_btn = page.locator('#tab-granada a.btn-booking').first
    href_gr_initial = first_gr_hotel_btn.get_attribute('href')
    assert 'checkin=2026-12-05' in href_gr_initial, "Initial Granada checkin should be 2026-12-05"

    # Click Valle de Nieve pill
    print("\n--- 5. Clicking Valle de Nieve Óptimo (Jan 22-25) in Granada ---")
    page.click('#pill-granada-snow')
    page.wait_for_timeout(500)

    v_snow = page.locator('#verdict-text-granada').inner_text()
    print("Snow verdict preview:", v_snow[:100])
    assert "Nieve" in v_snow or "trineos" in v_snow or "35%" in v_snow, "Verdict should mention snow/trineos/ahorro"

    href_gr_snow = first_gr_hotel_btn.get_attribute('href')
    print("Updated Granada Booking URL:", [x for x in href_gr_snow.split('&') if 'checkin=' in x or 'checkout=' in x])
    assert 'checkin=2027-01-22' in href_gr_snow, "Granada checkin should update to 2027-01-22"
    assert 'checkout=2027-01-25' in href_gr_snow, "Granada checkout should update to 2027-01-25"

    # Take screenshot of Granada Date Optimizer
    page.screenshot(path='C:/Users/ANAVARRO/.gemini/antigravity/brain/520f1cd2-1b21-4165-8006-9960d094228a/test_granada_date_opt.png')
    print("Saved test_granada_date_opt.png")

    browser.close()

print("\n🎉 ALL TESTS PASSED! Date management & Seasonal Valuation engine fully operational!")
