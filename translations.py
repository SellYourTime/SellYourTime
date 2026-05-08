"""
Timely Bot — سیستم چندزبانه
پشتیبانی از: فارسی، انگلیسی، آلمانی، روسی
"""

LANGUAGES = {
    "fa": "🇮🇷 فارسی",
    "en": "🇬🇧 English",
    "de": "🇩🇪 Deutsch",
    "ru": "🇷🇺 Русский",
}

# جهت نوشتار
RTL_LANGS = {"fa"}

TRANSLATIONS = {

    # ─── زبان ────────────────────────────────────────
    "choose_language": {
        "fa": "🌍 زبان خود را انتخاب کنید:",
        "en": "🌍 Please choose your language:",
        "de": "🌍 Bitte wähle deine Sprache:",
        "ru": "🌍 Пожалуйста, выберите язык:",
    },
    "language_set": {
        "fa": "✅ زبان فارسی انتخاب شد.",
        "en": "✅ Language set to English.",
        "de": "✅ Sprache auf Deutsch eingestellt.",
        "ru": "✅ Язык установлен на русский.",
    },

    # ─── شروع / منوی اصلی ────────────────────────────
    "welcome_back": {
        "fa": "👋 خوش برگشتی {nick}!\n\n⭐ امتیاز: {rating} ({count} نظر)\n💰 کیف پول: {balance} {currency}",
        "en": "👋 Welcome back {nick}!\n\n⭐ Rating: {rating} ({count} reviews)\n💰 Wallet: {balance} {currency}",
        "de": "👋 Willkommen zurück {nick}!\n\n⭐ Bewertung: {rating} ({count} Bewertungen)\n💰 Guthaben: {balance} {currency}",
        "ru": "👋 С возвращением {nick}!\n\n⭐ Рейтинг: {rating} ({count} отзывов)\n💰 Кошелёк: {balance} {currency}",
    },
    "welcome_new": {
        "fa": "⏱ به *Timely* خوش آمدید!\n\nجایی که می‌تونی با آدم‌های واقعی وقت بگذرونی.\n\nبرای شروع، اسم کاملت رو بنویس:",
        "en": "⏱ Welcome to *Timely*!\n\nWhere you can spend time with real people.\n\nTo get started, please enter your full name:",
        "de": "⏱ Willkommen bei *Timely*!\n\nHier kannst du echte Zeit mit echten Menschen verbringen.\n\nBitte gib deinen vollständigen Namen ein:",
        "ru": "⏱ Добро пожаловать в *Timely*!\n\nЗдесь ты можешь проводить время с реальными людьми.\n\nДля начала введи своё полное имя:",
    },
    "banned": {
        "fa": "❌ حساب شما به دلیل تخلف مسدود شده است.\nدلیل: {reason}",
        "en": "❌ Your account has been banned.\nReason: {reason}",
        "de": "❌ Dein Konto wurde gesperrt.\nGrund: {reason}",
        "ru": "❌ Ваш аккаунт заблокирован.\nПричина: {reason}",
    },

    # ─── منوی اصلی دکمه‌ها ───────────────────────────
    "menu_search": {
        "fa": "🔍 جستجوی همراه",
        "en": "🔍 Find a Companion",
        "de": "🔍 Begleiter suchen",
        "ru": "🔍 Найти компаньона",
    },
    "menu_events": {
        "fa": "📅 ایونت‌ها",
        "en": "📅 Events",
        "de": "📅 Veranstaltungen",
        "ru": "📅 События",
    },
    "menu_bookings": {
        "fa": "📋 رزروهای من",
        "en": "📋 My Bookings",
        "de": "📋 Meine Buchungen",
        "ru": "📋 Мои бронирования",
    },
    "menu_profile": {
        "fa": "👤 پروفایل من",
        "en": "👤 My Profile",
        "de": "👤 Mein Profil",
        "ru": "👤 Мой профиль",
    },
    "menu_referral": {
        "fa": "🎁 کد معرفی",
        "en": "🎁 Referral",
        "de": "🎁 Empfehlung",
        "ru": "🎁 Реферал",
    },
    "menu_rules": {
        "fa": "📜 قوانین",
        "en": "📜 Rules",
        "de": "📜 Regeln",
        "ru": "📜 Правила",
    },
    "menu_new_requests": {
        "fa": "📨 درخواست‌های جدید",
        "en": "📨 New Requests",
        "de": "📨 Neue Anfragen",
        "ru": "📨 Новые запросы",
    },
    "menu_earnings": {
        "fa": "💰 درآمدم",
        "en": "💰 My Earnings",
        "de": "💰 Meine Einnahmen",
        "ru": "💰 Мой доход",
    },
    "menu_language": {
        "fa": "🌍 تغییر زبان",
        "en": "🌍 Change Language",
        "de": "🌍 Sprache ändern",
        "ru": "🌍 Сменить язык",
    },

    # ─── ثبت‌نام ──────────────────────────────────────
    "reg_ask_gender": {
        "fa": "جنسیتت رو انتخاب کن:",
        "en": "Please select your gender:",
        "de": "Bitte wähle dein Geschlecht:",
        "ru": "Пожалуйста, выберите пол:",
    },
    "gender_male": {
        "fa": "مرد", "en": "Male", "de": "Mann", "ru": "Мужской",
    },
    "gender_female": {
        "fa": "زن", "en": "Female", "de": "Frau", "ru": "Женский",
    },
    "reg_ask_birthdate": {
        "fa": "تاریخ تولدت رو بنویس (مثال: 1375/03/15 یا 1996/06/05):",
        "en": "Enter your birth date (e.g. 1996/06/05):",
        "de": "Gib dein Geburtsdatum ein (z.B. 1996/06/05):",
        "ru": "Введите дату рождения (например: 1996/06/05):",
    },
    "reg_underage": {
        "fa": "❌ سن باید حداقل ۱۸ سال باشه.",
        "en": "❌ You must be at least 18 years old.",
        "de": "❌ Du musst mindestens 18 Jahre alt sein.",
        "ru": "❌ Вам должно быть не менее 18 лет.",
    },
    "reg_ask_city": {
        "fa": "شهرت رو انتخاب کن:",
        "en": "Select your city:",
        "de": "Wähle deine Stadt:",
        "ru": "Выберите ваш город:",
    },
    "reg_ask_role": {
        "fa": "می‌خوای وقت بخری یا بفروشی؟",
        "en": "Do you want to buy or sell time?",
        "de": "Möchtest du Zeit kaufen oder verkaufen?",
        "ru": "Вы хотите купить или продать время?",
    },
    "role_buyer": {
        "fa": "فقط می‌خرم ⬅️", "en": "Just buying ⬅️", "de": "Nur kaufen ⬅️", "ru": "Только покупаю ⬅️",
    },
    "role_seller": {
        "fa": "وقتم رو می‌فروشم ➡️", "en": "Selling my time ➡️", "de": "Verkaufe meine Zeit ➡️", "ru": "Продаю время ➡️",
    },
    "role_both": {
        "fa": "هر دو 🔄", "en": "Both 🔄", "de": "Beides 🔄", "ru": "Оба 🔄",
    },
    "reg_ask_nickname": {
        "fa": "یه نیک‌نیم منحصربه‌فرد انتخاب کن (فقط a-z، 0-9، _):",
        "en": "Choose a unique nickname (only a-z, 0-9, _):",
        "de": "Wähle einen einzigartigen Spitznamen (nur a-z, 0-9, _):",
        "ru": "Выберите уникальный никнейм (только a-z, 0-9, _):",
    },
    "reg_ask_bio": {
        "fa": "یه بیو کوتاه درباره خودت بنویس:",
        "en": "Write a short bio about yourself:",
        "de": "Schreibe eine kurze Bio über dich:",
        "ru": "Напишите краткое описание о себе:",
    },
    "reg_ask_photo": {
        "fa": "عکس پروفایلت رو بفرست (یا /skip):",
        "en": "Send your profile photo (or /skip):",
        "de": "Sende dein Profilfoto (oder /skip):",
        "ru": "Отправьте фото профиля (или /skip):",
    },
    "reg_ask_activities": {
        "fa": "فعالیت‌هایی که می‌تونی انجام بدی رو انتخاب کن:",
        "en": "Select the activities you can do:",
        "de": "Wähle die Aktivitäten, die du anbieten kannst:",
        "ru": "Выберите виды деятельности, которые вы предлагаете:",
    },
    "reg_ask_pet": {
        "fa": "آیا با همراه داشتن حیوان خانگی مشکلی داری؟",
        "en": "Are you okay with pets?",
        "de": "Ist es okay für dich, wenn jemand ein Haustier dabei hat?",
        "ru": "Вы не против домашних животных?",
    },
    "pet_yes": {
        "fa": "بله 🐾 قبول می‌کنم", "en": "Yes 🐾 Fine with pets", "de": "Ja 🐾 Haustiere ok", "ru": "Да 🐾 Со мной можно",
    },
    "pet_no": {
        "fa": "نه ❌", "en": "No ❌", "de": "Nein ❌", "ru": "Нет ❌",
    },
    "reg_ask_referral": {
        "fa": "اگه کد دعوت داری وارد کن (یا /skip):",
        "en": "Enter referral code if you have one (or /skip):",
        "de": "Gib deinen Empfehlungscode ein, falls vorhanden (oder /skip):",
        "ru": "Введите реферальный код, если есть (или /skip):",
    },
    "reg_confirm": {
        "fa": "✅ *اطلاعات ثبت‌نام:*\n\n👤 اسم: {name}\n🏷 نیک‌نیم: @{nick}\n📍 شهر: {city}\n🎭 نقش: {role}\n\nآیا تأیید می‌کنی؟",
        "en": "✅ *Registration Details:*\n\n👤 Name: {name}\n🏷 Nickname: @{nick}\n📍 City: {city}\n🎭 Role: {role}\n\nDo you confirm?",
        "de": "✅ *Registrierungsdetails:*\n\n👤 Name: {name}\n🏷 Nickname: @{nick}\n📍 Stadt: {city}\n🎭 Rolle: {role}\n\nBestätigst du?",
        "ru": "✅ *Данные регистрации:*\n\n👤 Имя: {name}\n🏷 Ник: @{nick}\n📍 Город: {city}\n🎭 Роль: {role}\n\nПодтверждаете?",
    },
    "confirm_yes": {
        "fa": "✅ بله، ثبت‌نام کن", "en": "✅ Yes, register me", "de": "✅ Ja, registrieren", "ru": "✅ Да, зарегистрировать",
    },
    "confirm_no": {
        "fa": "❌ از اول", "en": "❌ Start over", "de": "❌ Neu starten", "ru": "❌ Начать заново",
    },
    "reg_success": {
        "fa": "🎉 *ثبت‌نام موفق!*\n\nخوش اومدی به Timely @{nick}!\n\n{seller_note}",
        "en": "🎉 *Registration Successful!*\n\nWelcome to Timely @{nick}!\n\n{seller_note}",
        "de": "🎉 *Registrierung erfolgreich!*\n\nWillkommen bei Timely @{nick}!\n\n{seller_note}",
        "ru": "🎉 *Регистрация прошла успешно!*\n\nДобро пожаловать в Timely @{nick}!\n\n{seller_note}",
    },
    "seller_pending_note": {
        "fa": "⚠️ برای فعال شدن پروفایل فروشنده، هویتت توسط ادمین تأیید می‌شه.",
        "en": "⚠️ Your seller profile needs admin verification before going live.",
        "de": "⚠️ Dein Verkäuferprofil muss von einem Admin verifiziert werden.",
        "ru": "⚠️ Ваш профиль продавца должен быть подтверждён администратором.",
    },

    # ─── جستجو ───────────────────────────────────────
    "search_title": {
        "fa": "🔍 جستجوی همراه\n\nجنسیت:",
        "en": "🔍 Find a Companion\n\nGender:",
        "de": "🔍 Begleiter suchen\n\nGeschlecht:",
        "ru": "🔍 Найти компаньона\n\nПол:",
    },
    "gender_all": {
        "fa": "همه", "en": "All", "de": "Alle", "ru": "Все",
    },
    "search_ask_age": {
        "fa": "محدوده سنی (مثال: 20-35 یا /skip):",
        "en": "Age range (e.g. 20-35 or /skip):",
        "de": "Altersbereich (z.B. 20-35 oder /skip):",
        "ru": "Возрастной диапазон (например: 20-35 или /skip):",
    },
    "search_ask_city": {
        "fa": "شهر:", "en": "City:", "de": "Stadt:", "ru": "Город:",
    },
    "search_ask_activity": {
        "fa": "فعالیت مورد نظر:", "en": "Preferred activity:", "de": "Gewünschte Aktivität:", "ru": "Желаемое занятие:",
    },
    "activity_all": {
        "fa": "همه فعالیت‌ها", "en": "All activities", "de": "Alle Aktivitäten", "ru": "Все занятия",
    },
    "search_ask_pet": {
        "fa": "حیوان خانگی همراه داری؟",
        "en": "Do you have a pet with you?",
        "de": "Hast du ein Haustier dabei?",
        "ru": "У вас есть домашнее животное?",
    },
    "no_results": {
        "fa": "😔 هیچ همراهی با این مشخصات پیدا نشد.\nفیلترها رو تغییر بده.",
        "en": "😔 No companions found with these filters.\nTry changing the filters.",
        "de": "😔 Keine Begleiter mit diesen Filtern gefunden.\nVersuche andere Filter.",
        "ru": "😔 Никого не найдено с этими фильтрами.\nПопробуйте изменить фильтры.",
    },
    "profile_card": {
        "fa": "{verified} *@{nick}*{pet}\n{gender} {age} ساله | 📍 {city}\n⭐ {rating} ({count} نظر)\n💰 {price} ت/ساعت\n\n📝 {bio}\n\n🎯 {activities}",
        "en": "{verified} *@{nick}*{pet}\n{gender} {age} y.o. | 📍 {city}\n⭐ {rating} ({count} reviews)\n💰 {price}/hr\n\n📝 {bio}\n\n🎯 {activities}",
        "de": "{verified} *@{nick}*{pet}\n{gender} {age} J. | 📍 {city}\n⭐ {rating} ({count} Bewertungen)\n💰 {price}/Std\n\n📝 {bio}\n\n🎯 {activities}",
        "ru": "{verified} *@{nick}*{pet}\n{gender} {age} лет | 📍 {city}\n⭐ {rating} ({count} отзывов)\n💰 {price}/час\n\n📝 {bio}\n\n🎯 {activities}",
    },
    "btn_book": {
        "fa": "📅 رزرو @{nick}", "en": "📅 Book @{nick}", "de": "📅 Buchen @{nick}", "ru": "📅 Забронировать @{nick}",
    },
    "bio_translated": {
        "fa": "📝 {bio}\n_(ترجمه شده از {lang})_",
        "en": "📝 {bio}\n_(translated from {lang})_",
        "de": "📝 {bio}\n_(übersetzt aus {lang})_",
        "ru": "📝 {bio}\n_(переведено с {lang})_",
    },

    # ─── رزرو ────────────────────────────────────────
    "book_select_activity": {
        "fa": "فعالیت رو انتخاب کن:",
        "en": "Select an activity:",
        "de": "Wähle eine Aktivität:",
        "ru": "Выберите занятие:",
    },
    "book_select_hours": {
        "fa": "چند ساعت؟",
        "en": "How many hours?",
        "de": "Wie viele Stunden?",
        "ru": "Сколько часов?",
    },
    "book_ask_date": {
        "fa": "تاریخ و ساعت پیشنهادی قرار رو بنویس:",
        "en": "Enter your preferred date and time for the meeting:",
        "de": "Gib dein bevorzugtes Datum und Uhrzeit ein:",
        "ru": "Введите предпочтительную дату и время встречи:",
    },
    "book_summary": {
        "fa": "📋 *خلاصه رزرو:*\n\n👤 همراه: @{nick}\n🎯 فعالیت: {activity}\n⏱ مدت: {hours} ساعت\n📅 زمان: {date}\n\n💵 مبلغ: {original}\n{discount_line}💳 *مبلغ نهایی: {total}*\n\n⚠️ پس از تأیید فروشنده، پرداخت انجام می‌شه.",
        "en": "📋 *Booking Summary:*\n\n👤 Companion: @{nick}\n🎯 Activity: {activity}\n⏱ Duration: {hours} hours\n📅 Time: {date}\n\n💵 Amount: {original}\n{discount_line}💳 *Final amount: {total}*\n\n⚠️ Payment after seller confirms.",
        "de": "📋 *Buchungsübersicht:*\n\n👤 Begleiter: @{nick}\n🎯 Aktivität: {activity}\n⏱ Dauer: {hours} Stunden\n📅 Zeit: {date}\n\n💵 Betrag: {original}\n{discount_line}💳 *Endbetrag: {total}*\n\n⚠️ Zahlung nach Bestätigung des Verkäufers.",
        "ru": "📋 *Сводка бронирования:*\n\n👤 Компаньон: @{nick}\n🎯 Занятие: {activity}\n⏱ Продолжительность: {hours} ч.\n📅 Время: {date}\n\n💵 Сумма: {original}\n{discount_line}💳 *Итоговая сумма: {total}*\n\n⚠️ Оплата после подтверждения продавца.",
    },
    "btn_send_request": {
        "fa": "📨 ارسال درخواست", "en": "📨 Send Request", "de": "📨 Anfrage senden", "ru": "📨 Отправить запрос",
    },
    "btn_cancel": {
        "fa": "❌ انصراف", "en": "❌ Cancel", "de": "❌ Abbrechen", "ru": "❌ Отмена",
    },
    "booking_sent": {
        "fa": "📨 درخواست ارسال شد!\n\nمنتظر تأیید @{nick} بمون.\nشماره رزرو: #{id}",
        "en": "📨 Request sent!\n\nWaiting for @{nick} to confirm.\nBooking #{id}",
        "de": "📨 Anfrage gesendet!\n\nWarte auf Bestätigung von @{nick}.\nBuchung #{id}",
        "ru": "📨 Запрос отправлен!\n\nОжидаем подтверждения от @{nick}.\nБронирование #{id}",
    },

    # ─── تأیید فروشنده ────────────────────────────────
    "seller_new_request": {
        "fa": "📨 *درخواست رزرو جدید!*\n\n👤 از: @{buyer}\n🎯 فعالیت: {activity}\n⏱ {hours} ساعت\n📅 {date}\n💰 {amount} (سهم تو)\n\nتا ۲۴ ساعت وقت داری.",
        "en": "📨 *New Booking Request!*\n\n👤 From: @{buyer}\n🎯 Activity: {activity}\n⏱ {hours} hours\n📅 {date}\n💰 {amount} (your share)\n\nYou have 24 hours to respond.",
        "de": "📨 *Neue Buchungsanfrage!*\n\n👤 Von: @{buyer}\n🎯 Aktivität: {activity}\n⏱ {hours} Stunden\n📅 {date}\n💰 {amount} (dein Anteil)\n\nDu hast 24 Stunden Zeit.",
        "ru": "📨 *Новый запрос на бронирование!*\n\n👤 От: @{buyer}\n🎯 Занятие: {activity}\n⏱ {hours} ч.\n📅 {date}\n💰 {amount} (ваша доля)\n\nУ вас 24 часа на ответ.",
    },
    "btn_accept": {
        "fa": "✅ قبول می‌کنم", "en": "✅ Accept", "de": "✅ Annehmen", "ru": "✅ Принять",
    },
    "btn_reject": {
        "fa": "❌ رد می‌کنم", "en": "❌ Reject", "de": "❌ Ablehnen", "ru": "❌ Отклонить",
    },
    "booking_confirmed_buyer": {
        "fa": "✅ *@{nick} درخواستت رو تأیید کرد!*\n\nمبلغ {amount} رو پرداخت کن.",
        "en": "✅ *@{nick} confirmed your request!*\n\nPlease pay {amount}.",
        "de": "✅ *@{nick} hat deine Anfrage bestätigt!*\n\nBitte zahle {amount}.",
        "ru": "✅ *@{nick} подтвердил(а) ваш запрос!*\n\nПожалуйста, оплатите {amount}.",
    },
    "booking_rejected_buyer": {
        "fa": "❌ متأسفانه @{nick} درخواستت رو رد کرد.",
        "en": "❌ Unfortunately @{nick} rejected your request.",
        "de": "❌ Leider hat @{nick} deine Anfrage abgelehnt.",
        "ru": "❌ К сожалению, @{nick} отклонил(а) ваш запрос.",
    },
    "btn_pay": {
        "fa": "💳 پرداخت {amount}", "en": "💳 Pay {amount}", "de": "💳 Zahlen {amount}", "ru": "💳 Оплатить {amount}",
    },

    # ─── GPS ─────────────────────────────────────────
    "gps_start_msg": {
        "fa": "📍 دکمه زیر رو بزن تا موقعیتت ارسال بشه.\nوقتی هر دو در فاصله ۵۰ متری باشید، تایمر شروع می‌شه!",
        "en": "📍 Press the button below to share your location.\nThe timer starts when both of you are within 50 meters!",
        "de": "📍 Drücke den Knopf unten, um deinen Standort zu teilen.\nDer Timer startet, wenn beide innerhalb von 50 Metern sind!",
        "ru": "📍 Нажмите кнопку ниже, чтобы поделиться местоположением.\nТаймер запустится, когда оба будут в 50 метрах!",
    },
    "btn_share_location": {
        "fa": "📍 ارسال موقعیت", "en": "📍 Share Location", "de": "📍 Standort teilen", "ru": "📍 Поделиться локацией",
    },
    "gps_distance": {
        "fa": "📍 فاصله تا همراهت: *{dist} متر*\n{status}",
        "en": "📍 Distance to companion: *{dist} meters*\n{status}",
        "de": "📍 Entfernung zum Begleiter: *{dist} Meter*\n{status}",
        "ru": "📍 Расстояние до компаньона: *{dist} метров*\n{status}",
    },
    "gps_nearby": {
        "fa": "✅ نزدیک شدی!", "en": "✅ Almost there!", "de": "✅ Fast da!", "ru": "✅ Почти рядом!",
    },
    "gps_far": {
        "fa": "🚶 در راهه...", "en": "🚶 On the way...", "de": "🚶 Unterwegs...", "ru": "🚶 В пути...",
    },
    "timer_started": {
        "fa": "🟢 *تایمر شروع شد!*\n\n⏱ {hours} ساعت شروع شد.\nوقتی تموم شد، دکمه ⏹ پایان رو بزن.",
        "en": "🟢 *Timer started!*\n\n⏱ {hours} hours started.\nPress ⏹ End when done.",
        "de": "🟢 *Timer gestartet!*\n\n⏱ {hours} Stunden gestartet.\nDrücke ⏹ Ende wenn fertig.",
        "ru": "🟢 *Таймер запущен!*\n\n⏱ Начались {hours} часа.\nНажмите ⏹ Конец по завершении.",
    },
    "btn_end_session": {
        "fa": "⏹ پایان قرار", "en": "⏹ End Session", "de": "⏹ Sitzung beenden", "ru": "⏹ Завершить встречу",
    },
    "session_ended": {
        "fa": "🎉 *قرار موفق بود!*\n\nحالا @{nick} رو امتیاز بده 👇",
        "en": "🎉 *Session completed successfully!*\n\nNow rate @{nick} 👇",
        "de": "🎉 *Sitzung erfolgreich abgeschlossen!*\n\nBewerte jetzt @{nick} 👇",
        "ru": "🎉 *Встреча прошла успешно!*\n\nТеперь оцените @{nick} 👇",
    },

    # ─── امتیاز ──────────────────────────────────────
    "rate_title": {
        "fa": "@{nick} رو ارزیابی کن\n\nنظرت به بقیه کمک می‌کنه",
        "en": "Rate @{nick}\n\nYour feedback helps others",
        "de": "Bewerte @{nick}\n\nDeine Bewertung hilft anderen",
        "ru": "Оцените @{nick}\n\nВаш отзыв помогает другим",
    },
    "rate_labels": {
        "fa": ["", "خیلی بد 😞", "بد 😕", "متوسط 😐", "خوب 😊", "عالی 🤩"],
        "en": ["", "Very bad 😞", "Bad 😕", "OK 😐", "Good 😊", "Excellent 🤩"],
        "de": ["", "Sehr schlecht 😞", "Schlecht 😕", "OK 😐", "Gut 😊", "Ausgezeichnet 🤩"],
        "ru": ["", "Очень плохо 😞", "Плохо 😕", "Нормально 😐", "Хорошо 😊", "Отлично 🤩"],
    },
    "rate_need_reason": {
        "fa": "⚠️ دلیل نارضایتی رو انتخاب کن (الزامی):",
        "en": "⚠️ Select the reason for your dissatisfaction (required):",
        "de": "⚠️ Wähle den Grund deiner Unzufriedenheit (erforderlich):",
        "ru": "⚠️ Выберите причину недовольства (обязательно):",
    },
    "rate_reasons": {
        "fa": ["رفتار نامناسب", "دیر کردن زیاد", "عدم تطابق پروفایل", "عدم رعایت قوانین", "سایر"],
        "en": ["Inappropriate behavior", "Excessive lateness", "Profile mismatch", "Rule violation", "Other"],
        "de": ["Unangemessenes Verhalten", "Zu viel Verspätung", "Profilabweichung", "Regelverstoß", "Sonstiges"],
        "ru": ["Неподобающее поведение", "Опоздание", "Несоответствие профилю", "Нарушение правил", "Другое"],
    },
    "btn_submit_rating": {
        "fa": "✅ ثبت امتیاز", "en": "✅ Submit Rating", "de": "✅ Bewertung abgeben", "ru": "✅ Отправить оценку",
    },
    "rating_saved": {
        "fa": "🌟 ممنون از نظرت!\n\n✅ {amount} به حساب @{nick} واریز شد",
        "en": "🌟 Thank you for your feedback!\n\n✅ {amount} transferred to @{nick}",
        "de": "🌟 Danke für dein Feedback!\n\n✅ {amount} an @{nick} überwiesen",
        "ru": "🌟 Спасибо за отзыв!\n\n✅ {amount} переведено на счёт @{nick}",
    },

    # ─── معرفی ───────────────────────────────────────
    "referral_title": {
        "fa": "🎁 *سیستم معرفی*\n\nکد تو: `{code}`\nلینک دعوت:\n{link}\n\nتعداد معرفی‌های موفق: {count}\nتخفیف فعلی تو: {disc}٪\n\n{tiers}",
        "en": "🎁 *Referral System*\n\nYour code: `{code}`\nInvite link:\n{link}\n\nSuccessful referrals: {count}\nYour current discount: {disc}%\n\n{tiers}",
        "de": "🎁 *Empfehlungssystem*\n\nDein Code: `{code}`\nEinladungslink:\n{link}\n\nErfolgreiche Empfehlungen: {count}\nDein aktueller Rabatt: {disc}%\n\n{tiers}",
        "ru": "🎁 *Реферальная система*\n\nВаш код: `{code}`\nПригласительная ссылка:\n{link}\n\nУспешных рефералов: {count}\nВаша скидка: {disc}%\n\n{tiers}",
    },

    # ─── قوانین ──────────────────────────────────────
    "rules_title": {
        "fa": "📜 *قوانین و مقررات Timely*",
        "en": "📜 *Timely Terms & Rules*",
        "de": "📜 *Timely Regeln & Bedingungen*",
        "ru": "📜 *Правила и условия Timely*",
    },
    "rules_body": {
        "fa": (
            "🚫 *ممنوعیت کار:* هیچ فعالیت کاری در این وقت مجاز نیست.\n\n"
            "🔒 *حریم خصوصی:* هویت واقعی محفوظ است.\n\n"
            "✅ *هویت واقعی:* ثبت‌نام با مشخصات واقعی الزامی است.\n\n"
            "💳 *پرداخت امن:* پول به Timely، پس از قرار موفق آزاد می‌شود.\n\n"
            "⏱ *لغو:* هر دو طرف تا ۱ ساعت قبل می‌توانند لغو کنند.\n\n"
            "⭐ *امتیاز:* پس از قرار موفق، امتیاز الزامی است.\n\n"
            "⚖️ *سوءاستفاده:* رفتار نامناسب → مسدود دائمی.\n\n"
            "💰 *کارمزد:* ۷۵٪ به فروشنده، ۲۵٪ کارمزد پلتفرم."
        ),
        "en": (
            "🚫 *No Work:* No professional or business activities allowed.\n\n"
            "🔒 *Privacy:* Real identity stays private.\n\n"
            "✅ *Real Identity:* Registration with real info required.\n\n"
            "💳 *Secure Payment:* Funds held by Timely, released after session.\n\n"
            "⏱ *Cancellation:* Either party can cancel up to 1 hour before.\n\n"
            "⭐ *Rating:* Rating required after every successful session.\n\n"
            "⚖️ *Abuse:* Misconduct → permanent ban.\n\n"
            "💰 *Fee:* 75% to seller, 25% platform fee."
        ),
        "de": (
            "🚫 *Keine Arbeit:* Keine beruflichen Aktivitäten erlaubt.\n\n"
            "🔒 *Datenschutz:* Echte Identität bleibt privat.\n\n"
            "✅ *Echte Identität:* Registrierung mit echten Daten erforderlich.\n\n"
            "💳 *Sichere Zahlung:* Geld bei Timely, nach Sitzung freigegeben.\n\n"
            "⏱ *Stornierung:* Beide Parteien können bis 1 Stunde vorher stornieren.\n\n"
            "⭐ *Bewertung:* Nach jeder Sitzung erforderlich.\n\n"
            "⚖️ *Missbrauch:* Fehlverhalten → permanente Sperrung.\n\n"
            "💰 *Gebühr:* 75% an Verkäufer, 25% Plattformgebühr."
        ),
        "ru": (
            "🚫 *Нет работе:* Никакой профессиональной деятельности.\n\n"
            "🔒 *Конфиденциальность:* Реальная личность защищена.\n\n"
            "✅ *Реальная личность:* Регистрация с реальными данными обязательна.\n\n"
            "💳 *Безопасная оплата:* Средства у Timely, освобождаются после встречи.\n\n"
            "⏱ *Отмена:* Любая сторона может отменить за 1 час до встречи.\n\n"
            "⭐ *Оценка:* Обязательна после каждой встречи.\n\n"
            "⚖️ *Злоупотребление:* Неподобающее поведение → постоянная блокировка.\n\n"
            "💰 *Комиссия:* 75% продавцу, 25% платформе."
        ),
    },

    # ─── خطاها ───────────────────────────────────────
    "error_generic": {
        "fa": "❌ خطایی رخ داد. دوباره امتحان کن.",
        "en": "❌ An error occurred. Please try again.",
        "de": "❌ Ein Fehler ist aufgetreten. Bitte versuche es erneut.",
        "ru": "❌ Произошла ошибка. Попробуйте ещё раз.",
    },
    "not_registered": {
        "fa": "ابتدا /start بزن.",
        "en": "Please start with /start first.",
        "de": "Bitte starte mit /start.",
        "ru": "Пожалуйста, начните с /start.",
    },
}


def t(key: str, lang: str = "fa", **kwargs) -> str:
    """
    ترجمه یه کلید به زبان مشخص
    مثال: t("welcome_back", "en", nick="@Roya", rating=4.9, count=34, balance="150,000", currency="T")
    """
    translations = TRANSLATIONS.get(key, {})
    text = translations.get(lang) or translations.get("en") or f"[{key}]"
    if kwargs:
        try:
            text = text.format(**kwargs)
        except KeyError:
            pass
    return text


def t_list(key: str, lang: str = "fa") -> list:
    """برای کلیدهایی که مقدارشون لیسته (مثل rate_labels)"""
    translations = TRANSLATIONS.get(key, {})
    return translations.get(lang) or translations.get("en") or []


def get_lang_name(lang: str) -> str:
    return LANGUAGES.get(lang, "🌍")


def is_rtl(lang: str) -> bool:
    return lang in RTL_LANGS
