from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import db

TOKEN = "8134058728:AAHig6AdP-HoTdwATlolIgxumbi1h2qpeUg"

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
