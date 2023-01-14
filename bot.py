import discord
from discord.ext import commands
from discord.ext.commands import Context
from discord import app_commands
import pymongo
import asyncio
from datetime import datetime, timedelta
import time
import threading

#---Other Imports
import tok
import rewards
#import adventure 
MONGO = tok.mongo
client = pymongo.MongoClient (MONGO)
db = client.DiscordJasperBot

#------IntoDB -------
def intoDB (user_id: int):
    query = {"_id":user_id}
    #Collect times to show how long is left 3.0
    if (db.OnAdventure.count_documents(query) == 0):
        db.OnAdventure.insert_one({"_id": user_id,"cat1":True,"GC":0,"SC":0,"SNC":0,
        "OC":0,"GDC":0,"OC":0,"Total":0})

def intoDB2 (user_id: int):
    query = {"_id":user_id}
    if (db.UserAdventure.count_documents(query) == 0):
        db.UserAdventure.insert_one({"_id": user_id,"1G":False,"2G":False,"3G":False,"4G":False,
        "1S":False,"2S":False,"1SN":False,"2SN":False,"1O":False,"2O":False,"1GD":False,"2GD":False,"3GD":False,"1OH":False,"2OH":False,"3OH":False,"Grass":0,
        "Sand":0,"Glass":0,"Snow":0,"Ice":0,
        "Wood":0,"Gem":0,"Kernal":0,"Corn":0})

    
    #Can find glass in dessert and glass desert up
#------ Variables ------
TOKEN = tok.token
#------ Bot ------
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='?', intents=intents)

#--- Bot Startup
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}') #Bot Name
  
#------ Prefix Commands ------
@bot.command()
async def hello(ctx):
    await ctx.send('hello')
 
#------ Button ------
class buttonHandler(discord.ui.View):
    @discord.ui.button(label = "", style = discord.ButtonStyle.primary, 
    emoji = "🌳" )
    async def button1(self,interaction:discord.Interaction, button: discord.ui.Button):
        view = TreeTrue()
        des = rewards.description_Tree(interaction.user.id)
        embed = discord.Embed(title="🌳 Grass Lands (LVL 1+)", description=des, color=0x2D9922)
        await interaction.response.send_message(embed= embed,view=view)
    @discord.ui.button(label = "", style = discord.ButtonStyle.primary, 
    emoji = "🏜️" )
    async def button2(self,interaction:discord.Interaction, button: discord.ui.Button):
        view = SandTrue()   
        des = rewards.description_Sand(interaction.user.id)
        embed = discord.Embed(title="🏜️ Desert Dunes (LVL X+)", description=des, color=0x996822)
        await interaction.response.send_message(embed= embed,view=view)

    @discord.ui.button(label = "", style = discord.ButtonStyle.primary, 
    emoji = "<:snowtree:1059258720531521596>" )
    async def button3(self,interaction:discord.Interaction, button: discord.ui.Button):
        view = SnowTrue()   
        des = rewards.description_Frost(interaction.user.id)
        embed = discord.Embed(title="<:snowtree:1059258720531521596> Frost Wastelands (LVL X+)", description=des, color=0x0000FF)
        await interaction.response.send_message(embed= embed,view=view)

    @discord.ui.button(label = "", style = discord.ButtonStyle.primary, 
    emoji = "🦧" )
    async def button4(self,interaction:discord.Interaction, button: discord.ui.Button):
        view = JungleTrue()   
        des = rewards.description_Jungle(interaction.user.id) #orangatang
        embed = discord.Embed(title="🦧 Monkey Jungle (LVL X+)", description=des, color=0xFFA500)
        await interaction.response.send_message(embed= embed,view=view)

    @discord.ui.button(label = "", style = discord.ButtonStyle.primary, 
    emoji = "💎" )
    async def button5(self,interaction:discord.Interaction, button: discord.ui.Button):
        view = GlassTrue()   
        des = rewards.description_Glass(interaction.user.id)
        embed = discord.Embed(title="💎 Glass Desert (LVL X+)", description=des, color=0x89CFF0)
        await interaction.response.send_message(embed= embed,view=view)

    @discord.ui.button(label = "", style = discord.ButtonStyle.primary, 
    emoji = "<:amonguspog:886652968051560488>" )
    async def button6(self,interaction:discord.Interaction, button: discord.ui.Button):
        view = OhioTrue()   
        des = rewards.description_Ohio(interaction.user.id) 
        embed = discord.Embed(title="<:amonguspog:886652968051560488> Ohio! (LVL X+)", description=des, color=0x8b0000)
        await interaction.response.send_message(embed= embed,view=view)
