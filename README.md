# Stars Sniper Bot 

Telegram бот для автоматизации покупки Telegram Gifts.

### Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/vmilfe/stars_sniper.git
cd stars_sniper
```

2. Установите Redis:
```bash
# Для Ubuntu/Debian
sudo apt-get update
sudo apt-get install redis-server

# Для MacOS через Homebrew
brew install redis

# Для Windows
# Скачайте Redis с https://github.com/microsoftarchive/redis/releases
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Копируйте файл `config.yaml.example` в `config.yaml` 

5. Настройте конфигурацию в файле `config.yaml`

### Запуск

1. Запустите Redis сервер в фоновом режиме:
```bash
# Запуск Redis в фоновом режиме
redis-server --dir src/redis/storage --daemonize yes

# Проверить что Redis запущен
redis-cli ping
```

2. В новом терминале запустите бота:
```bash
python3 main.py
```

### Dev mode

1. Установить nodemon:
```js
npm install -g nodemon
```

2. Запустите:
```bash
nodemon --ext py main.py
```