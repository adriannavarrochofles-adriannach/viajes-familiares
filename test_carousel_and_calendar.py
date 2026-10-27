import sys, os, time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

print("Starting Playwright verification of Hotel Carousel and Outlook Calendar...")

INDEX_PATH = os.path.abspath("index.html")
FILE_URL = f"file:///{INDEX_PATH.replace(os.sep, '/')}"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    
    # ----------------------------------------------------
    # TEST 1: DESKTOP VIEWPORT (1280 x 900)
    # ----------------------------------------------------
    page = browser.new_page(viewport={"width": 1280, "height": 900})
    
    # Capture console errors
    console_errors = []
    page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
    page.on("pageerror", lambda err: console_errors.append(str(err)))

    page.goto(FILE_URL, wait_until="domcontentloaded")
    time.sleep(1)

    # Navigate to Cantabria tab
    page.click('.nav-btn[data-tab="cantabria"]')
    time.sleep(0.5)

    print("\n--- TEST HOTEL CAROUSEL ---")
    # Verify hotel carousel exists and has 6 cards
    hotel_cards = page.locator('#tab-cantabria .hotel-cards-container .hotel-card')
    card_count = hotel_cards.count()
    print(f"Cantabria hotel cards count: {card_count}")
    assert card_count == 6, f"Expected 6 cards, got {card_count}"

    # Verify horizontal layout
    container_box = page.locator('#tab-cantabria .hotel-cards-container').bounding_box()
    card1_box = hotel_cards.nth(0).bounding_box()
    card2_box = hotel_cards.nth(1).bounding_box()
    print(f"Card 1 X: {card1_box['x']}, Card 2 X: {card2_box['x']}")
    assert card2_box['x'] > card1_box['x'], "Cards should be arranged horizontally side by side"

    # Test clicking Next arrow
    initial_scroll = page.evaluate("document.querySelector('#tab-cantabria .hotel-cards-container').scrollLeft")
    page.click('#tab-cantabria .hotel-carousel-arrows .btn-scroll-arrow:has-text("Siguiente")')
    time.sleep(0.5)
    new_scroll = page.evaluate("document.querySelector('#tab-cantabria .hotel-cards-container').scrollLeft")
    print(f"Scroll after 'Siguiente': {initial_scroll} -> {new_scroll}")
    assert new_scroll > initial_scroll, "Carousel should scroll to the right"

    # Test selecting a different hotel: Apartamentos Rurales Picos de Europa (Potes, 260 € / 435 €)
    initial_kpi = page.locator('#ct-kpi-total').inner_text()
    print(f"Initial trip KPI budget: {initial_kpi}")

    btn_potes = page.locator('#btn-hotel-ct_potes')
    btn_potes.click()
    time.sleep(0.3)

    new_kpi = page.locator('#ct-kpi-total').inner_text()
    hotel_desc = page.locator('#ct-table-hotel-desc').inner_text()
    hotel_cost = page.locator('#ct-table-hotel-cost').inner_text()
    print(f"After selecting Potes: KPI={new_kpi}, TableDesc='{hotel_desc}', TableCost='{hotel_cost}'")
    assert "Potes" in hotel_desc or "Rurales" in hotel_desc, f"Hotel table desc should mention Potes: {hotel_desc}"
    assert "260" in hotel_cost or "435" in hotel_cost, f"Hotel cost should update: {hotel_cost}"

    # Select back default Casona del Saja
    page.locator('#btn-hotel-ct_casona_saja').click()
    time.sleep(0.3)

    print("\n--- TEST OUTLOOK ACTIVITY PLANNER ---")
    # Verify Outlook planner container is visible
    planner = page.locator('#outlook-planner-cantabria')
    assert planner.is_visible(), "Outlook planner should be visible"

    # Check 4 day columns
    cols = page.locator('#outlook-grid-cantabria .outlook-day-col')
    assert cols.count() == 4, f"Expected 4 day columns, got {cols.count()}"
    print(f"Found {cols.count()} day columns in Outlook planner")

    # Check Day 1 activities count and headers
    day1_cards = page.locator('#col-cantabria-day-1 .outlook-event-card')
    print(f"Day 1 initial activities: {day1_cards.count()}")
    assert day1_cards.count() == 5, f"Expected 5 activities on Day 1, got {day1_cards.count()}"

    # Check first activity has time badge, duration pills, etc.
    first_act = day1_cards.nth(0)
    time_badge = first_act.locator('.ev-time-badge').inner_text()
    insitu_pill = first_act.locator('.ev-pill-insitu').inner_text()
    travel_pill = first_act.locator('.ev-pill-travel').inner_text()
    total_pill = first_act.locator('.ev-pill-total').inner_text()
    print(f"First activity: Time='{time_badge}', InSitu='{insitu_pill}', Travel='{travel_pill}', Total='{total_pill}'")
    assert "11:55" in time_badge or "11:45" in time_badge, f"Unexpected time badge: {time_badge}"
    assert "1h 15m" in insitu_pill, f"Unexpected in situ pill: {insitu_pill}"
    assert "10m" in travel_pill, f"Unexpected travel pill: {travel_pill}"
    assert "1h 25m" in total_pill, f"Unexpected total pill: {total_pill}"

    # Test moving activity down: ▲ / ▼
    page.locator('#card-cantabria-ct_secuoyas .btn-ev-move:has-text("▼")').click()
    time.sleep(0.3)
    day1_cards_after_move = page.locator('#col-cantabria-day-1 .outlook-event-card')
    new_first_id = day1_cards_after_move.nth(0).get_attribute('data-act-id')
    print(f"After moving Secuoyas down, first activity is now: {new_first_id}")
    assert new_first_id == "ct_cocido_montanes", f"Expected Cocido to be first, got {new_first_id}"

    # Move it back up
    page.locator('#card-cantabria-ct_secuoyas .btn-ev-move:has-text("▲")').click()
    time.sleep(0.3)

    # Test moving an activity to another day (e.g. Move Cartes to Day 2)
    cartes_d2_btn = page.locator('#card-cantabria-ct_cartes .btn-ev-day:has-text("D2")')
    cartes_d2_btn.click()
    time.sleep(0.3)

    day1_after_transfer = page.locator('#col-cantabria-day-1 .outlook-event-card').count()
    day2_after_transfer = page.locator('#col-cantabria-day-2 .outlook-event-card').count()
    print(f"After moving Cartes to Day 2: Day 1 has {day1_after_transfer} acts, Day 2 has {day2_after_transfer} acts")
    assert day1_after_transfer == 4, f"Day 1 should now have 4 activities, got {day1_after_transfer}"
    assert day2_after_transfer == 6, f"Day 2 should now have 6 activities, got {day2_after_transfer}"

    # Reset schedule via button
    page.on("dialog", lambda dialog: dialog.accept())
    page.click('#outlook-planner-cantabria .btn-outlook-reset')
    time.sleep(0.5)

    day1_restored = page.locator('#col-cantabria-day-1 .outlook-event-card').count()
    print(f"After Reset: Day 1 has {day1_restored} activities")
    assert day1_restored == 5, f"Expected 5 restored activities, got {day1_restored}"

    # Test view switch to timeline and back
    page.click('#btn-view-tl-cantabria')
    time.sleep(0.3)
    assert not page.locator('#outlook-planner-cantabria').is_visible(), "Planner should hide in timeline mode"
    assert page.locator('#timeline-cantabria').is_visible(), "Timeline should show in timeline mode"

    page.click('#btn-view-cal-cantabria')
    time.sleep(0.3)
    assert page.locator('#outlook-planner-cantabria').is_visible(), "Planner should show in calendar mode"

    # Take desktop screenshot
    page.locator('#outlook-planner-cantabria').scroll_into_view_if_needed()
    time.sleep(0.3)
    page.screenshot(path="artifact_test_desktop_calendar.png", full_page=False)
    print("Desktop screenshot captured: artifact_test_desktop_calendar.png")

    # ----------------------------------------------------
    # TEST 2: MOBILE VIEWPORT (iPhone 14 / 390 x 844)
    # ----------------------------------------------------
    mobile_page = browser.new_page(viewport={"width": 390, "height": 844}, is_mobile=True)
    mobile_page.goto(FILE_URL, wait_until="domcontentloaded")
    time.sleep(1)

    mobile_page.click('.nav-btn[data-tab="cantabria"]')
    time.sleep(0.5)

    # Check mobile carousel
    mobile_carousel = mobile_page.locator('#tab-cantabria .hotel-cards-container')
    assert mobile_carousel.is_visible(), "Mobile hotel carousel should be visible"
    
    # Check mobile tabs in planner
    tab_d2 = mobile_page.locator('#mobile-tabs-cantabria button:has-text("Día 2")')
    assert tab_d2.is_visible(), "Mobile day 2 tab should be visible"
    tab_d2.click()
    time.sleep(0.3)

    col1_disp = mobile_page.locator('#col-cantabria-day-1').evaluate("el => window.getComputedStyle(el).display")
    col2_disp = mobile_page.locator('#col-cantabria-day-2').evaluate("el => window.getComputedStyle(el).display")
    print(f"Mobile tab 'Día 2' active: Col 1 display={col1_disp}, Col 2 display={col2_disp}")
    assert col1_disp == "none", "Col 1 should be hidden"
    assert col2_disp == "flex", "Col 2 should be displayed"

    # Scroll down to calendar card
    mobile_page.locator('#card-cantabria-ct_cabarceno_safari').scroll_into_view_if_needed()
    time.sleep(0.3)
    mobile_page.screenshot(path="artifact_test_mobile_calendar.png", full_page=False)
    print("Mobile screenshot captured: artifact_test_mobile_calendar.png")

    print("\nConsole errors during test:", console_errors)
    assert len(console_errors) == 0, f"Found console errors: {console_errors}"

    browser.close()

print("\nALL PLAYWRIGHT TESTS PASSED 100% PERFECTLY!")
