# -*- coding: utf-8 -*-
"""游戏状态管理"""
import json
import os
import random
from game_data import GHOSTS, ITEMS, LOCATIONS, STAGES, PROLOGUE, OFFLINE_EVENTS

SAVE_FILE = os.path.join(os.path.expanduser('~'), '.mystery_revival_save.json')


class GameState:
    def __init__(self):
        self.reset()

    def reset(self):
        self.player = {
            'name': '杨间',
            'health': 100,
            'sanity': 100,
            'revival': 0,
            'insight': 30,
            'ghostDomainLevel': 0,
            'capturedGhosts': [],
            'items': [],
            'stage': 0,
            'devourCount': 0,
            'restartUsed': False,
            'captainTrial': False,
        }
        self.currentScene = 'prologue'
        self.currentLocation = '第七高中'
        self.history = []
        self.prologueIndex = 0
        self.inBattle = False
        self.battle = None
        self.guichaEncounter = False

    def get_stage(self):
        p = self.player
        for i in range(len(STAGES) - 1, -1, -1):
            if len(p['capturedGhosts']) >= i and p['ghostDomainLevel'] >= i:
                return i
        return 0

    def can_ascend(self):
        p = self.player
        return ('鬼差' in p['capturedGhosts'] and p['devourCount'] >= 20
                and len(p['capturedGhosts']) >= 8 and p['ghostDomainLevel'] >= 8
                and '神位碎片' in p['items'])

    def apply_effects(self, effects):
        if not effects:
            return
        p = self.player
        if 'health' in effects:
            p['health'] = max(0, min(100, p['health'] + effects['health']))
        if 'sanity' in effects:
            p['sanity'] = max(0, min(100, p['sanity'] + effects['sanity']))
        if 'revival' in effects:
            p['revival'] = max(0, min(100, p['revival'] + effects['revival']))
        if 'insight' in effects:
            p['insight'] = max(0, p['insight'] + effects['insight'])
        if 'devour' in effects:
            p['devourCount'] += effects['devour']
        p['stage'] = self.get_stage()

    def is_dead(self):
        p = self.player
        return p['health'] <= 0 or p['revival'] >= 100 or p['sanity'] <= 0

    def death_reason(self):
        p = self.player
        if p['health'] <= 0:
            return '你的生命耗尽了。'
        if p['revival'] >= 100:
            return '厉鬼彻底复苏，你失去了人类意识。'
        if p['sanity'] <= 0:
            return '你的理智完全崩溃。'
        return ''

    def check_captain(self):
        p = self.player
        if (len(p['capturedGhosts']) >= 5 and p['ghostDomainLevel'] >= 5
                and not p['captainTrial']):
            p['captainTrial'] = True
            p['items'].append('队长令牌')
            return True
        return False

    def get_offline_event(self):
        """获取离线随机事件"""
        events = OFFLINE_EVENTS.get(self.currentLocation, OFFLINE_EVENTS['大昌市街道'])
        evt = random.choice(events)
        result = {
            'name': evt['name'],
            'description': evt['desc'],
            'effects': evt.get('effects'),
        }
        if 'item' in evt:
            result['item'] = {'name': evt['item']}
        if 'ghost' in evt:
            ghost_name = evt['ghost']
            if ghost_name == 'random':
                pool = [g for g in GHOSTS
                        if g not in self.player['capturedGhosts']
                        and GHOSTS[g]['danger'] != 'S']
                ghost_name = random.choice(pool) if pool else '鬼掐人'
            d = GHOSTS[ghost_name]
            result['ghost'] = {
                'name': ghost_name,
                'level': d['level'],
                'ghostDomainLevel': 4 if d['danger'] == 'S' else 3 if d['danger'] == 'A' else 2,
                'pattern': d['pattern']
            }
        return result

    def save(self):
        try:
            with open(SAVE_FILE, 'w', encoding='utf-8') as f:
                json.dump({
                    'player': self.player,
                    'currentScene': self.currentScene,
                    'currentLocation': self.currentLocation,
                    'history': self.history,
                    'prologueIndex': self.prologueIndex,
                }, f, ensure_ascii=False, indent=2)
            return True
        except Exception:
            return False

    def load(self):
        try:
            if not os.path.exists(SAVE_FILE):
                return False
            with open(SAVE_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.player = data['player']
            self.currentScene = data['currentScene']
            self.currentLocation = data['currentLocation']
            self.history = data['history']
            self.prologueIndex = data['prologueIndex']
            self.inBattle = False
            self.battle = None
            return True
        except Exception:
            return False

    @staticmethod
    def has_save():
        return os.path.exists(SAVE_FILE)