@bot.tree.command()
async def adventure(interaction: discord.Interaction):
    """Button Test"""
    embed = discord.Embed(title="Adventure with Jasper (Selection Menu)",description="🌳 Grass Lands\n🏜️ Desert Dunes\n<:snowtree:1059258720531521596> Frost Wasteland\n🦧 Orangutan Jungle\n💎 Glass Desert\n<:amonguspog:886652968051560488> Ohio!!\n", color=0x11806A)
    view = buttonHandler()
    await interaction.response.send_message(embed = embed,view=view)

@bot.tree.command()
async def status(interaction: discord.Interaction):
    """Button Test"""
    intoDB(interaction.user.id)
    intoDB2(interaction.user.id)
    await interaction.response.send_message("Inserted Correctly")



#------ Sync Command ------
@bot.command()
@commands.guild_only()
@commands.is_owner()
async def sync(ctx: Context):
	synced = await ctx.bot.tree.sync()
	await ctx.send(f"Synced {len(synced)} commands {'globally'}")


# EXTERNAL

#Delete or disable button after claim
class Claim(discord.ui.View):
    @discord.ui.button(label = "Claim", style = discord.ButtonStyle.success)
    #Embed of the rewards gotten
    async def start1(self,interaction:discord.Interaction, button: discord.ui.Button):
        #Cat is back from adventure
        catData = db.OnAdventure.find_one({"_id": interaction.user.id})
        #Rewrok this when add more then one cat
        if catData["cat1"] == False:
            catData["cat1"] = True
            db.OnAdventure.replace_one({"_id":interaction.user.id}, catData)
            #Take temp awards 
            UserRewards = db.RewardHold.find_one({"_id": interaction.user.id})
            db.RewardHold.delete_one({"_id": interaction.user.id})
            embed = discord.Embed(title="Rewards Claimed", description=UserRewards["rewards"],color=0xFFD700)
            await interaction.response.send_message(embed=embed,ephemeral=True)
        else:
            button.disabled = True
            await interaction.response.edit_message(view=self)
            await interaction.followup.send(content="Can't Claim Rewards More Then Once", ephemeral=True)


    #Can update decs time in adventure thread and checkinng speed    
async def adventure_thread(time_left, user_id, loot):
    await asyncio.sleep(time_left)
    #gen rewards set to id (Once clamied send to status and del)
    rewards.generate_rewards(user_id, loot)
    delete_data(time_left, user_id)
    view = Claim()
    embed = discord.Embed(title="Rewards are Ready", description=f"<@{user_id}> your rewards are ready", color=0x4E1972)
    await bot.get_channel(885411221875081228).send(embed=embed, view=view)
    #await bot Chnaged or Del Afte Time

#Find out a way to pull and itterate channel it was called/guild
def insert_data(time_left, user_id, loot):
    data = {"time_left": time_left, "user_id": user_id, "loot": loot}
    db.tempAdventure.insert_one(data)
    #Cat is on adventure
    catData = db.OnAdventure.find_one({"_id": user_id})
    catData["cat1"] = False
    db.OnAdventure.replace_one({"_id":user_id}, catData)

def delete_data(time_left, user_id):
    data = {"time_left": time_left, "user_id": user_id}
    db.tempAdventure.delete_one(data)


def lvl_requirements(user_id:int, lvl:int)->bool:
    userData = db.UserStatus.find_one({"_id": user_id})
    userLvl= userData["love_am"]
    if userLvl >= lvl:
        return True
    elif userLvl < lvl:
        return False

def cat_requirment(user_id:int)->bool:
    catData = db.OnAdventure.find_one({"_id": user_id})
    catAdventure= catData["cat1"]
    if catAdventure == True:
        return True
    elif catAdventure == False:
        return False

