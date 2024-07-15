from uuid import uuid4

from telegram import Update, InlineQueryResultArticle, InputTextMessageContent, ReplyKeyboardRemove
from telegram.ext import ContextTypes, ConversationHandler

from module_imports.module_imports import logger


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Hello {user.username}.\n\n I can help you convert your documents from: \n\n a.  Word to PDF \n b. PDF to Word. \n\nTo begin, send the /file command."
    )


async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = ' '.join(context.args)
    if text.strip():
        text_caps = text.upper()
    else:
        text_caps = "empty text"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)


async def inline_caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query
    if not query:
        return
    results = [InlineQueryResultArticle(
        id=str(uuid4()),
        title='Caps',
        input_message_content=InputTextMessageContent(query.upper())
    )]
    await context.bot.answer_inline_query(update.inline_query.id, results)


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.username)
    await update.message.reply_text(
        f"Bye {user.username}! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

