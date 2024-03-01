import telebot
from django.core.management.base import BaseCommand
from bot.models import Message
from bot.models import Profile

# Объявление переменной бота
bot = telebot.TeleBot("6908538128:AAEFlBcdoUq3xePGZhAPhGnq5_FEC-m9M7U", threaded=False)


def print_info(message):
    print(
        f"""
        id: {message.from_user.id}
        name: {message.from_user.first_name}
        last_name: {message.from_user.full_name}"""
    )


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    p, _ = Profile.objects.get_or_create(
        external_id=message.from_user.id,
        defaults={
            'name': message.from_user.first_name
        }
    )
    Message(
        profile=p,
        text=message.text,
    ).save()
    print_info(message)
    bot.reply_to(message, f"Ответ {message.text}")


# Название класса обязательно - "Command"
class Command(BaseCommand):
    # Используется как описание команды обычно
    help = 'Just a command for launching a Telegram bot.'

    def handle(self, *args, **kwargs):
        bot.enable_save_next_step_handlers(delay=2)  # Сохранение обработчиков
        bot.load_next_step_handlers()  # Загрузка обработчиков
        bot.infinity_polling()  # Бесконечный цикл бота
