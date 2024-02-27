import discord
import psutil
import asyncio
import platform
import datetime
import aiohttp
import matplotlib.pyplot as plt
import numpy as np
from discord.ext import commands

intents = discord.Intents.default()
intents.typing = False  
intents.presences = False 

bot = commands.Bot(command_prefix='!', intents=intents)

VPS_NAME = "Your vps name"
last_message = None

async def update_stats(channel):
    global last_message
    while True:
        cpu_usage = psutil.cpu_percent()
        ram = psutil.virtual_memory()
        disk = psutil.disk_usage('/')

        cpu_cores = psutil.cpu_count(logical=False)
        cpu_threads = psutil.cpu_count(logical=True)
        cpu_model = "Your cpu model"  
        uptime = datetime.datetime.now() - datetime.datetime.fromtimestamp(psutil.boot_time())
        uptime_str = str(uptime).split('.')[0] 

        ram_usage_gb = ram.used / (1024**3)
        ram_total_gb = ram.total / (1024**3)
        disk_usage_gb = disk.used / (1024**3)
        disk_total_gb = disk.total / (1024**3)

        async with aiohttp.ClientSession() as session:
            async with session.get('https://ipinfo.io/json') as response:
                ip_info = await response.json()
                ip = ip_info['ip']
                provider = ip_info['org']

        timestamps = np.arange(0, 30, 1) 
        cpu_data = [psutil.cpu_percent() for _ in timestamps]
        ram_data = [psutil.virtual_memory().percent for _ in timestamps]
        disk_data = [psutil.disk_usage('/').percent for _ in timestamps]

        plt.figure(figsize=(10, 8))

        plt.subplot(3, 2, 1)
        plt.plot(timestamps, cpu_data, label='CPU', color='blue')
        plt.xlabel('Time (seconds)')
        plt.ylabel('CPU usage (%)')
        plt.title('CPU usage')
        plt.grid(True)

        plt.subplot(3, 2, 2)
        plt.plot(timestamps, ram_data, label='RAM', color='green')
        plt.xlabel('Time (seconds)')
        plt.ylabel('RAM usage (%)')
        plt.title('RAM usage')
        plt.grid(True)

        plt.subplot(3, 2, 3)
        plt.plot(timestamps, disk_data, label='Storage', color='red')
        plt.xlabel('Time (seconds)')
        plt.ylabel('Storage usage (%)')
        plt.title('Storage usage')
        plt.grid(True)

        plt.tight_layout()
        plt.savefig('stats.png')
  
        plt.close('all')

        embed = discord.Embed(title=f"System Status : {VPS_NAME}", color=0x00ff00)
        embed.add_field(name="CPU Model", value=cpu_model, inline=False)
        embed.add_field(name="CPU Usage", value=f"{cpu_usage}%", inline=False)
        embed.add_field(name="Cores/Threads", value=f"Cores: {cpu_cores}, Threads: {cpu_threads}", inline=False)
        embed.add_field(name="Uptime", value=uptime_str, inline=False)
        embed.add_field(name="RAM Usage", value=f"{ram_usage_gb:.2f} GB / {ram_total_gb:.2f} GB", inline=False)
        embed.add_field(name="Storage Usage", value=f"{disk_usage_gb:.2f} GB / {disk_total_gb:.2f} GB", inline=False)
        embed.add_field(name="IP", value=ip, inline=False)
        embed.set_image(url="attachment://stats.png")
        embed.set_footer(text="©KubaruGames")

        if last_message:
            await last_message.delete()

        last_message = await channel.send(embed=embed, file=discord.File('stats.png'))
        await asyncio.sleep(30) 

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    channel = bot.get_channel(Your Channel ID)  # Canal donde enviar el mensaje
    bot.loop.create_task(update_stats(channel))
bot.run('Your Bot Token')
