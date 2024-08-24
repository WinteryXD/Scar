# db - msg_id, user_id, guild_id


import asyncio
import discord
import os
import json
import pickle
import time
import datetime
from dotenv import load_dotenv
from discord.ui import Modal, InputText, View, Button, Select
from discord.utils import get
from discord.ext import commands
from dbutil import MessageDB
from dbutil import StartButtonDB
from dbutil import GuildAppDB
import math
from datetime import datetime 
from typing import Union
import random

from action import Action, ActionInteraction, actions

usable_actions = actions


load_dotenv()

TOKEN = os.getenv("TOKEN")
INVITE_LINK = os.getenv("INVITE_LINK")
SUPPORT_LINK = os.getenv("SUPPORT_LINK")
bot = discord.Bot(command_prefix='s.', intents=discord.Intents.default())
intents = discord.Intents.default()
intents.guilds = True



















# FORMULARIOS



async def load_extensions():
    for filename in os.listdir('./commands'):
        if filename.endswith('.py'):
            await bot.load_extension(f'commands.{filename[:-3]}')

async def setup(bot):
    await bot.add_cog(EmbedCreator(bot))
    await bot.tree.sync()

@bot.event
async def on_ready():
    bot.add_view(ApplicationButtonsView())
    bot.add_view(ApplicationStartButtonView())
    activity = discord.Activity(name=f"Skibidi Toilet - Super Sigma Remix", type=discord.ActivityType.listening)
    await bot.change_presence(activity=activity, status = discord.Status.idle)

    print("[💮]  Sincronização de servidores iniciada...")
    new_guild_count = 0
    for i in bot.guilds:
        if str(i.id) not in GuildAppDB.get_all_guilds():
            GuildAppDB.create_guild(str(i.id), i.name)
            new_guild_count+=1
            print(f"Entry para {i.id} criada")

    print(f"[🔑]  Logado como {bot.user}")
    
    await bot.sync_commands(force=True)
    print("[👍]  Sincronização de comandos concluída!")

@bot.event
async def on_guild_join(guild):
    GuildAppDB.create_guild(str(guild.id), guild.name)
    print(f"[📢]  O bot foi adicionado ao servidor {guild.name}: {guild.id}")

@bot.event
async def on_guild_remove(guild):
    print(f"[🗑️]  Removido do servidor {guild.name}: {guild.id}")

@bot.event
async def on_application_command_error(ctx: discord.ApplicationContext, error: discord.DiscordException):
    if isinstance(error, commands.MissingPermissions):
        await ctx.respond("❌  Você precisa de permissões de Administrador para utilizar este comando!", ephemeral=True)
        print(f"{ctx.guild.name} {ctx.user.display_name} needs admin")
    else:
        raise error  # Error go brrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr


@bot.slash_command(name="list_servers", description="Lista os servidores em que fui adicionado.")
async def list_servers(interaction: discord.Interaction):
    # Verifica se o comando foi executado pelo usuário com o ID correto
    if interaction.user.id != 378723181139329024:
        await interaction.response.send_message("❌  Você não tem permissão para usar este comando: Este comando só pode ser utilizado pela desenvolvedora do bot.", ephemeral=True)
        return
    
    # Gera a lista de servidores
    server_list = "\n".join([f'`{guild.name}` \n ⌞ ID: {guild.id}' for guild in bot.guilds])
    
    # Envia a mensagem apenas para o usuário que executou o comando (ephemeral=True)
    await interaction.response.send_message(f"`🛜`  **SERVIDORES CONECTADOS**\n{server_list}", ephemeral=True)



@bot.slash_command(description = "Um comando de ajuda")
async def help(ctx):
    embed = discord.Embed(title="`💮`  Precisa de ajuda? :3", description="Hai! Me chamo `Scar`! \nTodos os meus comandos são usados com Slash, não se confunda, hein! \nCaso queira gerenciar aplicações, você precisará de permissão de Administrador.")
    embed.add_field(name=f"```/application create [nome]```", value="Cria uma nova aplicação", inline=False)
    embed.add_field(name=f"```/application response_channel```", value="Define o canal para serem enviadas as aplicações. **[Importante]**", inline=False)
    embed.add_field(name=f"```/application remove [nome]```", value="Remove a aplicação especificada.", inline=False)
    embed.add_field(name=f"```/application list```", value="Lista todas as aplicações", inline=False)
    embed.add_field(name=f"```/application editor```", value="Abre o editor para a aplicação", inline=False)
    embed.add_field(name=f"```/application actions```", value="Abre um editor de ações para a aplicação", inline=False)
    embed.add_field(name=f"```/start_button```", value="Cria o prompt para a aplicação dos membros", inline=False)
    await ctx.response.send_message(embed=embed, ephemeral=True)

@commands.has_permissions(administrator=True)
@bot.slash_command(description = "Comando usado para configurar o Prompt de Aplicação")
async def start_button(ctx):
    view = discord.ui.View()
    options = SelectApplicationStartButton(max_values=1, placeholder="📩  Selecione a aplicação")
    applications = GuildAppDB.get_applications(str(ctx.guild.id))
    if len(applications) == 0:
        await ctx.response.send_message(content="❌  Não existe uma configuração para aplicações. \nCrie uma aplicação antes.", ephemeral=True)
        return
    for i in applications:
        options.add_option(label=i, value=i)
    view.add_item(options)
    await ctx.response.send_message(view=view, ephemeral=True)