class TreeTrue(discord.ui.View):
    @discord.ui.button(label = "Start", style = discord.ButtonStyle.success)
    async def start1(self,interaction:discord.Interaction, button: discord.ui.Button):
        cat_avalible = cat_requirment(interaction.user.id)
        if cat_avalible == False:
            button.disabled = True
            await interaction.response.edit_message(view=self)
            await interaction.followup.send(content="Currently On An Adventure Try Again Later", ephemeral=True)
        else:
            insert_data(5, interaction.user.id, "Tree")
            bot.loop.create_task(adventure_thread(5,interaction.user.id,"Tree"))
            await interaction.response.send_message(content="The Journey Has Began",ephemeral=True)
    @discord.ui.button(label = "Back", style = discord.ButtonStyle.grey)
    async def back(self,interaction:discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title="Adventure with Jasper (Selection Menu)",description="🌳 Grass Lands\n🏜️ Desert Dunes\n<:snowtree:1059258720531521596> Frost Wasteland\n🦧 Orangutan Jungle\n💎 Glass Desert\n<:amonguspog:886652968051560488> Ohio!!\n", color=0x11806A)
        view = buttonHandler()
        await interaction.response.send_message(embed = embed,view=view)


class SandTrue(discord.ui.View):
    #If statment in on_timeout that checks for lvl runs if true
    @discord.ui.button(label = "Start", style = discord.ButtonStyle.success)
    async def ex_button(self,interaction:discord.Interaction, button: discord.ui.Button):
        lvl_requirement_passed = lvl_requirements(interaction.user.id, 1)
        cat_avalible = cat_requirment(interaction.user.id)
        if cat_avalible == False:
            button.disabled = True
            await interaction.response.edit_message(view=self)
            await interaction.followup.send(content="Currently On An Adventure Try Again Later", ephemeral=True)
        elif lvl_requirement_passed == True:
            insert_data(5, interaction.user.id, "Sand")
            bot.loop.create_task(adventure_thread(5,interaction.user.id,"Sand"))
            await interaction.response.send_message(content="The Journey Has Began")
        else:
            #Show LVL needed and current 3.0
            button.disabled = True
            await interaction.response.edit_message(view=self)
            await interaction.followup.send(content="Lvl Too Low", ephemeral=True)
    @discord.ui.button(label = "Back", style = discord.ButtonStyle.grey)
    async def back(self,interaction:discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title="Adventure with Jasper (Selection Menu)",description="🌳 Grass Lands\n🏜️ Desert Dunes\n<:snowtree:1059258720531521596> Frost Wasteland\n🦧 Orangutan Jungle\n💎 Glass Desert\n<:amonguspog:886652968051560488> Ohio!!\n", color=0x11806A)
        view = buttonHandler()
        await interaction.response.send_message(embed = embed,view=view)
    

class SnowTrue(discord.ui.View):
    #If statment in on_timeout that checks for lvl runs if true
    @discord.ui.button(label = "Start", style = discord.ButtonStyle.success)
    async def ex_button(self,interaction:discord.Interaction, button: discord.ui.Button):
        lvl_requirement_passed = lvl_requirements(interaction.user.id, 1)
        cat_avalible = cat_requirment(interaction.user.id)
        if cat_avalible == False:
            button.disabled = True
            await interaction.response.edit_message(view=self)
            await interaction.followup.send(content="Currently On An Adventure Try Again Later", ephemeral=True)
        elif lvl_requirement_passed == True:
            insert_data(5, interaction.user.id, "Snow")
            bot.loop.create_task(adventure_thread(5,interaction.user.id,"Snow"))
            await interaction.response.send_message(content="The Journey Has Began")
        else:
            #Show LVL needed and current 3.0
            button.disabled = True
            await interaction.response.edit_message(view=self)
            await interaction.followup.send(content="Lvl Too Low", ephemeral=True)
    @discord.ui.button(label = "Back", style = discord.ButtonStyle.grey)
    async def back(self,interaction:discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title="Adventure with Jasper (Selection Menu)",description="🌳 Grass Lands\n🏜️ Desert Dunes\n<:snowtree:1059258720531521596> Frost Wasteland\n🦧 Orangutan Jungle\n💎 Glass Desert\n<:amonguspog:886652968051560488> Ohio!!\n", color=0x11806A)
        view = buttonHandler()
        await interaction.response.send_message(embed = embed,view=view)
    
