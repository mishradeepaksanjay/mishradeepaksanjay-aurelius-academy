"""
screens/chat_screen.py — Main Chat Screen (Android-optimised)
"""

import threading
import json
import os
import sys

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout     import BoxLayout
from kivy.uix.label         import Label
from kivy.uix.button        import Button
from kivy.uix.scrollview    import ScrollView
from kivy.uix.textinput     import TextInput
from kivy.uix.widget        import Widget
from kivy.metrics           import dp
from kivy.lang              import Builder
from kivy.clock             import Clock
from kivy.uix.popup         import Popup

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "modules"))
from aurelius_engine import AureliusEngine
from pdf_engine      import PDFEngine
from quiz_engine     import QuizEngine

CFG_FILE    = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.json")
HNI_TRIGGER = 10

GOLD  = (0.788, 0.659, 0.298, 1)
DARK  = (0.051, 0.051, 0.102, 1)
TEXT  = (0.910, 0.910, 0.941, 1)
TEXT2 = (0.565, 0.565, 0.690, 1)
TEXT3 = (0.314, 0.314, 0.439, 1)
PANEL = (0.059, 0.059, 0.133, 1)
CARD  = (0.075, 0.075, 0.169, 1)
INP   = (0.035, 0.035, 0.086, 1)
RED   = (0.937, 0.325, 0.314, 1)
GREEN = (0.400, 0.733, 0.416, 1)
USER_BG = (0.102, 0.180, 0.333, 1)
AI_BG   = (0.063, 0.102, 0.063, 1)
PULSE_BG= (0.047, 0.102, 0.047, 1)

WELCOME = """\
💎 Welcome, {name}!

I'm Professor Aurelius — your elite guide through gemology, lab-grown diamonds, and luxury HNI markets.

Quick tips:
• Type a topic or question below
• Say "Open Left Drawer" for session history
• Say "Enter Private Cabin" for off-topic help
• HNI Market Pulse fires every {n} Q&As!

Loaded Books: {books}

Ready when you are. Let's make you brilliant! ✨"""


def _cfg():
    if os.path.exists(CFG_FILE):
        try:
            with open(CFG_FILE) as f:
                return json.load(f)
        except Exception:
            pass
    return {"api_key": "", "pdf_folder": "", "model": ""}


# ── Bubble widget ─────────────────────────────────────────────────────────────

