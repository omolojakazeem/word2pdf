from telegram import Update, InlineQueryResultArticle, InputTextMessageContent, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, InlineQueryHandler, \
    ConversationHandler
from module_imports.module_imports import logger


first_name, last_name, gender, age = range(4)


async def start_bio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Hi! I am here to take you details. "
        "Send /cancel to stop talking to me.\n\n"
        "Please enter your first name?",
    )
    return first_name


async def get_first_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    await update.message.reply_text(
        "Please enter your last name?",
    )
    return last_name


async def get_last_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    reply_keyboard = [["Male", "Female"]]

    await update.message.reply_text(
        "Are you a male or a female?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Male or Female?"
        ),
    )
    return gender


async def get_gender(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    await update.message.reply_text(
        "Please enter your age",
    )
    return age


async def get_age(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger.info(f"Details of the user variable {type(user)}, {user}")
    await update.message.reply_text("Thank you! I hope we can talk again some day.")
    return ConversationHandler.END
