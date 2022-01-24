from mcdreforged.api.command import Literal, Text
from mcdreforged.api.decorator import new_thread
import json
import os
import time


PLUGIN_METADATA = {
    "id": "fakeplayer_limit",
    "version": "1.0.0",
    "name": "FakeplayerLimit",
    "description": "假人数量限制",
    "author": "noionion",
    "link": "None",
    "dependencies": {
        "mcdreforged": ">=2.1.0",
        "minecraft_data_api": "*"
    }
}

config = {
    "enable": True,
    "limit": 2,
    "admin":["2x_ercha", "GamerNoTitle"]
}

def save_config():
    global config
    with open('./config/FakeplayerLimit.json', 'w', encoding="utf-8") as f:
        f.write(json.dumps(config, indent=2, separators=(',', ':'), ensure_ascii=False))


def load_config():
    global config
    with open('./config/FakeplayerLimit.json', 'r', encoding="utf-8") as f:
        config = json.load(f)
    return config

def on_load(server, prev):
    global config
    if not os.path.exists('./config/FakeplayerLimit.json'):
        save_config()
    else:
        load_config()
    server.register_help_message('!!fl <num>', 'bot数量限制')
    server.register_command(Literal('!!fl').then(Text('num').runs(change)))

@new_thread(PLUGIN_METADATA['id'])
def on_player_joined(server, player, info):
    global config
    api = server.get_plugin_instance('minecraft_data_api')
    amount, limit, players = api.get_server_player_list()
    botnum = len([bot for bot in players if bot.startswith('bot_')])
    if botnum > config['limit'] and player.startswith('bot_') and config['enable']:
        time.sleep(1)
        server.execute('kill {}'.format(player))
        server.broadcast('§7[§3FL§f/§aINFO§7] §b当前服务器内假人已到达数量限制：§e{}§b，如有需要请联系管理员'.format(config['limit']))

def change(commandsource, context):
    global config
    if commandsource.is_player:
        if commandsource.player in config['admin']:
            if int(context['num']) == 0:
                config['enable'] = False
                commandsource.reply('§7[§3FL§f/§aINFO§7] §b假人数量限制已关闭')
            else:
                config['enable'] = True
                config['limit'] = int(context['num'])
                commandsource.reply('§7[§3FL§f/§aINFO§7] §b假人数量限制已修改为 §e{}'.format(context['num']))
            save_config()
        else:
            commandsource.reply('§7[§3FL§f/§cWARN§7] §b权限不足')
    else:
        if int(context['num']) == 0:
            config['enable'] = False
            commandsource.reply('§7[§3FL§f/§aINFO§7] §b假人数量限制已关闭')
        else:
            config['enable'] = True
            config['limit'] = int(context['num'])
            commandsource.reply('§7[§3FL§f/§aINFO§7] §b假人数量限制已修改为 §e{}'.format(context['num']))
        save_config()