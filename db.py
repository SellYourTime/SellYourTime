"""
Timely Bot — Database Layer
اتصال به PostgreSQL با asyncpg
"""
import asyncpg
import os
from typing import Optional, List, Dict, Any
from dotenv import load_dotenv

load_dotenv()

_pool: Optional[asyncpg.Pool] = None

async def get_pool() -> asyncpg.Pool:
    global _pool
    if _pool is None:
        _pool = await asyncpg.create_pool(
            os.getenv("DATABASE_URL"),
            min_size=5,
            max_size=20,
            command_timeout=30
        )
    return _pool

async def close_pool():
    global _pool
    if _pool:
        await _pool.close()
        _pool = None

# ─── USERS ───────────────────────────────────────

async def get_user(telegram_id: int) -> Optional[Dict]:
    pool = await get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT * FROM users WHERE telegram_id = $1", telegram_id
        )
        return dict(row) if row else None

async def create_user(data: Dict) -> Dict:
    pool = await get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow("""
            INSERT INTO users (
                telegram_id, telegram_username, nickname, full_name,
                gender, birth_date, city, bio, is_seller,
                price_per_hour, pet_friendly, referral_code, referred_by
            ) VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13)
            RETURNING *
        """,
            data['telegram_id'], data.get('telegram_username'),
            data['nickname'], data['full_name'], data['gender'],
            data['birth_date'], data['city'], data.get('bio'),
            data.get('is_seller', False), data.get('price_per_hour', 200000),
            data.get('pet_friendly', False), data['referral_code'],
            data.get('referred_by')
        )
        return dict(row)

async def update_user(telegram_id: int, **kwargs) -> bool:
    if not kwargs:
        return False
    pool = await get_pool()
    fields = ", ".join(f"{k} = ${i+2}" for i, k in enumerate(kwargs))
    values = list(kwargs.values())
    async with pool.acquire() as conn:
        result = await conn.execute(
            f"UPDATE users SET {fields}, last_active = NOW() WHERE telegram_id = $1",
            telegram_id, *values
        )
        return result == "UPDATE 1"

async def search_sellers(
    city: Optional[str] = None,
    gender: Optional[str] = None,
    min_age: int = 18,
    max_age: int = 60,
    activity: Optional[str] = None,
    pet_friendly: bool = False,
    limit: int = 10,
    offset: int = 0
) -> List[Dict]:
    pool = await get_pool()
    conditions = ["u.is_seller = TRUE", "u.is_active = TRUE", "u.is_banned = FALSE", "u.is_verified = TRUE"]
    params = []
    i = 1

    if city:
        conditions.append(f"u.city = ${i}")
        params.append(city); i += 1
    if gender:
        conditions.append(f"u.gender = ${i}")
        params.append(gender); i += 1
    if pet_friendly:
        conditions.append("u.pet_friendly = TRUE")

    conditions.append(f"EXTRACT(YEAR FROM AGE(u.birth_date)) BETWEEN ${i} AND ${i+1}")
    params.extend([min_age, max_age]); i += 2

    join_activity = ""
    if activity:
        join_activity = f"JOIN user_activities ua ON ua.user_id = u.id AND ua.activity = ${i}"
        params.append(activity); i += 1

    params.extend([limit, offset])
    query = f"""
        SELECT u.*, 
               ARRAY_AGG(DISTINCT ua2.activity) as activities
        FROM users u
        LEFT JOIN user_activities ua2 ON ua2.user_id = u.id
        {join_activity}
        WHERE {' AND '.join(conditions)}
        GROUP BY u.id
        ORDER BY u.rating_avg DESC, u.rating_count DESC
        LIMIT ${i} OFFSET ${i+1}
    """
    async with pool.acquire() as conn:
        rows = await conn.fetch(query, *params)
        return [dict(r) for r in rows]

# ─── BOOKINGS ────────────────────────────────────

async def create_booking(data: Dict) -> Dict:
    total = data['hours'] * data['price_per_hour']
    discount = data.get('discount_pct', 0)
    discounted_total = int(total * (1 - discount / 100))
    fee = int(discounted_total * 0.25)
    seller_amount = discounted_total - fee

    pool = await get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow("""
            INSERT INTO bookings (
                buyer_id, seller_id, activity, hours,
                price_per_hour, total_amount, platform_fee,
                seller_amount, discount_pct, scheduled_at, status
            ) VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,'pending')
            RETURNING *
        """,
            data['buyer_id'], data['seller_id'], data['activity'],
            data['hours'], data['price_per_hour'], discounted_total,
            fee, seller_amount, discount, data.get('scheduled_at')
        )
        return dict(row)

async def get_booking(booking_id: int) -> Optional[Dict]:
    pool = await get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow("""
            SELECT b.*, 
                   buyer.nickname as buyer_nick, buyer.telegram_id as buyer_tg,
                   seller.nickname as seller_nick, seller.telegram_id as seller_tg
            FROM bookings b
            JOIN users buyer ON buyer.id = b.buyer_id
            JOIN users seller ON seller.id = b.seller_id
            WHERE b.id = $1
        """, booking_id)
        return dict(row) if row else None

async def update_booking_status(booking_id: int, status: str, **kwargs) -> bool:
    pool = await get_pool()
    extra = ""
    params = [status, booking_id]
    i = 3
    for k, v in kwargs.items():
        extra += f", {k} = ${i}"
        params.insert(-1, v); i += 1

    async with pool.acquire() as conn:
        result = await conn.execute(
            f"UPDATE bookings SET status = $1{extra} WHERE id = $2",
            *params
        )
        return result == "UPDATE 1"

