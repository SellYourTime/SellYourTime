"""
Timely Bot — ربات ادمین
پنل مدیریت کامل پلتفرم
"""
import os
import sys
from datetime import datetime
from typing import Optional

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, ConversationHandler, ContextTypes, filters
)
from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.db import *

ADMIN_IDS = [int(x) for x in os.getenv("ADMIN_CHAT_IDS", "0").split(",")]

def fmt(n) -> str:
    return f"{int(n):,}".replace(",", "٬")

def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS

# ─── States ───
BAN_REASON, VERIFY_USER, REJECT_REASON, BROADCAST_TEXT, EVENT_DECISION = range(5)

# ═══════════════════════════════════════════════
#  GUARD
# ═══════════════════════════════════════════════

async def admin_guard(update: Update) -> bool:
    if not is_admin(update.effective_user.id):
        await update.effective_message.reply_text("⛔ دسترسی ندارید.")
        return False
    return True

# ═══════════════════════════════════════════════
#  MAIN MENU
# ═══════════════════════════════════════════════

ADMIN_MENU = InlineKeyboardMarkup([
    [InlineKeyboardButton("📊 آمار کلی", callback_data="adm_stats"),
     InlineKeyboardButton("👥 کاربران", callback_data="adm_users")],
    [InlineKeyboardButton("✅ تأیید فروشنده", callback_data="adm_verify"),
     InlineKeyboardButton("📋 رزروها", callback_data="adm_bookings")],
    [InlineKeyboardButton("🎭 ایونت‌های گروهی", callback_data="adm_events"),
     InlineKeyboardButton("🚨 گزارش‌ها", callback_data="adm_reports")],
    [InlineKeyboardButton("📢 ارسال پیام همگانی", callback_data="adm_broadcast"),
     InlineKeyboardButton("💰 مالی", callback_data="adm_finance")],
])

async def admin_start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not await admin_guard(update): return
    await update.message.reply_text(
        "🛠 *پنل ادمین Timely*\n\nیه بخش رو انتخاب کن:",
        parse_mode="Markdown",
        reply_markup=ADMIN_MENU
    )

async def back_to_menu(q, text="پنل ادمین"):
    await q.edit_message_text(
        f"🛠 *{text}*\n\nیه بخش رو انتخاب کن:",
        parse_mode="Markdown",
        reply_markup=ADMIN_MENU
    )

# ═══════════════════════════════════════════════
#  STATS
# ═══════════════════════════════════════════════

async def adm_stats_cb(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    if not is_admin(q.from_user.id): return

    stats = await get_platform_stats()
    text = (
        f"📊 *آمار کلی پلتفرم*\n\n"
        f"👥 کاربران فعال: {fmt(stats['total_users'])}\n"
        f"🧑‍💼 فروشندگان فعال: {fmt(stats['active_sellers'])}\n"
        f"✅ رزروهای کامل‌شده: {fmt(stats['completed_bookings'])}\n"
        f"🟢 رزروهای جاری: {fmt(stats['active_bookings'])}\n"
        f"💰 درآمد کل پلتفرم: {fmt(stats['total_revenue'])} ت\n"
        f"🚨 گزارش‌های باز: {fmt(stats['open_reports'])}\n"
        f"📋 ایونت‌های در انتظار: {fmt(stats['pending_events'])}\n\n"
        f"🕐 آخرین بروزرسانی: {datetime.now().strftime('%H:%M')}"
    )
    kb = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 بازگشت", callback_data="adm_back")]])
    await q.edit_message_text(text, parse_mode="Markdown", reply_markup=kb)

# ═══════════════════════════════════════════════
#  USER MANAGEMENT
# ═══════════════════════════════════════════════

async def adm_users_cb(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔍 جستجوی کاربر", callback_data="adm_user_search"),
         InlineKeyboardButton("🚫 مسدودها", callback_data="adm_user_banned")],
        [InlineKeyboardButton("📊 فروشندگان برتر", callback_data="adm_top_sellers")],
        [InlineKeyboardButton("🔙 بازگشت", callback_data="adm_back")],
    ])
    await q.edit_message_text("👥 *مدیریت کاربران*", parse_mode="Markdown", reply_markup=kb)

