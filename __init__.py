"""
screens/login_screen.py — Login & Register Screen
"""

from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.clock import Clock

Builder.load_string("""
#:import dp kivy.metrics.dp

<LoginScreen>:
    canvas.before:
        Color:
            rgba: 0.051, 0.051, 0.102, 1
        Rectangle:
            pos: self.pos
            size: self.size

    BoxLayout:
        orientation: 'vertical'
        padding: dp(32)
        spacing: dp(16)

        # ── Logo ──
        BoxLayout:
            orientation: 'vertical'
            size_hint_y: None
            height: dp(160)
            spacing: dp(6)

            Label:
                text: '💎'
                font_size: dp(52)
                size_hint_y: None
                height: dp(72)
                halign: 'center'

            Label:
                text: 'AURELIUS ACADEMY'
                font_size: dp(22)
                bold: True
                color: 0.788, 0.659, 0.298, 1
                halign: 'center'
                size_hint_y: None
                height: dp(34)

            Label:
                text: 'Gemology  ·  Luxury Markets  ·  HNI Intelligence'
                font_size: dp(11)
                color: 0.565, 0.565, 0.690, 1
                halign: 'center'
                size_hint_y: None
                height: dp(22)

        # ── Card ──
        BoxLayout:
            orientation: 'vertical'
            spacing: dp(12)
            padding: dp(24)
            canvas.before:
                Color:
                    rgba: 0.075, 0.075, 0.169, 1
                RoundedRectangle:
                    pos: self.pos
                    size: self.size
                    radius: [dp(16)]

            # Tab row
            BoxLayout:
                size_hint_y: None
                height: dp(44)
                spacing: dp(6)

                Button:
                    id: btn_login
                    text: 'Sign In'
                    font_size: dp(13)
                    bold: True
                    background_normal: ''
                    background_color: 0.788, 0.659, 0.298, 1
                    color: 0.051, 0.051, 0.102, 1
                    on_release: root.switch_tab('login')

                Button:
                    id: btn_reg
                    text: 'Register'
                    font_size: dp(13)
                    background_normal: ''
                    background_color: 0.102, 0.102, 0.220, 1
                    color: 0.565, 0.565, 0.690, 1
                    on_release: root.switch_tab('register')

            # ── Login Fields ──
            BoxLayout:
                id: login_fields
                orientation: 'vertical'
                spacing: dp(10)

                Label:
                    text: 'Username'
                    font_size: dp(11)
                    color: 0.565, 0.565, 0.690, 1
                    halign: 'left'
                    text_size: self.size
                    size_hint_y: None
                    height: dp(18)

                TextInput:
                    id: inp_user
                    hint_text: 'Enter username'
                    multiline: False
                    size_hint_y: None
                    height: dp(44)
                    background_color: 0.035, 0.035, 0.086, 1
                    foreground_color: 0.910, 0.910, 0.941, 1
                    cursor_color: 0.788, 0.659, 0.298, 1
                    hint_text_color: 0.314, 0.314, 0.439, 1
                    font_size: dp(14)
                    padding: [dp(12), dp(10)]

                Label:
                    text: 'Password'
                    font_size: dp(11)
                    color: 0.565, 0.565, 0.690, 1
                    halign: 'left'
                    text_size: self.size
                    size_hint_y: None
                    height: dp(18)

                TextInput:
                    id: inp_pwd
                    hint_text: 'Enter password'
                    password: True
                    multiline: False
                    size_hint_y: None
                    height: dp(44)
                    background_color: 0.035, 0.035, 0.086, 1
                    foreground_color: 0.910, 0.910, 0.941, 1
                    cursor_color: 0.788, 0.659, 0.298, 1
                    hint_text_color: 0.314, 0.314, 0.439, 1
                    font_size: dp(14)
                    padding: [dp(12), dp(10)]

            # ── Register Fields (hidden by default) ──
            BoxLayout:
                id: reg_fields
                orientation: 'vertical'
                spacing: dp(10)
                opacity: 0
                disabled: True

                Label:
                    text: 'Full Name'
                    font_size: dp(11)
                    color: 0.565, 0.565, 0.690, 1
                    halign: 'left'
                    text_size: self.size
                    size_hint_y: None
                    height: dp(18)

                TextInput:
                    id: inp_name
                    hint_text: 'Your full name'
                    multiline: False
                    size_hint_y: None
                    height: dp(44)
                    background_color: 0.035, 0.035, 0.086, 1
                    foreground_color: 0.910, 0.910, 0.941, 1
                    cursor_color: 0.788, 0.659, 0.298, 1
                    hint_text_color: 0.314, 0.314, 0.439, 1
                    font_size: dp(14)
                    padding: [dp(12), dp(10)]

                Label:
                    text: 'Role (e.g. Floor Manager)'
                    font_size: dp(11)
                    color: 0.565, 0.565, 0.690, 1
                    halign: 'left'
                    text_size: self.size
                    size_hint_y: None
                    height: dp(18)

                TextInput:
                    id: inp_role
                    hint_text: 'Floor Manager'
                    multiline: False
                    size_hint_y: None
                    height: dp(44)
                    background_color: 0.035, 0.035, 0.086, 1
                    foreground_color: 0.910, 0.910, 0.941, 1
                    cursor_color: 0.788, 0.659, 0.298, 1
                    hint_text_color: 0.314, 0.314, 0.439, 1
                    font_size: dp(14)
                    padding: [dp(12), dp(10)]

            Label:
                id: err_lbl
                text: ''
                font_size: dp(12)
                color: 0.937, 0.325, 0.314, 1
                size_hint_y: None
                height: dp(24)
                halign: 'center'

            Button:
                id: action_btn
                text: 'Enter the Academy  →'
                font_size: dp(14)
                bold: True
                size_hint_y: None
                height: dp(50)
                background_normal: ''
                background_color: 0.788, 0.659, 0.298, 1
                color: 0.051, 0.051, 0.102, 1
                on_release: root.action()

        Widget:
            size_hint_y: 0.1
""")


