"""
Timely Bot — ربات اصلی کاربران
هم برای خریداران (buyer) هم فروشندگان (seller)
"""
import os
import asyncio
import random
import string
from datetime import datetime, timedelta
from math import radians, cos, sin, asin, sqrt
from typing import Optional

from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup,
    KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
)
from telegram.ext import (
    Application, CommandHandler, MessageHandler, CallbackQueryHandler,
    ConversationHandler, ContextTypes, filters
)
from dotenv import load_dotenv

load_dotenv()
sys_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import sys; sys.path.insert(0, sys_path)
from database.db import *

# ─── States ──────────────────────────────────────
(
    REG_NAME, REG_GENDER, REG_BIRTHDATE, REG_CITY, REG_ROLE,
    REG_NICKNAME, REG_BIO, REG_PHOTO, REG_ACTIVITIES, REG_PET,
    REG_REFERRAL, REG_CONFIRM,
    SEARCH_GENDER, SEARCH_AGE, SEARCH_CITY, SEARCH_ACTIVITY, SEARCH_PET,
    BOOK_HOURS, BOOK_ACTIVITY, BOOK_DATE, BOOK_CONFIRM,
    RATE_STARS, RATE_REASONS, RATE_NOTE,
    GPS_TRACKING,
    SELLER_CONFIRM_BOOKING,
    REPORT_REASON,
) = range(27)

ACTIVITIES = {
    "🌿 طبیعت": ["پیاده‌روی", "کوهنوردی", "دوچرخه‌سواری", "پارک نشستن"],
    "🎭 فرهنگی": ["سینما", "موزه", "گالری", "تئاتر", "کتاب‌خوانی"],
    "☕ اجتماعی": ["کافه", "رستوران", "بازی فکری", "خرید"],
    "🧘 آرامش":  ["درد و دل", "مدیتیشن", "موسیقی", "نقاشی"],
}
ALL_ACTIVITIES = [a for acts in ACTIVITIES.values() for a in acts]
CITIES = ["تهران", "اصفهان", "شیراز", "مشهد", "تبریز", "کرج", "قم", "سایر"]

def gen_referral():
    return "TIM-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=6))

def haversine(lat1, lon1, lat2, lon2) -> float:
    """فاصله دو نقطه GPS به متر"""
    R = 6371000
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlon/2)**2
    return 2 * R * asin(sqrt(a))

def fmt(n: int) -> str:
    return f"{n:,}".replace(",", "٬")

def main_menu_keyboard(is_seller: bool = False) -> ReplyKeyboardMarkup:
    kb = [
        ["🔍 جستجوی همراه", "📅 ایونت‌ها"],
        ["📋 رزروهای من", "👤 پروفایل من"],
        ["🎁 کد معرفی", "📜 قوانین"],
    ]
    if is_seller:
        kb.insert(0, ["📨 درخواست‌های جدید", "💰 درآمدم"])
    return ReplyKeyboardMarkup(kb, resize_keyboard=True)

# ═══════════════════════════════════════════════
#  START / MAIN MENU
# ═══════════════════════════════════════════════

async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user = await get_user(update.effective_user.id)

    # بررسی referral code در لینک
    args = ctx.args
    if args and args[0].startswith("ref_"):
        ctx.user_data['referral_from'] = args[0][4:]

    if user and not user['is_banned']:
        await update.message.reply_text(
            f"👋 خوش برگشتی @{user['nickname']}!\n\n"
            f"⭐ امتیاز: {user['rating_avg']:.1f} ({user['rating_count']} نظر)\n"
            f"💰 کیف پول: {fmt(user['balance'])} تومان",
            reply_markup=main_menu_keyboard(user['is_seller'])
        )
        return ConversationHandler.END

    elif user and user['is_banned']:
        await update.message.reply_text(
            f"❌ حساب شما به دلیل تخلف مسدود شده است.\n"
            f"دلیل: {user['ban_reason']}"
        )
        return ConversationHandler.END

    else:
        await update.message.reply_text(
            "⏱ به *Timely* خوش آمدید!\n\n"
            "جایی که می‌تونی با آدم‌های واقعی وقت بگذرونی.\n\n"
            "برای شروع، اسم کاملت رو بنویس:",
            parse_mode="Markdown"
        )
        return REG_NAME

# ═══════════════════════════════════════════════
#  REGISTRATION FLOW
# ═══════════════════════════════════════════════

