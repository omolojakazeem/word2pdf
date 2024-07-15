from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, InlineQueryHandler, \
    ConversationHandler, Updater

from module_imports.module_imports import TELEGRAM_API_KEY, NGROK_URL, PORT, SECRET_TOKEN, SSL_KEY, SSL_CERT, WEBHOOK_URL
from pdf_operations import (start_file_operation, get_file, operation, uploaded_file, perform_file_operation)
from profile_operations import (start_bio, get_first_name, get_last_name, get_gender, get_age, first_name, last_name, gender, age)
from trivials import (start, caps, inline_caps, cancel, unknown)

if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_API_KEY).build()

    start_handler = CommandHandler('start', start)
    caps_handler = CommandHandler('caps', caps)
    inline_caps_handler = InlineQueryHandler(inline_caps)

    conv_handler_bio = ConversationHandler(
        entry_points=[CommandHandler("start_bio", start_bio)],
        states={
            first_name: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_first_name)],
            last_name: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_last_name)],
            gender: [MessageHandler(filters.Regex("^(Male|Female)$"), get_gender)],
            age: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_age)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    conv_handler_file = ConversationHandler(
        entry_points=[CommandHandler("file", start_file_operation)],
        states={
            operation: [MessageHandler(filters.Regex("^(Convert to PDF|Convert to Word|Compress PDF)$"), get_file)],
            uploaded_file: [
                # MessageHandler(filters.Document.MimeType(["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]),
                #                perform_file_operation)]
                # MessageHandler(filters.Document.ALL, perform_file_operation)
                MessageHandler(filters.Document.MimeType("application/pdf") | filters.Document.MimeType("application/vnd.openxmlformats-officedocument.wordprocessingml.document"), perform_file_operation)
            ]
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    unknown_handler = MessageHandler(filters.COMMAND, unknown)

    application.add_handler(start_handler)
    application.add_handler(caps_handler)
    application.add_handler(inline_caps_handler)
    application.add_handler(conv_handler_bio)
    application.add_handler(conv_handler_file)
    application.add_handler(unknown_handler)

    # Polling
    # application.run_polling(allowed_updates=Update.ALL_TYPES)

    # Webhook
    application.run_webhook(
        listen='0.0.0.0',
        port=PORT,
        secret_token=SECRET_TOKEN,
        key=SSL_KEY,
        cert=SSL_CERT,
        webhook_url=WEBHOOK_URL
    )
    application.idle()

    # url = f"https://api.telegram.org/bot{TELEGRAM_API_KEY}/setWebhook?url={NGROK_URL}/webhook"
