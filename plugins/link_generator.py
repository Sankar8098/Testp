from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from bot import Bot
from config import ADMINS
from helper_func import encode, get_message_id


@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command('batch'))
async def batch(client: Client, message: Message):
    while True:
        try:
            first_message = await client.ask(text = "Forward the First Message from DB Channel ⏩ (with Quotes)..\n\nor Send the DB Channel Post Link\nUse /sbatch for stopping.", chat_id = message.from_user.id, filters=(filters.forwarded | (filters.text & ~filters.forwarded)), timeout=60)
        except Exception as e:
            print(e)
            return
        if first_message.text == "/sbatch":
            return
        f_msg_id = await get_message_id(client, first_message)
        
        if f_msg_id:
            break
        else:
            await first_message.reply("❌ Error\n\nthis Forwarded Post is not from my DB Channel or this Link is taken from DB Channel", quote = True)
            continue
    while True:
        try:
            second_message = await client.ask(text = "Forward the Last Message from DB Channel ⏩ (with Quotes)..\nor Send the DB Channel Post link\nUse /sbatch for stopping.", chat_id = message.from_user.id, filters=(filters.forwarded | (filters.text & ~filters.forwarded)), timeout=60)
        except:
            return
        if second_message.text == "/sbatch":
            return
        s_msg_id = await get_message_id(client, second_message)
        if s_msg_id:
            break
        else:
            await second_message.reply("❌ Error\n\nthis Forwarded Post is not from my DB Channel or this Link is taken from DB Channel", quote = True)
            continue
        
    string = f"get-{f_msg_id * abs(client.db_channel.id)}-{s_msg_id * abs(client.db_channel.id)}"
    base64_string = await encode(string)
    link = f"https://tamilserialbot.jasurun.workers.dev?start={base64_string}"
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]])
    await second_message.reply_text(f"🔗 ➟ {link}", quote=True, reply_markup=reply_markup)



@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command('genlink'))
async def link_generator(client: Client, message: Message):
    while True:
        try:
            channel_message = await client.ask(text = "Forward Message from the DB Channel ⏩ (with Quotes)..\nor Send the DB Channel Post link\nType /sgen for stopping.", chat_id = message.from_user.id, filters=(filters.forwarded | (filters.text & ~filters.forwarded)), timeout=60)
        except Exception:
            return
        if channel_message.text == "/sgen":
            return
        msg_id = await get_message_id(client, channel_message)
        if msg_id:
            break
        else:
            await channel_message.reply("❌ Error\n\nthis Forwarded Post is not from my DB Channel or this Link is not taken from DB Channel", quote = True)
            continue
    base64_string = await encode(f"get-{msg_id * abs(client.db_channel.id)}")
    link = f"https://tamilserialbot.jasurun.workers.dev?start={base64_string}"
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(f"🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]])
    await channel_message.reply_text(f"<b>★○★○★○★\n{file_name} - {🌺 {duration}} - 🌺 {file_size}\n\n{link}\n★○★○★○★</b>", quote=True, reply_markup=reply_markup)