class LoginScreen(Screen):
    app  = None
    _tab = "login"

    def switch_tab(self, tab):
        self._tab = tab
        lf = self.ids.login_fields
        rf = self.ids.reg_fields
        bl = self.ids.btn_login
        br = self.ids.btn_reg
        ab = self.ids.action_btn
        self.ids.err_lbl.text = ""

        if tab == "login":
            lf.opacity = 1; lf.disabled = False
            rf.opacity = 0; rf.disabled = True
            bl.background_color = (0.788, 0.659, 0.298, 1)
            bl.color            = (0.051, 0.051, 0.102, 1)
            br.background_color = (0.102, 0.102, 0.220, 1)
            br.color            = (0.565, 0.565, 0.690, 1)
            ab.text = "Enter the Academy  →"
        else:
            lf.opacity = 0; lf.disabled = True
            rf.opacity = 1; rf.disabled = False
            br.background_color = (0.788, 0.659, 0.298, 1)
            br.color            = (0.051, 0.051, 0.102, 1)
            bl.background_color = (0.102, 0.102, 0.220, 1)
            bl.color            = (0.565, 0.565, 0.690, 1)
            ab.text = "Create Account  →"

    def action(self):
        if self._tab == "login":
            self._do_login()
        else:
            self._do_register()

    def _do_login(self):
        uname = self.ids.inp_user.text.strip()
        pwd   = self.ids.inp_pwd.text.strip()
        if not uname or not pwd:
            self.ids.err_lbl.text = "⚠️  Please enter username and password"
            return
        user = self.app.db.login(uname, pwd)
        if user:
            self.ids.inp_user.text = ""
            self.ids.inp_pwd.text  = ""
            self.ids.err_lbl.text  = ""
            self.app.on_login(user)
        else:
            self.ids.err_lbl.text = "❌  Invalid username or password"

    def _do_register(self):
        name  = self.ids.inp_name.text.strip()
        uname = self.ids.inp_user.text.strip()
        pwd   = self.ids.inp_pwd.text.strip()
        role  = self.ids.inp_role.text.strip() or "Floor Manager"
        if not all([name, uname, pwd]):
            self.ids.err_lbl.text = "⚠️  Please fill all required fields"
            return
        if self.app.db.register(uname, pwd, name, role):
            self.ids.err_lbl.text = f"✅  Welcome {name}! Please Sign In."
            self.switch_tab("login")
        else:
            self.ids.err_lbl.text = "❌  Username already taken"