async def adm_user_info(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    """دستور: /user <telegram_id>"""
    if not await admin_guard(update): return
    args = update.message.text.split()
    if len(args) < 2:
        await update.message.reply_text("استفاده: /user <telegram_id>")
        return

    try:
        tg_id = int(args[1])
    except:
        await update.message.reply_text("❌ ID معتبر نیست.")
        return

    user = await get_user(tg_id)
    if not user:
        await update.message.reply_text("❌ کاربر پیدا نشد.")
        return

    age = (datetime.now().date() - user['birth_date']).days // 365 if user.get('birth_date') else "؟"
    text = (
        f"👤 *اطلاعات کاربر*\n\n"
        f"🆔 Telegram ID: `{user['telegram_id']}`\n"
        f"🏷 نیک‌نیم: @{user['nickname']}\n"
        f"👤 اسم: {user['full_name']}\n"
        f"📍 شهر: {user['city']}\n"
        f"🎂 سن: {age} سال\n"
        f"⭐ امتیاز: {user['rating_avg']:.1f} ({user['rating_count']} نظر)\n"
        f"💰 کیف پول: {fmt(user['balance'])} ت\n"
        f"🎭 نقش: {'فروشنده' if user['is_seller'] else 'خریدار'}\n"
        f"✅ تأیید: {'بله' if user['is_verified'] else 'خیر'}\n"
        f"🚫 مسدود: {'بله ⚠️' if user['is_banned'] else 'خیر'}\n"
        f"📅 عضویت: {user['created_at'].strftime('%Y/%m/%d') if user.get('created_at') else '؟'}"
    )
    kb = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ تأیید هویت", callback_data=f"verify_{tg_id}"),
            InlineKeyboardButton("🚫 مسدود کردن", callback_data=f"ban_{tg_id}"),
        ],
        [InlineKeyboardButton("📋 رزروهای کاربر", callback_data=f"ubookings_{tg_id}")],
    ])
    await update.message.reply_text(text, parse_mode="Markdown", reply_markup=kb)

# ═══════════════════════════════════════════════
#  SELLER VERIFICATION
# ═══════════════════════════════════════════════

async def adm_verify_list_cb(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    pending = await get_pending_verifications()
    if not pending:
        await q.edit_message_text(
            "✅ هیچ درخواست تأیید معلقی وجود ندارد.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 بازگشت", callback_data="adm_back")]])
        )
        return

    for u in pending[:5]:
        age = (datetime.now().date() - u['birth_date']).days // 365 if u.get('birth_date') else "؟"
        text = (
            f"🔍 *درخواست تأیید فروشنده*\n\n"
            f"👤 @{u['nickname']} | {u['full_name']}\n"
            f"📍 {u['city']} | {age} سال\n"
            f"📝 {u['bio']}\n"
            f"📅 ثبت‌نام: {u['created_at'].strftime('%Y/%m/%d') if u.get('created_at') else '؟'}"
        )
        kb = InlineKeyboardMarkup([[
            InlineKeyboardButton("✅ تأیید", callback_data=f"verify_{u['telegram_id']}"),
            InlineKeyboardButton("❌ رد", callback_data=f"reject_{u['telegram_id']}"),
        ]])
        await q.message.reply_text(text, parse_mode="Markdown", reply_markup=kb)