@start_button.error
async def on_application_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.respond("❌  Você precisa de permissões de Administrador para utilizar este comando.", ephemeral=True)
    else:
        raise error


#@bot.command(description="Posts invite button for the bot")
#async def invite(ctx):
    #view = discord.ui.View()
    #invite_button = discord.ui.Button(label="Invite", style=discord.ButtonStyle.link, url=INVITE_LINK)
    #view.add_item(invite_button)
    #embed = discord.Embed(title="Invite Me", color=0x70ff50, description="If you like the bot and want to invite it to other servers, click the button below")
    #embed.set_footer(text="Made by @anorak01", icon_url="https://cdn.discordapp.com/avatars/269164865480949760/a1af9962da20d5ddaa136043cf45d015?size=1024")
    #try:
    #    await ctx.response.send_message(embed=embed, view=view)
   # except discord.HTTPException as e:
  #      await ctx.response.send_message(content="It looks like the bot owner didn't set up this link correctly")
 #       raise e

#@bot.command(description="Posts support button for the bot")
#async def support(ctx):
    #view = discord.ui.View()
    #invite_button = discord.ui.Button(label="Support server", style=discord.ButtonStyle.link, url=SUPPORT_LINK)
    #view.add_item(invite_button)
    #embed = discord.Embed(title="Support", color=0x70ff50, description="If you're having issues with the bot, you can join my support server with the button below")
    #embed.set_footer(text="Made by @anorak01", icon_url="https://cdn.discordapp.com/avatars/269164865480949760/a1af9962da20d5ddaa136043cf45d015?size=1024")
    #try:
    #    await ctx.response.send_message(embed=embed, view=view)
   # except discord.HTTPException as e:
  #      await ctx.response.send_message(content="It looks like the bot owner didn't set up this link correctly")
 #       raise e

#@bot.command(description="Leave a review", id="review", name="review")
#async def review(ctx):
#    view = discord.ui.View()
#    invite_button = discord.ui.Button(label="Review", style=discord.ButtonStyle.link, url="https://top.gg/bot/1143622923136024767#reviews")
 #   view.add_item(invite_button)
  #  embed = discord.Embed(title="Review", color=0x70ff50, description="If you like the bot, please consider leaving a review and upvote my bot, it will really help a lot!")
   # embed.set_footer(text="Made by @anorak01", icon_url="https://cdn.discordapp.com/avatars/269164865480949760/a1af9962da20d5ddaa136043cf45d015?size=1024")
   #await ctx.response.send_message(embed=embed, view=view)

application = discord.SlashCommandGroup("application", "O comando principal para gerenciar aplicações.")

@commands.has_permissions(administrator=True)
@application.command(description="Cria uma nova aplicação totalmente personalizável.")
async def create(ctx, application):
    if len(application) < 40:
        result = GuildAppDB.add_application_entry(str(ctx.guild.id), application)
        if result == "success":
            view = discord.ui.View()
            options = SelectResponseChannel(select_type=discord.ComponentType.channel_select, channel_types=[discord.ChannelType.text], max_values=1, placeholder="Select channel")
            options.set_app_name(application)
            view.add_item(options)
            await ctx.response.send_message(f"Aplicação criada: {application}\n\nSelecione um canal para enviar as aplicações:", ephemeral=True, view=view) # create a new application, modal with name ask
    else:
        await ctx.response.send_message(f"❌  Escolha um nome diferente!", ephemeral=True)

@commands.has_permissions(administrator=True)
@application.command(description="Remove uma aplicação de sua escolha.")
async def remove(ctx, application):
    result = GuildAppDB.remove_application_entry(str(ctx.guild.id), application)
    if result == "success":
        await ctx.response.send_message(f"🗑️  Aplicação removida com sucesso: {application}", ephemeral=True)
    else:
        await ctx.response.send_message(f"❌  Aplicação {application} não encontrada.", ephemeral=True)

@commands.has_permissions(administrator=True)
@application.command(description="Lista todas as aplicações")
async def list(ctx):
    applications = GuildAppDB.get_applications(str(ctx.guild.id))
    embed = discord.Embed(title="**Lista de Aplicações**")
    embed.set_footer(text="Scar - System", icon_url="https://cdn.discordapp.com/avatars/1239736590184611880/77384c5b97174281d898e4fd676b3e43.webp")
    if len(applications) == 0:
        embed.title="❌  Você ainda não criou nenhuma aplicação."
    else:
        for i, app in enumerate(applications):
            embed.add_field(value=f"**{i+1}. {app}**", name="", inline=False)
    await ctx.response.send_message(embed=embed, ephemeral=True)

@commands.has_permissions(administrator=True)
@application.command(description="Abre o editor para a aplicação selecionada")
async def editor(ctx):
    view = discord.ui.View()
    options = SelectApplicationOptionsEditor(max_values=1, placeholder="📩  Selecione a aplicação")
    for i in GuildAppDB.get_applications(str(ctx.guild.id)):
        options.add_option(label=i, value=i)
    view.add_item(options)
    await ctx.response.send_message(view=view, ephemeral=True)

