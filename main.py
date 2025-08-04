import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Token e ID do grupo
TOKEN = "8144201595:AAFg4j7TM1ChTzopBbrJyXG-8xv3APDgOcw"
GROUP_ID = -4890083404

# Inicialização de log
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

win_count = 0
loss_count = 0

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Bot de sinais da Blaze iniciado com sucesso!")

# /status
async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    total = win_count + loss_count
    taxa = (win_count / total) * 100 if total > 0 else 0
    msg = (
        f"📊 Estatísticas atuais:\n"
        f"✅ WINs: {win_count}\n"
        f"❌ LOSSes: {loss_count}\n"
        f"🎯 Assertividade: {taxa:.2f}%"
    )
    await update.message.reply_text(msg)

# /green
async def green(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global win_count
    win_count += 1
    await update.message.reply_text("✅ WIN registrado com sucesso!")

# /red
async def red(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global loss_count
    loss_count += 1
    await update.message.reply_text("❌ LOSS registrado com sucesso!")

# /sinal
async def sinal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = (
        "🚨 NOVO SINAL DETECTADO 🚨\n"
        "🎯 Apostar NO BRANCO nas próximas jogadas!\n"
        "💡 Estratégia ativa com alta assertividade.\n"
        "✅ Entre com cautela.\n\n"
        "#Blaze #Sinal #Bot"
    )
    await context.bot.send_message(chat_id=GROUP_ID, text=texto)
    await update.message.reply_text("✅ Sinal enviado ao grupo com sucesso!")

# Iniciar bot
def iniciar_comandos():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("green", green))
    app.add_handler(CommandHandler("red", red))
    app.add_handler(CommandHandler("sinal", sinal))
    app.run_polling()

# Rodar
if __name__ == '__main__':
    iniciar_comandos()