async def adm_verify_user_cb(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    tg_id = int(q.data.split("_")[1])

    await update_user(tg_id, is_verified=True)
    await q.edit_message_text(f"✅ کاربر {tg_id} تأیید شد.")

    try:
        await q.bot.send_message(
            tg_id,
            "🎉 *تبریک! پروفایل فروشنده‌ات تأیید شد!*\n\n"
            "حالا در جستجوی دیگران ظاهر می‌شی.",
            parse_mode="Markdown"
        )
    except:
        pass

async def adm_reject_user_cb(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    tg_id = int(q.data.split("_")[1])
    ctx.user_data['reject_tg_id'] = tg_id
    await q.message.reply_text("دلیل رد شدن رو بنویس:")
    return REJECT_REASON

async def adm_reject_reason(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    reason = update.message.text.strip()
    tg_id = ctx.user_data.get('reject_tg_id')
    if tg_id:
        try:
            await update.get_bot().send_message(
                tg_id,
                f"❌ *درخواست فروشنده‌ات رد شد.*\n\n"
                f"دلیل: {reason}\n\n"
                f"می‌تونی اطلاعاتت رو اصلاح کنی و دوباره درخواست بدی.",
                parse_mode="Markdown"
            )
        except:
            pass
    await update.message.reply_text("✅ رد شدن اطلاع‌رسانی شد.")
    return ConversationHandler.END

# ═══════════════════════════════════════════════
#  BAN USER
# ═══════════════════════════════════════════════

async def adm_ban_cb(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    tg_id = int(q.data.split("_")[1])
    ctx.user_data['ban_tg_id'] = tg_id
    await q.message.reply_text(f"دلیل مسدود کردن کاربر {tg_id} رو بنویس:")
    return BAN_REASON

async def adm_ban_reason(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    reason = update.message.text.strip()
    tg_id = ctx.user_data.get('ban_tg_id')
    if tg_id:
        success = await ban_user(update.effective_user.id, tg_id, reason)
        if success:
            await update.message.reply_text(f"✅ کاربر {tg_id} مسدود شد.")
            try:
                await update.get_bot().send_message(
                    tg_id,
                    f"🚫 حساب شما به دلیل تخلف مسدود شده است.\nدلیل: {reason}"
                )
            except:
                pass
        else:
            await update.message.reply_text("❌ خطا در مسدود کردن.")
    return ConversationHandler.END

# ═══════════════════════════════════════════════
#  BOOKING MANAGEMENT
# ═══════════════════════════════════════════════

async def adm_bookings_cb(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("🟢 جاری", callback_data="adm_bk_active"),
         InlineKeyboardButton("⚠️ اختلاف", callback_data="adm_bk_disputed")],
        [InlineKeyboardButton("✅ کامل‌شده امروز", callback_data="adm_bk_today")],
        [InlineKeyboardButton("🔙 بازگشت", callback_data="adm_back")],
    ])
    await q.edit_message_text("📋 *مدیریت رزروها*", parse_mode="Markdown", reply_markup=kb)

async def adm_booking_detail(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    """دستور: /booking <id>"""
    if not await admin_guard(update): return
    args = update.message.text.split()
    if len(args) < 2:
        await update.message.reply_text("استفاده: /booking <id>")
        return

    booking = await get_booking(int(args[1]))
    if not booking:
        await update.message.reply_text("❌ رزرو پیدا نشد.")
        return

    text = (
        f"📋 *رزرو #{booking['id']}*\n\n"
        f"👤 خریدار: @{booking['buyer_nick']}\n"
        f"🧑‍💼 فروشنده: @{booking['seller_nick']}\n"
        f"🎯 فعالیت: {booking['activity']}\n"
        f"⏱ مدت: {booking['hours']} ساعت\n"
        f"💰 مبلغ کل: {fmt(booking['total_amount'])} ت\n"
        f"🏦 کارمزد: {fmt(booking['platform_fee'])} ت\n"
        f"💵 سهم فروشنده: {fmt(booking['seller_amount'])} ت\n"
        f"📊 وضعیت: {booking['status']}\n"
        f"📅 ایجاد: {booking['created_at'].strftime('%Y/%m/%d %H:%M') if booking.get('created_at') else '؟'}"
    )

    kb = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ تأیید دستی", callback_data=f"adm_force_complete_{booking['id']}"),
            InlineKeyboardButton("💸 استرداد", callback_data=f"adm_refund_{booking['id']}"),
        ]
    ])
    await update.message.reply_text(text, parse_mode="Markdown", reply_markup=kb)

# ═══════════════════════════════════════════════
#  GROUP EVENTS
# ═══════════════════════════════════════════════

async def adm_events_cb(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    # دریافت ایونت‌های در انتظار تأیید
    pool = await get_pool()
    async with pool.acquire() as conn:
        events = await conn.fetch("""
            SELECT ge.*, u.nickname as leader_nick
            FROM group_events ge
            JOIN users u ON u.id = ge.leader_id
            WHERE ge.status = 'pending'
            ORDER BY ge.created_at
            LIMIT 5
        """)

    if not events:
        await q.edit_message_text(
            "✅ هیچ ایونت گروهی در انتظار تأیید نیست.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 بازگشت", callback_data="adm_back")]])
        )
        return

    for ev in events:
        text = (
            f"🎭 *ایونت گروهی جدید*\n\n"
            f"📌 {ev['title']}\n"
            f"👤 لیدر: @{ev['leader_nick']}\n"
            f"📍 {ev['location']} | 📅 {ev['event_date'].strftime('%Y/%m/%d') if ev.get('event_date') else '؟'}\n"
            f"⏱ {ev['duration_hours']} ساعت\n"
            f"💰 {fmt(ev['price'])} ت\n\n"
            f"📝 {ev['description']}\n\n"
            f"*رزومه لیدر:*\n{ev['leader_bio']}"
        )
        kb = InlineKeyboardMarkup([[
            InlineKeyboardButton("✅ تأیید", callback_data=f"event_approve_{ev['id']}"),
            InlineKeyboardButton("❌ رد", callback_data=f"event_reject_{ev['id']}"),
        ]])
        await q.message.reply_text(text, parse_mode="Markdown", reply_markup=kb)

