from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters

TOKEN = "8368686437:AAH09Qb-EmM7GuM4mH_qy1x-jm4LtnyjXWk"
BOT_USERNAME = "dotaskandearn_bot"
FORCE_JOIN_CHANNEL = "@onlineearning2026toinfinite"
YOUTUBE_LINK = "https://youtube.com/@clipstorm2026?si=7VLhiEbtKrix6g16"
BONUS_CHANNEL = "https://t.me/SHOORVEERALLEPISODE1TOEND"
QR_IMAGE_URL = "https://i.imgur.com/GnNd0KD.jpg"  # Upload your QR to imgur and paste link here

# --- In-Memory Storage ---
users = {}
claimed_bonus = set()

# --- Main Menu ---
def main_menu():
    keyboard = [
        [InlineKeyboardButton("🎁 Bonus Tasks", callback_data="earn")],
        [InlineKeyboardButton("👥 Referral", callback_data="refer")],
        [InlineKeyboardButton("💰 Balance", callback_data="balance")],
        [InlineKeyboardButton("🎉 Daily Bonus", callback_data="daily_bonus")],
        [InlineKeyboardButton("🏧 Withdraw", callback_data="withdraw")],
        [InlineKeyboardButton("💸 Add Cash", callback_data="add_cash")],
        [InlineKeyboardButton("📖 How to Use", callback_data="how_to_use")],
    ]
    return InlineKeyboardMarkup(keyboard)

# --- Start Command ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    users.setdefault(user.id, {"balance": 0})

    chat_member = await context.bot.get_chat_member(chat_id=FORCE_JOIN_CHANNEL, user_id=user.id)
    if chat_member.status in ["member", "administrator", "creator"]:
        await update.message.reply_text(
            f"🎉 Welcome {user.first_name}!\n\n✅ You can now use the bot.",
            reply_markup=main_menu()
        )
    else:
        keyboard = [
            [InlineKeyboardButton("🔗 Join Telegram Channel", url="https://t.me/onlineearning2026toinfinite")],
            [InlineKeyboardButton("▶️ Subscribe YouTube", url="https://youtube.com/@clipstorm2026?si=BEJRFSxR8rkAZvLK")],
            [InlineKeyboardButton("✅ I Have Done", callback_data="check_joined")]
        ]
        await update.message.reply_text(
            "🚫 Please join and subscribe to use the bot.",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

# --- Check Join Callback ---
async def check_joined_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    chat_member = await context.bot.get_chat_member(chat_id=FORCE_JOIN_CHANNEL, user_id=user_id)
    if chat_member.status in ["member", "administrator", "creator"]:
        await query.edit_message_text("✅ You're verified!", reply_markup=main_menu())
    else:
        await query.answer("❌ Not joined yet!", show_alert=True)

# --- Bonus Task ---
async def earn_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.edit_message_text(
        text=(
            "🎁 *Earn More Bonus Tasks*\n\n"
            "1️⃣ Join [Bonus Channel](" + BONUS_CHANNEL + ")\n"
            "2️⃣ Subscribe [YouTube](" + YOUTUBE_LINK + ")\n\n"
            "📢 _More tasks coming soon..._"
        ),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("📲 Join Bonus Channel", https://t.me/SHOORVEERALLEPISODE1TOEND=)],
            [InlineKeyboardButton("▶️ Subscribe YouTube", url="https://youtube.com/@clipstorm2026?si=BEJRFSxR8rkAZvLK")], 
            
        parse_mode="Markdown"
    )

# --- Referral ---
async def refer_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.callback_query.from_user
    ref_link = f"https://t.me/{dotaskandearn_bot}?start={user.id}"
    await update.callback_query.edit_message_text(
        f"🔗 Your referral link:\n{ref_link}\n\n👥 Earn ₹10 per referral!"
    )

# --- Balance ---
async def balance_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.callback_query.from_user.id
    bal = users.get(user_id, {}).get("balance", 0)
    await update.callback_query.edit_message_text(f"💰 Your current balance is ₹{bal}")

# --- Daily Bonus ---
async def daily_bonus_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.callback_query.from_user.id
    if user_id in claimed_bonus:
        await update.callback_query.answer("🎁 You already claimed today’s bonus!", show_alert=True)
    else:
        users[user_id]["balance"] += 7
        claimed_bonus.add(user_id)
        await update.callback_query.edit_message_text("✅ ₹7 Daily Bonus added to your balance!")

# --- Withdraw ---
async def withdraw_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.edit_message_text(
        "🏧 To withdraw, send your UPI ID and amount to admin:\n\n📩 @id_buyer_and_seller_ff"
    )

# --- Add Cash ---
async def add_cash_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.message.reply_photo(
        photo="https://tg-cloud-file-small-file.ajz.workers.dev/photos/file_371048.jpg?file_name=aqad0ccxg6dxufr9.jpg&expire=1753903047&signature=fZvBby1ZF782y0LHSef9Iv0dSiHMkF42QaoQiNDyCAc%3D"
        caption=(
            "💸 *Add Cash Instructions:*\n\n"
            "1️⃣ Scan above QR (J&K Bank)\n"
            "2️⃣ Pay desired amount\n"
            "3️⃣ Send UPI REF NO. like `514560109000` in chat\n\n"
            "_Balance will be updated after verification._"
        ),
        parse_mode="Markdown"
    )
    return

# --- UPI REF NO. Handler ---
async def handle_upi_reference(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.strip()

    if text.isdigit() and len(text) >= 10:
        users[user_id]["balance"] += 50  # Manual default top-up
        await update.message.reply_text("✅ ₹50 has been added to your account after UPI verification.")
    else:
        await update.message.reply_text("❌ Invalid UPI REF number. Please try again.")

# --- How to Use ---
async def how_to_use_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.edit_message_text(
        "📖 *How to Use This Bot:*\n\n"
        "1️⃣ Join required Telegram and YouTube\n"
        "2️⃣ Use referral link to earn ₹10 per friend\n"
        "3️⃣ Complete bonus tasks for more cash\n"
        "4️⃣ Claim ₹7 Daily Bonus\n"
        "5️⃣ Add cash by UPI and withdraw when ready\n\n"
        "👍 Simple and rewarding!",
        parse_mode="Markdown"
    )

# --- Main ---
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(check_joined_callback, pattern="check_joined"))
    app.add_handler(CallbackQueryHandler(earn_callback, pattern="earn"))
    app.add_handler(CallbackQueryHandler(refer_callback, pattern="refer"))
    app.add_handler(CallbackQueryHandler(balance_callback, pattern="balance"))
    app.add_handler(CallbackQueryHandler(daily_bonus_callback, pattern="daily_bonus"))
    app.add_handler(CallbackQueryHandler(withdraw_callback, pattern="withdraw"))
    app.add_handler(CallbackQueryHandler(add_cash_callback, pattern="add_cash"))
    app.add_handler(CallbackQueryHandler(how_to_use_callback, pattern="how_to_use"))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_upi_reference))

    print("✅ Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