@commands.has_permissions(administrator=True)
@application.command(description="Abre o Painel de Ações.")
async def actions(ctx):
    view = discord.ui.View()
    options = SelectActionOptionsEditor(max_values=1, placeholder="📩  Selecione a aplicação")
    for i in GuildAppDB.get_applications(str(ctx.guild.id)):
        options.add_option(label=i, value=i)
    view.add_item(options)
    await ctx.response.send_message(view=view, ephemeral=True)

@commands.has_permissions(administrator=True)
@application.command(description="📝  Selecione o canal para enviar as aplicações:")
async def response_channel(ctx):
    view = discord.ui.View()
    options = SelectApplicationOptionsRespChannel(max_values=1, placeholder="📩  Selecione a aplicação")
    for i in GuildAppDB.get_applications(str(ctx.guild.id)):
        options.add_option(label=i, value=i)
    view.add_item(options)
    await ctx.response.send_message(view=view, ephemeral=True)

bot.add_application_command(application) # add application group commands


def get_questions_embed(guild_id, application) -> discord.Embed:
    embed = discord.Embed(title=f"Aplicação: {application}")
    questions, length = GuildAppDB.get_questions(str(guild_id), application)
    for i, que in enumerate(questions):
        embed.add_field(value=f"**{i+1}. {que}**", name="", inline=False)
    embed.set_footer(text="Scar - System", icon_url="https://cdn.discordapp.com/avatars/1239736590184611880/77384c5b97174281d898e4fd676b3e43.webp")
    return embed


class SelectApplicationStartButton(discord.ui.Select):
    async def callback(self, interaction: discord.Interaction):
        self.disabled = True

        embed = discord.Embed(title="🌟  **Inicie sua aplicação aqui!**")
        embed.add_field(name=f"Clique no botão abaixo para iniciar sua aplicação de: {self.values[0]}", value="", inline=False)
        embed.set_footer(text="Scar - System", icon_url="https://cdn.discordapp.com/avatars/1239736590184611880/77384c5b97174281d898e4fd676b3e43.webp")
        appStartView = ApplicationStartButtonView()

        try:
            message = await interaction.channel.send(embed = embed, view=appStartView)
        except discord.errors.Forbidden:
            await interaction.response.edit_message(content="❌  Sem acesso para enviar mensagens", view=None)
            return
        await interaction.response.edit_message(embed=None, content="Botão da aplicação criado", view=None)
        StartButtonDB.add_start_msg(str(message.id), str(self.values[0]), str(interaction.guild.id))


class SelectResponseChannelView(discord.ui.View):
    @discord.ui.select(
        select_type=discord.ComponentType.channel_select,
        channel_types=[discord.ChannelType.text],
        max_values=1
    )
    async def select_callback(self, select, interaction: discord.Interaction):
        self.disable_all_items()
        GuildAppDB.set_response_channel(interaction.guild.id, )
        await interaction.response.edit_message(content=f"♾️  Canal selecionado: {select.values[0].mention}", view=None)


class SelectApplicationOptionsEditor(discord.ui.Select):
    async def callback(self, interaction: discord.Interaction):
        self.disabled = True
        editor = ApplicationEditorView(str(interaction.guild.id), self.values[0])
        embed = get_questions_embed(str(interaction.guild.id), self.values[0])
        await interaction.response.edit_message(embed = embed, view=editor)

class SelectApplicationOptionsRespChannel(discord.ui.Select):
    async def callback(self, interaction: discord.Interaction):
        self.disabled = True
        view = discord.ui.View()
        options = SelectResponseChannel(select_type=discord.ComponentType.channel_select, channel_types=[discord.ChannelType.text], max_values=1, placeholder="Selecione o canal")
        options.set_app_name(self.values[0])
        view.add_item(options)
        await interaction.response.edit_message(view=view)

class SelectResponseChannel(discord.ui.Select):
    def set_app_name(self, app_name):
        self.app_name = app_name

    async def callback(self, interaction: discord.Interaction):
        self.disabled = True
        GuildAppDB.set_response_channel(str(interaction.guild.id), self.app_name, str(self.values[0].id))
        await interaction.response.edit_message(content=f"♾️  Canal selecionado: {self.values[0].mention} para aplicação: {self.app_name}", view=None)