async def adm_event_approve_cb(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    event_id = int(q.data.split("_")[2])

    pool = await get_pool()
    async with pool.acquire() as conn:
        ev = await conn.fetchrow("""
            UPDATE group_events SET status = 'approved' WHERE id = $1
            RETURNING *, (SELECT telegram_id FROM users WHERE id = leader_id) as leader_tg
        """, event_id)

    await q.edit_message_text(f"✅ ایونت #{event_id} تأیید شد.")
    if ev:
        try:
            await q.bot.send_message(
                ev['leader_tg'],
                f"🎉 *ایونت گروهی شما تأیید شد!*\n\n"
                f"'{ev['title']}' حالا در لیست ایونت‌ها نمایش داده می‌شه.",
                parse_mode="Markdown"
            )
        except:
            pass

async def adm_event_reject_cb(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    event_id = int(q.data.split("_")[2])

    pool = await get_pool()
    async with pool.acquire() as conn:
        await conn.execute("UPDATE group_events SET status = 'rejected' WHERE id = $1", event_id)

    await q.edit_message_text(f"❌ ایونت #{event_id} رد شد.")

# ═══════════════════════════════════════════════
#  REPORTS
# ═══════════════════════════════════════════════

async def adm_reports_cb(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    pool = await get_pool()
    async with pool.acquire() as conn:
        reports = await conn.fetch("""
            SELECT r.*, 
                   reporter.nickname as reporter_nick,
                   reported.nickname as reported_nick
            FROM reports r
            JOIN users reporter ON reporter.id = r.reporter_id
            JOIN users reported ON reported.id = r.reported_id
            WHERE r.status = 'open'
            ORDER BY r.created_at ASC
            LIMIT 5
        """)

    if not reports:
        await q.edit_message_text(
            "✅ هیچ گزارش باز جدیدی وجود ندارد.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 بازگشت", callback_data="adm_back")]])
        )
        return

    for r in reports:
        text = (
            f"🚨 *گزارش #{r['id']}*\n\n"
            f"👤 گزارش‌دهنده: @{r['reporter_nick']}\n"
            f"🎯 گزارش‌شده: @{r['reported_nick']}\n"
            f"📝 دلیل: {r['reason']}\n"
            f"💬 توضیح: {r['description'] or '—'}\n"
            f"📅 {r['created_at'].strftime('%Y/%m/%d') if r.get('created_at') else '؟'}"
        )
        kb = InlineKeyboardMarkup([[
            InlineKeyboardButton("🚫 مسدود کاربر", callback_data=f"ban_{r['reported_id']}"),
            InlineKeyboardButton("✅ بی‌اساس", callback_data=f"dismiss_report_{r['id']}"),
        ]])
        await q.message.reply_text(text, parse_mode="Markdown", reply_markup=kb)

