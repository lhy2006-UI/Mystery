# -*- coding: utf-8 -*-
"""
神秘复苏 · 驭鬼者 - 手机游戏
Python + Kivy 开发，可打包为Android APK
"""
import os
import sys
import random
import threading

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.core.text import LabelBase
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.utils import get_color_from_hex

from game_state import GameState
from api_client import APIClient
from game_data import GHOSTS, ITEMS, LOCATIONS, STAGES, PROLOGUE

# ========== 颜色 ==========
C_BG = get_color_from_hex('#050508')
C_PANEL = get_color_from_hex('#0e0e16')
C_PANEL2 = get_color_from_hex('#16161e')
C_BORDER = get_color_from_hex('#2a2a3a')
C_TEXT = get_color_from_hex('#d8d0c8')
C_MUTED = get_color_from_hex('#7a7068')
C_RED = get_color_from_hex('#a01818')
C_RED2 = get_color_from_hex('#e03030')
C_GOLD = get_color_from_hex('#c9a227')
C_GOLD2 = get_color_from_hex('#e8c84a')
C_CYAN = get_color_from_hex('#3a8aaa')
C_GREEN = get_color_from_hex('#3a8a4a')
C_PURPLE = get_color_from_hex('#8a3aaa')


def risk_color(risk):
    if risk == 'low':
        return C_GREEN
    if risk == 'high':
        return C_RED2
    if risk == 'divine':
        return C_PURPLE
    return C_GOLD


def risk_text(risk):
    return {'low': '安全', 'high': '危险', 'divine': '神启'}.get(risk, '中等')


class ColoredBox(BoxLayout):
    """带背景色的BoxLayout"""
    def __init__(self, bg_color=C_PANEL, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(*bg_color)
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update_rect, size=self._update_rect)

    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


