import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(autouse=True)
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    # Переходим на страницу авторизации
    driver.get('https://petfriends.skillfactory.ru/login')
    yield driver
    driver.quit()


def test_show_all_pets(driver):
    # Активируем неявные ожидания
    driver.implicitly_wait(10)
    # Вводим email
    driver.find_element(By.ID, 'email').send_keys('vasya@mail.com')
    # Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys('12345')
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"
    # Проверка карточек
    images = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-img-top')
    names = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-title')
    descriptions = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-text')
    for i in range(len(names)):
       assert images[i].get_attribute('src') != ''
       assert names[i].text != ''
       assert descriptions[i].text != ''
       assert ', ' in descriptions[i]
       parts = descriptions[i].text.split(", ")
       assert len(parts[0]) > 0
       assert len(parts[1]) > 0


def test_30_3_1(driver):
    # Вводим email
    driver.find_element(By.ID, 'email').send_keys('alkdsjfladjkf@mail.ru')
    # Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys('123')
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

    # Переходим на страницу своих питомцев
    driver.find_element(By.CLASS_NAME, 'nav-link').click()

    # Создаём объект WebDriberWait для явного ожидания
    wait = WebDriverWait(driver, 10)

    # Ищем в теле таблицы все фото питомцев и ожидаем увидеть их на странице
    image_my_pets = driver.find_elements(By.CSS_SELECTOR, 'img[style="max-width: 100px; max-height: 100px;"]')
    for i in range(len(image_my_pets)):
        if image_my_pets[i].get_attribute('src') != '':
            assert wait.until(EC.visibility_of(image_my_pets[i]))

    # Ищем в теле таблицы все имена питомцев и ожидаем увидеть их на странице:
    name_my_pets = driver.find_elements(By.XPATH, '//tbody/tr/td[1]')
    for i in range(len(name_my_pets)):
        assert wait.until(EC.visibility_of(name_my_pets[i]))

    # Ищем в теле таблицы все породы питомцев и ожидаем увидеть их на странице:
    type_my_pets = driver.find_elements(By.XPATH, '//tbody/tr/td[2]')
    for i in range(len(type_my_pets)):
        assert wait.until(EC.visibility_of(type_my_pets[i]))

    # Ищем в теле таблицы все данные возраста питомцев и ожидаем увидеть их на странице:
    age_my_pets = driver.find_elements(By.XPATH, '//tbody/tr/td[3]')
    for i in range(len(age_my_pets)):
        assert wait.until(EC.visibility_of(age_my_pets[i]))

    # Проверяем, присутствуют ли все питомцы
    pets_number = int(driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]').text.split('\n')[1].split()[1])
    pets_elements = driver.find_elements(By.TAG_NAME, "tr")[1:]
    assert pets_number == len(pets_elements)

    # Проверяем что хотя бы у половины питомцев есть фото
    pets_images = driver.find_elements(By.CSS_SELECTOR, 'img[style="max-width: 100px; max-height: 100px;"]')
    pets_with_photo = pets_number
    for pet_image in pets_images:
        if pet_image.get_attribute('src') == '':
            pets_with_photo -= 1
    assert pets_with_photo >= (pets_number/2)

    # Проверяем что у всех питомцев есть имя, порода и возраст
    pets_names = [element.text for element in driver.find_elements(By.XPATH, '//tbody/tr/td[1]')]
    for pet_name in pets_names:
        assert pet_name != ''

    pets_types = [element.text for element in driver.find_elements(By.XPATH, '//tbody/tr/td[2]')]
    for pet_type in pets_types:
        assert pet_type != ''

    pets_ages = [element.text for element in driver.find_elements(By.XPATH, '//tbody/tr/td[3]')]
    for pet_age in pets_ages:
        assert pet_age != ''

    # Проверяем что у всех питомцев разные имена
    assert len(pets_names) == len(set(pets_names))

    # Проверяем что в списке нет повторяющихся питомцев
    pets_data = list(zip(pets_names, pets_types, pets_ages))
    assert len(pets_data) == len(set(pets_data))