async def get_user_bookings(telegram_id: int, role: str = "buyer", limit: int = 5) -> List[Dict]:
    pool = await get_pool()
    field = "buyer.telegram_id" if role == "buyer" else "seller.telegram_id"
    async with pool.acquire() as conn:
        rows = await conn.fetch(f"""
            SELECT b.*, 
                   buyer.nickname as buyer_nick,
                   seller.nickname as seller_nick
            FROM bookings b
            JOIN users buyer ON buyer.id = b.buyer_id
            JOIN users seller ON seller.id = b.seller_id
            WHERE {field} = $1
            ORDER BY b.created_at DESC LIMIT $2
        """, telegram_id, limit)
        return [dict(r) for r in rows]

# ─── RATINGS ─────────────────────────────────────

async def create_rating(booking_id: int, rater_id: int, rated_id: int,
                        stars: int, reasons: List[str] = None, note: str = None) -> Dict:
    pool = await get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow("""
            INSERT INTO ratings (booking_id, rater_id, rated_id, stars, reasons, note)
            VALUES ($1,$2,$3,$4,$5,$6) RETURNING *
        """, booking_id, rater_id, rated_id, stars, reasons or [], note)
        return dict(row)

# ─── GPS ─────────────────────────────────────────

async def update_gps(booking_id: int, user_type: str, lat: float, lng: float) -> Optional[Dict]:
    """user_type: 'buyer' or 'seller'"""
    pool = await get_pool()
    async with pool.acquire() as conn:
        # upsert
        await conn.execute(f"""
            INSERT INTO gps_sessions (booking_id, {user_type}_lat, {user_type}_lng, {user_type}_updated)
            VALUES ($1, $2, $3, NOW())
            ON CONFLICT (booking_id) DO UPDATE SET
                {user_type}_lat = $2, {user_type}_lng = $3, {user_type}_updated = NOW()
        """, booking_id, lat, lng)

        row = await conn.fetchrow("SELECT * FROM gps_sessions WHERE booking_id = $1", booking_id)
        return dict(row) if row else None

# ─── EVENTS ──────────────────────────────────────

async def get_dual_events(city: Optional[str] = None, limit: int = 5) -> List[Dict]:
    pool = await get_pool()
    async with pool.acquire() as conn:
        query = "SELECT * FROM dual_events WHERE is_active = TRUE"
        params = []
        if city:
            query += " AND city = $1"
            params.append(city)
        query += f" ORDER BY event_date LIMIT ${len(params)+1}"
        params.append(limit)
        rows = await conn.fetch(query, *params)
        return [dict(r) for r in rows]

async def get_group_events(city: Optional[str] = None, limit: int = 5) -> List[Dict]:
    pool = await get_pool()
    async with pool.acquire() as conn:
        query = """
            SELECT ge.*, u.nickname as leader_nick, u.rating_avg as leader_rating,
                   COUNT(gep.id) as participant_count
            FROM group_events ge
            JOIN users u ON u.id = ge.leader_id
            LEFT JOIN group_event_participants gep ON gep.event_id = ge.id
            WHERE ge.is_active = TRUE AND ge.status = 'approved'
        """
        params = []
        if city:
            query += " AND ge.city = $1"
            params.append(city)
        query += f" GROUP BY ge.id, u.nickname, u.rating_avg ORDER BY ge.event_date LIMIT ${len(params)+1}"
        params.append(limit)
        rows = await conn.fetch(query, *params)
        return [dict(r) for r in rows]

# ─── ADMIN ───────────────────────────────────────

async def get_platform_stats() -> Dict:
    pool = await get_pool()
    async with pool.acquire() as conn:
        stats = await conn.fetchrow("""
            SELECT
                (SELECT COUNT(*) FROM users WHERE is_active = TRUE) as total_users,
                (SELECT COUNT(*) FROM users WHERE is_seller = TRUE AND is_verified = TRUE) as active_sellers,
                (SELECT COUNT(*) FROM bookings WHERE status = 'completed') as completed_bookings,
                (SELECT COUNT(*) FROM bookings WHERE status = 'in_progress') as active_bookings,
                (SELECT COALESCE(SUM(platform_fee),0) FROM bookings WHERE status = 'completed') as total_revenue,
                (SELECT COUNT(*) FROM reports WHERE status = 'open') as open_reports,
                (SELECT COUNT(*) FROM group_events WHERE status = 'pending') as pending_events
        """)
        return dict(stats)

async def get_pending_verifications(limit: int = 10) -> List[Dict]:
    pool = await get_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT * FROM users
            WHERE is_seller = TRUE AND is_verified = FALSE AND is_banned = FALSE
            ORDER BY created_at ASC LIMIT $1
        """, limit)
        return [dict(r) for r in rows]

async def ban_user(admin_id: int, user_telegram_id: int, reason: str) -> bool:
    pool = await get_pool()
    async with pool.acquire() as conn:
        async with conn.transaction():
            user = await conn.fetchrow("SELECT id FROM users WHERE telegram_id = $1", user_telegram_id)
            if not user:
                return False
            await conn.execute(
                "UPDATE users SET is_banned = TRUE, ban_reason = $1 WHERE telegram_id = $2",
                reason, user_telegram_id
            )
            await conn.execute("""
                INSERT INTO admin_logs (admin_id, action, target_type, target_id, note)
                VALUES ($1, 'ban_user', 'user', $2, $3)
            """, admin_id, user['id'], reason)
            return True
