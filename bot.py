
from telegram.ext.filters import Filters
from telegram import ParseMode
import os
from telegram import Update, replymarkup
from telegram.ext import (Updater,
                          PicklePersistence,
                          CommandHandler,
                          MessageHandler,
                          Filters,
                          CallbackQueryHandler,
                          CallbackContext,
                          ConversationHandler)
from telegram import InlineKeyboardButton as IKB, InlineKeyboardMarkup, ForceReply


BOT_TOKEN = os.environ.get('BOT_TOKEN')


def start(update: Update, context: CallbackContext):
    ''' Replies to start command '''
    update.message.reply_text('Hi, i am button creator bot! \nFirst add a button using /add, then send any message to me, i will add the button to that.')


def add_button(update: Update, context: CallbackContext):
    args = ' '.join(context.args).strip()
    if not args:
        update.message.reply_text(
            'Please send the text and link with the command. \nExample: \n\n`/add Click here - https://aahnik.github.io`',parse_mode= ParseMode.MARKDOWN)
        return
    try:
        splitted = args.split('-')
        print(splitted)
        text = splitted[0].strip()
        url = splitted[1].strip()
        print(text,url)
    except Exception as err:
        update.message.reply_text(str(err)[:2000])
        return

    user_d = context.user_data
    if not 'buttons' in user_d:
        user_d['buttons'] = []
    user_d['buttons'].append([IKB(text, url=url)])
    update.message.reply_text('Done')


def preview(update: Update, context: CallbackContext):
    user_d = context.user_data
    buttons = user_d.get('buttons')
    if buttons:
        if update.effective_message.text:
            if not "start" and not "add" in update.message['text']:
                update.message.reply_text(
                    'B', reply_markup=InlineKeyboardMarkup(buttons))
            else:
                update.message.reply_text('No buttons added yet')
        if update.message['audio'] == []:
            caption = update.message['caption']
            chat_id = update.message['chat_id']
            fileID = update.message['audio']['file_id']
            fileName = update.message['audio']['file_name']
            context.bot.sendAudio(
                chat_id = chat_id,
                filename = fileName,
                caption = caption,
                audio = fileID,
                reply_markup = InlineKeyboardMarkup(buttons)
            )
        else:
            update.message.reply_text('No buttons added yet')


if __name__ == "__main__":

    updater = Updater(token=BOT_TOKEN)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(
        MessageHandler(
            (Filters.audio | Filters.text),
        preview
        )
    )
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('add', add_button))

    updater.start_polling()
