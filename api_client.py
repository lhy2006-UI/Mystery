# -*- coding: utf-8 -*-
"""API客户端：在线调用大模型，离线时返回None"""
import json
import urllib.request
import urllib.error
import socket


class APIClient:
    def __init__(self, base_url='http://localhost:3000/api', timeout=15):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.online = False

    def _post(self, endpoint, data):
        """发送POST请求，失败返回None"""
        url = f"{self.base_url}/{endpoint}"
        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(data).encode('utf-8'),
                headers={'Content-Type': 'application/json'},
                method='POST'
            )
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                result = json.loads(resp.read().decode('utf-8'))
                if result.get('success'):
                    return result.get('data')
                return None
        except (urllib.error.URLError, socket.timeout, ConnectionError, OSError):
            return None

    def check_health(self):
        """检查后端是否可用"""
        try:
            req = urllib.request.Request(f"{self.base_url}/health")
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                self.online = data.get('apiConfigured', False)
                return self.online
        except Exception:
            self.online = False
            return False

    def advance(self, player_state, scene, choice, history):
        """剧情推进"""
        return self._post('advance', {
            'playerState': player_state,
            'currentScene': scene,
            'lastChoice': choice,
            'history': history
        })

    def combat(self, player_state, enemy, action, combat_history):
        """战斗判定"""
        return self._post('combat', {
            'playerState': player_state,
            'enemyGhost': enemy,
            'playerAction': action,
            'combatHistory': combat_history
        })

    def capture(self, player_state, target, method, items):
        """驾驭判定"""
        return self._post('capture', {
            'playerState': player_state,
            'targetGhost': target,
            'method': method,
            'hasItems': items
        })

    def event(self, player_state, location):
        """随机事件"""
        return self._post('event', {
            'playerState': player_state,
            'location': location
        })
