import discord
from discord.ext import commands
import regex as re
from collections import defaultdict

intents = discord.Intents.default()
intents.message_content_filter = True

bot = commands.Bot(command_prefix='_', intents=intents)

# Danh sách từ cấm tiếng Việt
bad_words = [
    "sex", "buồi", "lồn", "dái", "địt", "óc chó", "đụ", "parky",
    "cặc", "dái", "đĩ", "đụ má", "cặc kẹ", "địt mẹ", "địt con mẹ mày"
]

# Danh sách các kênh không kiểm tra
excluded_channels = ["1245114225739960492"]

# Đối tượng lưu trữ điểm số của từng người dùng
user_scores = defaultdict(int)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_message(message):
    # Kiểm tra xem có nằm trong danh sách kênh không kiểm tra
    if str(message.channel.id) in excluded_channels:
        return

    # Kiểm tra nội dung tin nhắn
    content = message.content.lower()

    # Kiểm tra các từ cấm tiếng Việt
    for word in bad_words:
        # Tìm kiếm từ cấm có dấu hoặc không dấu trong tin nhắn
        pattern = r'\b' + re.escape(word) + r'\b'
        if re.search(pattern, content, flags=re.IGNORECASE | re.UNICODE):
            await message.delete()
            await message.channel.send(f"{message.author.mention},Vừa nói cái gì đấy?? ANH NHẮC EMMM.")
            user_scores[message.author.id] += 1  # Tăng điểm số của người dùng

            # Kiểm tra điểm số và áp dụng hình phạt nếu cần
            if user_scores[message.author.id] == 1:  # Mỗi 5 điểm
                member = message.author
                muted_role = discord.utils.get(message.guild.roles, name="Muted")  # Tên role mute
                await member.add_roles(muted_role)
                await message.channel.send(f"{member.mention} anh nhắc em lần 1 đấy nhé. Im lặng 5 phút đi, lần sau là 30 phút.")
                await asyncio.sleep(1800)  # Mute trong 30 phút (1800 giây)
                await member.remove_roles(muted_role)  # Sau khi hết thời gian mute
        
            if user_scores[message.author.id] % 3 == 0:  # Mỗi 5 điểm
                member = message.author
                muted_role = discord.utils.get(message.guild.roles, name="Muted")  # Tên role mute
                await member.add_roles(muted_role)
                await message.channel.send(f"{member.mention} đã bị mute 30 phút vì vi phạm quy định.")
                await asyncio.sleep(1800)  # Mute trong 30 phút (1800 giây)
                await member.remove_roles(muted_role)  # Sau khi hết thời gian mute

            return  # Kết thúc khi tìm thấy từ cấm

    await bot.process_commands(message)