class ApplicationEditorView(discord.ui.View):
    def __init__(self, guild_id, application_name):
        super().__init__(timeout=180)
        self.guild_id = guild_id
        self.application_name = application_name

    @discord.ui.button(
        label="Novo",
        style=discord.ButtonStyle.green,
        custom_id="editor:add",
        row=0
    )
    async def add_question(self, button: discord.ui.Button, interaction: discord.Interaction):
        modal = AddQuestionModal(self.application_name)
        await interaction.response.send_modal(modal)

    @discord.ui.button(
        label="Remover",
        style=discord.ButtonStyle.red,
        custom_id="editor:remove",
        row=0
    )
    async def remove_question(self, button, interaction: discord.Interaction):
        view = ApplicationEditorView(str(interaction.guild.id), self.application_name)
        options = RemoveQuestionSelect(max_values=1, placeholder="📩  Selecione uma pergunta para remover")
        options.set_app_name(self.application_name)
        questions, length = GuildAppDB.get_questions(str(interaction.guild.id), self.application_name)
        if length == 0:
            await interaction.response.edit_message(view=view)
            return
        for i, que in enumerate(questions):
            if len(que) > 100:
                options.add_option(label=f"{str(i+1)}. {que[0:90]}..", value=str(i))
            else:
                options.add_option(label=f"{str(i+1)}. {que}", value=str(i))
        view.add_item(options)
        await interaction.response.edit_message(view=view)

    @discord.ui.button(
        label="Editar",
        style=discord.ButtonStyle.primary,
        custom_id="editor:edit",
        row=0
    )
    async def edit_question(self, button, interaction: discord.Interaction):
        view = ApplicationEditorView(str(interaction.guild.id), self.application_name)
        options = EditQuestionSelect(max_values=1, placeholder="📩  Selecione uma pergunta para editar")
        options.set_app_name(self.application_name)
        questions, length = GuildAppDB.get_questions(str(interaction.guild.id), self.application_name)
        if length == 0:
            await interaction.response.edit_message(view=view)
            return
        for i, que in enumerate(questions):
            if len(que) > 100:
                options.add_option(label=f"{str(i+1)}. {que[0:90]}..", value=str(i))
            else:
                options.add_option(label=f"{str(i+1)}. {que}", value=str(i))
        view.add_item(options)
        await interaction.response.edit_message(view=view)

    @discord.ui.button(
        label="Mover",
        style=discord.ButtonStyle.gray,
        custom_id="editor:move",
        row=0
    )
    async def move_question(self, button, interaction: discord.Interaction):
        view = ApplicationEditorView(str(interaction.guild.id), self.application_name)
        options = MoveQuestionSelect(max_values=1, placeholder="📩  Selecione uma pergunta para mover")
        options.set_app_name(self.application_name)
        questions, length = GuildAppDB.get_questions(str(interaction.guild.id), self.application_name)
        if length == 0:
            await interaction.response.edit_message(view=view)
            return
        for i, que in enumerate(questions):
            if len(que) > 100:
                options.add_option(label=f"{str(i+1)}. {que[0:90]}..", value=str(i))
            else:
                options.add_option(label=f"{str(i+1)}. {que}", value=str(i))
        view.add_item(options)
        await interaction.response.edit_message(view=view)


class AddQuestionModal(discord.ui.Modal):
    def __init__(self, app_name):
        self.app_name = app_name
        super().__init__(discord.ui.InputText(label=f"➕  Nova pergunta: "), title = "")

    async def callback(self, interaction: discord.Interaction):
        question = self.children[0].value
        if len(question) > 250:
            await interaction.response.send_message(f"❌  Pergunta muito longa, o máximo de caracteres é 100!", ephemeral=True)
            return
        GuildAppDB.add_question(str(interaction.guild.id), self.app_name, question)
        embed = get_questions_embed(str(interaction.guild.id), self.app_name)
        await interaction.response.edit_message(embed=embed)


class RemoveQuestionSelect(discord.ui.Select):
    def set_app_name(self, app_name):
        self.app_name = app_name

    async def callback(self, interaction: discord.Interaction):
        self.disabled = True
        GuildAppDB.remove_question(str(interaction.guild.id), self.app_name, int(self.values[0])+1)
        editor = ApplicationEditorView(str(interaction.guild.id), self.app_name)
        embed = get_questions_embed(str(interaction.guild.id), self.app_name)
        await interaction.response.edit_message(embed = embed, view = editor)


class EditQuestionSelect(discord.ui.Select):
    def set_app_name(self, app_name):
        self.app_name = app_name

    async def callback(self, interaction: discord.Interaction):
        self.disabled = True
        editor = ApplicationEditorView(str(interaction.guild.id), self.app_name)
        modal = EditQuestionModal(self.app_name, int(self.values[0])+1)
        await interaction.response.send_modal(modal)
        await interaction.followup.edit_message(view = editor, message_id=interaction.message.id)

class EditQuestionModal(discord.ui.Modal):
    def __init__(self, app_name, question_index):
        self.app_name = app_name
        self.question_index = question_index
        super().__init__(discord.ui.InputText(label=f"✏️  Pergunta editada: "), title = "")

    async def callback(self, interaction: discord.Interaction):
        question = self.children[0].value
        GuildAppDB.edit_question(str(interaction.guild.id), self.app_name, self.question_index, question)
        embed = get_questions_embed(str(interaction.guild.id), self.app_name)
        await interaction.response.edit_message(embed=embed)


class MoveQuestionSelect(discord.ui.Select):
    def set_app_name(self, app_name):
        self.app_name = app_name

    async def callback(self, interaction: discord.Interaction):
        self.disabled = True
        view = ApplicationEditorView(str(interaction.guild.id), self.app_name)
        options = MoveQuestionSelectNum(max_values=1, placeholder="📩  Selecione o lugar para mover")
        options.set_app_name(self.app_name)
        options.set_init_index(int(self.values[0])+1)
        questions, length = GuildAppDB.get_questions(str(interaction.guild.id), self.app_name)
        for i in range(length):
            options.add_option(label=str(i+1), value=str(i+1))
        view.add_item(options)
        await interaction.response.edit_message(view = view)

