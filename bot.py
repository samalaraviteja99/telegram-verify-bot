
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
from database import *

BOT_TOKEN = "7079574116:AAF3Yf0xnPCPGpv2GkuIS0VdZ9PZXJMjrHo"
ADMIN_ID = 1257082796
MIN_WITHDRAW = 1

CHANNEL_USERNAME = "@campignloots"
CHANNEL_ID = -1002807227544
VERIFY_URL = "http://YOUR_SERVER_IP:5000/verify"

user_state = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    add_user(user.id)

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("📢 Join Channel", url=f"https://t.me/{CHANNEL_USERNAME.replace('@','')}")],
        [InlineKeyboardButton("🔐 Verify & Earn ₹1", callback_data="verify")],
        [InlineKeyboardButton("💼 Wallet", callback_data="wallet")]
    ])
    await update.message.reply_text("Welcome 👋", reply_markup=keyboard)

async def verify_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id

    if is_verified(user_id):
        await query.message.reply_text("⚠️ Already verified")
        return

    try:
        member = await context.bot.get_chat_member(CHANNEL_ID, user_id)
        if member.status not in ["member", "administrator", "creator"]:
            await query.message.reply_text("❌ Join channel first")
            return

        link = f"{VERIFY_URL}?uid={user_id}"
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🌐 Complete Verification", url=link)]
        ])
        await query.message.reply_text("Channel verified ✅\nComplete IP verification 👇", reply_markup=keyboard)

    except:
        await query.message.reply_text("❌ Error checking channel")

async def wallet_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user

    if not is_verified(user.id):
        await query.message.reply_text("❌ Please verify first")
        return

    balance = get_wallet(user.id)
    await query.message.reply_text(f"💼 Wallet Balance: ₹{balance}")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(verify_click, pattern="verify"))
app.add_handler(CallbackQueryHandler(wallet_click, pattern="wallet"))
app.run_polling()
