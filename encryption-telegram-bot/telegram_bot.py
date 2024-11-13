import os
import logging
import sqlite3
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
import re
from decrypt import Decryptor

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Retrieve sensitive information from environment variables
CUSTOMER_BOT_TOKEN = os.getenv("CUSTOMER_BOT_TOKEN")
ADMIN_BOT_TOKEN = os.getenv("ADMIN_BOT_TOKEN")
ADMIN_CHAT_IDS = os.getenv("ADMIN_CHAT_IDS").split(",")  # Admins' chat IDs (comma separated)

if not CUSTOMER_BOT_TOKEN or not ADMIN_BOT_TOKEN or not ADMIN_CHAT_IDS:
    logger.critical("CUSTOMER_BOT_TOKEN, ADMIN_BOT_TOKEN, or ADMIN_CHAT_IDS is not set in the environment.")
    exit(1)

# SQLite database connection setup
def get_db_connection():
    conn = sqlite3.connect('client_chat_mapping.db')
    conn.row_factory = sqlite3.Row  # Enable accessing columns by name
    return conn

# Function to create the database and table if they don't exist
def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS client_chat_mapping (
            client_chat_id INTEGER PRIMARY KEY,
            file_id TEXT NOT NULL,
            pending_code TEXT
        );
    ''')
    conn.commit()
    conn.close()

# Function to store client chat ID, file ID, and pending code
def store_client_data(client_chat_id, file_id, pending_code=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO client_chat_mapping (client_chat_id, file_id, pending_code)
        VALUES (?, ?, ?);
    ''', (client_chat_id, file_id, pending_code))
    conn.commit()
    conn.close()

# Function to get client data based on chat ID
def get_client_data(client_chat_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM client_chat_mapping WHERE client_chat_id = ?;
    ''', (client_chat_id,))
    client_data = cursor.fetchone()
    conn.close()
    return client_data

# Function to delete client data based on chat ID
def delete_client_data(client_chat_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM client_chat_mapping WHERE client_chat_id = ?;
    ''', (client_chat_id,))
    conn.commit()
    conn.close()

def extract_code_from_message(message: str) -> str:
    pattern = r"\|([^|]+)\|"  # Matches content between vertical bars
    match = re.search(pattern, message)
    return match.group(1) if match else ""  # Extract the part between "|"

def is_valid_key(key): # chatgpt method. I don't know a thing
    # Pattern explanation:
    # - `[a-zA-Z]{4}`: exactly 4 alphabetic characters
    # - `[#$@]{3}`: exactly 3 special characters from the set `#@$`
    # - `\d`: exactly one digit
    # - `.*`: matches any characters between these components
    pattern = re.compile(r'^(?=(.*[a-zA-Z]){4})(?=(.*[#@$]){3})(?=(.*\d){1}).{8}$')

    # Check if key matches the pattern and has exactly 8 characters
    return bool(pattern.match(key))

# Escape special MarkdownV2 characters
def escape_markdown_v2(text):
    return re.sub(r'([#_*\[\]()~`>+\-=|{}.!])', r'\\\1', text)

# 200
async def get_pass_code(update: Update, context: CallbackContext) -> None:
    message_text = update.message.text # user ပို့လိုက်တဲ့ message ကိုဖတ်မယ်။
    code = extract_code_from_message(message_text) # || ကိုဖယ်ပြီး ကျန်တာယူမယ်။

    if not is_valid_key(code): # အဆင်မပြေတဲ့ကောင်ကျော်မယ်။
        await update.message.reply_text(f"Not a valid code. Your code {code}")
        return

    if code: # if there is code
        await update.message.reply_text("Please upload an image of your payment proof for verification.")
        context.user_data['pending_code'] = code # user data မှာ ငါတို့ ခဏတာ variable ကို assign လုပ်နိုင်တယ်။
        context.user_data['awaiting_image'] = True # ပုံစောင့်နေတုန်း

    # else: # hide it for now. အကုန်လုံး ပြန်မပြောစေချင်ဘူး
    #     await update.message.reply_text("This is not a valid key")

# Send messages to all admins 200
async def send_message_to_admins(context: ContextTypes.DEFAULT_TYPE, message: str) -> None:
    for admin_chat_id in ADMIN_CHAT_IDS:
        try:
            await context.bot.send_message(chat_id=admin_chat_id, text=message)
            logger.info(f"Message sent to admin {admin_chat_id}: {message}")
        except Exception as e:
            logger.error(f"Error sending message to admin {admin_chat_id}: {e}")

