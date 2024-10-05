translations = {
    'en': {
        "Ви вже зареєстровані.": "You are already registered.",
        "Ви успішно зареєструвалися, бот надає інформацію про монети, які показують різький зріст або падіння в ціні. По замовчуванню сигналів надходити при зрості і падінні монети на 5% та -5%, ви можете налаштувати поріг сигналів.": "You have successfully registered, the bot provides information about coins that show a sharp rise or fall in price. By default, signals are sent when the coin rises and falls by 5% and -5%, you can adjust the signal threshold.",
        "Мінімальний відсоток при зростанні": "The minimum percentage during growth",
        "Мінімальний відсоток при падінні": "Minimum percentage when falling",
        "Змінити мову": "Change language",
        "Ви успішно повернулись в головне меню.": "You have successfully returned to the main menu.",
        "Ви можете встановити мінімальний відсоток при падінні монети.\nВи отримуватимете інформацію про монети, які впали на цей відсоток, або вище сьогодні.": "You can set a minimum percentage when a coin drops.\nYou will receive information about coins that have dropped by this percentage or higher today.",
        "Ви можете встановити мінімальний відсоток при зростанні монети.\nВи отримуватимете інформацію про монети, які зросли на цей відсоток, або вище сьогодні.": "You can set a minimum percentage for a coin to grow.\nYou will receive information about coins that have grown by this percentage or higher today.",
        "Ви можете встановити інтервали, за які будуть братись зміни ціни монет.": "You can set the intervals for which changes in the price of coins will be taken.",
        "Встановити": "Install",
        "Встановлено": "Installed",
        'Видалити': 'Uninstall', 
        "Ви успішно встановили поріг": "You have successfully set the threshold",
        "Ви вже використовуєте поріг": "You are already using the threshold",
        "Ви успішно встановили крок": "You have successfully set the step",
        "Ви вже використовуєте крок": "You are already using the step",
        "Ви успішно встановили інтервал": "You have successfully set the interval",
        "Інтервал вже використовується": "The interval is already in use",
        "Ви успішно видалили інтервал": "You have successfully deleted the interval",
        "Інтервал не використовується": "No space is used",
        "Введіть корректне число.": "Enter a valid number.",
        "Сталась помилка, спробуйте пізніше.": "An error occurred, please try again later.",
        "Перейти до торгівлі": "Go to trade",
        "Крок між сигналами": "Step between signals",
        "Налаштування сигналів": "Signal settings",
        "Налаштування відкатів": "Rollback settings",
        "Головне меню": "General menu",
        "Мінімальний відсоток відкатів": "Minimum percentage of rollbacks",
        "Крок між відкатами": "Step between rollbacks",
        "Налаштування сигналів успішно відкрито.": "Signal settings successfully opened.",
        "Налаштування відкатів успішно відкрито.": "Rollback settings successfully opened.",
        "Встановити відкат": "Install rollback",
        "Встановити крок сигналу": "Install signal step",
        "Встановити крок відкату": "Install rollback step",
        "Ви можете встановити мінімальний відсоток при відкаті монети.\nВи отримуватимете інформацію про монети, які відкатились.": "You can set a minimum percentage when the coin is rolled back.\nYou will receive information about the coins that have been rolled back.",
        'Скасувати': 'Cancel',
        "Часові проміжки сигналів": "Time intervals of signals",
        "Часові проміжки відкатів": "Time intervals of rollbacks",
        "Отримати звіт": "Get report",
        "Прив'язати пошту": "Bind mail",
        "Введіть пошту.": "Enter mail",
        "Пошту успішно прив`язно.": "Mail has been linked successfully.",
        "Неправильний формат пошти. Спробуйте ще раз.": "Incorrect mail format. Try again.",
        "Додати до обраних": "Add to favorites",
        "Монету успішно додано до обраних.": "The coin has been successfully added to favorites.",
        "Монета вже знаходиться в обраних.": "The coin is already in the favorites.",
        "Обрані монети": "Favourite coins",
        "Список обраних монет успішно відкрито.": "The list of selected coins has been successfully opened.",
        "Монета": "Coin",
        "Керування монетою успішно відкрито.": "Coin management successfully opened.",
        "Видалити монету": "Delete coin",
        "Монета не знаходиться в обраних.": "The coin is not in favorites.",
        "Монету успішно видалено з обраних.": "The coin has been successfully removed from favorites.",
    }
}

def translate(text, lang):
    global translations
    if lang == 'ukr':
        return text
    elif lang is None:
        try:
            global translations
            return translations['en'][text]
        except:
            return text
    else:
        try:
            return translations[lang][text]
        except:
            return text