class MoveQuestionSelectNum(discord.ui.Select):
    def set_app_name(self, app_name):
        self.app_name = app_name

    def set_init_index(self, init_index: int):
        self.init_index = init_index

    async def callback(self, interaction: discord.Interaction):
        self.disabled = True
        editor = ApplicationEditorView(str(interaction.guild.id), self.app_name)
        GuildAppDB.move_question(str(interaction.guild.id), self.app_name, int(self.init_index), int(self.values[0]))
        embed = get_questions_embed(str(interaction.guild.id), self.app_name)
        await interaction.response.edit_message(view = editor, embed=embed)



def get_actions_embed(guild_id, application, action_type: ActionInteraction) -> discord.Embed:
    embed = discord.Embed(title=f"Aplicação: {application}", description=f"🔮  Ações acontecendo em: {action_type.value}")
    actions = GuildAppDB.get_actions(str(guild_id), application, action_type)
    for i, que in enumerate(actions):
        if que["action_type"] == "add_role":
            role = bot.get_guild(int(guild_id)).get_role(que["data"]["role_id"]).name
            embed.add_field(value=f"**{i+1}. {que['display_type']}: {role}**", name="", inline=False)
        else:
            embed.add_field(value=f"**{i+1}. {que['display_type']}**", name="", inline=False)
    embed.set_footer(text="Scar - System", icon_url="https://cdn.discordapp.com/avatars/1239736590184611880/77384c5b97174281d898e4fd676b3e43.webp")
    return embed

class ActionAcceptEditorView(discord.ui.View):
    def __init__(self, guild_id, application_name):
        super().__init__(timeout=180)
        self.guild_id = guild_id
        self.application_name = application_name

    @discord.ui.button(
        label="➕",
        style=discord.ButtonStyle.green,
        custom_id="action_accept_editor:add",
        row=0
    )
    async def add_action(self, button: discord.ui.Button, interaction: discord.Interaction):
        view = ActionAcceptEditorView(str(interaction.guild.id), self.application_name)
        options = AddActionSelect(max_values=1, placeholder="📩  Selecione uma ação para adicionar")
        options.set_app_name(self.application_name)
        options.set_action_type(ActionInteraction.ACCEPT)
        for i, que in enumerate(usable_actions):
            options.add_option(label=f"{str(i+1)}. {que}", value=str(usable_actions[que]))
        view.add_item(options)
        await interaction.response.edit_message(view=view)

    @discord.ui.button(
        label="➖",
        style=discord.ButtonStyle.red,
        custom_id="action_accept_editor:remove",
        row=0
    )
    async def remove_action(self, button, interaction: discord.Interaction):
        view = ActionAcceptEditorView(str(interaction.guild.id), self.application_name)
        options = RemoveActionSelect(max_values=1, placeholder="📩  Selecione uma ação para remover")
        options.set_app_name(self.application_name)
        actions = GuildAppDB.get_actions(str(interaction.guild.id), self.application_name, action_type=ActionInteraction.ACCEPT)
        options.set_action_type(ActionInteraction.ACCEPT)
        if len(actions) == 0:
            await interaction.response.edit_message(view=view)
            return
        for i, que in enumerate(actions):
            if que["action_type"] == "add_role":
                role = interaction.guild.get_role(que["data"]["role_id"]).name
                options.add_option(label=f"{str(i+1)}. {que['display_type']}: {role}", value=str(i))
            else:
                options.add_option(label=f"{str(i+1)}. {que['display_type']}", value=str(i))
        view.add_item(options)
        await interaction.response.edit_message(view=view)

class ActionDeclineEditorView(discord.ui.View):
    def __init__(self, guild_id, application_name):
        super().__init__(timeout=180)
        self.guild_id = guild_id
        self.application_name = application_name

    @discord.ui.button(
        label="➕",
        style=discord.ButtonStyle.green,
        custom_id="action_decline_editor:add",
        row=0
    )
    async def add_action(self, button: discord.ui.Button, interaction: discord.Interaction):
        view = ActionDeclineEditorView(str(interaction.guild.id), self.application_name)
        options = AddActionSelect(max_values=1, placeholder="📩  Selecione uma ação para adicionar")
        options.set_app_name(self.application_name)
        options.set_action_type(ActionInteraction.DECLINE)
        for i, que in enumerate(usable_actions):
            options.add_option(label=f"{str(i+1)}. {que}", value=str(usable_actions[que]))
        view.add_item(options)
        await interaction.response.edit_message(view=view)

    @discord.ui.button(
        label="➖",
        style=discord.ButtonStyle.red,
        custom_id="action_decline_editor:remove",
        row=0
    )
    async def remove_action(self, button, interaction: discord.Interaction):
        view = ActionDeclineEditorView(str(interaction.guild.id), self.application_name)
        options = RemoveActionSelect(max_values=1, placeholder="📩  Selecione uma ação para remover")
        options.set_app_name(self.application_name)
        actions = GuildAppDB.get_actions(str(interaction.guild.id), self.application_name, action_type=ActionInteraction.DECLINE)
        options.set_action_type(ActionInteraction.DECLINE)
        if len(actions) == 0:
            await interaction.response.edit_message(view=view)
            return
        for i, que in enumerate(actions):
            if que["action_type"] == "add_role":
                role = interaction.guild.get_role(que["data"]["role_id"]).name
                options.add_option(label=f"{str(i+1)}. {que['display_type']}: {role}", value=str(i))
            else:
                options.add_option(label=f"{str(i+1)}. {que['display_type']}", value=str(i))
        view.add_item(options)
        await interaction.response.edit_message(view=view)

