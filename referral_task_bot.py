from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Bot Configuration
TOKEN = "8368686437:AAH09Qb-EmM7GuM4mH_qy1x-jm4LtnyjXWk"
BOT_USERNAME = "dotaskandearn_bot"
FORCE_JOIN_CHANNEL = "@onlineearning2026toinfinite"
YOUTUBE_LINK = "https://youtube.com/@clipstorm2026?si=7VLhiEbtKrix6g16"
BONUS_CHANNEL = "https://t.me/SHOORVEERALLEPISODE1TOEND"

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_member = await context.bot.get_chat_member(chat_id=FORCE_JOIN_CHANNEL, user_id=user.id)

    if chat_member.status in ["member", "administrator", "creator"]:
        await update.message.reply_text(
            f"🎉 Welcome {user.first_name}!\n\n✅ You can now use the bot.",
            reply_markup=main_menu()
        )
    else:
        keyboard = [
            [InlineKeyboardButton("🔗 Join Telegram Channel", url="https://t.me/onlineearning2026toinfinite")],
            [InlineKeyboardButton("▶️ Subscribe YouTube", url=YOUTUBE_LINK)],
            [InlineKeyboardButton("✅ I Have Done", callback_data="check_joined")]
        ]
        await update.message.reply_text(
            "🚫 To use this bot, please:\n\n1️⃣ Join Telegram channel\n2️⃣ Subscribe YouTube channel",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

# Main menu
def main_menu():
    keyboard = [
        [InlineKeyboardButton("🎁 Earn Bonus Tasks", callback_data="earn")],
        [InlineKeyboardButton("👥 Referral", callback_data="refer")],
    ]
    return InlineKeyboardMarkup(keyboard)

# Check if user joined
async def check_joined_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    chat_member = await context.bot.get_chat_member(chat_id=FORCE_JOIN_CHANNEL, user_id=user_id)

    if chat_member.status in ["member", "administrator", "creator"]:
        await query.edit_message_text(
            "✅ Thank you! You've joined the required channels.",
            reply_markup=main_menu()
        )
    else:
        await query.answer("❌ You're still not a member!", show_alert=True)

# Bonus task
async def earn_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()

    keyboard = [
        [InlineKeyboardButton("📲 Join Bonus Channel", url=BONUS_CHANNEL)],
        [InlineKeyboardButton("▶️ Subscribe YouTube", url=YOUTUBE_LINK)],
    ]

    await update.callback_query.edit_message_text(
        text=(
            "🎁 *Earn More Bonus Tasks*\n\n"
            "1️⃣ Join: [SHOORVEERALLEPISODE1TOEND](" + BONUS_CHANNEL + ")\n"
            "2️⃣ Subscribe: [@clipstorm2026](" + YOUTUBE_LINK + ")\n\n"
            "📢 _More tasks coming soon..._"
        ),
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

# Referral task
async def refer_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.callback_query.from_user
    referral_link = f"https://t.me/{BOT_USERNAME}?start={user.id}"
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        f"🔗 Your referral link:\n{referral_link}\n\n👥 Earn ₹10 per referral!"
    )

# Main runner
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(check_joined_callback, pattern="check_joined"))
    app.add_handler(CallbackQueryHandler(earn_callback, pattern="earn"))
    app.add_handler(CallbackQueryHandler(refer_callback, pattern="refer"))
    print("✅ Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
