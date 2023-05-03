import datetime

import pytest
from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


@pytest.mark.usefixtures("browser")
def test_ui_automation_task_xm(browser='Chrome'):
    # Using needed browser
    if browser == 'Chrome':
        driver = webdriver.Chrome()
    elif browser == 'Firefox':
        driver = webdriver.Firefox()
    else:
        print('Invalid browser selection')

    # Navigating to URL
    driver.get('https://www.xm.com/')

    driver.maximize_window()

    # Closing the pop-up
    driver.find_element(By.XPATH, '//button[text()="ACCEPT ALL"]').click()

    # Asserting that the test is on the home page
    xml_logo = driver.find_element(By.XPATH, '//a[@href="https://www.xm.com"]')
    assert xml_logo.size != 0, 'Home Page not present'

    # Opening the RESEARCH & EDUCATION dropdown
    driver.find_element(By.LINK_TEXT, 'RESEARCH & EDUCATION').click()

    # Asserting the RESEARCH & EDUCATION appeared
    research_page = driver.find_element(By.XPATH, '//a[@href="https://www.xm.com/research/overview"]').is_displayed()
    assert research_page, 'RESEARCH & EDUCATION menu not present'

    # Waiting for the Economic Calendar page to appear on the dropdown
    WebDriverWait(driver, 3).until(
        EC.element_to_be_clickable((By.XPATH, '//a[@href="https://www.xm.com/research/economicCalendar"]')))

    # Navigating to the Economic calendar page
    driver.find_element(By.XPATH, '//a[@href="https://www.xm.com/research/economicCalendar"]').click()
    economic_calendar = driver.find_element(By.XPATH, '//h2[text()="Economic Calendar"]').is_displayed()
    assert economic_calendar, 'Economic Calendar page not opened'

    # Waiting for the Event table to load and switching to the iframe
    WebDriverWait(driver, 10).until(
        EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, 'iframe#iFrameResizer0')))
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'mat-slider-thumb')))

    # Getting the Recent and Next Events count
    recent_and_next_events_count = driver.find_element(By.XPATH,
                                                       '//div[@class="tc-economic-calendar-view-container-title tc-normal-text"]').text

    # Getting the slider and moving it to get the Today events
    slider = driver.find_element(By.CLASS_NAME, 'mat-slider-thumb')
    move = webdriver.ActionChains(driver)
    move.click_and_hold(slider).move_by_offset(30, 0).release().perform()

    # Waiting that it says Today in the calendar
    period_value = driver.find_element(By.CLASS_NAME, 'tc-finalval-tmz')
    WebDriverWait(period_value, 10).until(
        EC.text_to_be_present_in_element((By.CLASS_NAME, 'ng-star-inserted'), 'Today'))

    # Waiting for the events list to be updated
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.TAG_NAME, 'tc-economic-calendar-row')))

    # Getting the count of events for Today
    todays_events_count = driver.find_element(By.XPATH,
                                              '//div[@class="tc-economic-calendar-view-container-title tc-normal-text"]').text

    # Verify that the count has been updated
    assert recent_and_next_events_count != todays_events_count, 'Event count has not been updated when changing to Today'

    # Asserting the date in the calendar is correct
    current_date = driver.find_element(By.XPATH,
                                       '//span[@class="tc-economic-calendar-item-header-left-title tc-normal-text"]').text
    assert current_date == datetime.datetime.now().strftime("%Y %B %d"), 'The date for today is not correct in the calendar'

    # Getting the first three rows from the events list
    today_events = driver.find_elements(By.TAG_NAME, 'tc-economic-calendar-row')
    first_today_event = today_events[0].text
    second_today_event = today_events[1].text
    third_today_event = today_events[2].text

    # Moving the slider to Tomorrow
    move.click_and_hold(slider).move_by_offset(60, 0).release().perform()

    # Waiting for it to say Tomorrow
    WebDriverWait(period_value, 10).until(
        EC.text_to_be_present_in_element((By.CLASS_NAME, 'ng-star-inserted'), 'Tomorrow'))

    # Waiting for the Events list to be updated
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.TAG_NAME, 'tc-economic-calendar-row')))

    # Getting the date from the calendar
    tomorrow_date = driver.find_element(By.XPATH,
                                        '//span[@class="tc-economic-calendar-item-header-left-title tc-normal-text"]').text

    # Verifying the date in the calendar is correct
    assert tomorrow_date == (datetime.datetime.now() + datetime.timedelta(days=1)).strftime(
        "%Y %B %d"), 'Time interval is not correct, should be date from tomorrow'

    # Verifying that the events count has been updated
    tomorrows_events_count = driver.find_element \
        (By.XPATH, '//div[@class="tc-economic-calendar-view-container-title tc-normal-text"]').text
    assert tomorrows_events_count != todays_events_count, 'Event count has not been updated for tomorrow'

    # Getting the first three rows for tomorrow events
    tomorrows_events = driver.find_elements(By.TAG_NAME, 'tc-economic-calendar-row')
    first_tomorrow_event = tomorrows_events[0].text
    second_tomorrow_event = tomorrows_events[1].text
    third_tomorrow_event = tomorrows_events[2].text

    # Verifying the event list has been updated when changing to Tomorrow
    assert ((first_today_event != first_tomorrow_event) or (second_today_event != second_tomorrow_event)
            or (third_today_event != third_tomorrow_event)), 'Event list has not been updated when changing to tomorrow'

    # Moving the slider to Next Week
    move.click_and_hold(slider).move_by_offset(90, 0).release().perform()

    # Waiting for it to say Next Week
    WebDriverWait(period_value, 10).until(
        EC.text_to_be_present_in_element((By.CLASS_NAME, 'ng-star-inserted'), 'Next Week'))

    # Waiting for the Events list to be updated
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.TAG_NAME, 'tc-economic-calendar-row')))

    # Getting the date from the calendar
    next_week_date = driver.find_element(By.XPATH,
                                         '//span[@class="tc-economic-calendar-item-header-left-title tc-normal-text"]').text

    # Verifying the date in the calendar is correct
    last_monday = datetime.date.today() + datetime.timedelta(days=-datetime.date.today().weekday(), weeks=1)
    assert next_week_date == last_monday.strftime("%Y %B %d"), 'Time interval is not correct, should be next Monday'

    # Verifying that the events count has been updated
    next_week_events_count = driver.find_element \
        (By.XPATH, '//div[@class="tc-economic-calendar-view-container-title tc-normal-text"]').text
    assert tomorrows_events_count != next_week_events_count, 'Number of events has not been updated'

    # Getting the first three rows for next week events
    next_week_events = driver.find_elements(By.TAG_NAME, 'tc-economic-calendar-row')
    first_next_week_event = next_week_events[0].text
    second_next_week_event = next_week_events[1].text
    third_next_week_event = next_week_events[2].text

    # Verifying the event list has been updated when changing to Next Week
    assert ((first_next_week_event != first_tomorrow_event) or (second_next_week_event != second_tomorrow_event)
            or (third_next_week_event != third_tomorrow_event))

    # Moving the slider to Next Month
    move.click_and_hold(slider).move_by_offset(150, 0).release().perform()

    # Waiting for it to say Next Week
    WebDriverWait(period_value, 10).until(
        EC.text_to_be_present_in_element((By.CLASS_NAME, 'ng-star-inserted'), 'Next Month'))

    # Waiting for the Events list to be updated
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.TAG_NAME, 'tc-economic-calendar-row')))

    # Getting the date from the calendar
    next_month_date = driver.find_element(By.XPATH,
                                          '//span[@class="tc-economic-calendar-item-header-left-title tc-normal-text"]').text

    # Verifying the date in the calendar is correct
    first_day_of_next_month = (datetime.datetime.now().replace(day=1) + datetime.timedelta(days=32)).replace(day=1)
    assert next_month_date == first_day_of_next_month.strftime(
        "%Y %b %d"), 'Time interval is not correct, should be the 1st of next month'

    # Verifying that the events count has been updated
    next_month_events_count = driver.find_element \
        (By.XPATH, '//div[@class="tc-economic-calendar-view-container-title tc-normal-text"]').text
    assert next_month_events_count != next_week_events_count, 'Number of events has not been updated'

    # Getting the first three rows for next month events
    next_month_events = driver.find_elements(By.TAG_NAME, 'tc-economic-calendar-row')
    first_next_month_event = next_month_events[0].text
    second_next_month_event = next_month_events[1].text
    third_next_month_event = next_month_events[2].text

    # Verifying the event list has been updated when changing to Next Month
    assert ((first_next_month_event != first_next_week_event) or (second_next_month_event != second_next_week_event)
            or (third_next_month_event != third_next_week_event)), 'Event list for Next Month has not been updated'
