# Crypto Bot Demo (solo simulazione)

Questo progetto legge dati pubblici BTC/EUR da Binance tramite CCXT e calcola EMA20, EMA50 e RSI14 su candele da 15 minuti.

**Non invia ordini, non accede a Deblock e non usa denaro reale.** Il segnale è sperimentale e non è una raccomandazione finanziaria.

## Avvio manuale su GitHub

1. Carica i file mantenendo esattamente la struttura delle cartelle.
2. Apri la scheda **Actions** del repository.
3. Se richiesto, abilita GitHub Actions.
4. Apri **Crypto Bot Demo** e premi **Run workflow** per una prova manuale.

Il workflow è programmato per tentare un'esecuzione ogni 15 minuti. GitHub può ritardare o saltare esecuzioni programmate; non è un servizio di trading continuo né adatto a eseguire ordini in tempo reale.

## Notifiche Telegram (facoltative)

Nelle impostazioni del repository vai in **Settings → Secrets and variables → Actions → New repository secret** e crea:
- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`

Inserisci i valori direttamente nei campi segreti di GitHub. **Non** inserirli nel codice, nei file, negli screenshot o nelle chat.

Se i segreti non sono configurati, il bot stampa comunque il risultato nei log di Actions.

## File

- `crypto_bot_demo.py`: analisi demo di mercato
- `requirements.txt`: dipendenze Python
- `.github/workflows/crypto-bot.yml`: esecuzione manuale e programmata