class AddActionSelect(discord.ui.Select):
    def set_app_name(self, app_name):
        self.app_name = app_name

    def set_action_type(self, action_type):
        self.action_type = action_type

    async def callback(self, interaction: discord.Interaction):
        self.disabled = True
        action = self.values[0]
        if action == "add_role":
            view = discord.ui.View()
            options = SelectRoleToAdd(select_type=discord.ComponentType.role_select, max_values=1, placeholder="📩  Selecione um cargo para adicionar")
            options.set_app_name(self.app_name)
            options.set_action_type(self.action_type)
            view.add_item(options)
            await interaction.response.edit_message(view=view)

class SelectRoleToAdd(discord.ui.Select):
    def set_app_name(self, app_name):
        self.app_name = app_name

    def set_action_type(self, action_type):
        self.action_type = action_type

    async def callback(self, interaction: discord.Interaction):
        self.disabled = True
        role = self.values[0]
        action = {"result": self.action_type, "action_type": "add_role", "display_type": "Add Role", "data": {"role_id": role.id}}
        GuildAppDB.add_action(str(interaction.guild.id), self.app_name, action)
        if self.action_type == ActionInteraction.ACCEPT:
            editor = ActionAcceptEditorView(str(interaction.guild.id), self.app_name)
            embed = get_actions_embed(str(interaction.guild.id), self.app_name, ActionInteraction.ACCEPT)
        if self.action_type == ActionInteraction.DECLINE:
            editor = ActionDeclineEditorView(str(interaction.guild.id), self.app_name)
            embed = get_actions_embed(str(interaction.guild.id), self.app_name, ActionInteraction.DECLINE)
        await interaction.response.edit_message(embed = embed, view = editor)


class RemoveActionSelect(discord.ui.Select):
    def set_app_name(self, app_name):
        self.app_name = app_name

    def set_action_type(self, action_type: ActionInteraction):
        self.action_type = action_type

    async def callback(self, interaction: discord.Interaction):
        self.disabled = True
        GuildAppDB.remove_action(str(interaction.guild.id), self.app_name, self.action_type, int(self.values[0])+1)
        if self.action_type == ActionInteraction.ACCEPT:
            editor = ActionAcceptEditorView(str(interaction.guild.id), self.app_name)
            embed = get_actions_embed(str(interaction.guild.id), self.app_name, ActionInteraction.ACCEPT)
        if self.action_type == ActionInteraction.DECLINE:
            editor = ActionDeclineEditorView(str(interaction.guild.id), self.app_name)
            embed = get_actions_embed(str(interaction.guild.id), self.app_name, ActionInteraction.DECLINE)
        await interaction.response.edit_message(embed = embed, view = editor)


class SelectActionOptionsEditor(discord.ui.Select):
    async def callback(self, interaction: discord.Interaction):
        self.disabled = True

        view = discord.ui.View()
        options = SelectActionType(max_values=1, placeholder="Tipo de Select Action™")
        options.add_option(label="✅", value="aprovar")
        options.add_option(label="❌", value="reprovar")
        options.set_app_name(self.values[0])
        view.add_item(options)
        await interaction.response.edit_message(view=view)

class SelectActionType(discord.ui.Select):
    def set_app_name(self, app_name):
        self.app_name = app_name

    async def callback(self, interaction: discord.Interaction):
        self.disabled = True
        if self.values[0] == "aprovar":
            editor = ActionAcceptEditorView(str(interaction.guild.id), self.app_name)
            embed = get_actions_embed(str(interaction.guild.id), self.app_name, ActionInteraction.ACCEPT)
        if self.values[0] == "reprovar":
            editor = ActionDeclineEditorView(str(interaction.guild.id), self.app_name)
            embed = get_actions_embed(str(interaction.guild.id), self.app_name, ActionInteraction.DECLINE)
        await interaction.response.edit_message(embed = embed, view=editor)



