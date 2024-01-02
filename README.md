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
.env (Database config and cookie config)
.gitignore (Git ignore file)
app.py (Flask web app with all endpoints)
README.md (Project documentation)
schema.sql (Mysql tables schema)
```
------------------
## Popis aplikace
- **URL:** [http://138.68.93.217:5000/](http://138.68.93.217:5000/) 
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

------------------