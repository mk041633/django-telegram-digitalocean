from django.core.management.base import BaseCommand
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from messenger.models import BotToken, TelegramUser
from TelegramBotProject.settings import TELEGRAM_BOT_TOKEN

class Command(BaseCommand):
    help = 'Run the Telegram bot'

    def handle(self, *args, **options):
        def start(update: Update, context: CallbackContext) -> None:
            update.message.reply_text('Привет! Пожалуйста, отправьте свой токен.')

        def handle_token(update: Update, context: CallbackContext) -> None:
            chat_id = update.message.chat_id
            user_token = update.message.text
            username = update.message.from_user.username 

            try:
                bot_token = BotToken.objects.get(token=user_token)
                user = bot_token.user
                telegram_user, created = TelegramUser.objects.get_or_create(user=user)
                
                telegram_user.chat_id = chat_id
                telegram_user.telegram_token = bot_token.token
                telegram_user.username = username
                telegram_user.save()

                update.message.reply_text('Токен успешно связан с вашим аккаунтом в Telegram.')
            except BotToken.DoesNotExist:
                update.message.reply_text('Токен не найден.')

        bot_token = TELEGRAM_BOT_TOKEN
        bot = Bot(token=bot_token)

        updater = Updater(bot=bot)
        dispatcher = updater.dispatcher

        dispatcher.add_handler(CommandHandler("start", start))
        dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_token))

        updater.start_polling()
        updater.idle()