# View with button that starts the application process
class ApplicationStartButtonView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="📩  Iniciar aplicação!",
        style=discord.ButtonStyle.green,
        custom_id=f"persistent:start_application",
    )
    async def start_app(self, button: discord.ui.Button, interaction: discord.Interaction):
        app_name, guild_id = StartButtonDB.get_start_msg(interaction.message.id)

        questions, max_questions=GuildAppDB.get_questions(guild_id, app_name)
        if questions == "error on get questions: application not found":
            await interaction.response.send_message(content="`❌`  A aplicação não existe mais!", ephemeral=True)
            return
        if max_questions == 0:
            await interaction.response.send_message(content="`❌`  A aplicação não possui nenhuma pergunta!", ephemeral=True)
            return
        response_channel = GuildAppDB.get_response_channel(guild_id, app_name)

        user = await interaction.user.create_dm()
        embedd = discord.Embed(title=f'`📧`  {interaction.guild.name} - Aplicação', description="Sua aplicação foi iniciada! Você possui **5 minutos** para concluir.")
        embedd.add_field(value="- Respostas com mais de 1000 caracteres serão encurtadas.", name="", inline=False)
        embedd.add_field(value=f'- Você pode cancelar seu formulário a qualquer momento digitando "cancelar" em qualquer pergunta.', name="", inline=False)
        embedd.add_field(value=f'- DICA: Evite usar respostas vagas! A equipe deste servidor pode te reprovar por falta de informações em seu formulário.', name="", inline=False)
        embedd.set_footer(text="Scar - System", icon_url="https://cdn.discordapp.com/avatars/1239736590184611880/77384c5b97174281d898e4fd676b3e43.webp")
        
        try:
            first_mes = await user.send(embed=embedd)
        except discord.Forbidden:
            await interaction.response.send_message(content="`❗` Não foi possível iniciar seu formulário: Esta ação requer que suas **Mensagens Diretas** sejam ativadas em suas **Configurações de Privacidade**.", ephemeral=True)
            return

        await interaction.response.send_message(content=f"`✔️`  Aplicação iniciada! Clique aqui para começar a responder: {user.jump_url}", ephemeral=True)

        time_now = time.time()

        application = {'userId': interaction.user.id}

        for i in range(0, max_questions):
            try:
                embed = discord.Embed(title=f'`📝`  Pergunta [{i+1}/{max_questions}]', description=questions[i])
                await user.send(embed=embed)
                response = await bot.wait_for('message', check=lambda m: m.author == interaction.user and m.channel == user, timeout=300)
                if response.content.startswith("cancelar"):
                    await user.send("`🗑️` Sua aplicação foi cancelada.")
                    return
                else:
                    application[f'question{i}'] = response.content[0:1000]
            except asyncio.TimeoutError:
                await user.send(content="`⏰`  Visto que você não respondeu em 5 minutos, seu formulário foi finalizado.")
                return

        channel = bot.get_channel(int(response_channel))

        app_time = time.time() - time_now
        time_rounded = round(app_time, 2)

        #embed_start = discord.Embed(title=f"**{interaction.user.display_name}**'s application for {app_name}") #User:` {interaction.user.display_name}\n`User Mention:` {interaction.user.mention}")
        
        text_representation = ""
        send_as_file = False
        
        embed_text_len = 0 # limit 6k characters, but ideally less
        question_embeds = []
        embee = discord.Embed(title=f"`📄`  Aplicação de **{interaction.user.display_name}** em {app_name}") # create first embed
        for i in range(0, max_questions):
            if embed_text_len > 5000: # if the first embed is full, create new one
                question_embeds.append(embee)
                embee = discord.Embed()
                embed_text_len = 0
                send_as_file = True
			
            embee.add_field(name=f'{questions[i]}', value=application[f'question{i}'], inline=False)
            embed_text_len += len(questions[i]) + len(application[f'question{i}'])
            text_representation += questions[i] + ":\n" + application[f'question{i}'] + "\n\n"
        question_embeds.append(embee)

        embed_controls = discord.Embed()
        embed_controls.add_field(name="`📊`  Análises da Aplicação", value=f"""
                        `⏳`  **Tempo levado para conclusão**: *{time_rounded} segundo(s)*
                        `📧`  **Menção do usuário**: {interaction.user.mention}
                        `📁`  **ID do usuário**: *{interaction.user.id}*
                        `🕛`  **Conta criada**: <t:{round(interaction.user.created_at.timestamp())}:R>
                        """)

        embed_controls.set_thumbnail(url=interaction.user.display_avatar.url)
        embed_controls.set_footer(text="Scar - System", icon_url="https://cdn.discordapp.com/avatars/1239736590184611880/77384c5b97174281d898e4fd676b3e43.webp")
       # await channel.send(f"")

        question_embeds.append(embed_controls)
        #for embe in question_embeds:
        #    await channel.send(embed=embe)

        appView = ApplicationButtonsView()

        if send_as_file:
            from io import StringIO
            text_file = StringIO(text_representation)
            text_file = discord.File(text_file, filename="application.txt")
            last_msg = await channel.send(content="`📨`  Aplicação muito longa para ser enviada por texto. Enviada como arquivo.", view=appView, file=text_file, embed=embed_controls)

        else:
            last_msg = await channel.send(embeds=question_embeds, view=appView)

        MessageDB.add_application_msg(last_msg.id, interaction.user.id, interaction.guild.id, app_name)

        await user.send('`✅`  Yipeee! Sua aplicação foi enviada! Agora é só esperar um membro da equipe do servidor te aprovar, cheque o servidor com frequência e obrigada pela sua aplicação! :3')


