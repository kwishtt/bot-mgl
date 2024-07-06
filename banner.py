import discord
from discord.ext import commands
from collections import defaultdict

intents = discord.Intents.default()
intents.message_content_filter = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Danh sách từ cấm
bad_words = ["bad_word1", "bad_word2", "từ_cấm_1", "từ_cấm_2"]

# Danh sách các kênh không kiểm tra
excluded_channels = ["channel_id_1", "channel_id_2"]

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
    for word in bad_words:
        if word in content:
            await message.delete()
            await message.channel.send(f"{message.author.mention}, vui lòng không sử dụng từ ngữ không phù hợp.")
            user_scores[message.author.id] += 1  # Tăng điểm số của người dùng

            # Kiểm tra điểm số và áp dụng hình phạt nếu cần
            if user_scores[message.author.id] % 5 == 0:  # Mỗi 5 điểm
                member = message.author
                muted_role = discord.utils.get(message.guild.roles, name="Muted")  # Tên role mute
                await member.add_roles(muted_role)
                await message.channel.send(f"{member.mention} đã bị mute 30 phút vì vi phạm quy định.")
                await asyncio.sleep(1800)  # Mute trong 30 phút (1800 giây)
                await member.remove_roles(muted_role)  # Sau khi hết thời gian mute

            return  # Kết thúc khi tìm thấy từ cấm

    await bot.process_commands(message)

bot.run('YOUR_BOT_TOKEN')
