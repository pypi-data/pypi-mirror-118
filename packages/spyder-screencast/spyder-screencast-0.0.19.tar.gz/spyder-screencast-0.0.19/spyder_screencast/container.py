# -*- coding: utf-8 -*-

# Third party imports
from qtpy.QtCore import QSize, QPoint, Signal
from spyder.api.translations import get_translation
from spyder.api.widgets.main_container import PluginMainContainer

# Local imports
from spyder_screencast.api import ScreenResolutions
from spyder_screencast.widgets import ScreenCastStatusWidget


# Localization
_ = get_translation('spyder_screencast')


class ScreenCastContainer(PluginMainContainer):
    DEFAULT_OPTIONS = {
        'resolution': ScreenResolutions.Screen1080x1020
    }

    # Signals
    sig_resize_main_window_requested = Signal(QSize)
    sig_move_main_window_requested = Signal(QPoint)

    def __init__(self, name, plugin, parent=None):
        super().__init__(name, plugin, parent)

    def init_screen_cast_widget(self, main):
        self.status_widget = ScreenCastStatusWidget(parent=self, main_window=main)

    # --- PluginMainContainer API
    # ------------------------------------------------------------------------
    def setup(self, options=DEFAULT_OPTIONS):
        self.create_action(
            'screencast_action',
            text=_("Start recording..."),
            icon=self.create_icon("python"),
            triggered=self.start_recording,
        )

    def on_option_update(self, option, value):
        pass

    def update_actions(self):
        pass

    # --- Public API
    # ------------------------------------------------------------------------
    def start_recording(self):
        pass

    def stop_recording(self):
        pass

    def update_size(self, size):
        pass

    def update_position(self, position):
        pass