async def reg_name(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    name = update.message.text.strip()
    if len(name) < 2 or len(name) > 64:
        await update.message.reply_text("❌ اسم باید بین ۲ تا ۶۴ کاراکتر باشه.")
        return REG_NAME
    ctx.user_data['full_name'] = name
    kb = [["مرد", "زن"]]
    await update.message.reply_text(
        "جنسیتت رو انتخاب کن:",
        reply_markup=ReplyKeyboardMarkup(kb, resize_keyboard=True, one_time_keyboard=True)
    )
    return REG_GENDER

async def reg_gender(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    g = update.message.text.strip()
    if g not in ["مرد", "زن"]:
        await update.message.reply_text("❌ لطفاً از دکمه‌ها استفاده کن.")
        return REG_GENDER
    ctx.user_data['gender'] = "male" if g == "مرد" else "female"
    await update.message.reply_text(
        "تاریخ تولدت رو بنویس (مثال: 1375/03/15):",
        reply_markup=ReplyKeyboardRemove()
    )
    return REG_BIRTHDATE

async def reg_birthdate(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    try:
        parts = text.replace("-", "/").split("/")
        year, month, day = int(parts[0]), int(parts[1]), int(parts[2])
        # تبدیل تقریبی شمسی به میلادی
        if year > 1300:
            year -= 621
        birth = datetime(year, month, day)
        age = (datetime.now() - birth).days // 365
        if age < 18:
            await update.message.reply_text("❌ سن باید حداقل ۱۸ سال باشه.")
            return REG_BIRTHDATE
        ctx.user_data['birth_date'] = birth.date()
    except:
        await update.message.reply_text("❌ فرمت اشتباه. مثال: 1375/03/15")
        return REG_BIRTHDATE

    kb = [[c] for c in CITIES]
    await update.message.reply_text(
        "شهرت رو انتخاب کن:",
        reply_markup=ReplyKeyboardMarkup(kb, resize_keyboard=True, one_time_keyboard=True)
    )
    return REG_CITY

async def reg_city(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    ctx.user_data['city'] = update.message.text.strip()
    kb = [["فقط می‌خرم ⬅️", "وقتم رو می‌فروشم ➡️"], ["هر دو 🔄"]]
    await update.message.reply_text(
        "می‌خوای وقت بخری یا بفروشی؟",
        reply_markup=ReplyKeyboardMarkup(kb, resize_keyboard=True, one_time_keyboard=True)
    )
    return REG_ROLE

async def reg_role(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    ctx.user_data['is_seller'] = "فروش" in text or "هر دو" in text
    await update.message.reply_text(
        "یه نیک‌نیم منحصربه‌فرد انتخاب کن (این نام عمومیه):\n"
        "فقط حروف انگلیسی، عدد و آندرلاین مجاز است.",
        reply_markup=ReplyKeyboardRemove()
    )
    return REG_NICKNAME

async def reg_nickname(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    nick = update.message.text.strip()
    if not nick.replace("_", "").isalnum() or len(nick) < 3 or len(nick) > 24:
        await update.message.reply_text("❌ نیک‌نیم باید ۳-۲۴ کاراکتر، فقط a-z, 0-9, _ باشه.")
        return REG_NICKNAME
    # بررسی تکراری نبودن (در محیط واقعی با دیتابیس)
    ctx.user_data['nickname'] = nick
    await update.message.reply_text("یه بیو کوتاه درباره خودت بنویس:")
    return REG_BIO

async def reg_bio(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    ctx.user_data['bio'] = update.message.text.strip()[:256]
    await update.message.reply_text("عکس پروفایلت رو بفرست (یا /skip برای رد کردن):")
    return REG_PHOTO

async def reg_photo(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if update.message.photo:
        ctx.user_data['avatar_file_id'] = update.message.photo[-1].file_id
    
    # انتخاب فعالیت‌ها (فقط برای فروشنده)
    if ctx.user_data.get('is_seller'):
        kb = []
        for cat, acts in ACTIVITIES.items():
            kb.append([cat])
            kb.append([f"✓ {a}" for a in acts[:2]] + [f"✓ {a}" for a in acts[2:]])
        
        ctx.user_data['selected_activities'] = []
        buttons = []
        for cat, acts in ACTIVITIES.items():
            buttons.append([InlineKeyboardButton(f"━━ {cat} ━━", callback_data="cat_header")])
            row = []
            for a in acts:
                row.append(InlineKeyboardButton(a, callback_data=f"act_{a}"))
                if len(row) == 2:
                    buttons.append(row); row = []
            if row: buttons.append(row)
        buttons.append([InlineKeyboardButton("✅ تأیید", callback_data="act_done")])
        
        await update.message.reply_text(
            "فعالیت‌هایی که می‌تونی انجام بدی رو انتخاب کن:",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
        return REG_ACTIVITIES
    else:
        return await _ask_referral(update, ctx)

async def reg_activities_cb(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    data = q.data

    if data == "cat_header":
        return REG_ACTIVITIES
    
    if data == "act_done":
        if not ctx.user_data.get('selected_activities'):
            await q.answer("❌ حداقل یه فعالیت انتخاب کن!", show_alert=True)
            return REG_ACTIVITIES
        
        kb = [["بله 🐾 قبول می‌کنم", "نه ❌"]]
        await q.message.reply_text(
            "آیا با همراه داشتن حیوان خانگی مشکلی داری؟",
            reply_markup=ReplyKeyboardMarkup(kb, resize_keyboard=True, one_time_keyboard=True)
        )
        return REG_PET

    act = data[4:]
    selected = ctx.user_data.get('selected_activities', [])
    if act in selected:
        selected.remove(act)
    else:
        selected.append(act)
    ctx.user_data['selected_activities'] = selected

    # بروزرسانی دکمه‌ها
    buttons = []
    for cat, acts in ACTIVITIES.items():
        buttons.append([InlineKeyboardButton(f"━━ {cat} ━━", callback_data="cat_header")])
        row = []
        for a in acts:
            label = f"✅ {a}" if a in selected else a
            row.append(InlineKeyboardButton(label, callback_data=f"act_{a}"))
            if len(row) == 2:
                buttons.append(row); row = []
        if row: buttons.append(row)
    buttons.append([InlineKeyboardButton(f"✅ تأیید ({len(selected)} مورد)", callback_data="act_done")])
    
    await q.edit_message_reply_markup(InlineKeyboardMarkup(buttons))
    return REG_ACTIVITIES

async def reg_pet(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    ctx.user_data['pet_friendly'] = "بله" in update.message.text
    return await _ask_referral(update, ctx)

async def _ask_referral(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "اگه کد دعوت داری وارد کن (یا /skip):",
        reply_markup=ReplyKeyboardRemove()
    )
    return REG_REFERRAL

async def reg_referral(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    code = update.message.text.strip() if update.message.text != "/skip" else None
    ctx.user_data['referral_code_entered'] = code
    return await reg_confirm(update, ctx)

async def reg_confirm(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    d = ctx.user_data
    role = "فروشنده + خریدار" if d.get('is_seller') else "خریدار"
    text = (
        f"✅ *اطلاعات ثبت‌نام:*\n\n"
        f"👤 اسم: {d.get('full_name')}\n"
        f"🏷 نیک‌نیم: @{d.get('nickname')}\n"
        f"📍 شهر: {d.get('city')}\n"
        f"🎭 نقش: {role}\n\n"
        f"آیا تأیید می‌کنی؟"
    )
    kb = [["✅ بله، ثبت‌نام کن", "❌ از اول"]]
    await update.message.reply_text(
        text, parse_mode="Markdown",
        reply_markup=ReplyKeyboardMarkup(kb, resize_keyboard=True, one_time_keyboard=True)
    )
    return REG_CONFIRM

async def reg_save(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if "از اول" in update.message.text:
        await start(update, ctx)
        return REG_NAME

    tg_user = update.effective_user
    d = ctx.user_data

    try:
        user = await create_user({
            'telegram_id': tg_user.id,
            'telegram_username': tg_user.username,
            'nickname': d['nickname'],
            'full_name': d['full_name'],
            'gender': d['gender'],
            'birth_date': d['birth_date'],
            'city': d['city'],
            'bio': d.get('bio', ''),
            'is_seller': d.get('is_seller', False),
            'pet_friendly': d.get('pet_friendly', False),
            'referral_code': gen_referral(),
            'referred_by': None  # در واقعیت: جستجو بر اساس کد دعوت
        })

        await update.message.reply_text(
            f"🎉 *ثبت‌نام موفق!*\n\n"
            f"خوش اومدی به Timely @{user['nickname']}!\n\n"
            f"{'⚠️ برای فعال شدن پروفایل فروشنده، هویتت توسط ادمین تأیید می‌شه.' if d.get('is_seller') else ''}",
            parse_mode="Markdown",
            reply_markup=main_menu_keyboard(d.get('is_seller', False))
        )
    except Exception as e:
        await update.message.reply_text(f"❌ خطا در ثبت‌نام. دوباره /start بزن.")

    return ConversationHandler.END

# ═══════════════════════════════════════════════
#  SEARCH
# ═══════════════════════════════════════════════

async def search_start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    ctx.user_data['search'] = {}
    kb = [["مرد", "زن", "همه"]]
    await update.message.reply_text(
        "🔍 جستجوی همراه\n\nجنسیت:",
        reply_markup=ReplyKeyboardMarkup(kb, resize_keyboard=True, one_time_keyboard=True)
    )
    return SEARCH_GENDER

async def search_gender(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    g = update.message.text
    ctx.user_data['search']['gender'] = None if g == "همه" else ("male" if g == "مرد" else "female")
    await update.message.reply_text(
        "محدوده سنی (مثال: 20-35 یا /skip):",
        reply_markup=ReplyKeyboardRemove()
    )
    return SEARCH_AGE

async def search_age(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text != "/skip":
        try:
            parts = text.replace(" ", "").split("-")
            ctx.user_data['search']['min_age'] = int(parts[0])
            ctx.user_data['search']['max_age'] = int(parts[1])
        except:
            await update.message.reply_text("❌ فرمت اشتباه. مثال: 20-35")
            return SEARCH_AGE

    kb = [[c] for c in CITIES] + [["/skip"]]
    await update.message.reply_text(
        "شهر:", reply_markup=ReplyKeyboardMarkup(kb, resize_keyboard=True, one_time_keyboard=True)
    )
    return SEARCH_CITY

async def search_city(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    ctx.user_data['search']['city'] = None if text == "/skip" else text

    buttons = []
    for cat, acts in ACTIVITIES.items():
        buttons.append([InlineKeyboardButton(f"━ {cat} ━", callback_data="s_header")])
        row = []
        for a in acts:
            row.append(InlineKeyboardButton(a, callback_data=f"s_act_{a}"))
            if len(row) == 2: buttons.append(row); row = []
        if row: buttons.append(row)
    buttons.append([InlineKeyboardButton("همه فعالیت‌ها", callback_data="s_act_all")])

    await update.message.reply_text(
        "فعالیت مورد نظر:", reply_markup=InlineKeyboardMarkup(buttons)
    )
    return SEARCH_ACTIVITY

async def search_activity_cb(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    data = q.data
    if data == "s_header": return SEARCH_ACTIVITY

    ctx.user_data['search']['activity'] = None if data == "s_act_all" else data[6:]

    kb = [["بله 🐾 (فقط pet-friendly)", "نه، فرقی نمی‌کنه"]]
    await q.message.reply_text(
        "حیوان خانگی همراه داری؟",
        reply_markup=ReplyKeyboardMarkup(kb, resize_keyboard=True, one_time_keyboard=True)
    )
    return SEARCH_PET

async def search_pet(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    ctx.user_data['search']['pet_friendly'] = "بله" in update.message.text
    return await do_search(update, ctx)

async def do_search(update: Update, ctx: ContextTypes.DEFAULT_TYPE, page: int = 0):
    s = ctx.user_data.get('search', {})
    results = await search_sellers(
        city=s.get('city'),
        gender=s.get('gender'),
        min_age=s.get('min_age', 18),
        max_age=s.get('max_age', 60),
        activity=s.get('activity'),
        pet_friendly=s.get('pet_friendly', False),
        limit=5, offset=page * 5
    )

    if not results:
        await update.message.reply_text(
            "😔 هیچ همراهی با این مشخصات پیدا نشد.\n"
            "فیلترها رو تغییر بده.",
            reply_markup=main_menu_keyboard()
        )
        return ConversationHandler.END

    for p in results:
        acts = p.get('activities') or []
        age = (datetime.now().date() - p['birth_date']).days // 365 if p.get('birth_date') else "؟"
        text = (
            f"{'🟢' if p['is_verified'] else '⚪'} *@{p['nickname']}*"
            f"{'  🐾' if p['pet_friendly'] else ''}\n"
            f"{'👩' if p['gender']=='female' else '👨'} {age} ساله | 📍 {p['city']}\n"
            f"⭐ {p['rating_avg']:.1f} ({p['rating_count']} نظر)\n"
            f"💰 {fmt(p['price_per_hour'])} ت/ساعت\n\n"
            f"📝 {p['bio']}\n\n"
            f"🎯 {' · '.join((acts or [])[:4])}"
        )
        kb = [[InlineKeyboardButton(f"📅 رزرو @{p['nickname']}", callback_data=f"book_{p['id']}")]]
        await update.message.reply_text(
            text, parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(kb)
        )

    if len(results) == 5:
        kb = [[InlineKeyboardButton("➡️ صفحه بعد", callback_data=f"search_page_{page+1}")]]
        await update.message.reply_text(
            "نتایج بیشتر:", reply_markup=InlineKeyboardMarkup(kb)
        )

    return ConversationHandler.END

# ═══════════════════════════════════════════════
#  BOOKING FLOW
# ═══════════════════════════════════════════════

async def book_start_cb(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    seller_id = int(q.data.split("_")[1])
    ctx.user_data['booking'] = {'seller_db_id': seller_id}

    # دریافت فعالیت‌های فروشنده
    pool = await get_pool()
    import asyncpg
    async with (await get_pool()).acquire() as conn:
        acts = await conn.fetch("SELECT activity FROM user_activities WHERE user_id = $1", seller_id)

    buttons = [[InlineKeyboardButton(r['activity'], callback_data=f"bact_{r['activity']}")] for r in acts]
    await q.message.reply_text("فعالیت رو انتخاب کن:", reply_markup=InlineKeyboardMarkup(buttons))
    return BOOK_ACTIVITY

async def book_activity_cb(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    ctx.user_data['booking']['activity'] = q.data[5:]

    kb = [[str(h) for h in range(1, 4)], [str(h) for h in range(4, 7)]]
    await q.message.reply_text(
        "چند ساعت؟",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(f"{h} ساعت", callback_data=f"bhr_{h}")] for h in range(1,7)]
        )
    )
    return BOOK_HOURS

async def book_hours_cb(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    ctx.user_data['booking']['hours'] = int(q.data[4:])
    await q.message.reply_text(
        "تاریخ و ساعت پیشنهادی قرار رو بنویس:\n(مثال: فردا ساعت ۱۸ یا 1403/03/20 18:00)",
        reply_markup=ReplyKeyboardRemove()
    )
    return BOOK_DATE

async def book_date(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    ctx.user_data['booking']['date_text'] = update.message.text.strip()

    b = ctx.user_data['booking']
    buyer = await get_user(update.effective_user.id)
    
    # دریافت اطلاعات فروشنده
    async with (await get_pool()).acquire() as conn:
        seller = await conn.fetchrow("SELECT * FROM users WHERE id = $1", b['seller_db_id'])
    
    total = b['hours'] * seller['price_per_hour']
    disc = buyer.get('discount_pct', 0)
    final = int(total * (1 - disc / 100))
    fee = int(final * 0.25)
    seller_gets = final - fee

    text = (
        f"📋 *خلاصه رزرو:*\n\n"
        f"👤 همراه: @{seller['nickname']}\n"
        f"🎯 فعالیت: {b['activity']}\n"
        f"⏱ مدت: {b['hours']} ساعت\n"
        f"📅 زمان: {b['date_text']}\n\n"
        f"💵 مبلغ: {fmt(total)} تومان\n"
        + (f"✂️ تخفیف ({disc}٪): -{fmt(total-final)} تومان\n" if disc else "")
        + f"💳 *مبلغ نهایی: {fmt(final)} تومان*\n\n"
        f"⚠️ پس از تأیید فروشنده، پرداخت انجام می‌شه."
    )
    ctx.user_data['booking']['total'] = final
    ctx.user_data['booking']['seller_tg'] = seller['telegram_id']
    ctx.user_data['booking']['seller_nick'] = seller['nickname']

    kb = [["✅ ارسال درخواست", "❌ انصراف"]]
    await update.message.reply_text(
        text, parse_mode="Markdown",
        reply_markup=ReplyKeyboardMarkup(kb, resize_keyboard=True, one_time_keyboard=True)
    )
    return BOOK_CONFIRM

async def book_confirm(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if "انصراف" in update.message.text:
        await update.message.reply_text("❌ رزرو لغو شد.", reply_markup=main_menu_keyboard())
        return ConversationHandler.END

    b = ctx.user_data['booking']
    buyer = await get_user(update.effective_user.id)
    
    async with (await get_pool()).acquire() as conn:
        seller = await conn.fetchrow("SELECT * FROM users WHERE id = $1", b['seller_db_id'])

    booking = await create_booking({
        'buyer_id': buyer['id'],
        'seller_id': b['seller_db_id'],
        'activity': b['activity'],
        'hours': b['hours'],
        'price_per_hour': seller['price_per_hour'],
        'discount_pct': buyer.get('discount_pct', 0),
    })

    # اطلاع‌رسانی به خریدار
    await update.message.reply_text(
        f"📨 درخواست ارسال شد!\n\n"
        f"منتظر تأیید @{seller['nickname']} بمون.\n"
        f"شماره رزرو: #{booking['id']}",
        reply_markup=main_menu_keyboard(buyer['is_seller'])
    )

    # اطلاع‌رسانی به فروشنده
    kb = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ قبول می‌کنم", callback_data=f"sconf_y_{booking['id']}"),
            InlineKeyboardButton("❌ رد می‌کنم", callback_data=f"sconf_n_{booking['id']}")
        ]
    ])
    try:
        await ctx.bot.send_message(
            chat_id=seller['telegram_id'],
            text=(
                f"📨 *درخواست رزرو جدید!*\n\n"
                f"👤 از: @{buyer['nickname']}\n"
                f"🎯 فعالیت: {b['activity']}\n"
                f"⏱ {b['hours']} ساعت\n"
                f"📅 {b.get('date_text', 'نامشخص')}\n"
                f"💰 {fmt(booking['seller_amount'])} تومان (سهم تو)\n\n"
                f"تا ۲۴ ساعت وقت داری."
            ),
            parse_mode="Markdown",
            reply_markup=kb
        )
    except:
        pass

    return ConversationHandler.END

# ─── Seller confirms/rejects booking ─────────────

async def seller_confirm_cb(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    parts = q.data.split("_")
    decision = parts[1]  # y or n
    booking_id = int(parts[2])

    booking = await get_booking(booking_id)
    if not booking:
        await q.edit_message_text("❌ رزرو پیدا نشد.")
        return

    if decision == "y":
        await update_booking_status(booking_id, "confirmed")
        await q.edit_message_text(f"✅ درخواست #{booking_id} تأیید شد!")

        # اطلاع‌رسانی به خریدار
        pay_kb = InlineKeyboardMarkup([[
            InlineKeyboardButton(
                f"💳 پرداخت {fmt(booking['total_amount'])} تومان",
                callback_data=f"pay_{booking_id}"
            )
        ]])
        try:
            await ctx.bot.send_message(
                chat_id=booking['buyer_tg'],
                text=(
                    f"✅ *@{booking['seller_nick']} درخواستت رو تأیید کرد!*\n\n"
                    f"مبلغ {fmt(booking['total_amount'])} تومان رو پرداخت کن."
                ),
                parse_mode="Markdown",
                reply_markup=pay_kb
            )
        except:
            pass
    else:
        await update_booking_status(booking_id, "cancelled", cancelled_by=booking['seller_id'])
        await q.edit_message_text(f"❌ درخواست #{booking_id} رد شد.")
        try:
            await ctx.bot.send_message(
                chat_id=booking['buyer_tg'],
                text=f"❌ متأسفانه @{booking['seller_nick']} درخواستت رو رد کرد."
            )
        except:
            pass

# ─── Payment (شبیه‌سازی) ──────────────────────────

async def payment_cb(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    booking_id = int(q.data.split("_")[1])
    booking = await get_booking(booking_id)

    # در واقعیت: ریدایرکت به درگاه زرین‌پال
    # اینجا شبیه‌سازی پرداخت موفق
    await update_booking_status(booking_id, "paid")
    await q.edit_message_text(
        f"✅ *پرداخت موفق!*\n\n"
        f"مبلغ {fmt(booking['total_amount'])} تومان دریافت شد.\n"
        f"شماره پیگیری: TIM{booking_id:08d}\n\n"
        f"حالا وقتی کنار @{booking['seller_nick']} قرار گرفتی،\n"
        f"دکمه 📍 *شروع GPS* رو بزن.",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("📍 شروع GPS", callback_data=f"gps_start_{booking_id}")
        ]])
    )

# ─── GPS Tracking ──────────────────────────────

async def gps_start_cb(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    booking_id = int(q.data.split("_")[2])

    kb = ReplyKeyboardMarkup(
        [[KeyboardButton("📍 ارسال موقعیت", request_location=True)]],
        resize_keyboard=True, one_time_keyboard=False
    )
    ctx.user_data['gps_booking_id'] = booking_id
    await update_booking_status(booking_id, "gps_waiting")
    await q.message.reply_text(
        "📍 دکمه زیر رو بزن تا موقعیتت ارسال بشه.\n"
        "وقتی هر دو در فاصله ۵۰ متری باشید، تایمر شروع می‌شه!",
        reply_markup=kb
    )

async def gps_location(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    loc = update.message.location
    booking_id = ctx.user_data.get('gps_booking_id')
    if not booking_id:
        return

    user = await get_user(update.effective_user.id)
    booking = await get_booking(booking_id)
    if not booking:
        return

    # تشخیص نقش
    user_type = "buyer" if user['id'] == booking['buyer_id'] else "seller"
    session = await update_gps(booking_id, user_type, loc.latitude, loc.longitude)

    if not session:
        return

    # بررسی فاصله
    if (session.get('buyer_lat') and session.get('seller_lat')):
        dist = haversine(
            session['buyer_lat'], session['buyer_lng'],
            session['seller_lat'], session['seller_lng']
        )
        dist_int = int(dist)

        if dist_int <= 50 and not session.get('proximity_hit'):
            # شروع تایمر!
            await update_booking_status(booking_id, "in_progress", started_at=datetime.now())
            for tg_id in [booking['buyer_tg'], booking['seller_tg']]:
                try:
                    await ctx.bot.send_message(
                        tg_id,
                        f"🟢 *تایمر شروع شد!*\n\n"
                        f"⏱ {booking['hours']} ساعت شروع شد.\n"
                        f"وقتی تموم شد، دکمه ⏹ پایان رو بزن.",
                        parse_mode="Markdown",
                        reply_markup=InlineKeyboardMarkup([[
                            InlineKeyboardButton("⏹ پایان قرار", callback_data=f"end_booking_{booking_id}")
                        ]])
                    )
                except:
                    pass
        else:
            await update.message.reply_text(
                f"📍 فاصله تا همراهت: *{dist_int} متر*\n"
                f"{'✅ نزدیک شدی!' if dist_int < 200 else '🚶 در راهه...'}",
                parse_mode="Markdown"
            )

async def end_booking_cb(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    booking_id = int(q.data.split("_")[2])
    booking = await get_booking(booking_id)

    await update_booking_status(booking_id, "completed", ended_at=datetime.now())
    # آزاد کردن پول (در واقعیت: انتقال به حساب فروشنده)

    for tg_id, nick in [(booking['buyer_tg'], booking['seller_nick'])]:
        try:
            await ctx.bot.send_message(
                tg_id,
                f"🎉 *قرار با موفقیت انجام شد!*\n\n"
                f"حالا @{nick} رو امتیاز بده 👇",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton(f"{s}⭐", callback_data=f"rate_{booking_id}_{s}")
                    for s in range(1, 6)
                ]])
            )
        except:
            pass

    await q.edit_message_text("✅ قرار ثبت شد.")

# ─── Rating ──────────────────────────────────────

async def rate_cb(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    _, booking_id, stars = q.data.split("_")
    booking_id, stars = int(booking_id), int(stars)
    ctx.user_data['rating'] = {'booking_id': booking_id, 'stars': stars}

    if stars < 4:
        reasons = ["رفتار نامناسب","دیر کردن زیاد","عدم تطابق پروفایل","عدم رعایت قوانین","سایر"]
        ctx.user_data['rating']['selected_reasons'] = []
        kb = [[InlineKeyboardButton(r, callback_data=f"reason_{r}")] for r in reasons]
        kb.append([InlineKeyboardButton("✅ ثبت", callback_data="reason_done")])
        await q.edit_message_text(
            f"{'⭐'*stars} امتیاز ثبت شد.\n\n⚠️ دلیل نارضایتی رو انتخاب کن:",
            reply_markup=InlineKeyboardMarkup(kb)
        )
        return RATE_REASONS
    else:
        await _save_rating(q, ctx, stars, [], None)
        return ConversationHandler.END

async def rate_reason_cb(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    if q.data == "reason_done":
        reasons = ctx.user_data['rating'].get('selected_reasons', [])
        if not reasons:
            await q.answer("❌ حداقل یه دلیل انتخاب کن!", show_alert=True)
            return RATE_REASONS
        await _save_rating(q, ctx, ctx.user_data['rating']['stars'], reasons, None)
        return ConversationHandler.END

    reason = q.data[7:]
    selected = ctx.user_data['rating'].get('selected_reasons', [])
    if reason in selected:
        selected.remove(reason)
    else:
        selected.append(reason)
    ctx.user_data['rating']['selected_reasons'] = selected
    await q.answer(f"{'✅' if reason in selected else '❌'} {reason}")
    return RATE_REASONS

async def _save_rating(q, ctx, stars, reasons, note):
    r = ctx.user_data['rating']
    booking = await get_booking(r['booking_id'])
    rater = await get_user(q.from_user.id)
    rated_id = booking['seller_id'] if rater['id'] == booking['buyer_id'] else booking['buyer_id']

    await create_rating(r['booking_id'], rater['id'], rated_id, stars, reasons, note)
    label = ["","خیلی بد 😞","بد 😕","متوسط 😐","خوب 😊","عالی 🤩"][stars]
    await q.edit_message_text(f"{'⭐'*stars} {label}\nامتیاز ثبت شد. ممنون! 🙏")

# ─── My bookings ────────────────────────────────

async def my_bookings(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user = await get_user(update.effective_user.id)
    if not user:
        await update.message.reply_text("ابتدا /start بزن.")
        return

    bookings = await get_user_bookings(update.effective_user.id, "buyer")
    if not bookings:
        await update.message.reply_text("هنوز رزروی نداری.")
        return

    status_fa = {
        'pending': '⏳ منتظر تأیید', 'confirmed': '✅ تأیید شده',
        'paid': '💳 پرداخت شده', 'in_progress': '🟢 در حال انجام',
        'completed': '🎉 انجام شد', 'cancelled': '❌ لغو شده',
    }
    text = "📋 *رزروهای من:*\n\n"
    for b in bookings:
        text += (
            f"#{b['id']} — @{b['seller_nick']}\n"
            f"🎯 {b['activity']} | ⏱ {b['hours']}ساعت\n"
            f"💰 {fmt(b['total_amount'])} ت | {status_fa.get(b['status'], b['status'])}\n\n"
        )
    await update.message.reply_text(text, parse_mode="Markdown")

# ─── Referral ────────────────────────────────────

async def referral_info(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user = await get_user(update.effective_user.id)
    if not user:
        return
    code = user['referral_code']
    count = user['referral_count']
    disc = user['discount_pct']
    bot_username = (await ctx.bot.get_me()).username
    link = f"https://t.me/{bot_username}?start=ref_{code}"

    tiers = [(1,10),(3,25),(5,40),(10,50)]
    tier_text = ""
    for n, d in tiers:
        mark = "✅" if count >= n else "⬜"
        tier_text += f"{mark} {n} معرفی → {d}٪ تخفیف\n"

    await update.message.reply_text(
        f"🎁 *سیستم معرفی*\n\n"
        f"کد تو: `{code}`\n"
        f"لینک دعوت:\n{link}\n\n"
        f"تعداد معرفی‌های موفق: {count}\n"
        f"تخفیف فعلی تو: {disc}٪\n\n"
        f"{tier_text}",
        parse_mode="Markdown"
    )

# ─── Main ────────────────────────────────────────

def build_user_bot() -> Application:
    app = Application.builder().token(os.getenv("BOT_TOKEN")).build()

    # Registration conversation
    reg_conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            REG_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, reg_name)],
            REG_GENDER: [MessageHandler(filters.TEXT, reg_gender)],
            REG_BIRTHDATE: [MessageHandler(filters.TEXT, reg_birthdate)],
            REG_CITY: [MessageHandler(filters.TEXT, reg_city)],
            REG_ROLE: [MessageHandler(filters.TEXT, reg_role)],
            REG_NICKNAME: [MessageHandler(filters.TEXT, reg_nickname)],
            REG_BIO: [MessageHandler(filters.TEXT, reg_bio)],
            REG_PHOTO: [
                MessageHandler(filters.PHOTO, reg_photo),
                CommandHandler("skip", reg_photo),
            ],
            REG_ACTIVITIES: [CallbackQueryHandler(reg_activities_cb, pattern="^act_")],
            REG_PET: [MessageHandler(filters.TEXT, reg_pet)],
            REG_REFERRAL: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, reg_referral),
                CommandHandler("skip", reg_referral),
            ],
            REG_CONFIRM: [MessageHandler(filters.TEXT, reg_save)],
        },
        fallbacks=[CommandHandler("start", start)],
        per_message=False,
    )

    # Search conversation
    search_conv = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("🔍 جستجوی همراه"), search_start)],
        states={
            SEARCH_GENDER: [MessageHandler(filters.TEXT, search_gender)],
            SEARCH_AGE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, search_age),
                CommandHandler("skip", search_age),
            ],
            SEARCH_CITY: [MessageHandler(filters.TEXT, search_city)],
            SEARCH_ACTIVITY: [CallbackQueryHandler(search_activity_cb, pattern="^s_")],
            SEARCH_PET: [MessageHandler(filters.TEXT, search_pet)],
        },
        fallbacks=[],
    )

    # Booking conversation
    book_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(book_start_cb, pattern="^book_")],
        states={
            BOOK_ACTIVITY: [CallbackQueryHandler(book_activity_cb, pattern="^bact_")],
            BOOK_HOURS: [CallbackQueryHandler(book_hours_cb, pattern="^bhr_")],
            BOOK_DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, book_date)],
            BOOK_CONFIRM: [MessageHandler(filters.TEXT, book_confirm)],
        },
        fallbacks=[],
    )

    # Rating
    rate_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(rate_cb, pattern="^rate_")],
        states={
            RATE_REASONS: [CallbackQueryHandler(rate_reason_cb, pattern="^reason_")],
        },
        fallbacks=[],
    )

    app.add_handler(reg_conv)
    app.add_handler(search_conv)
    app.add_handler(book_conv)
    app.add_handler(rate_conv)
    app.add_handler(CallbackQueryHandler(seller_confirm_cb, pattern="^sconf_"))
    app.add_handler(CallbackQueryHandler(payment_cb, pattern="^pay_"))
    app.add_handler(CallbackQueryHandler(gps_start_cb, pattern="^gps_start_"))
    app.add_handler(CallbackQueryHandler(end_booking_cb, pattern="^end_booking_"))
    app.add_handler(MessageHandler(filters.LOCATION, gps_location))
    app.add_handler(MessageHandler(filters.Regex("📋 رزروهای من"), my_bookings))
    app.add_handler(MessageHandler(filters.Regex("🎁 کد معرفی"), referral_info))

    return app

if __name__ == "__main__":
    app = build_user_bot()
    print("✅ Timely User Bot started...")
    app.run_polling()