class JungleTrue(discord.ui.View):
    #If statment in on_timeout that checks for lvl runs if true
    @discord.ui.button(label = "Start", style = discord.ButtonStyle.success)
    async def ex_button(self,interaction:discord.Interaction, button: discord.ui.Button):
        lvl_requirement_passed = lvl_requirements(interaction.user.id, 1)
        cat_avalible = cat_requirment(interaction.user.id)
        if cat_avalible == False:
            button.disabled = True
            await interaction.response.edit_message(view=self)
            await interaction.followup.send(content="Currently On An Adventure Try Again Later", ephemeral=True)
        elif lvl_requirement_passed == True:
            insert_data(5, interaction.user.id, "Jungle")
            bot.loop.create_task(adventure_thread(5,interaction.user.id,"Jungle"))
            await interaction.response.send_message(content="The Journey Has Began")
        else:
            #Show LVL needed and current 3.0
            button.disabled = True
            await interaction.response.edit_message(view=self)
            await interaction.followup.send(content="Lvl Too Low", ephemeral=True)
    @discord.ui.button(label = "Back", style = discord.ButtonStyle.grey)
    async def back(self,interaction:discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title="Adventure with Jasper (Selection Menu)",description="🌳 Grass Lands\n🏜️ Desert Dunes\n<:snowtree:1059258720531521596> Frost Wasteland\n🦧 Orangutan Jungle\n💎 Glass Desert\n<:amonguspog:886652968051560488> Ohio!!\n", color=0x11806A)
        view = buttonHandler()
        await interaction.response.send_message(embed = embed,view=view)
    
class GlassTrue(discord.ui.View):
    #If statment in on_timeout that checks for lvl runs if true
    @discord.ui.button(label = "Start", style = discord.ButtonStyle.success)
    async def ex_button(self,interaction:discord.Interaction, button: discord.ui.Button):
        lvl_requirement_passed = lvl_requirements(interaction.user.id, 1)
        cat_avalible = cat_requirment(interaction.user.id)
        if cat_avalible == False:
            button.disabled = True
            await interaction.response.edit_message(view=self)
            await interaction.followup.send(content="Currently On An Adventure Try Again Later", ephemeral=True)
        elif lvl_requirement_passed == True:
            insert_data(5, interaction.user.id, "Glass")
            bot.loop.create_task(adventure_thread(5,interaction.user.id,"Glass"))
            await interaction.response.send_message(content="The Journey Has Began")
        else:
            #Show LVL needed and current 3.0
            button.disabled = True
            await interaction.response.edit_message(view=self)
            await interaction.followup.send(content="Lvl Too Low", ephemeral=True)
    @discord.ui.button(label = "Back", style = discord.ButtonStyle.grey)
    async def back(self,interaction:discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title="Adventure with Jasper (Selection Menu)",description="🌳 Grass Lands\n🏜️ Desert Dunes\n<:snowtree:1059258720531521596> Frost Wasteland\n🦧 Orangutan Jungle\n💎 Glass Desert\n<:amonguspog:886652968051560488> Ohio!!\n", color=0x11806A)
        view = buttonHandler()
        await interaction.response.send_message(embed = embed,view=view)
    
class OhioTrue(discord.ui.View):
    #If statment in on_timeout that checks for lvl runs if true
    @discord.ui.button(label = "Start", style = discord.ButtonStyle.success)
    async def ex_button(self,interaction:discord.Interaction, button: discord.ui.Button):
        lvl_requirement_passed = lvl_requirements(interaction.user.id, 1)
        cat_avalible = cat_requirment(interaction.user.id)
        if cat_avalible == False:
            button.disabled = True
            await interaction.response.edit_message(view=self)
            await interaction.followup.send(content="Currently On An Adventure Try Again Later", ephemeral=True)
        elif lvl_requirement_passed == True:
            insert_data(5, interaction.user.id, "Ohio")
            bot.loop.create_task(adventure_thread(5,interaction.user.id,"Ohio"))
            await interaction.response.send_message(content="The Journey Has Began")
        else:
            #Show LVL needed and current 3.0
            button.disabled = True
            await interaction.response.edit_message(view=self)
            await interaction.followup.send(content="Lvl Too Low", ephemeral=True)
    @discord.ui.button(label = "Back", style = discord.ButtonStyle.grey)
    async def back(self,interaction:discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title="Adventure with Jasper (Selection Menu)",description="🌳 Grass Lands\n🏜️ Desert Dunes\n<:snowtree:1059258720531521596> Frost Wasteland\n🦧 Orangutan Jungle\n💎 Glass Desert\n<:amonguspog:886652968051560488> Ohio!!\n", color=0x11806A)
        view = buttonHandler()
        await interaction.response.send_message(embed = embed,view=view)
    


bot.run(TOKEN)