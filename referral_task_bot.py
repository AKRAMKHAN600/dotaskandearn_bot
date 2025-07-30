import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram.constants import ParseMode

# === Bot Configuration ===
TOKEN = "8368686437:AAH09Qb-EmM7GuM4mH_qy1x-jm4LtnyjXWk"
BOT_USERNAME = "dotaskandearn_bot"
MAIN_CHANNEL = "@onlineearning2026toinfinite"
YOUTUBE_CHANNEL_LINK = "https://youtube.com/@clipstorm2026?si=qMs_5pF4NDR9Rtod"
BONUS_YT_SHORT_LINK = "https://youtube.com/shorts/aySwZWcM3Mc?si=d7NS2iNLqSALwbGO"
BONUS_TELEGRAM_CHANNEL = "https://t.me/SHOORVEERALLEPISODE1TOEND"

MIN_WITHDRAW = 100
DAILY_BONUS = 5
REF_BONUS = 10

users = {}

logging.basicConfig(level=logging.INFO)

def get_ref_link(user_id):
    return f"https://t.me/{BOT_USERNAME}?start={user_id}"


# === /start ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id

    if user_id not in users:
        users[user_id] = {
            "balance": 0,
            "referrals": [],
            "daily_bonus": False,
            "verified": False
        }

        # Handle referral
        if context.args:
            ref_id = int(context.args[0])
            if ref_id != user_id and ref_id in users:
                if user_id not in users[ref_id]["referrals"]:
                    users[ref_id]["referrals"].append(user_id)
                    users[ref_id]["balance"] += REF_BONUS

    keyboard = [
        [InlineKeyboardButton("📢 Join Telegram Channel", url=f"https://t.me/{MAIN_CHANNEL[1:]}")],
        [InlineKeyboardButton("📺 Subscribe YouTube", url=YOUTUBE_CHANNEL_LINK)],
        [InlineKeyboardButton("✅ I’ve Done All Tasks", callback_data="check_join")]
    ]
    await update.message.reply_text(
        f"👋 Welcome {user.first_name}!\n\n🚨 *Before using the bot*, complete these 2 steps:\n\n"
        "1️⃣ Join our Telegram channel\n"
        "2️⃣ Subscribe to our YouTube channel\n\n"
        "Then click '✅ I’ve Done All Tasks' to continue.",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.MARKDOWN
    )


# === Task Verification ===
async def check_join_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user
    user_id = user.id

    await query.answer()
    member = await context.bot.get_chat_member(chat_id=MAIN_CHANNEL, user_id=user.id)

    if member.status in ["member", "administrator", "creator"]:
        users[user_id]["verified"] = True
        keyboard = [
            [InlineKeyboardButton("💸 Balance", callback_data="balance"),
             InlineKeyboardButton("🎁 Daily Bonus", callback_data="daily_bonus")],
            [InlineKeyboardButton("👥 Refer & Earn", callback_data="refer"),
             InlineKeyboardButton("💰 Withdraw", callback_data="withdraw")],
            [InlineKeyboardButton("📝 Tasks", callback_data="tasks")]
        ]
        await query.edit_message_text(
            "✅ *All tasks verified!*\n\nWelcome to the bot 🎉",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode=ParseMode.MARKDOWN
        )
    else:
        await query.edit_message_text(
            "❌ You haven’t joined the required Telegram channel.\n\nPlease join and try again."
        )


# === Main Menu Button Actions ===
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    data = query.data

    await query.answer()

    if not users.get(user_id, {}).get("verified"):
        await query.edit_message_text("🚫 Please complete all tasks first by using /start.")
        return

    if data == "balance":
        bal = users[user_id]["balance"]
        await query.edit_message_text(f"💰 Your current balance is: ₹{bal}")

    elif data == "refer":
        ref_link = get_ref_link(user_id)
        refs = len(users[user_id]["referrals"])
        await query.edit_message_text(
            f"👥 You referred *{refs}* people.\n\n"
            f"🔗 Your referral link:\n{ref_link}\n\n"
            f"Earn ₹{REF_BONUS} per referral!",
            parse_mode=ParseMode.MARKDOWN
        )

    elif data == "daily_bonus":
        if not users[user_id]["daily_bonus"]:
            users[user_id]["balance"] += DAILY_BONUS
            users[user_id]["daily_bonus"] = True
            await query.edit_message_text(f"🎁 Bonus received! ₹{DAILY_BONUS} added to your balance.")
        else:
            await query.edit_message_text("⛔ You already claimed today's bonus.")

    elif data == "withdraw":
        bal = users[user_id]["balance"]
        if bal >= MIN_WITHDRAW:
            users[user_id]["balance"] = 0
            await query.edit_message_text("✅ Withdrawal requested. Payment will be sent soon!")
        else:
            await query.edit_message_text(f"❌ Minimum withdraw is ₹{MIN_WITHDRAW}. Your balance: ₹{bal}")

    elif data == "tasks":
        await query.edit_message_text(
            "📝 *Available Tasks:*\n\n"
            f"1️⃣ Subscribe to our YouTube channel → [ClipStorm2026]({YOUTUBE_CHANNEL_LINK}) → ₹5\n"
            f"2️⃣ Join Telegram channel → [SHOORVEER Episodes]({BONUS_TELEGRAM_CHANNEL}) → ₹2\n"
            f"3️⃣ Like & Comment this Short → [Watch Video]({BONUS_YT_SHORT_LINK}) → ₹3\n\n"
            "👉 *More tasks coming soon...*",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True
        )


# === Main ===
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(check_join_callback, pattern="check_join"))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("✅ Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