class GameButton(Button):
    """游戏按钮"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = (0.12, 0.1, 0.16, 1)
        self.color = C_TEXT
        self.font_size = '14sp'
        self.size_hint_y = None
        self.height = '52dp'
        self.border = (2, 2, 2, 2)
        self.bind(on_press=self._on_press)

    def _on_press(self, instance):
        self.background_color = (0.3, 0.08, 0.08, 1)
        Clock.schedule_once(lambda dt: setattr(self, 'background_color', (0.12, 0.1, 0.16, 1)), 0.15)


# ========== 标题页 ==========
class TitleScreen(Screen):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.build_ui()

    def build_ui(self):
        root = ColoredBox(bg_color=C_BG, orientation='vertical', padding='40dp', spacing='12dp')

        # 标题
        title = Label(text='神秘复苏', font_size='48sp', color=C_RED,
                      font_name=self.app.font_name, bold=True)
        root.add_widget(title)

        sub = Label(text='驭 鬼 者', font_size='16sp', color=C_GOLD)
        root.add_widget(sub)

        root.add_widget(Label(size_hint_y=None, height='40dp'))

        # 按钮
        btn_new = GameButton(text='新 的 游 戏', on_press=self.start_new)
        root.add_widget(btn_new)

        self.btn_continue = GameButton(text='继 续 游 戏', on_press=self.continue_game)
        self.btn_continue.disabled = not GameState.has_save()
        root.add_widget(self.btn_continue)

        btn_set = GameButton(text='设 置', on_press=self.open_settings)
        root.add_widget(btn_set)

        btn_about = GameButton(text='关 于', on_press=self.open_about)
        root.add_widget(btn_about)

        root.add_widget(Label(size_hint_y=None, height='30dp'))

        # 网络状态
        self.net_label = Label(text='检测网络中...', font_size='11sp', color=C_MUTED)
        root.add_widget(self.net_label)

        root.add_widget(Label(size_hint_y=None, height='20dp'))
        footer = Label(text='鬼无法被杀死 · 唯有以鬼制鬼', font_size='10sp', color=C_MUTED)
        root.add_widget(footer)

        self.add_widget(root)

    def on_pre_enter(self):
        self.btn_continue.disabled = not GameState.has_save()
        self.update_net_status()

    def update_net_status(self):
        if self.app.api.online:
            self.net_label.text = '● 在线 · API模式'
            self.net_label.color = C_GREEN
        else:
            self.net_label.text = '● 离线 · 本地模式'
            self.net_label.color = C_RED2

    def start_new(self, instance):
        self.app.game.reset()
        self.app.start_game()

    def continue_game(self, instance):
        if self.app.game.load():
            self.app.start_game(loaded=True)

    def open_settings(self, instance):
        content = BoxLayout(orientation='vertical', padding='20dp', spacing='12dp')
        content.add_widget(Label(text='后端API地址：', font_size='13sp', color=C_TEXT, size_hint_y=None, height='30dp'))
        api_input = TextInput(text=self.app.api.base_url, multiline=False,
                              size_hint_y=None, height='44dp',
                              background_color=(0.05, 0.05, 0.08, 1),
                              foreground_color=C_TEXT)
        content.add_widget(api_input)

        net_text = '在线 · API模式' if self.app.api.online else '离线 · 本地模式'
        content.add_widget(Label(text=f'当前状态：{net_text}', font_size='12sp', color=C_MUTED))

        btn_test = GameButton(text='检测网络', on_press=lambda x: self._test_api(api_input))
        content.add_widget(btn_test)
        btn_close = GameButton(text='关闭', on_press=lambda x: self._popup.dismiss())
        content.add_widget(btn_close)

        self._popup = Popup(title='设置', content=content, size_hint=(0.85, 0.6),
                            background=C_PANEL, title_color=C_GOLD)
        self._popup.open()

    def _test_api(self, api_input):
        self.app.api.base_url = api_input.text.strip().rstrip('/')
        threading.Thread(target=self._check_api_thread, daemon=True).start()

    def _check_api_thread(self):
        self.app.api.check_health()
        Clock.schedule_once(lambda dt: self.update_net_status())

    def open_about(self, instance):
        content = BoxLayout(orientation='vertical', padding='20dp', spacing='10dp')
        about_text = ('《神秘复苏·驭鬼者》\n\n'
                      '基于小说《神秘复苏》世界观的灵异生存游戏。\n'
                      '自由探索大昌市，驾驭厉鬼，走原作杨间的成神路线。\n\n'
                      '隐藏路线：黄岗村鬼差 → 吞噬成长 → 黄金门登神\n\n'
                      '鬼无法被杀死，只能被关押或驾驭。')
        content.add_widget(Label(text=about_text, font_size='13sp', color=C_TEXT))
        btn_close = GameButton(text='关闭', on_press=lambda x: self._popup.dismiss())
        content.add_widget(btn_close)
        self._popup = Popup(title='关于', content=content, size_hint=(0.85, 0.6),
                            background=C_PANEL, title_color=C_GOLD)
        self._popup.open()


# ========== 顶部状态栏 ==========
class TopBar(ColoredBox):
    def __init__(self, app, **kwargs):
        super().__init__(bg_color=(0.05, 0.05, 0.08, 0.95), orientation='horizontal',
                         size_hint_y=None, height='52dp', padding='8dp', spacing='6dp')
        self.app = app
        self.stats = {}
        for key, label, color in [('health', '生命', C_RED), ('sanity', '理智', C_CYAN),
                                   ('revival', '复苏', C_PURPLE), ('insight', '洞察', C_GOLD)]:
            box = BoxLayout(orientation='vertical', size_hint_x=1)
            lbl = Label(text=label, font_size='9sp', color=C_MUTED, size_hint_y=None, height='14dp')
            box.add_widget(lbl)
            track = ColoredBox(bg_color=(0, 0, 0, 0.5), size_hint_y=None, height='8dp')
            fill = ColoredBox(bg_color=color, size_hint=(None, 1), width=0)
            track.add_widget(fill)
            box.add_widget(track)
            self.add_widget(box)
            self.stats[key] = fill

        self.stage_label = Label(text='新手', font_size='11sp', color=C_GOLD,
                                 size_hint_x=None, width='60dp', bold=True)
        self.add_widget(self.stage_label)

    def update(self):
        p = self.app.game.player
        self.stats['health'].width = self.stats['health'].parent.width * (p['health'] / 100) if self.stats['health'].parent else 0
        self.stats['sanity'].width = self.stats['sanity'].parent.width * (p['sanity'] / 100) if self.stats['sanity'].parent else 0
        self.stats['revival'].width = self.stats['revival'].parent.width * (p['revival'] / 100) if self.stats['revival'].parent else 0
        self.stats['insight'].width = self.stats['insight'].parent.width * (min(p['insight'], 100) / 100) if self.stats['insight'].parent else 0
        stage_idx = self.app.game.get_stage()
        self.stage_label.text = STAGES[stage_idx][:4]


# ========== 底部Tab栏 ==========
class TabBar(ColoredBox):
    def __init__(self, app, **kwargs):
        super().__init__(bg_color=(0.05, 0.05, 0.08, 0.95), orientation='horizontal',
                         size_hint_y=None, height='58dp')
        self.app = app
        self.tabs = {}
        for page, icon, label in [('story', '📜', '剧情'), ('map', '🗺', '地图'),
                                   ('ghost', '👻', '厉鬼'), ('char', '👤', '角色')]:
            btn = Button(text=f'{icon}\n{label}', font_size='11sp', color=C_MUTED,
                         background_normal='', background_color=(0, 0, 0, 0))
            btn.bind(on_press=lambda x, p=page: self.switch(p))
            self.add_widget(btn)
            self.tabs[page] = btn

    def switch(self, page):
        self.app.sm.current = page
        self.update_active(page)

    def update_active(self, page):
        for p, btn in self.tabs.items():
            btn.color = C_GOLD if p == page else C_MUTED


# ========== 剧情页 ==========
class StoryScreen(Screen):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.build_ui()

    def build_ui(self):
        root = BoxLayout(orientation='vertical')
        self.topbar = TopBar(self.app)
        root.add_widget(self.topbar)

        # 叙事区
        content = BoxLayout(orientation='vertical', padding='12dp', spacing='12dp')
        self.story_scroll = ScrollView()
        self.story_label = Label(text='', font_size='15sp', color=C_TEXT,
                                 size_hint_y=None, markup=True,
                                 text_size=(self.width - 40, None))
        self.story_label.bind(texture_size=self.story_label.setter('size'))
        self.story_scroll.add_widget(self.story_label)
        content.add_widget(self.story_scroll)

        # 选项区
        self.choices_box = BoxLayout(orientation='vertical', spacing='10dp',
                                     size_hint_y=None, height='200dp')
        content.add_widget(self.choices_box)

        root.add_widget(content)

        self.tabbar = TabBar(self.app)
        root.add_widget(self.tabbar)
        self.add_widget(root)

    def on_pre_enter(self):
        self.topbar.update()
        self.tabbar.update_active('story')

    def show_story(self, text):
        self.story_label.text = text.replace('\n', '\n')
        Clock.schedule_once(lambda dt: setattr(self.story_scroll, 'scroll_y', 0), 0.1)

    def show_choices(self, choices):
        self.choices_box.clear_widgets()
        self.choices_box.height = min(len(choices) * 62, 250)
        for ch in choices:
            btn = GameButton(text=ch['text'], height='56dp')
            btn.background_color = (0.1, 0.08, 0.14, 1)
            btn.bind(on_press=lambda x, c=ch: self.app.make_choice(c))
            # 风险标签放在按钮文本后面
            risk = risk_text(ch.get('risk', 'medium'))
            btn.text = f"{ch['text']}  [{risk}]"
            self.choices_box.add_widget(btn)


# ========== 地图页 ==========
class MapScreen(Screen):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.build_ui()

    def build_ui(self):
        root = BoxLayout(orientation='vertical')
        self.topbar = TopBar(self.app)
        root.add_widget(self.topbar)

        title = Label(text='大 昌 市 · 灵 异 地 图', font_size='18sp', color=C_GOLD,
                      size_hint_y=None, height='40dp', bold=True)
        root.add_widget(title)

        self.scroll = ScrollView()
        self.grid = GridLayout(cols=1, spacing='10dp', padding='12dp',
                               size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter('height'))
        self.scroll.add_widget(self.grid)
        root.add_widget(self.scroll)

        self.tabbar = TabBar(self.app)
        root.add_widget(self.tabbar)
        self.add_widget(root)

    def on_pre_enter(self):
        self.topbar.update()
        self.tabbar.update_active('map')
        self.refresh()

    def refresh(self):
        self.grid.clear_widgets()
        for loc in LOCATIONS:
            btn = GameButton(text=f"{loc['name']}\n[size=11sp][color=#7a7068]{loc['desc']}[/color]  [{loc['danger']}级][/size]",
                             height='72dp', markup=True)
            btn.bind(on_press=lambda x, l=loc: self.app.travel_to(l))
            self.grid.add_widget(btn)


# ========== 厉鬼页 ==========
class GhostScreen(Screen):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.build_ui()

    def build_ui(self):
        root = BoxLayout(orientation='vertical')
        self.topbar = TopBar(self.app)
        root.add_widget(self.topbar)

        self.scroll = ScrollView()
        self.content = BoxLayout(orientation='vertical', spacing='10dp', padding='12dp',
                                 size_hint_y=None)
        self.content.bind(minimum_height=self.content.setter('height'))
        self.scroll.add_widget(self.content)
        root.add_widget(self.scroll)

        self.tabbar = TabBar(self.app)
        root.add_widget(self.tabbar)
        self.add_widget(root)

    def on_pre_enter(self):
        self.topbar.update()
        self.tabbar.update_active('ghost')
        self.refresh()

    def refresh(self):
        self.content.clear_widgets()
        p = self.app.game.player

        title1 = Label(text='已驾驭厉鬼', font_size='14sp', color=C_GOLD,
                       size_hint_y=None, height='30dp', bold=True)
        self.content.add_widget(title1)

        if not p['capturedGhosts']:
            self.content.add_widget(Label(text='暂无', font_size='13sp', color=C_MUTED,
                                          size_hint_y=None, height='40dp'))
        else:
            for g in p['capturedGhosts']:
                d = GHOSTS.get(g, {'name': g, 'level': '未知', 'pattern': '未知', 'abilities': []})
                divine = d.get('divine', False)
                text = f"[b]{d['name']}{' ✦' if divine else ''}[/b]  [{d['level']}]\n{d['pattern']}\n[color=#c9a227]{' · '.join(d.get('abilities', []))}[/color]"
                lbl = Label(text=text, font_size='12sp', color=C_TEXT, markup=True,
                            size_hint_y=None, height='70dp',
                            padding=(10, 8))
                self.content.add_widget(lbl)

        title2 = Label(text='灵异物品', font_size='14sp', color=C_GOLD,
                       size_hint_y=None, height='30dp', bold=True)
        self.content.add_widget(title2)

        if not p['items']:
            self.content.add_widget(Label(text='暂无', font_size='13sp', color=C_MUTED,
                                          size_hint_y=None, height='40dp'))
        else:
            for i in p['items']:
                d = ITEMS.get(i, {'name': i, 'desc': '', 'type': ''})
                lbl = Label(text=f"{d['name']}  [{d['type']}]\n[size=11sp][color=#7a7068]{d['desc']}[/color][/size]",
                            font_size='12sp', color=C_TEXT, markup=True,
                            size_hint_y=None, height='50dp', padding=(10, 4))
                self.content.add_widget(lbl)


# ========== 角色页 ==========
class CharScreen(Screen):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.build_ui()

    def build_ui(self):
        root = BoxLayout(orientation='vertical')
        self.topbar = TopBar(self.app)
        root.add_widget(self.topbar)

        self.scroll = ScrollView()
        self.content = BoxLayout(orientation='vertical', spacing='10dp', padding='12dp',
                                 size_hint_y=None)
        self.content.bind(minimum_height=self.content.setter('height'))
        self.scroll.add_widget(self.content)
        root.add_widget(self.scroll)

        self.tabbar = TabBar(self.app)
        root.add_widget(self.tabbar)
        self.add_widget(root)

    def on_pre_enter(self):
        self.topbar.update()
        self.tabbar.update_active('char')
        self.refresh()

    def refresh(self):
        self.content.clear_widgets()
        p = self.app.game.player
        stage_idx = self.app.game.get_stage()

        # 角色头部
        header = BoxLayout(orientation='vertical', size_hint_y=None, height='100dp',
                           padding='10dp', spacing='4dp')
        header.add_widget(Label(text='👁', font_size='32sp', size_hint_y=None, height='40dp'))
        header.add_widget(Label(text='杨 间', font_size='20sp', color=C_GOLD, bold=True,
                                size_hint_y=None, height='28dp'))
        header.add_widget(Label(text=STAGES[stage_idx], font_size='12sp', color=C_MUTED,
                                size_hint_y=None, height='20dp'))
        self.content.add_widget(header)

        # 四大属性
        for key, label, color in [('health', '生命值', C_RED), ('sanity', '理智值', C_CYAN),
                                   ('revival', '复苏度', C_PURPLE), ('insight', '洞察力', C_GOLD)]:
            val = p[key]
            if key == 'revival':
                val_str = f"{val}%"
            else:
                val_str = str(val)
            row = BoxLayout(orientation='vertical', size_hint_y=None, height='50dp')
            row.add_widget(Label(text=f"{label}: {val_str}", font_size='13sp', color=C_TEXT,
                                 size_hint_y=None, height='22dp'))
            track = ColoredBox(bg_color=(0, 0, 0, 0.5), size_hint_y=None, height='10dp')
            pct = min(val, 100) / 100
            fill = ColoredBox(bg_color=color, size_hint=(None, 1), width=track.width * pct if track.width else 0)
            track.add_widget(fill)
            row.add_widget(track)
            self.content.add_widget(row)

        # 详细信息
        info_title = Label(text='详细信息', font_size='14sp', color=C_GOLD,
                           size_hint_y=None, height='30dp', bold=True)
        self.content.add_widget(info_title)

        info_lines = [
            f"鬼域层级: {p['ghostDomainLevel']}层",
            f"已驾驭厉鬼: {len(p['capturedGhosts'])}只",
            f"灵异物品: {len(p['items'])}件",
            f"当前位置: {self.app.game.currentLocation}",
        ]
        if '鬼差' in p['capturedGhosts']:
            info_lines.append(f"鬼差压制数: {p['devourCount']}")
        for line in info_lines:
            self.content.add_widget(Label(text=line, font_size='13sp', color=C_TEXT,
                                          size_hint_y=None, height='26dp'))

        self.content.add_widget(Label(size_hint_y=None, height='10dp'))

        # 功能按钮
        if '鬼差' in p['capturedGhosts'] and p['devourCount'] >= 10 and not p['restartUsed']:
            btn_restart = GameButton(text='⏳ 重启时间（鬼差能力）', height='50dp')
            btn_restart.bind(on_press=lambda x: self.app.use_restart())
            self.content.add_widget(btn_restart)

        if self.app.game.can_ascend():
            btn_ascend = GameButton(text='✦ 前往黄金门登神', height='50dp')
            btn_ascend.background_color = (0.2, 0.08, 0.3, 1)
            btn_ascend.bind(on_press=lambda x: self.app.attempt_ascend())
            self.content.add_widget(btn_ascend)

        btn_save = GameButton(text='💾 保存游戏', height='50dp')
        btn_save.bind(on_press=lambda x: self.app.save_game())
        self.content.add_widget(btn_save)

        btn_title = GameButton(text='⚙ 返回标题', height='50dp')
        btn_title.bind(on_press=lambda x: self.app.back_to_title())
        self.content.add_widget(btn_title)


# ========== 战斗弹窗 ==========
class BattlePopup(Popup):
    def __init__(self, app, ghost, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.ghost = ghost
        self.turn = 1
        self.pattern_broken = False
        self.can_devour = False
        self.title = f'战斗 · {ghost["name"]}'
        self.title_color = C_RED2
        self.background = C_PANEL
        self.size_hint = (0.95, 0.95)
        self.build_ui()

    def build_ui(self):
        root = BoxLayout(orientation='vertical', padding='12dp', spacing='10dp')

        # 双方状态
        stats = BoxLayout(orientation='horizontal', spacing='10dp', size_hint_y=None, height='90dp')
        p = self.app.game.player
        pbox = ColoredBox(bg_color=(0.08, 0.06, 0.12, 1), orientation='vertical', padding='8dp')
        pbox.add_widget(Label(text='杨间', font_size='14sp', color=C_CYAN, bold=True,
                              size_hint_y=None, height='22dp'))
        pbox.add_widget(Label(text=f"HP:{p['health']} 理智:{p['sanity']}\n复苏:{p['revival']}% 鬼域:{p['ghostDomainLevel']}层",
                              font_size='10sp', color=C_MUTED))
        stats.add_widget(pbox)

        ebox = ColoredBox(bg_color=(0.12, 0.04, 0.04, 1), orientation='vertical', padding='8dp')
        ebox.add_widget(Label(text=self.ghost['name'], font_size='14sp', color=C_RED2, bold=True,
                              size_hint_y=None, height='22dp'))
        ebox.add_widget(Label(text=f"{self.ghost['level']}\n鬼域:{self.ghost['ghostDomainLevel']}层",
                              font_size='10sp', color=C_MUTED))
        stats.add_widget(ebox)
        root.add_widget(stats)

        # 战斗日志
        self.log_scroll = ScrollView()
        self.log_label = Label(text='', font_size='12sp', color=C_TEXT, size_hint_y=None,
                               markup=True)
        self.log_label.bind(texture_size=self.log_label.setter('size'))
        self.log_scroll.add_widget(self.log_label)
        root.add_widget(self.log_scroll)

        # 行动按钮
        self.actions = GridLayout(cols=2, spacing='8dp', size_hint_y=None, height='180dp')
        root.add_widget(self.actions)
        self.refresh_actions()

        self.add_log(f'遭遇 {self.ghost["name"]}！等级：{self.ghost["level"]}', 'info')
        self.add_log(f'杀人规律：{self.ghost.get("pattern", "未知")}', 'info')

        self.content = root

    def add_log(self, text, log_type=''):
        color = {'dmg': '#e03030', 'heal': '#5aca6a', 'info': '#e8c84a',
                 'divine': '#c06aea'}.get(log_type, '#d8d0c8')
        current = self.log_label.text
        self.log_label.text = current + f'\n[color={color}]【回合{self.turn}】{text}[/color]'
        Clock.schedule_once(lambda dt: setattr(self.log_scroll, 'scroll_y', 0), 0.05)

    def refresh_actions(self):
        self.actions.clear_widgets()
        p = self.app.game.player
        actions = [
            ('👁 鬼域', 'domain'),
            ('⚡ 能力', 'ability'),
            (f'🔍 破解({p["insight"]})', 'decipher'),
            ('📦 物品', 'item'),
        ]
        if self.ghost['ghostDomainLevel'] <= 0 and self.pattern_broken:
            actions.append(('⛓ 关押', 'capture'))
        if '鬼差' in p['capturedGhosts'] and self.can_devour:
            actions.append(('✦ 吞噬', 'devour'))
        actions.append(('🏃 逃跑', 'flee'))

        for text, action in actions:
            btn = GameButton(text=text, height='52dp')
            if action == 'devour':
                btn.background_color = (0.2, 0.08, 0.3, 1)
            btn.bind(on_press=lambda x, a=action: self.app.battle_action(a, self))
            self.actions.add_widget(btn)

    def enemy_attack(self):
        if self.ghost['name'] == '鬼差':
            self.add_log('鬼差："压制数>现场鬼数，瞬杀。"', 'dmg')
            self.app.game.apply_effects({'health': -999})
            self.app.check_death()
            return
        if self.pattern_broken:
            self.add_log('利用破解的规律规避了攻击！', 'info')
        else:
            dmg = self.ghost['ghostDomainLevel'] * 15 + 10
            self.app.game.apply_effects({'health': -dmg, 'sanity': -10})
            self.add_log(f'{self.ghost["name"]}攻击！受到{dmg}点伤害！', 'dmg')
        self.turn += 1
        self.refresh_actions()
        self.app.check_death()


# ========== 主App ==========
class MysteryRevivalApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game = GameState()
        self.api = APIClient(base_url=os.environ.get('MR_API_URL', 'http://localhost:3000/api'))
        self.font_name = 'Roboto'
        self.battle_popup = None

    def build(self):
        # 注册中文字体
        self._register_font()

        self.sm = ScreenManager()
        self.title_screen = TitleScreen(self, name='title')
        self.story_screen = StoryScreen(self, name='story')
        self.map_screen = MapScreen(self, name='map')
        self.ghost_screen = GhostScreen(self, name='ghost')
        self.char_screen = CharScreen(self, name='char')

        self.sm.add_widget(self.title_screen)
        self.sm.add_widget(self.story_screen)
        self.sm.add_widget(self.map_screen)
        self.sm.add_widget(self.ghost_screen)
        self.sm.add_widget(self.char_screen)

        # 后台检测网络
        threading.Thread(target=self.api.check_health, daemon=True).start()

        return self.sm

    def _register_font(self):
        """尝试注册中文字体"""
        font_paths = [
            '/system/fonts/NotoSansCJK-Regular.ttc',
            '/system/fonts/DroidSansFallback.ttf',
            '/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc',
            '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
        ]
        for fp in font_paths:
            if os.path.exists(fp):
                try:
                    LabelBase.register(name='ChineseFont', fn_regular=fp)
                    self.font_name = 'ChineseFont'
                    break
                except Exception:
                    pass

    def start_game(self, loaded=False):
        self.sm.current = 'story'
        if loaded:
            if self.game.currentScene == 'prologue':
                self.show_prologue_node()
            else:
                self.enter_free_roam()
        else:
            self.show_prologue_node()

    def back_to_title(self):
        self.sm.current = 'title'

    def show_prologue_node(self):
        idx = self.game.prologueIndex
        if idx >= len(PROLOGUE):
            self.enter_free_roam()
            return
        node = PROLOGUE[idx]
        self.story_screen.show_story(node['narration'])
        self.game.history.append(node['narration'][:40])
        if node.get('effects'):
            self.game.apply_effects(node['effects'])
        if node.get('rewards'):
            r = node['rewards']
            if r.get('ghost'):
                self.game.player['capturedGhosts'].append(r['ghost'])
                self.game.player['ghostDomainLevel'] = 1
                self.show_popup('驾驭成功', f'你成功驾驭了 {r["ghost"]}！\n鬼域提升至1层。')
            if r.get('item'):
                self.game.player['items'].append(r['item'])
        self.story_screen.topbar.update()
        self.story_screen.show_choices(node['choices'])

    def make_choice(self, choice):
        if self.game.currentScene == 'prologue':
            idx = self.game.prologueIndex
            if idx == 1 and '后门' in choice['text']:
                self.game.apply_effects({'health': -40, 'sanity': -20})
                self.story_screen.show_story('你冲进走廊撞上敲门鬼，它的手穿过了你的胸膛。你拼尽全力逃回教室，受了重伤。')
                Clock.schedule_once(lambda dt: self._next_prologue(), 2.5)
                return
            if idx == 2 and '打开厕所门' in choice['text']:
                self.game.apply_effects({'health': -30, 'revival': 15})
                self.story_screen.show_story('你推开厕所门，外面是无限走廊，敲门鬼就在不远处。你猛地关门，但还是被波及。')
                Clock.schedule_once(lambda dt: self._next_prologue(), 2.5)
                return
            self._next_prologue()
            return
        self.handle_choice(choice)

    def _next_prologue(self):
        self.game.prologueIndex += 1
        self.show_prologue_node()

    def enter_free_roam(self):
        self.game.currentScene = 'freeroam'
        self.game.currentLocation = '第七高中'
        self.show_popup('序章完成', '你逃离了第七高中，成为了一名驭鬼者。\n灵异复苏的时代来临。\n\n提示：黄岗村藏着改变命运的机缘……')
        self.story_screen.show_story('你站在大昌市的街道上，青黑色天空下暗流涌动。\n\n你已驾驭鬼眼，拥有人皮纸。但这只是开始——更多厉鬼正在苏醒。听说黄岗村深处沉睡着一只足以改变一切的鬼。')
        self.story_screen.show_choices([
            {'text': '打开地图前往其他地点', 'risk': 'low'},
            {'text': '在当前区域探索', 'risk': 'medium'},
            {'text': '寻找安全地方休息', 'risk': 'low'},
        ])

    def handle_choice(self, choice):
        if '地图' in choice['text']:
            self.sm.current = 'map'
            return
        if '休息' in choice['text']:
            self.rest_action()
            return
        if '探索' in choice['text']:
            self.explore_action()
            return
        # API或离线
        threading.Thread(target=self._advance_thread, args=(choice,), daemon=True).start()

    def _advance_thread(self, choice):
        r = self.api.advance(self.game.player, f'位置：{self.game.currentLocation}',
                             choice['text'], self.game.history)
        Clock.schedule_once(lambda dt: self._advance_result(r, choice))

    def _advance_result(self, result, choice):
        if result:
            self.story_screen.show_story(result.get('narration', ''))
            self.game.history.append(result.get('narration', '')[:40])
            if result.get('effects'):
                self.game.apply_effects(result['effects'])
            if result.get('encounterGhost'):
                Clock.schedule_once(lambda dt: self.start_battle(result['encounterGhost']), 1)
                return
            if result.get('discoveredItem'):
                self.game.player['items'].append(result['discoveredItem'])
            choices = result.get('choices') or [
                {'text': '继续探索', 'risk': 'medium'},
                {'text': '前往其他地点', 'risk': 'low'},
            ]
            self.story_screen.show_choices(choices)
        else:
            self.offline_explore()
        self.story_screen.topbar.update()

    def explore_action(self):
        # 黄岗村隐藏触发
        if (self.game.currentLocation == '黄岗村'
                and self.game.player['insight'] >= 50
                and len(self.game.player['capturedGhosts']) >= 2
                and '鬼差' not in self.game.player['capturedGhosts']):
            self.trigger_guicha()
            return
        threading.Thread(target=self._event_thread, daemon=True).start()

    def _event_thread(self):
        r = self.api.event(self.game.player, self.game.currentLocation)
        Clock.schedule_once(lambda dt: self._event_result(r))

    def _event_result(self, result):
        if result:
            self.story_screen.show_story(f"【{result.get('eventName', '事件')}】\n\n{result.get('description', '')}")
            if result.get('immediateEffects'):
                self.game.apply_effects(result['immediateEffects'])
            if result.get('ghost'):
                Clock.schedule_once(lambda dt: self.start_battle(result['ghost']), 1)
                return
            if result.get('item'):
                self.game.player['items'].append(result['item']['name'])
            choices = result.get('choices') or [
                {'text': '继续探索', 'risk': 'medium'},
                {'text': '离开这里', 'risk': 'low'},
            ]
            self.story_screen.show_choices(choices)
        else:
            self.offline_explore()
        self.story_screen.topbar.update()

    def offline_explore(self):
        evt = self.game.get_offline_event()
        self.story_screen.show_story(f"【{evt['name']}】\n\n{evt['description']}")
        if evt.get('effects'):
            self.game.apply_effects(evt['effects'])
        if evt.get('item'):
            self.game.player['items'].append(evt['item']['name'])
            self.show_popup('获得物品', f"获得：{evt['item']['name']}")
        if evt.get('ghost'):
            Clock.schedule_once(lambda dt: self.start_battle(evt['ghost']), 1)
            return
        self.story_screen.show_choices([
            {'text': '继续探索', 'risk': 'medium'},
            {'text': '前往其他地点', 'risk': 'low'},
            {'text': '休息恢复', 'risk': 'low'},
        ])
        self.story_screen.topbar.update()

    def rest_action(self):
        if self.game.currentLocation == '观江小区':
            self.game.apply_effects({'health': 30, 'sanity': 20, 'revival': -15})
            self.story_screen.show_story('你在黄金安全屋休息，黄金压制了体内厉鬼，状态大幅恢复。')
        else:
            self.game.apply_effects({'health': 10, 'sanity': 10})
            self.story_screen.show_story('你找了个角落休息，但随时可能有厉鬼袭来，恢复有限。')
        self.story_screen.show_choices([
            {'text': '继续探索', 'risk': 'medium'},
            {'text': '前往其他地点', 'risk': 'low'},
        ])
        self.story_screen.topbar.update()

    def trigger_guicha(self):
        self.game.currentScene = 'guicha_encounter'
        self.story_screen.show_story('你在黄岗村废墟深处探索，洞察告诉你这里隐藏着什么。\n\n枯井底部，你发现了一具穿清朝官服的干尸，手握生锈令牌，散发着恐怖气息。\n\n这不是普通厉鬼——这是鬼差。\n\n它缓缓睁眼，整个黄岗村温度骤降。"压制数……零。现场鬼数……一。判定：瞬杀。"')
        self.story_screen.show_choices([
            {'text': '开启全部鬼域拼死一战', 'risk': 'high'},
            {'text': '立即逃离黄岗村', 'risk': 'medium'},
            {'text': '用人皮纸交易，询问鬼差秘密', 'risk': 'high'},
        ])

    def travel_to(self, loc):
        self.game.currentLocation = loc['name']
        self.sm.current = 'story'
        if loc['id'] == 'safehouse':
            self.story_screen.show_story(f"你来到了 {loc['name']}。\n\n{loc['desc']}\n\n黄金墙壁压制着厉鬼，这里是安全之地。")
            self.story_screen.show_choices([
                {'text': '在安全屋休息', 'risk': 'low'},
                {'text': '在周围探索', 'risk': 'low'},
                {'text': '前往其他地点', 'risk': 'low'},
            ])
        else:
            self.story_screen.show_story(f"你来到了 {loc['name']}。\n\n{loc['desc']}")
            self.story_screen.show_choices([
                {'text': '深入探索', 'risk': 'medium'},
                {'text': '前往其他地点', 'risk': 'low'},
            ])
        self.story_screen.topbar.update()

    def start_battle(self, ghost):
        self.battle_popup = BattlePopup(self, ghost)
        self.battle_popup.open()

    def battle_action(self, action, popup):
        p = self.game.player
        g = popup.ghost

        # 鬼差遭遇特殊处理
        if self.game.currentScene == 'guicha_encounter':
            if action in ('domain', 'ability'):
                self.game.apply_effects({'health': -50, 'sanity': -20, 'revival': 20})
                popup.add_log('你拼尽全力，但鬼差一挥手就撕碎了你的鬼域。"压制数+1。现场鬼数2。判定：继续。"', 'dmg')
                if p['health'] > 0:
                    popup.add_log('你侥幸活下来，鬼差对你产生了兴趣。', 'info')
                    popup.can_devour = True
                    popup.refresh_actions()
                return
            if action == 'item':
                if '人皮纸' in p['items']:
                    self.game.apply_effects({'sanity': -15, 'insight': 20})
                    popup.add_log('你展开人皮纸与鬼差交易，得知了吞噬成长的秘密。', 'info')
                    popup.add_log('"吞噬其他鬼，压制数增长。超过现场鬼数就能瞬杀。足够多时可重启一切。"', 'divine')
                    popup.can_devour = True
                    popup.refresh_actions()
                else:
                    popup.add_log('你没有合适的物品与鬼差交易！')
                return
            if action == 'flee':
                popup.add_log('你无法逃离鬼差的鬼域！', 'dmg')
                popup.enemy_attack()
                return
            if action in ('devour', 'capture'):
                self.devour_guicha(popup)
                return

        if action == 'domain':
            if p['ghostDomainLevel'] < 1:
                popup.add_log('无法开启鬼域！')
                return
            self.game.apply_effects({'revival': 5})
            g['ghostDomainLevel'] = max(0, g['ghostDomainLevel'] - p['ghostDomainLevel'])
            popup.add_log(f"开启{p['ghostDomainLevel']}层鬼域！对方鬼域压制至{g['ghostDomainLevel']}层", 'info')
        elif action == 'ability':
            if not p['capturedGhosts']:
                popup.add_log('没有驾驭任何厉鬼！')
                return
            self.game.apply_effects({'revival': 8, 'sanity': -5})
            g['ghostDomainLevel'] = max(0, g['ghostDomainLevel'] - 1)
            popup.add_log(f"使用 {p['capturedGhosts'][0]} 的能力！对方鬼域-1层", 'dmg')
        elif action == 'decipher':
            if p['insight'] < 20:
                popup.add_log('洞察不足（需20）')
                return
            self.game.apply_effects({'insight': -20})
            popup.pattern_broken = True
            popup.add_log(f"破解了 {g['name']} 的杀人规律！", 'info')
        elif action == 'item':
            if not p['items']:
                popup.add_log('没有可用物品！')
                return
            if '棺材钉' in p['items']:
                g['ghostDomainLevel'] = 0
                popup.add_log('使用棺材钉！对方被完全限制！', 'info')
            else:
                popup.add_log(f"使用了 {p['items'][0]}，效果有限。")
        elif action == 'capture':
            threading.Thread(target=self._capture_thread, args=(popup,), daemon=True).start()
            return
        elif action == 'devour':
            self.devour_ghost(popup)
            return
        elif action == 'flee':
            if random.random() < 0.5 + p['ghostDomainLevel'] * 0.1:
                popup.add_log('成功逃离！', 'info')
                Clock.schedule_once(lambda dt: self.end_battle(popup, False), 0.8)
            else:
                popup.add_log('逃跑失败！', 'dmg')
                popup.enemy_attack()
            return

        popup.refresh_actions()
        if g['ghostDomainLevel'] > 0 or not popup.pattern_broken:
            Clock.schedule_once(lambda dt: popup.enemy_attack(), 0.7)
        else:
            popup.add_log('对方已被完全压制，可以关押了！', 'info')
            popup.can_devour = True
            popup.refresh_actions()
        self.story_screen.topbar.update()

    def _capture_thread(self, popup):
        r = self.api.capture(self.game.player, popup.ghost, '直接驾驭', self.game.player['items'])
        Clock.schedule_once(lambda dt: self._capture_result(r, popup))

    def _capture_result(self, result, popup):
        if result:
            popup.add_log(result.get('narration', ''))
            success = result.get('success', False)
        else:
            success = random.random() < 0.6 + (0.3 if '棺材钉' in self.game.player['items'] else 0)
        if success:
            name = popup.ghost['name']
            self.game.player['capturedGhosts'].append(name)
            self.game.player['ghostDomainLevel'] = min(10, self.game.player['ghostDomainLevel'] + 1)
            popup.add_log(f"驾驭成功！获得 {name}，鬼域提升至{self.game.player['ghostDomainLevel']}层！", 'info')
            if self.game.check_captain():
                self.show_popup('队长试炼', '你驾驭了足够多的厉鬼，被授予队长令牌！')
            self.story_screen.topbar.update()
            Clock.schedule_once(lambda dt: self.end_battle(popup, True), 1.2)
        else:
            popup.add_log('驾驭失败！被灵异反噬！', 'dmg')
            self.game.apply_effects({'health': -25, 'revival': 20})
            Clock.schedule_once(lambda dt: popup.enemy_attack(), 0.7)

    def devour_ghost(self, popup):
        p = self.game.player
        if '鬼差' not in p['capturedGhosts']:
            return
        p['devourCount'] += 1
        self.game.apply_effects({'revival': 10, 'sanity': -10})
        popup.add_log(f"鬼差吞噬了 {popup.ghost['name']}！压制数+1（当前：{p['devourCount']}）", 'divine')
        if p['devourCount'] == 10:
            popup.add_log('鬼差力量达到新阶段——感受到了"重启"的可能性！', 'divine')
        if p['devourCount'] >= 20:
            popup.add_log('压制数足够高，感受到通往神之领域的大门！', 'divine')
        self.story_screen.topbar.update()
        Clock.schedule_once(lambda dt: self.end_battle(popup, True), 1.2)

    def devour_guicha(self, popup):
        p = self.game.player
        p['capturedGhosts'].append('鬼差')
        p['ghostDomainLevel'] = min(10, p['ghostDomainLevel'] + 2)
        p['devourCount'] = 1
        self.game.apply_effects({'revival': 15, 'sanity': -10})
        popup.add_log('你成为了鬼差的容器！鬼差纳入体内，鬼域+2层，压制数=1', 'divine')
        popup.add_log('鬼差的声音在你脑海中响起："吞噬更多的鬼，我会让你成为神。"', 'divine')
        self.game.currentScene = 'freeroam'
        self.story_screen.topbar.update()
        Clock.schedule_once(lambda dt: self.end_battle(popup, True), 1.5)

    def end_battle(self, popup, victory):
        popup.dismiss()
        self.battle_popup = None
        if victory:
            self.story_screen.show_story('战斗结束。你驾驭了新的厉鬼，力量增长，但复苏威胁也在逼近。')
        else:
            self.story_screen.show_story('你从战斗中撤离。灵异世界充满危险。')
        self.story_screen.show_choices([
            {'text': '继续探索', 'risk': 'medium'},
            {'text': '前往其他地点', 'risk': 'low'},
            {'text': '休息恢复', 'risk': 'low'},
        ])

    def use_restart(self):
        p = self.game.player
        if '鬼差' not in p['capturedGhosts'] or p['devourCount'] < 10 or p['restartUsed']:
            return
        p['restartUsed'] = True
        p['health'] = min(100, p['health'] + 50)
        p['sanity'] = min(100, p['sanity'] + 30)
        p['revival'] = max(0, p['revival'] - 30)
        self.story_screen.topbar.update()
        self.show_popup('重启', '鬼差力量发动——时间倒流。\n伤口愈合，理智恢复，复苏被压制。\n\n重启能力已使用（每局一次）')

    def attempt_ascend(self):
        if not self.game.can_ascend():
            self.show_popup('条件不足', '需要：鬼差 + 压制数≥20 + 驾驭≥8鬼 + 鬼域≥8层 + 神位碎片')
            return
        self.game.player['stage'] = 5
        self.show_popup('✦ 成神结局 ✦',
                        '你已超越源头，成为新的神。\n\n'
                        '驾驭鬼差，吞噬二十只厉鬼，鬼域八层，手握神位碎片——你推开了黄金之门。\n\n'
                        '鬼差的压制规则成为了你的规则，所有灵异在你面前如同蝼蚁。\n\n'
                        '但你也不再是人类了。杨间这个名字，成为了传说。\n\n—— 完 ——')

    def save_game(self):
        if self.game.save():
            self.show_popup('保存成功', '游戏进度已保存。')
        else:
            self.show_popup('保存失败', '无法保存游戏。')

    def check_death(self):
        if self.game.is_dead():
            reason = self.game.death_reason()
            if self.battle_popup:
                self.battle_popup.dismiss()
            self.show_popup('游戏结束', f'{reason}\n\n驾驭厉鬼的道路充满死亡。',
                            on_dismiss=self.back_to_title)

    def show_popup(self, title, message, on_dismiss=None):
        content = BoxLayout(orientation='vertical', padding='20dp', spacing='15dp')
        lbl = Label(text=message, font_size='14sp', color=C_TEXT)
        content.add_widget(lbl)
        btn = GameButton(text='确 定', height='48dp')
        content.add_widget(btn)
        popup = Popup(title=title, content=content, size_hint=(0.85, 0.5),
                      background=C_PANEL, title_color=C_GOLD)
        btn.bind(on_press=lambda x: (popup.dismiss(), on_dismiss() if on_dismiss else None))
        popup.open()


if __name__ == '__main__':
    MysteryRevivalApp().run()
