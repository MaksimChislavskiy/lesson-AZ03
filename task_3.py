import requests
from bs4 import BeautifulSoup
import csv
import matplotlib.pyplot as plt
import time

url = 'https://www.divan.ru/category/divany-i-kresla'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
}

prices = []


def parse_page(page_url):
    try:
        response = requests.get(page_url, headers=headers, allow_redirects=True, timeout=10)

        # Если URL изменился (редирект), используем новый URL
        if response.history and response.url != page_url:
            print(f"Перенаправление с {page_url} на {response.url}")

        if response.status_code != 200:
            print(f'Ошибка при загрузке страницы: {page_url}, статус: {response.status_code}')
            return None

        soup = BeautifulSoup(response.text, 'html.parser')
        products = soup.find_all('div', class_='q5Uds')  # Карточки товаров

        page_prices = []
        for product in products:
            price_tag = product.find('span', class_='ui-LD-ZU')  # Тег с ценой
            if price_tag:
                price_text = price_tag.get_text(strip=True)
                price_number = ''.join(filter(str.isdigit, price_text))
                if price_number:
                    price = int(price_number)
                    page_prices.append(price)

        return page_prices

    except Exception as e:
        print(f'Ошибка при парсинге страницы: {e}')
        return None


# Парсим страницы 1–5
for page_num in range(1, 6):
    page_url = f'{url}?page={page_num}' if page_num > 1 else url
    print(f"Парсинг страницы: {page_url}")

    page_prices = parse_page(page_url)
    if page_prices:
        prices.extend(page_prices)
    else:
        print(f"Не удалось получить данные со страницы {page_num}")

    time.sleep(2)  # Задержка между запросами

if prices:
    print(f'Общее количество цен: {len(prices)}')
    print(f'Минимальная цена: {min(prices)} руб.')
    print(f'Максимальная цена: {max(prices)} руб.')
    print(f'Средняя цена: {sum(prices) / len(prices):.2f} руб.')

    # Запись в CSV
    with open('divans_prices.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Price'])
        for price in prices:
            writer.writerow([price])

    # Гистограмма
    plt.figure(figsize=(10, 6))
    plt.hist(prices, bins=15, color='blue', edgecolor='black', alpha=0.7)
    plt.title('Распределение цен на диваны (divan.ru)')
    plt.xlabel('Цена (руб.)')
    plt.ylabel('Количество')
    plt.grid(axis='y', linestyle='--')
    plt.show()
else:
    print('Цены не найдены. Проверьте URL или классы элементов.')