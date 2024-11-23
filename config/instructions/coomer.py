from bs4 import BeautifulSoup
import requests
import random
import time

# Создаём сессию для повторного использования соединений
session = requests.Session()

# Заголовки User-Agent для имитации запросов от браузера
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.59 Safari/537.36',
]

# Функция для отправки запросов с задержкой и случайным User-Agent
def make_request_with_delay(url):
    headers = {
        'User-Agent': random.choice(user_agents)
    }
    # Случайная задержка между 1 и 3 секундами
    time.sleep(random.uniform(0.2, 3))
    
    response = session.get(url, headers=headers)
    
    if response.status_code == 429:  # Если получаем ошибку 429, делаем паузу
        print("Received 429, waiting for 5 seconds before retrying...")
        time.sleep(5)  # Пауза на 5 секунд
        response = session.get(url, headers=headers)
    
    response.raise_for_status()  # Проверка успешности запроса
    return response

def parse_post(url, selectors):
    """Парсит медиа (картинки и видео) с поста."""
    try:
        response = make_request_with_delay(url)
        response.raise_for_status()  # Проверить успешность запроса
        soup = BeautifulSoup(response.text, 'html.parser')
        
        print(f"Parsing post: {url}")

        folder_name_selector = selectors['folder_title']

        # Извлекаем изображения
        images = [tag['href'] for tag in soup.select(selectors['post']['images'])]
        # Извлекаем видео
        videos = [tag['href'] for tag in soup.select(selectors['post']['videos'])]

        # Извлекаем название папки
        folder_name = soup.select_one(folder_name_selector).text.strip()
        
        return {
            "images": images,
            "videos": videos,
            "folder_name": folder_name
        }
    except Exception as e:
        print(f"Error parsing coomer post: {e}")
        return {"images": [], "videos": [], "folder_name": None}


def parse_folder(url, domain, selectors):
    """Парсит папку, переходя по ссылкам на посты и собирая медиа."""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Извлекаем ссылки на посты
    post_links = [domain+tag['href'] for tag in soup.select(selectors['folder']['post_links'])]
    print(f"Found {len(post_links)} posts in folder.")

    # Для каждого поста вызываем парсинг
    all_media = []
    for post_url in post_links:
        media = parse_post(post_url, selectors)
        all_media.append(media)
    
    # Проверка на наличие следующей страницы
    next_page_tag = soup.select_one(selectors['folder']['next_page'])
    if next_page_tag:
        next_page_url = domain+next_page_tag['href']
        print(f"Found next page: {next_page_url}")
        # Рекурсивно парсим следующую страницу
        all_media += parse_folder(next_page_url, domain, selectors)

    return all_media