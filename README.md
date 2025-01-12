# Stars Sniper Bot 

Telegram бот для автоматизации покупки Telegram Gifts.

### Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/vmilfe/stars_sniper.git
cd stars_sniper
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Копируйте файл `config.yaml.example` в `config.yaml` 

4. Настройте конфигурацию в файле `config.yaml`

### Запуск

1. Запустите Redis сервер:
```bash
redis-server --dir src/redis/storage
```

2. В новом терминале запустите бота:
```bash
python3 main.py
```
