#!/usr/bin/python3
import re
import subprocess

def parse_players(server_output):
    """Parses /players output generated by factorio server. Output example:
    Players (2):
      Player A (online)
      Player B
    """
    player_regex = re.compile("\s+(.*?)( \(online\))?")
    players = {}
    for player_line in server_output.splitlines():
        match = player_regex.fullmatch(player_line)
        if match:
            name = match.group(1)
            online = 1 if match.group(2) != None else 0
            players[name] = online
    return players

def online_players(players):
    return [player for player, online in players.items() if online ]

def metrics(players):
    metrics = { f"player_{player}" : online for player, online in players.items() }
    metrics["players_online"] = sum(players.values())
    metrics["players_known"] = len(players.keys())
    return metrics

def get_server_output():
    command = 'sudo /opt/factorio-init/factorio cmd -o /players'.split(' ')
    process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, check=False)
    if process.returncode != 0:
        raise Exception(f"Error reading factorio users - error code {process.returncode}, stderr: '{process.stderr.strip()}', stdout: '{process.stdout.strip()}'")
    return process.stdout.strip()


try:
    players = parse_players(get_server_output())
except Exception as e:
    print(f"CRITICAL: {e}")
    exit(0)

players_online = online_players(players)
player_metrics = metrics(players)

formatted_players = ', '.join(players_online) if len(players_online) > 0 else 'nobody'
formatted_metrics = " ".join([ f"'{name}'={value}" for name,value in player_metrics.items() ])

print(f"OK: currently online: {formatted_players} | {formatted_metrics}")
