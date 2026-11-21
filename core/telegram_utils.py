import threading
import requests
from django.conf import settings


def _send_request(method, payload, files=None):
    token = getattr(settings, 'TELEGRAM_BOT_TOKEN', '')
    if not token or token == 'توکن_ربات_شما':
        return

    url = f"https://api.telegram.org/bot{token}/{method}"
    try:
        requests.post(url, data=payload, files=files, timeout=10)
    except Exception as e:
        print(f"Telegram Error ({method}): {e}")


def run_async(func, *args, **kwargs):
    thread = threading.Thread(target=func, args=args, kwargs=kwargs, daemon=True)
    thread.start()


# --- ۱. ارسال پیام متنی به ربات مدیریت (ادمین) ---
def send_admin_message(text):
    chat_id = getattr(settings, 'TELEGRAM_ADMIN_CHAT_ID', '')
    if not chat_id:
        return
    payload = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'HTML',
    }
    run_async(_send_request, 'sendMessage', payload)


def notify_new_order(order):
    items_lines = []
    for item in order.items.all():
        size_name = item.product_size.name if item.product_size else '-'
        items_lines.append(
            f"▫️ {item.product.name} | سایز: {size_name} | تعداد: {item.quantity}"
        )

    items_text = "\n".join(items_lines)
    total_cost = int(order.get_total_cost())
    admin_link = f"{settings.SITE_URL}/dashboard/orders/{order.id}/"

    text = (
        f"🛍 <b>سفارش جدید پرداخت شد! (#{order.id})</b>\n"
        f"━━━━━━━━━━━━━━\n"
        f"👤 <b>مشتری:</b> {order.first_name} {order.last_name}\n"
        f"📞 <b>موبایل:</b> <code>{order.phone}</code>\n"
        f"📍 <b>آدرس:</b> {order.address}\n"
        f"━━━━━━━━━━━━━━\n"
        f"👕 <b>اقلام سفارش:</b>\n{items_text}\n"
        f"━━━━━━━━━━━━━━\n"
        f"🚚 <b>هزینه ارسال:</b> {order.shipping_cost:,} تومان\n"
        f"💰 <b>مبلغ کل پرداختی:</b> <b>{total_cost:,} تومان</b>\n\n"
        f"🔗 <a href='{admin_link}'>مشاهده و مدیریت در داشبورد</a>"
    )
    send_admin_message(text)


def notify_low_stock(size_obj):
    text = (
        f"⚠️ <b>هشدار اتمام موجودی!</b>\n\n"
        f"👕 محصول: <b>{size_obj.product.name}</b>\n"
        f"📏 سایز: <b>{size_obj.name}</b>\n"
        f"📦 موجودی فعلی به <b>۰</b> رسید."
    )
    send_admin_message(text)


def notify_stock_request(size_obj, phone):
    text = (
        f"🔔 <b>درخواست جدید «خبرم کن»</b>\n\n"
        f"👕 محصول: <b>{size_obj.product.name}</b>\n"
        f"📏 سایز: <b>{size_obj.name}</b>\n"
        f"📞 شماره مشتری: <code>{phone}</code>"
    )
    send_admin_message(text)


# --- ۲. انتشار خودکار محصول در کانال تلگرام ---
def post_product_to_channel(product):
    channel_id = getattr(settings, 'TELEGRAM_CHANNEL_ID', '')
    if not channel_id:
        return

    # استخراج سایزهای موجود محصول
    available_sizes = [s.name for s in product.sizes.filter(stock__gt=0)]
    sizes_text = "، ".join(available_sizes) if available_sizes else "مشاهده در سایت"

    # لینک صفحه محصول
    product_url = f"{settings.SITE_URL}/products/{product.id}/"

    # خلاصه توضیحات (حداکثر ۱۸۰ کاراکتر برای خوانایی در کانال)
    short_desc = (product.description[:180] + '...') if len(product.description) > 180 else product.description

    caption = (
        f"✨ <b>{product.name}</b>\n\n"
        f"🏷 دسته‌بندی: {product.get_gender_display()}\n"
        f"👶 رده سنی: {product.min_age} تا {product.max_age} سال\n"
        f"📏 سایزهای موجود: {sizes_text}\n"
        f"💳 قیمت: <b>{product.price:,} تومان</b>\n\n"
        f"📝 {short_desc}\n\n"
        f"👇 برای دیدن عکس‌های بیشتر و ثبت سفارش کلیک کنید:"
    )

    import json
    reply_markup = json.dumps({
        'inline_keyboard': [[
            {'text': '🛒 مشاهده و خرید آنلاین', 'url': product_url}
        ]]
    })

    # پیدا کردن اولین عکس (گالری یا عکس اصلی)
    first_gallery = product.images.first()
    image_field = first_gallery.image if first_gallery else product.image

    def _publish():
        if image_field:
            img_url = image_field.url
            # اگر عکس روی فضای ابری (لینک کامل https) باشد مستقیم می‌فرستیم
            if img_url.startswith('http'):
                payload = {
                    'chat_id': channel_id,
                    'photo': img_url,
                    'caption': caption,
                    'parse_mode': 'HTML',
                    'reply_markup': reply_markup,
                }
                _send_request('sendPhoto', payload)
            else:
                # حالت لوکال: ارسال فایل عکس از دیسک
                try:
                    with open(image_field.path, 'rb') as f:
                        payload = {
                            'chat_id': channel_id,
                            'caption': caption,
                            'parse_mode': 'HTML',
                            'reply_markup': reply_markup,
                        }
                        _send_request('sendPhoto', payload, files={'photo': f})
                except Exception as e:
                    print(f"Telegram Local Photo Error: {e}")
        else:
            payload = {
                'chat_id': channel_id,
                'text': caption,
                'parse_mode': 'HTML',
                'reply_markup': reply_markup,
            }
            _send_request('sendMessage', payload)

    run_async(_publish)