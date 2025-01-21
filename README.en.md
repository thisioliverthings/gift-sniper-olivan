<p align="center">
  <a href="README.md">Русский</a> |
  <a href="README.en.md">English</a> 
</p>

# Telegram Gifts Sniper Bot 

<div align="center">
  <img src="images/gift.png" alt="Bot gift" width="400">
  <img src="images/menu.png" alt="Bot gift" width="400">
</div>

## Features

- Automatic tracking and purchase of new Telegram Gifts
- Two operation modes:
  - Standard
  - VIP 
- Purchase mode settings:
  - Purchase with entire balance
  - Percentage limit of balance (in development)
  - Fixed stars limit (in development)
- Stars balance top-up
- VIP status purchase (also through stars)
- Common stars bank in the system
- VIP status management
- User balance modification

## Installation

1. Clone the repository:
```bash
git clone https://github.com/vmilfe/gift_sniper.git
cd stars_sniper
```

2. Install Redis:
```bash
# For Ubuntu/Debian
sudo apt-get update
sudo apt-get install redis-server

# For MacOS using Homebrew
brew install redis

# For Windows
# Download Redis from https://github.com/microsoftarchive/redis/releases
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Copy `config.yaml.example` to `config.yaml`

5. Configure settings in `config.yaml` file

### Launch

1. Start Redis server in a separate terminal:
```bash
# Start Redis in background mode
redis-server --dir src/redis/storage

# Check if Redis is running
redis-cli ping
```

2. In a new terminal, start the bot:
```bash
python3 main.py
```
> **Note**: Before launching, make sure you have copied and configured the `config.yaml` file

### Dev mode

1. Install nodemon:
```js
npm install -g nodemon
```

2. Run:
```bash
nodemon --ext py main.py
```

### You can also use Docker

1. Build and start containers:
```bash
docker-compose up -d --build
```

2. To view logs:
```bash
docker-compose logs -f bot
```

3. To stop:
```bash
docker-compose down
```

## Support

For all questions, contact the developer:
- Telegram: [@awixa](https://t.me/awixa)
