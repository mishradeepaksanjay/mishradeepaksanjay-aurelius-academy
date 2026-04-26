"""
screens/settings_screen.py — Settings Screen
"""

import json, os
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

CFG = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.json")

Builder.load_string("""
#:import dp kivy.metrics.dp

<SettingsScreen>:
    canvas.before:
        Color:
            rgba: 0.051, 0.051, 0.102, 1
        Rectangle:
            pos: self.pos
            size: self.size

    BoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(14)

        # Header
        BoxLayout:
            size_hint_y: None
            height: dp(52)
            padding: [0, dp(8)]

            Button:
                text: '← Back'
                size_hint_x: None
                width: dp(80)
                font_size: dp(13)
                background_normal: ''
                background_color: 0.102, 0.102, 0.220, 1
                color: 0.910, 0.910, 0.941, 1
                on_release: root.go_back()

            Label:
                text: '⚙️  Settings'
                font_size: dp(18)
                bold: True
                color: 0.788, 0.659, 0.298, 1
                halign: 'center'

            Widget:
                size_hint_x: None
                width: dp(80)

        ScrollView:
            BoxLayout:
                orientation: 'vertical'
                spacing: dp(14)
                size_hint_y: None
                height: self.minimum_height
                padding: dp(4)

                # API Key Card
                BoxLayout:
                    orientation: 'vertical'
                    spacing: dp(8)
                    size_hint_y: None
                    height: dp(140)
                    padding: dp(16)
                    canvas.before:
                        Color:
                            rgba: 0.075, 0.075, 0.169, 1
                        RoundedRectangle:
                            pos: self.pos
                            size: self.size
                            radius: [dp(12)]

                    Label:
                        text: '🔑  Anthropic API Key'
                        font_size: dp(13)
                        bold: True
                        color: 0.788, 0.659, 0.298, 1
                        halign: 'left'
                        text_size: self.size
                        size_hint_y: None
                        height: dp(22)

                    Label:
                        text: 'Get yours FREE at: console.anthropic.com'
                        font_size: dp(10)
                        color: 0.314, 0.314, 0.439, 1
                        halign: 'left'
                        text_size: self.size
                        size_hint_y: None
                        height: dp(18)

                    TextInput:
                        id: inp_key
                        hint_text: 'sk-ant-api03-...'
                        password: True
                        multiline: False
                        size_hint_y: None
                        height: dp(44)
                        background_color: 0.035, 0.035, 0.086, 1
                        foreground_color: 0.910, 0.910, 0.941, 1
                        cursor_color: 0.788, 0.659, 0.298, 1
                        hint_text_color: 0.314, 0.314, 0.439, 1
                        font_size: dp(12)
                        padding: [dp(12), dp(10)]

                # PDF Folder Card
                BoxLayout:
                    orientation: 'vertical'
                    spacing: dp(8)
                    size_hint_y: None
                    height: dp(130)
                    padding: dp(16)
                    canvas.before:
                        Color:
                            rgba: 0.075, 0.075, 0.169, 1
                        RoundedRectangle:
                            pos: self.pos
                            size: self.size
                            radius: [dp(12)]

                    Label:
                        text: '📂  PDF Books Folder Path'
                        font_size: dp(13)
                        bold: True
                        color: 0.788, 0.659, 0.298, 1
                        halign: 'left'
                        text_size: self.size
                        size_hint_y: None
                        height: dp(22)

                    Label:
                        text: 'Full path to folder containing your GIA PDF books'
                        font_size: dp(10)
                        color: 0.314, 0.314, 0.439, 1
                        halign: 'left'
                        text_size: self.size
                        size_hint_y: None
                        height: dp(18)

                    TextInput:
                        id: inp_folder
                        hint_text: '/storage/emulated/0/Download/GIA_Books'
                        multiline: False
                        size_hint_y: None
                        height: dp(44)
                        background_color: 0.035, 0.035, 0.086, 1
                        foreground_color: 0.910, 0.910, 0.941, 1
                        cursor_color: 0.788, 0.659, 0.298, 1
                        hint_text_color: 0.314, 0.314, 0.439, 1
                        font_size: dp(12)
                        padding: [dp(12), dp(10)]

                # Model Card
                BoxLayout:
                    orientation: 'vertical'
                    spacing: dp(8)
                    size_hint_y: None
                    height: dp(120)
                    padding: dp(16)
                    canvas.before:
                        Color:
                            rgba: 0.075, 0.075, 0.169, 1
                        RoundedRectangle:
                            pos: self.pos
                            size: self.size
                            radius: [dp(12)]

                    Label:
                        text: '🤖  AI Model  (leave blank for default)'
                        font_size: dp(13)
                        bold: True
                        color: 0.788, 0.659, 0.298, 1
                        halign: 'left'
                        text_size: self.size
                        size_hint_y: None
                        height: dp(22)

                    Label:
                        text: 'Default: claude-haiku-4-5-20251001'
                        font_size: dp(10)
                        color: 0.314, 0.314, 0.439, 1
                        halign: 'left'
                        text_size: self.size
                        size_hint_y: None
                        height: dp(18)

                    TextInput:
                        id: inp_model
                        hint_text: 'claude-haiku-4-5-20251001'
                        multiline: False
                        size_hint_y: None
                        height: dp(44)
                        background_color: 0.035, 0.035, 0.086, 1
                        foreground_color: 0.910, 0.910, 0.941, 1
                        cursor_color: 0.788, 0.659, 0.298, 1
                        hint_text_color: 0.314, 0.314, 0.439, 1
                        font_size: dp(12)
                        padding: [dp(12), dp(10)]

                Label:
                    id: save_lbl
                    text: ''
                    font_size: dp(12)
                    color: 0.400, 0.733, 0.416, 1
                    size_hint_y: None
                    height: dp(24)
                    halign: 'center'

                Button:
                    text: '💾  Save Settings'
                    font_size: dp(15)
                    bold: True
                    size_hint_y: None
                    height: dp(52)
                    background_normal: ''
                    background_color: 0.788, 0.659, 0.298, 1
                    color: 0.051, 0.051, 0.102, 1
                    on_release: root.save()

                Widget:
                    size_hint_y: None
                    height: dp(20)
""")


def _load_cfg():
    if os.path.exists(CFG):
        try:
            with open(CFG) as f:
                return json.load(f)
        except Exception:
            pass
    return {"api_key": "", "pdf_folder": "", "model": ""}


def _save_cfg(cfg):
    with open(CFG, "w") as f:
        json.dump(cfg, f, indent=2)


class SettingsScreen(Screen):
    app = None

    def on_enter(self):
        cfg = _load_cfg()
        self.ids.inp_key.text    = cfg.get("api_key",    "")
        self.ids.inp_folder.text = cfg.get("pdf_folder", "")
        self.ids.inp_model.text  = cfg.get("model",      "")

    def save(self):
        cfg = {
            "api_key":    self.ids.inp_key.text.strip(),
            "pdf_folder": self.ids.inp_folder.text.strip(),
            "model":      self.ids.inp_model.text.strip(),
        }
        _save_cfg(cfg)
        # Push to chat screen engine
        if self.app:
            chat = self.app.root.get_screen("chat")
            chat.apply_settings(cfg)
        self.ids.save_lbl.text = "✅  Settings saved!"

    def go_back(self):
        self.manager.current = "chat"