class BubbleLabel(BoxLayout):
    def __init__(self, role, name, text, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.size_hint_y = None
        self.padding     = [dp(8), dp(6)]
        self.spacing     = dp(4)

        is_user = role == "user"
        bg_col  = USER_BG if is_user else AI_BG

        # Role label
        rl = Label(
            text   = f"👤 {name}" if is_user else "🎓 Professor Aurelius",
            font_size = dp(11),
            bold   = True,
            color  = TEXT2 if is_user else GOLD,
            size_hint_y = None,
            height = dp(18),
            halign = "right" if is_user else "left",
        )
        rl.bind(size=lambda w,s: setattr(w, "text_size", s))
        self.add_widget(rl)

        # Message bubble
        lbl = Label(
            text      = text,
            font_size = dp(13),
            color     = TEXT,
            size_hint_y = None,
            halign    = "right" if is_user else "left",
            markup    = False,
            padding   = (dp(12), dp(10)),
        )
        lbl.bind(texture_size=lambda w,s: setattr(w, "height", s[1] + dp(20)))
        lbl.bind(width=lambda w,_: setattr(w, "text_size", (w.width, None)))

        # Bubble background
        from kivy.uix.floatlayout import FloatLayout
        from kivy.graphics import Color, RoundedRectangle

        container = BoxLayout(size_hint_y=None)
        container.bind(minimum_height=container.setter("height"))
        with container.canvas.before:
            Color(*bg_col)
            self._rect = RoundedRectangle(radius=[dp(12)])
        def upd_rect(*_):
            self._rect.pos  = container.pos
            self._rect.size = container.size
        container.bind(pos=upd_rect, size=upd_rect)

        if is_user:
            container.add_widget(Widget())
        container.add_widget(lbl)
        if not is_user:
            container.add_widget(Widget())

        self.add_widget(container)
        self.bind(minimum_height=self.setter("height"))


class PulseBubble(BoxLayout):
    def __init__(self, text, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.size_hint_y = None
        self.padding     = [dp(12), dp(10)]
        self.spacing     = dp(6)

        from kivy.graphics import Color, RoundedRectangle, Line
        with self.canvas.before:
            Color(*PULSE_BG)
            self._bg = RoundedRectangle(radius=[dp(12)])
            Color(*GREEN)
            self._border = Line(rounded_rectangle=[0,0,0,0,dp(12)], width=dp(1.5))
        def upd(*_):
            self._bg.pos    = self.pos;   self._bg.size    = self.size
            self._border.rounded_rectangle = [self.x, self.y, self.width, self.height, dp(12)]
        self.bind(pos=upd, size=upd)

        hdr = Label(text="📈 HNI MARKET PULSE", font_size=dp(14), bold=True,
                    color=GREEN, size_hint_y=None, height=dp(26),
                    halign="left")
        hdr.bind(size=lambda w,s: setattr(w,"text_size",s))
        self.add_widget(hdr)

        body = Label(text=text, font_size=dp(12), color=TEXT,
                     size_hint_y=None, halign="left")
        body.bind(texture_size=lambda w,s: setattr(w,"height",s[1]+dp(10)))
        body.bind(width=lambda w,_: setattr(w,"text_size",(w.width,None)))
        self.add_widget(body)
        self.bind(minimum_height=self.setter("height"))


# ── Chat Screen ───────────────────────────────────────────────────────────────

Builder.load_string("""
#:import dp kivy.metrics.dp

<ChatScreen>:
    canvas.before:
        Color:
            rgba: 0.051, 0.051, 0.102, 1
        Rectangle:
            pos: self.pos
            size: self.size

    BoxLayout:
        orientation: 'vertical'

        # ── Top bar ──
        BoxLayout:
            size_hint_y: None
            height: dp(52)
            padding: [dp(12), dp(6)]
            spacing: dp(8)
            canvas.before:
                Color:
                    rgba: 0.059, 0.059, 0.133, 1
                Rectangle:
                    pos: self.pos
                    size: self.size

            Label:
                text: '💎 AURELIUS'
                font_size: dp(16)
                bold: True
                color: 0.788, 0.659, 0.298, 1
                size_hint_x: None
                width: dp(120)

            Label:
                id: qa_lbl
                text: 'Q&A: 0'
                font_size: dp(10)
                color: 0.314, 0.314, 0.439, 1

            Button:
                text: '☰'
                font_size: dp(18)
                size_hint_x: None
                width: dp(40)
                background_normal: ''
                background_color: 0.102, 0.102, 0.220, 1
                color: 0.910, 0.910, 0.941, 1
                on_release: root.toggle_drawer()

            Button:
                text: '⚙️'
                font_size: dp(16)
                size_hint_x: None
                width: dp(40)
                background_normal: ''
                background_color: 0.102, 0.102, 0.220, 1
                color: 0.910, 0.910, 0.941, 1
                on_release: root.go_settings()

            Button:
                text: '🚪'
                font_size: dp(16)
                size_hint_x: None
                width: dp(40)
                background_normal: ''
                background_color: 0.102, 0.102, 0.220, 1
                color: 0.937, 0.325, 0.314, 1
                on_release: root.logout()

        # ── PDF status ──
        Label:
            id: pdf_lbl
            text: 'No books loaded — go to ⚙️ Settings'
            font_size: dp(10)
            color: 0.314, 0.314, 0.439, 1
            size_hint_y: None
            height: dp(20)
            halign: 'center'

        # ── Chat scroll ──
        ScrollView:
            id: scroll
            do_scroll_x: False
            BoxLayout:
                id: msg_box
                orientation: 'vertical'
                size_hint_y: None
                height: self.minimum_height
                padding: [dp(8), dp(6)]
                spacing: dp(6)

        # ── Quick prompts ──
        ScrollView:
            size_hint_y: None
            height: dp(44)
            do_scroll_y: False
            BoxLayout:
                id: quick_row
                orientation: 'horizontal'
                size_hint_x: None
                width: self.minimum_width
                spacing: dp(6)
                padding: [dp(8), dp(4)]

        # ── Input bar ──
        BoxLayout:
            size_hint_y: None
            height: dp(64)
            padding: [dp(10), dp(8)]
            spacing: dp(8)
            canvas.before:
                Color:
                    rgba: 0.075, 0.075, 0.169, 1
                Rectangle:
                    pos: self.pos
                    size: self.size

            TextInput:
                id: msg_inp
                hint_text: 'Ask Professor Aurelius anything…'
                multiline: False
                size_hint_x: 1
                background_color: 0.035, 0.035, 0.086, 1
                foreground_color: 0.910, 0.910, 0.941, 1
                cursor_color: 0.788, 0.659, 0.298, 1
                hint_text_color: 0.314, 0.314, 0.439, 1
                font_size: dp(13)
                padding: [dp(12), dp(10)]
                on_text_validate: root.send()

            Button:
                text: '→'
                font_size: dp(20)
                bold: True
                size_hint_x: None
                width: dp(50)
                background_normal: ''
                background_color: 0.788, 0.659, 0.298, 1
                color: 0.051, 0.051, 0.102, 1
                on_release: root.send()

        Label:
            id: status_lbl
            text: 'Ready ✅'
            font_size: dp(10)
            color: 0.314, 0.314, 0.439, 1
            size_hint_y: None
            height: dp(18)
""")


class ChatScreen(Screen):
    app        = None
    _user      = {}
    _messages  = []
    _session_id= None
    _qa_count  = 0
    _pulse_at  = HNI_TRIGGER
    _drawer_open = False
    _drawer_popup= None

    def on_user_login(self, user):
        self._user     = user
        self._messages = []
        self._qa_count = 0
        self._pulse_at = HNI_TRIGGER

        cfg = _cfg()
        self.engine   = AureliusEngine(cfg.get("api_key",""), cfg.get("model",""))
        self.pdf_eng  = PDFEngine(self.app.db, cfg.get("pdf_folder",""))
        self.quiz_eng = QuizEngine(self.app.db)

        self._session_id = self.app.db.create_session(user["id"])
        self._setup_quick_prompts()
        self._clear_messages()
        self._post_welcome()
        self._upd_qa()

        if cfg.get("pdf_folder"):
            self._load_pdfs_bg()

    def apply_settings(self, cfg):
        self.engine.set_api_key(cfg.get("api_key",""))
        self.engine.set_model(cfg.get("model",""))
        if cfg.get("pdf_folder"):
            self.pdf_eng.set_folder(cfg["pdf_folder"])
            self._load_pdfs_bg()

    def _setup_quick_prompts(self):
        row = self.ids.quick_row
        row.clear_widgets()
        prompts = [
            ("📂 Drawer",    "Open Left Drawer"),
            ("🚪 Cabin",     "Enter Private Cabin"),
            ("📈 HNI Pulse", "Give me the HNI Market Pulse now"),
            ("💎 The 4Cs",   "Teach me the 4Cs of diamonds"),
            ("🔬 LGD vs Natural", "Compare lab-grown vs natural diamonds for a showroom pitch"),
            ("🏷️ HNI Pitch",     "How do I close a sale with a high net worth diamond buyer?"),
        ]
        for label, prompt in prompts:
            btn = Button(
                text=label, font_size=dp(11),
                size_hint=(None,None), height=dp(34),
                width=dp(len(label)*7.5 + 20),
                background_normal="",
                background_color=CARD,
                color=TEXT2,
            )
            btn.bind(on_release=lambda b, p=prompt: self._quick(p))
            row.add_widget(btn)
        row.width = sum(c.width + dp(6) for c in row.children) + dp(16)

    def _post_welcome(self):
        books = self.pdf_eng.get_book_list()
        bs = ", ".join(b.replace(".pdf","") for b in books) if books else "None — go to ⚙️ Settings"
        text = WELCOME.format(name=self._user.get("full_name",""), n=HNI_TRIGGER, books=bs)
        self._add_bubble("assistant", text)

    def _clear_messages(self):
        self.ids.msg_box.clear_widgets()

    def _add_bubble(self, role, text, pulse=False):
        if pulse:
            w = PulseBubble(text=text)
        else:
            w = BubbleLabel(role=role, name=self._user.get("full_name","You"), text=text)
        self.ids.msg_box.add_widget(w)
        Clock.schedule_once(lambda _: self._scroll_end(), 0.1)

    def _scroll_end(self):
        self.ids.scroll.scroll_y = 0

    def _upd_qa(self):
        rem = max(self._pulse_at - self._qa_count, 0)
        self.ids.qa_lbl.text = f"Q&A: {self._qa_count}  |  Pulse in: {rem}"

    # ── SEND ──────────────────────────────────────────────────────────────────

    def _quick(self, text):
        self.ids.msg_inp.text = text
        self.send()

    def send(self):
        text = self.ids.msg_inp.text.strip()
        if not text: return
        self.ids.msg_inp.text = ""
        self._add_bubble("user", text)
        self._messages.append({"role":"user","content":text})
        self.app.db.add_message(self._session_id, "user", text)

        if len(self._messages)==1:
            title = text[:50]+("…" if len(text)>50 else "")
            self.app.db.update_session_title(self._session_id, title)

        self.ids.status_lbl.text = "✍️ Professor Aurelius is composing…"
        threading.Thread(target=self._fetch, args=(text,), daemon=True).start()

    def _fetch(self, user_text):
        ctx   = self.pdf_eng.get_context(user_text) if self.pdf_eng.loaded else ""
        reply = self.engine.chat(self._messages.copy(), context=ctx)
        Clock.schedule_once(lambda _: self._on_reply(reply, user_text))

    def _on_reply(self, reply, user_text):
        self._add_bubble("assistant", reply)
        self._messages.append({"role":"assistant","content":reply})
        self.app.db.add_message(self._session_id, "assistant", reply)

        pairs = self.quiz_eng.extract_qa_pairs(reply)
        if pairs:
            prev = self._qa_count
            self._qa_count += len(pairs)
            self.quiz_eng.save_qa_pairs(
                self._user["id"], self._session_id, pairs, user_text[:60])
            self.quiz_eng.increment_qa(self._user["id"], len(pairs), user_text[:60])
            self._upd_qa()
            if (prev // HNI_TRIGGER) < (self._qa_count // HNI_TRIGGER):
                self._fire_pulse()

        self.ids.status_lbl.text = "Ready ✅"

    def _fire_pulse(self):
        self.ids.status_lbl.text = "📈 Fetching HNI Market Pulse…"
        pulse_q = ("SYSTEM TRIGGER: Deliver the '📈 Quick News Update: The HNI Market Pulse' "
                   "with 5 specific, current, insider bullet points on what HNI buyers are "
                   "discussing or purchasing in diamonds and jewelry globally right now.")
        msgs = self._messages[-4:] + [{"role":"user","content":pulse_q}]
        def run():
            reply = self.engine.chat(msgs, context="")
            Clock.schedule_once(lambda _: self._pulse_done(reply))
        threading.Thread(target=run, daemon=True).start()

    def _pulse_done(self, reply):
        self._add_bubble("assistant", reply, pulse=True)
        self._messages.append({"role":"assistant","content":reply})
        self.app.db.add_message(self._session_id, "assistant", reply)
        self._pulse_at += HNI_TRIGGER
        self._upd_qa()
        self.ids.status_lbl.text = "Ready ✅"

    # ── PDF ───────────────────────────────────────────────────────────────────

    def _load_pdfs_bg(self):
        self.ids.pdf_lbl.text = "⏳ Indexing PDF books…"
        def run():
            def cb(msg, _):
                Clock.schedule_once(lambda _,m=msg: setattr(self.ids.pdf_lbl,"text",m))
            self.pdf_eng.load_all(progress_cb=cb)
            books = self.pdf_eng.get_book_list()
            Clock.schedule_once(lambda _:
                setattr(self.ids.pdf_lbl,"text",
                        f"✅ {len(books)} books · {self.pdf_eng.total_chunks()} chunks"))
        threading.Thread(target=run, daemon=True).start()

    # ── DRAWER (History popup) ────────────────────────────────────────────────

    def toggle_drawer(self):
        sessions = self.app.db.get_sessions(self._user["id"])

        content = BoxLayout(orientation="vertical", spacing=dp(8), padding=dp(12))
        content.add_widget(Label(text="📚 Session History", font_size=dp(15),
                                 bold=True, color=GOLD, size_hint_y=None, height=dp(30)))

        sv = ScrollView()
        inner = BoxLayout(orientation="vertical", size_hint_y=None, spacing=dp(4))
        inner.bind(minimum_height=inner.setter("height"))

        for s in sessions[:20]:
            row = BoxLayout(size_hint_y=None, height=dp(44), spacing=dp(4))
            btn = Button(
                text=f"💬 {s['title'][:35]}", halign="left",
                font_size=dp(12), background_normal="",
                background_color=CARD, color=TEXT2,
            )
            btn.bind(on_release=lambda b, sid=s["id"], t=s["title"]: (
                popup.dismiss(), self._load_sess(sid, t)
            ))
            row.add_widget(btn)
            inner.add_widget(row)

        if not sessions:
            inner.add_widget(Label(text="No sessions yet", color=TEXT3,
                                   size_hint_y=None, height=dp(36)))

        sv.add_widget(inner)
        content.add_widget(sv)
        content.add_widget(Button(
            text="＋ New Chat", font_size=dp(13), bold=True,
            size_hint_y=None, height=dp(46),
            background_normal="", background_color=GOLD, color=DARK,
            on_release=lambda _: (popup.dismiss(), self._new_chat())
        ))
        content.add_widget(Button(
            text="Close", font_size=dp(12),
            size_hint_y=None, height=dp(38),
            background_normal="", background_color=CARD, color=TEXT2,
            on_release=lambda _: popup.dismiss()
        ))

        popup = Popup(
            title="", content=content,
            size_hint=(0.88, 0.75),
            background="",
            background_color=(0.075, 0.075, 0.169, 0.97),
            separator_height=0,
        )
        popup.open()

    def _new_chat(self):
        self._session_id = self.app.db.create_session(self._user["id"])
        self._messages   = []
        self._qa_count   = 0
        self._pulse_at   = HNI_TRIGGER
        self._clear_messages()
        self._post_welcome()
        self._upd_qa()

    def _load_sess(self, sid, title):
        self._session_id = sid
        self._messages   = self.app.db.get_messages(sid)
        self._clear_messages()
        for m in self._messages:
            self._add_bubble(m["role"], m["content"])

    # ── NAV ───────────────────────────────────────────────────────────────────

    def go_settings(self):
        self.manager.current = "settings"

    def logout(self):
        self.app.on_logout()
