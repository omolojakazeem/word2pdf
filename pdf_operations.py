from io import BytesIO

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
import os
from module_imports.module_imports import logger, get_current_datetime_in_ms
from pdf2docx import Converter
from docx2pdf import convert


operation, uploaded_file = range(5, 7)

## ==================== Helper Functions ============================== ##

async def save_file(context, file_id):
    user_file = await context.bot.get_file(file_id)
    path = await user_file.download_to_drive()
    return user_file, path


async def delete_file(user_file_path, file_id):
    if user_file_path and file_id:
        if os.path.exists(user_file_path):
            os.remove(user_file_path)
            return True
        return False
    else:
        return False


async def delete_file_from_path(user_file_path):
    if user_file_path:
        if os.path.exists(user_file_path):
            os.remove(user_file_path)
            return True
        return False
    else:
        return False

async def convert_pdf_to_docx(pdf_file_path, file_id, user_name):
    file_name = f"converted_{file_id[:3]}{get_current_datetime_in_ms()}.docx"
    cv = Converter(pdf_file_path)
    cv.convert(file_name, start=0, end=None)  # Converts all pages
    cv.close()

    with open(file_name, 'rb') as f:
        docx_data = f.read()
        docx_stream = BytesIO(docx_data)
    return docx_stream, file_name


async def convert_word_to_pdf(docx_file, file_id, user_name):
    file_name = f"converted_{file_id[:3]}{get_current_datetime_in_ms()}.pdf"
    convert(docx_file, file_name)
    with open(file_name, 'rb') as f:
        pdf_data = f.read()
        pdf_stream = BytesIO(pdf_data)
    return pdf_stream, file_name
#
#
## ==================== Helper Functions ============================== ##

## ==================== Bot Functions ================================= ##
async def start_file_operation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    reply_keyboard = [["Convert to PDF", "Convert to Word"]]
    await update.message.reply_text(
        "Hi! I am here to help perform various operations on your file your pdf.\n\n",
        reply_markup = ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Convert to PDF, Convert to Word"
        )
    )
    return operation


async def get_file(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    key = 'file_operation'
    context.chat_data[key] = update.message.text
    await update.message.reply_text(
        "Please upload your file?",
    )
    return uploaded_file


async def perform_file_operation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    document = update.message.document
    document_type = 'pdf' if document.mime_type == 'application/pdf' else 'word'
    file_id = document.file_id
    file_operation = context.chat_data.get('file_operation')
    logger.info(f"Starting operation {file_operation}")
    user_file = await save_file(context, file_id)
    operated = False
    if file_operation == "Convert to PDF":
        logger.info(f"Operation - To PDF")
        if document_type == 'word':
            converted_file = await convert_word_to_pdf(user_file[1], user_file[0].file_id, update.message.from_user.username)
            send_file = converted_file[1]
            operated = True
        else:
            logger.info("Uploaded file is already pdf")
            send_file = file_id

    else:
        logger.info(f"Operation - To Word")
        if document_type == 'pdf':
            converted_file = await convert_pdf_to_docx(user_file[1], user_file[0].file_id, update.message.from_user.username)
            send_file = converted_file[1]
            operated = True
        else:
            logger.info("Uploaded file is already in word")
            send_file = file_id
    await context.bot.send_document(chat_id=update.message.chat_id, document=send_file)

    if operated:
        original_deleted = await delete_file_from_path(user_file[1])
        converted_deleted = await delete_file_from_path(send_file)
        if converted_deleted:
            logger.info("Converted file has been deleted from memory")
        else:
            logger.info('Converted file can not be deleted or file already removed.')
    else:
        original_deleted = await delete_file_from_path(user_file[1])
    if original_deleted:
        logger.info("Uploaded file has been deleted from memory")
    else:
        logger.info('Uploaded file can not be deleted or file already removed.')

    return ConversationHandler.END
