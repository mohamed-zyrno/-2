from datetime import datetime
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.utils import platform

if platform == 'android':
    from android.permissions import request_permissions, Permission
    from jnius import autoclass
    request_permissions([
        Permission.INTERNET,
        Permission.READ_EXTERNAL_STORAGE,
        Permission.WRITE_EXTERNAL_STORAGE,
        Permission.POST_NOTIFICATIONS
    ])

    # للوصول إلى نغمة النظام
    MediaPlayer = autoclass('android.media.MediaPlayer')
    RingtoneManager = autoclass('android.media.RingtoneManager')
    Uri = autoclass('android.net.Uri')

class AlarmLayout(BoxLayout):
    alarm_time = None
    alarm_active = False

    def set_alarm(self):
        try:
            hour = int(self.ids.hour_input.text)
            minute = int(self.ids.minute_input.text)
            self.alarm_time = f"{hour:02}:{minute:02}"
            self.alarm_active = True
            self.ids.status_label.text = f"⏰ المنبه مضبوط على {self.alarm_time}"
        except ValueError:
            self.ids.status_label.text = "⚠️ رجاءً أدخل أرقام صحيحة!"

    def cancel_alarm(self):
        self.alarm_active = False
        self.ids.status_label.text = "❌ تم إلغاء المنبه"

    def check_alarm(self, dt):
        if self.alarm_active:
            now = datetime.now().strftime("%H:%M")
            if now == self.alarm_time:
                self.trigger_alarm()

    def trigger_alarm(self):
        self.alarm_active = False
        self.ids.status_label.text = "🔔 الوقت حان!"
        if platform == 'android':
            try:
                uri = RingtoneManager.getDefaultUri(RingtoneManager.TYPE_ALARM)
                ringtone = RingtoneManager.getRingtone(App.get_running_app()._activity, uri)
                ringtone.play()
            except Exception as e:
                print("Error playing alarm sound:", e)

class AlarmApp(App):
    def build(self):
        layout = AlarmLayout()
        Clock.schedule_interval(layout.check_alarm, 1)
        return layout

if __name__ == "__main__":
    AlarmApp().run()
