#!/usr/bin/python3
import requests

import helpers

info_endpoint = 'http://localhost:3001/info'

try:
    response = requests.get(info_endpoint)
    response.raise_for_status()
    response_body = response.json()
except Exception as e:
    helpers.exit_with_CRITICAL(e)

metrics = {
    'online_players': response_body['OnlinePlayers'],
    'total_players': response_body['TotalPlayers'],
    'animals': response_body['Animals'],
    'plants': response_body['Plants'],
    'laws': response_body['Laws'],
}


formatted_metrics = " ".join(
    [f"'{name}'={value}" for name, value in metrics.items()])

helpers.exit_with_OK(f"Eco stats fetched successfully | {formatted_metrics}")