# View containing accept and decline buttons for each application
class ApplicationButtonsView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="✔️",
        style=discord.ButtonStyle.green,
        custom_id=f"persistent:accept",
    )
    async def accept(self, button: discord.ui.Button, interaction: discord.Interaction):
        msg_id = str(interaction.message.id)

        user_id, guild_id, app_name = MessageDB.get_application_msg(msg_id)
        user = await bot.get_or_fetch_user(user_id)
        modal = ApplicationModal(title=f"`❕`  Você está prestes a aprovar: {user.display_name}, tem certeza disso?")
        modal.set_action("acc")
       # modal.add_item(discord.ui.InputText(label=f"Mensagem adicional: "))
        await interaction.response.send_modal(modal)

    @discord.ui.button(
        label="✖️",
        style=discord.ButtonStyle.red,
        custom_id=f"persistent:decline",
    )
    async def decline(self, button: discord.ui.Button, interaction: discord.Interaction):
        msg_id = str(interaction.message.id)

        user_id, guild_id, app_name = MessageDB.get_application_msg(msg_id)

        user = await bot.get_or_fetch_user(user_id)
        modal = ApplicationModal(title=f"`❕`  Você está prestes a reprovar: {user.display_name}, tem certeza disso?")
        modal.set_action("dec")
        modal.add_item(discord.ui.InputText(label=f"`🛑`  Motivo definido pelo moderador: "))
        await interaction.response.send_modal(modal)


# Modal functioning as a callback for Accepting/Declining application
class ApplicationModal(discord.ui.Modal):
    def set_action(self, action):
        self.action = action

    async def callback(self, interaction: discord.Interaction):
        reason = self.children[0].value
        msg_id = str(interaction.message.id)
        user_id, guild_id, app_name = MessageDB.get_application_msg(msg_id)
        if self.action == "acc":
            user = await bot.get_or_fetch_user(user_id)
            user = await user.create_dm()
            try:
                await user.send(f"`🎊`  Seu registro foi aceito! Divirta-se em nosso servidor e não se esqueça de ler as regras! :3")
            except discord.errors.Forbidden as e:
                await interaction.response.send_message(content="`❌`  Não foi possível enviar mensagens a este usuário.\nEle provavelmente não está mais no servidor.", ephemeral=True)
                return
            await user.send(f"Motivo: {reason}")
            await interaction.response.send_message(content="`✅`  Aplicação aceita com sucesso!", ephemeral=True)

            actions = GuildAppDB.get_actions(str(guild_id), app_name, ActionInteraction.ACCEPT)
            for i in actions:
                if i["action_type"] == "add_role":
                    role = interaction.message.guild.get_role(int(i["data"]["role_id"]))
                    try:
                        user = await interaction.message.guild.fetch_member(int(user_id))
                    except:
                        print("[❌]  Não foi possível processar a ação, usuário não encontrado.")
                    try:
                        await user.add_roles(role)
                    except Exception as e:
                        await interaction.followup.send(content=f"❌  Não foi possível adicionar o cargo `{role.name}`: Sem permissão.")
                else:
                    print("[❌]  Ação desconhecida.")

            emb = interaction.message.embeds[0]
            emb.colour = discord.Colour.green()
            embed = discord.Embed(title='`✅`  Este usuário foi aprovado.')
            embed.add_field(name="", value=f"`🛑`  **Motivo definido pelo moderador**: {reason}\n`📧`  **Por**: {interaction.user.mention}\n`🕛`  **Horário**: <t:{round(time.time())}:f>")
            embed.colour = discord.Colour.green()
            await interaction.followup.edit_message(message_id = interaction.message.id, embeds=[emb, embed])
            view = discord.ui.View.from_message(interaction.message)
            view.disable_all_items()
            await interaction.followup.edit_message(message_id = interaction.message.id, view = view)


        if self.action == "dec":
            user = await bot.get_or_fetch_user(user_id)
            user = await user.create_dm()
            try:
                await user.send(f"`❌`  Lamentamos, mas seu registro foi negado. **Dica**: ||Não deixe suas respostas muito vagas, precisamos te conhecer direitinho!||")
            except discord.errors.Forbidden as e:
                await interaction.response.send_message(content="`❌`  Não foi possível enviar mensagens a este usuário.\nProvavelmente ele não está mais no servidor.", ephemeral=True)
                return
            await user.send(f"`🛑`  **Motivo definido pelo moderador**: {reason}")
            await interaction.response.send_message(content="[❎]  Aplicação negada com sucesso!", ephemeral=True)

            actions = GuildAppDB.get_actions(str(guild_id), app_name, ActionInteraction.DECLINE)
            for i in actions:
                if i["action_type"] == "add_role":
                    role = interaction.message.guild.get_role(int(i["data"]["role_id"]))
                    user = interaction.message.guild.get_member(int(user_id))
                    await user.add_roles(role)
                else:
                    print("[❌]  Ação desconhecida.")


            emb = interaction.message.embeds[0]
            emb.colour = discord.Colour.red()
            embed = discord.Embed(title='❌  Este usuário foi reprovado.')
            embed.add_field(name="", value=f"`🛑`  **Motivo definido pelo moderador**: {reason}\n`📧`  **Por**: {interaction.user.mention}\n`🕛`  **Horário**: <t:{round(time.time())}:f>")
            embed.colour = discord.Colour.red()
            await interaction.followup.edit_message(message_id = interaction.message.id, embeds=[emb, embed])
            view = discord.ui.View.from_message(interaction.message)
            view.disable_all_items()
            await interaction.followup.edit_message(message_id = interaction.message.id, view = view)




# end
bot.run(TOKEN)