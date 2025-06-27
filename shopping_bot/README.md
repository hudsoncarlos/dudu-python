Vamos criar um **bot de lista de compras** que pode ser usado tanto no **Telegram** quanto via **web (com interface básica)**. Aqui está o plano do projeto e a primeira versão do código:

---

### ✅ Funcionalidades do Bot

* 📋 Ver a lista de compras atual
* ✅ Marcar itens como comprados
* ➕ Adicionar novos itens
* ❌ Remover itens
* 🌐 Funcionar via Telegram e também com uma interface web simples

---

### 🔧 Stack sugerida

* **Backend**: Python (com Flask para Web API)
* **Banco de dados**: SQLite (simples e local)
* **Bot Telegram**: `python-telegram-bot`
* **Web**: HTML + JavaScript com Bootstrap (simples e funcional)

---

### 📁 Estrutura do projeto

```
shopping_bot/
├── bot.py              # Bot Telegram
├── webapp.py           # Interface web via Flask
├── db.py               # Funções do banco de dados (SQLite)
├── templates/
│   └── index.html      # Página da lista de compras
└── shopping.db         # Banco de dados SQLite
```

---

### 🎯 Começando: banco de dados `db.py`

```python
import sqlite3

DB_NAME = "shopping.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS shopping_list (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item TEXT NOT NULL,
            done BOOLEAN DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

def add_item(item):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("INSERT INTO shopping_list (item) VALUES (?)", (item,))
        conn.commit()

def get_items():
    with sqlite3.connect(DB_NAME) as conn:
        return conn.execute("SELECT id, item, done FROM shopping_list").fetchall()

def mark_done(item_id):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("UPDATE shopping_list SET done = 1 WHERE id = ?", (item_id,))
        conn.commit()

def delete_item(item_id):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("DELETE FROM shopping_list WHERE id = ?", (item_id,))
        conn.commit()
```

---

### 🤖 Bot Telegram: `bot.py`

```python
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import db

TOKEN = "SEU_TOKEN_DO_BOT"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🛒 Bem-vindo à lista de compras da família!\nUse /lista para ver os itens.")

async def lista(update: Update, context: ContextTypes.DEFAULT_TYPE):
    items = db.get_items()
    response = "\n".join([f"{'✅' if d else '⬜️'} {i}. {t}" for i, t, d in items])
    await update.message.reply_text(response or "Lista vazia.")

async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    item = " ".join(context.args)
    if item:
        db.add_item(item)
        await update.message.reply_text(f"Adicionado: {item}")
    else:
        await update.message.reply_text("Use: /add Detergente Ype")

async def done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        item_id = int(context.args[0])
        db.mark_done(item_id)
        await update.message.reply_text(f"Item {item_id} marcado como feito ✅")
    except:
        await update.message.reply_text("Use: /done 2")

def main():
    db.init_db()
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("lista", lista))
    app.add_handler(CommandHandler("add", add))
    app.add_handler(CommandHandler("done", done))

    print("Bot rodando...")
    app.run_polling()

if __name__ == "__main__":
    main()
```

---

### 🌐 Web interface: `webapp.py`

```python
from flask import Flask, render_template, request, redirect
import db

app = Flask(__name__)
db.init_db()

@app.route("/")
def index():
    items = db.get_items()
    return render_template("index.html", items=items)

@app.route("/add", methods=["POST"])
def add():
    db.add_item(request.form["item"])
    return redirect("/")

@app.route("/done/<int:item_id>")
def done(item_id):
    db.mark_done(item_id)
    return redirect("/")

@app.route("/delete/<int:item_id>")
def delete(item_id):
    db.delete_item(item_id)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
```

---

### 🧾 HTML: `templates/index.html`

```html
<!DOCTYPE html>
<html>
<head>
  <title>Lista de Compras</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="p-4">
  <h2>🛒 Lista de Compras da Família</h2>
  <form action="/add" method="post" class="mb-3 d-flex gap-2">
    <input type="text" name="item" class="form-control" placeholder="Novo item..." required>
    <button class="btn btn-primary">Adicionar</button>
  </form>
  <ul class="list-group">
    {% for id, item, done in items %}
    <li class="list-group-item d-flex justify-content-between align-items-center {% if done %}list-group-item-success{% endif %}">
      {{ item }}
      <span>
        {% if not done %}
          <a href="/done/{{ id }}" class="btn btn-sm btn-success">Feito</a>
        {% endif %}
        <a href="/delete/{{ id }}" class="btn btn-sm btn-danger">X</a>
      </span>
    </li>
    {% endfor %}
  </ul>
</body>
</html>
```

---

### 🚀 Como rodar tudo:

1. Crie um ambiente Python: `python -m venv venv && source venv/bin/activate`
2. Instale as dependências:

   ```
   pip install flask python-telegram-bot
   ```
3. Rode o webapp:

   ```
   python webapp.py
   ```
4. Rode o bot Telegram em outro terminal:

   ```
   python bot.py
   ```

