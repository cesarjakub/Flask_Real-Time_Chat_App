# Real Time Chat Aplikace
- **Developed by:** Jakub César

------------------
## File Structure

```
static/
  -css/
    -chat.css
    -mainpage.css
  -img/
    -icon.svg
  -script/
    -chat.js
templates/
  -404.html
  -base.html
  -chat.html
  -homepage.html
  -loginform.html
  -registerform.html
.env (Database config and session_secret config)
.gitignore (Git ignore file)
app.py (Flask web app with all endpoints)
README.md (Project documentation)
schema.sql (Mysql tables schema)
```
------------------
## Popis aplikace
- **URL:** [http://138.68.93.217:5000/](http://138.68.93.217:5000/) 

- Jednoduchá chatovací aplikace postavená pomocí technologie Flask pro backend a Socket.IO pro komunikaci v reálném čase. Umožňuje uživatelům připojit se k roomkam chatu, posílat a sledovat zprávy v reálném čase.

## Funkce
- Registrace a následné přihlášení do aplikace (sessions)
- Komunikace v reálném čase pomocí Socket.IO
- Připojování a opouštění skupin chatu
- Odesílání a přijímání zpráv v rámci skupin chatu
- Zobrazení chybných hlášení pokud nastanou
- Ukládání do databáze (Uživatele i jeho zprávy)
- Hashovaní hesla

------------------
## REST API endpointy

#### 1. Get All Chat Posts
Vrátí všechny zprávy z chatu.

- **Endpoint:** `/api/chat/`
- **Method:** `GET`
- **Parameters:** None
- **Authorization:** Potřeba (Uživatel musí být přihlášen)
- **Response:**
  - Success (200 OK): List zpráv z aplikace
  - Not Found (404): Nenalezeno nic

#### 2. Get Chat Posts by User
Vrátí všechny zprávy z chatu od specifického uživatele.

- **Endpoint:** `/api/chat/<name>`
- **Method:** `GET`
- **Parameters:**
  - `name` (string): Jmeno uživatele
- **Authorization:** Potřeba (Uživatel musí být přihlášen)
- **Response:**
  - Success (200 OK): List všech zpráv z chatu od specifického uživatele
  - Not Found (404): Nenalezeno nic

#### 3. Get Chat Posts by Chat Room
Vrátí všechny zprávy z chatu ze specifické roomky chatu.

- **Endpoint:** `/api/chat/<int:id>`
- **Method:** `GET`
- **Parameters:**
  - `id` (integer): Chat Room ID
- **Authorization:** Potřeba (Uživatel musí být přihlášen)
- **Response:**
  - Success (200 OK): List všech zpráv z chatu ze specifické roomky chatu
  - Not Found (404): Nenalezeno nic

#### 4. Get Chat Posts by Word
Vrátí všechny zprávy z chatu podle specifickho slova v chatu (case insensitive).

- **Endpoint:** `/api/chat/word/<word>`
- **Method:** `GET`
- **Parameters:**
  - `word` (string): Hledané slovo ve zprávě
- **Authorization:** Potřeba (Uživatel musí být přihlášen)
- **Response:**
  - Success (200 OK): List všech zpráv z chatu podle specifickho slova v chatu
  - Not Found (404): Nenalezeno nic

------------------
## Web socket

## Serverová část (Python s pomocí Flask a Socket.IO)
### Připojení do roomky chatu
- Událost `join` je spuštěna, když se uživatel připojí ke skupině chatu. Serverová funkce `handle_join` přidá uživatele do určené skupiny, vysílá systémovou zprávu oznamující, že uživatel vstoupil, a načte existující zprávy pro danou místnost.
```python
@socketio.on('join')
def handle_join(data):
    ...
```

### Opouštění skupiny chatu
- Událost `leave` je spuštěna, když uživatel opustí skupinu chatu. Serverová funkce `handle_leave` odejme uživatele ze skupiny a vysílá systémovou zprávu oznamující, že uživatel odešel.

```python
@socketio.on('leave')
def handle_leave(data):
    ...
```

### Odesílání a přijímání zpráv
- Událost `message` je spuštěna, když uživatel odešle zprávu. Serverová funkce `handle_message` vysílá zprávu všem uživatelům ve skupině a ukládá ji do databáze.

```python
@socketio.on('message')
def handle_message(data):
    ...
```

### Načítání zpráv pro místnost
- Událost `load_messages` je spuštěna pro načtení existujících zpráv pro místnost. Serverová funkce `get_messages_for_room` načte zprávy z databáze.

```python
def get_messages_for_room(room):
    ...
```

## Klientská část (JavaScript s Socket.IO)
## Připojení ke skupině
- Funkce `joinRoom` je volána, když uživatel klikne na tlačítko "Připojit se ke skupině". Odesílá událost `join` na server.

```javascript
function joinRoom() {
    ...
}
```

## Opouštění skupiny
- Funkce `leaveRoom` je volána, když uživatel klikne na tlačítko "Opustit skupinu". Odesílá událost `leave` na server.

```javascript
function leaveRoom() {
    ...
}
```

## Odesílání zprávy
- Funkce `sendMessage` je volána, když uživatel odešle zprávu. Odesílá událost `message` na server.

```javascript
function sendMessage() {
    ...
}
```

## Přijímání zpráv
- Klient naslouchá událostem `mm` (systémové zprávy) a `load_messages` ze serveru. Funkce `updateMessages` aktualizuje oblast chatu přijatými zprávami.

```javascript
socket.on('mm', function(data) {
    ...
});

socket.on('load_messages', function(data) {
    ...
});
```

------------------