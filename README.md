# enjoy-your-mood

/shop_project/
├── backend/
│ backend/
├── main.py # Точка входа, подключение роутеров
├── api/ # Эндпоинты (роутеры)
│ ├── products.py # Товары
│ ├── orders.py # Заказы
│ ├── users.py # Пользователи
│ ├── categories.py # Категории
│ └── init.py # Импорт роутеров
├── models/ # Pydantic-модели данных
│ ├── product.py
│ ├── order.py
│ └── user.py
├── services/ # Бизнес-логика (сервисы)
│ ├── product_service.py
│ ├── order_service.py
│ └── user_service.py
├── bots/
│ ├── telegram_bot.py
│ └── whatsapp_bot.py
├── frontend/
│ └── ...
├── .env
├── requirements.txt
└── README.md

---

## Как запускать

1. Установи зависимости:

```bash
    pip install fastapi uvicorn

```

2. Установи вритуалку:

```bash
    python -m venv venv

    .\venv\Scripts\Activate
```

3. Распакуй пакеты requirements.txt

```bash
    pip install -r requirements.txt
```

4. Создайте .env файл и добавьте ключи:

```
    AIRTABLE_API_KEY=your_api_key
    AIRTABLE_BASE_ID=your_base_id
    AIRTABLE_PRODUCTS_TABLE=Products
```

5. Запустите сервер:

```
uvicorn main:app --reload
```

6. Тесты запускаются, например

```
pytest -s tests/test_airtable.py
```