#
async def send_image_to_admins(context: ContextTypes.DEFAULT_TYPE, file, client_chat_id: int) -> None:
    store_client_data(client_chat_id, file.file_id, context.user_data['pending_code']) # db မှာသိမ်းမယ်။
    approve_button = InlineKeyboardButton("Approve", callback_data=f"approve_payment_{client_chat_id}") # callback_data က bot ကို return ပြန်လုပ်ပေးတယ်
    deny_button = InlineKeyboardButton("Deny", callback_data=f"deny_payment_{client_chat_id}") # ငြင်းတဲ့ ခလုတ် ထည့်ကြည့်မယ်
    reply_markup = InlineKeyboardMarkup([[approve_button], [deny_button]])

    for admin_chat_id in ADMIN_CHAT_IDS:
        try:
            await context.bot.send_photo(
                chat_id=admin_chat_id,
                photo=file.file_id,
                reply_markup=reply_markup
            )
            logger.info(f"Image sent to admin {admin_chat_id}.")
        except Exception as e:
            logger.error(f"Error sending image to admin {admin_chat_id}: {e}")

async def handle_approve_button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    print("This is query")
    print(query)
    await query.answer()

    data = query.data
    if data.startswith("approve_payment_"):
        client_chat_id = int(data.split("_")[-1]) # chat id တော့လွဲစရာရှိတယ်။
        client_data = get_client_data(client_chat_id)

        if client_data and client_data['pending_code']:
            try:
                # Your decryption code with escaped characters
                decrypted_code = Decryptor(client_data['pending_code']).decrypt()
                safe_decrypted_code = escape_markdown_v2(decrypted_code)

                await context.bot.send_message(
                    chat_id=client_chat_id,
                    text=f"✅ Your payment has been approved\\! \n"
                         f"🔑 Here's your passcode: `{safe_decrypted_code}`\n"
                         "🙏 Thank you for your purchase\\.\n"
                         "😊 Enjoy\\!",
                    parse_mode='MarkdownV2'
                )

                logger.info(f"Activation code sent to user {client_chat_id}.")
                # delete_client_data(client_chat_id) # let's test by not deleting

                approve_caption = "Payment approved! ✅"
                message_id = query.message.message_id
                chat_id = query.message.chat_id

                if query.message.caption != approve_caption:
                    await coyuntext.bot.edit_message_caption(
                        chat_id=chat_id,
                        message_id=message_id,
                        caption=approve_caption
                    )

                await context.bot.edit_message_reply_markup(
                    chat_id=chat_id,
                    message_id=message_id,
                    reply_markup=None
                )
                logger.info(f"Admin message for {chat_id} updated with approval confirmation.")
            except Exception as e:
                logger.error(f"Error sending approval message to user {client_chat_id}: {e}")
        else:
            logger.warning(f"Client chat ID {client_chat_id} not found or missing code in database.")

async def start_customer_bot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Hello there! 😊 I'm here to assist you with the activation process for Easypaste software.\n\n"
        "Please paste your passkey below to receive your activation passcode."
    )
    logger.info(f"Start command received from customer {update.message.from_user.id}")

async def handle_image_customer_bot(update: Update, context: CallbackContext) -> None:
    if not context.user_data.get('awaiting_image'):
        await update.message.reply_text("Please enter your code first.")
        return

    if not update.message.photo:
        await update.message.reply_text("Please upload a valid image.")
        return

    photo = update.message.photo[-1]
    file_size = photo.file_size

    if file_size > 10 * 1024 * 1024:
        await update.message.reply_text("The file is too large. Please upload a smaller image (max 10 MB).")
        return

    try:
        file = await context.bot.get_file(photo.file_id)
        client_chat_id = update.message.from_user.id
        await send_message_to_admins(context, f"New payment image uploaded by user @{update.message.from_user.username or update.message.from_user.id}. File ID: {photo.file_id}")
        await send_image_to_admins(context, file, client_chat_id)

        context.user_data['awaiting_image'] = False
        await update.message.reply_text("Image received! We will verify it and get back to you soon.")
    except Exception as e:
        await update.message.reply_text("An error occurred while processing the image.")
        logger.error(f"Error processing image for customer {update.message.from_user.id}: {e}")

async def help_customer_bot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Here’s what I can do:\n"
        "/start - Start the bot and upload your payment proof\n"
        "/help - Get help with commands"
    )
    logger.info(f"Help command received from customer {update.message.from_user.id}")

def main():
    create_table()
    customer_application = Application.builder().token(CUSTOMER_BOT_TOKEN).build()
    customer_application.add_handler(CommandHandler("start", start_customer_bot))
    customer_application.add_handler(CommandHandler("help", help_customer_bot))
    customer_application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, get_pass_code))
    customer_application.add_handler(MessageHandler(filters.PHOTO, handle_image_customer_bot))
    customer_application.add_handler(CallbackQueryHandler(handle_approve_button, pattern="^approve_payment_"))
    logger.info("Customer bot is running...")
    customer_application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