async def adm_dismiss_report_cb(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    report_id = int(q.data.split("_")[2])
    pool = await get_pool()
    async with pool.acquire() as conn:
        await conn.execute("UPDATE reports SET status = 'dismissed' WHERE id = $1", report_id)
    await q.edit_message_text(f"✅ گزارش #{report_id} بسته شد.")

# ═══════════════════════════════════════════════
#  BROADCAST
# ═══════════════════════════════════════════════

async def adm_broadcast_cb(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    await q.message.reply_text(
        "📢 متن پیام همگانی رو بنویس:\n\n"
        "(پشتیبانی از Markdown)"
    )
    return BROADCAST_TEXT

async def adm_broadcast_send(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not await admin_guard(update): return
    text = update.message.text

    pool = await get_pool()
    async with pool.acquire() as conn:
        users = await conn.fetch("SELECT telegram_id FROM users WHERE is_active = TRUE AND is_banned = FALSE LIMIT 1000")

    sent = 0
    failed = 0
    for u in users:
        try:
            await ctx.bot.send_message(u['telegram_id'], text, parse_mode="Markdown")
            sent += 1
        except:
            failed += 1
        await asyncio.sleep(0.05)  # جلوگیری از rate limit

    await update.message.reply_text(f"✅ ارسال شد: {sent}\n❌ ناموفق: {failed}")
    return ConversationHandler.END

# ═══════════════════════════════════════════════
#  FINANCE
# ═══════════════════════════════════════════════

async def adm_finance_cb(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    pool = await get_pool()
    async with pool.acquire() as conn:
        today_revenue = await conn.fetchval("""
            SELECT COALESCE(SUM(platform_fee), 0) FROM bookings
            WHERE status = 'completed' AND DATE(ended_at) = CURRENT_DATE
        """)
        pending_payouts = await conn.fetchval("""
            SELECT COALESCE(SUM(seller_amount), 0) FROM bookings
            WHERE status = 'completed' AND seller_confirmed = FALSE
        """)
        total_wallet = await conn.fetchval("SELECT COALESCE(SUM(balance), 0) FROM users")

    text = (
        f"💰 *گزارش مالی*\n\n"
        f"📈 درآمد امروز: {fmt(today_revenue)} ت\n"
        f"💸 پرداخت‌های معلق: {fmt(pending_payouts)} ت\n"
        f"🏦 جمع کیف‌پول‌ها: {fmt(total_wallet)} ت\n\n"
        f"🕐 {datetime.now().strftime('%H:%M')}"
    )
    kb = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 بازگشت", callback_data="adm_back")]])
    await q.edit_message_text(text, parse_mode="Markdown", reply_markup=kb)

# ═══════════════════════════════════════════════
#  BUILD & RUN
# ═══════════════════════════════════════════════

import asyncio

def build_admin_bot() -> Application:
    app = Application.builder().token(os.getenv("ADMIN_BOT_TOKEN")).build()

    # Conversations
    ban_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(adm_ban_cb, pattern="^ban_")],
        states={BAN_REASON: [MessageHandler(filters.TEXT & ~filters.COMMAND, adm_ban_reason)]},
        fallbacks=[]
    )
    reject_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(adm_reject_user_cb, pattern="^reject_")],
        states={REJECT_REASON: [MessageHandler(filters.TEXT & ~filters.COMMAND, adm_reject_reason)]},
        fallbacks=[]
    )
    broadcast_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(adm_broadcast_cb, pattern="^adm_broadcast")],
        states={BROADCAST_TEXT: [MessageHandler(filters.TEXT & ~filters.COMMAND, adm_broadcast_send)]},
        fallbacks=[]
    )

    app.add_handler(CommandHandler("start", admin_start))
    app.add_handler(CommandHandler("user", adm_user_info))
    app.add_handler(CommandHandler("booking", adm_booking_detail))
    app.add_handler(ban_conv)
    app.add_handler(reject_conv)
    app.add_handler(broadcast_conv)
    app.add_handler(CallbackQueryHandler(adm_stats_cb, pattern="^adm_stats"))
    app.add_handler(CallbackQueryHandler(adm_users_cb, pattern="^adm_users"))
    app.add_handler(CallbackQueryHandler(adm_verify_list_cb, pattern="^adm_verify"))
    app.add_handler(CallbackQueryHandler(adm_verify_user_cb, pattern="^verify_"))
    app.add_handler(CallbackQueryHandler(adm_bookings_cb, pattern="^adm_bookings"))
    app.add_handler(CallbackQueryHandler(adm_events_cb, pattern="^adm_events"))
    app.add_handler(CallbackQueryHandler(adm_event_approve_cb, pattern="^event_approve_"))
    app.add_handler(CallbackQueryHandler(adm_event_reject_cb, pattern="^event_reject_"))
    app.add_handler(CallbackQueryHandler(adm_reports_cb, pattern="^adm_reports"))
    app.add_handler(CallbackQueryHandler(adm_dismiss_report_cb, pattern="^dismiss_report_"))
    app.add_handler(CallbackQueryHandler(adm_finance_cb, pattern="^adm_finance"))
    app.add_handler(CallbackQueryHandler(lambda u, c: back_to_menu(u.callback_query), pattern="^adm_back"))

    return app

if __name__ == "__main__":
    app = build_admin_bot()
    print("✅ Timely Admin Bot started...")
    app.run_polling()
