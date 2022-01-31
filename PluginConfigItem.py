from typing import List
from tux_control.plugin.IPluginConfigItem import IPluginConfigItem
from tux_control.plugin.PluginConfigOption import PluginConfigOption


class PluginConfigItem(IPluginConfigItem):
    name = None
    key = 'main'
    is_deletable = False
    is_editable = True
    plugin_config_options = None

    def __init__(self,
                 name: str,
                 clean_start: bool,
                 kiosk: bool,
                 touchscreen: bool,
                 home_page: bool,
                 idle_time: int,
                 white_list_enabled: bool,
                 white_list_urls: List[str],
                 white_list_iframe_enabled: List[str],
                 nav_bar_enabled: bool,
                 nav_bar_enabled_buttons: List[str],
                 nav_bar_vertical_position: str,
                 nav_bar_horizontal_position: str,
                 nav_bar_width: int,
                 virtual_keyboard_enabled: bool,
                 screen_saver_enabled: bool,
                 screen_saver_idle_time: bool,
                 screen_saver_text: str,
                 screen_rotation: str,
                 touchscreen_rotation: str,
                 plugin_config_options: List[PluginConfigOption]
                 ):
        self.name = name
        self.clean_start = clean_start
        self.kiosk = kiosk
        self.touchscreen = touchscreen
        self.home_page = home_page
        self.idle_time = idle_time
        self.white_list_enabled = white_list_enabled
        self.white_list_urls = white_list_urls
        self.white_list_iframe_enabled = white_list_iframe_enabled
        self.nav_bar_enabled = nav_bar_enabled
        self.nav_bar_enabled_buttons = nav_bar_enabled_buttons
        self.nav_bar_vertical_position = nav_bar_vertical_position
        self.nav_bar_horizontal_position = nav_bar_horizontal_position
        self.nav_bar_width = nav_bar_width
        self.virtual_keyboard_enabled = virtual_keyboard_enabled
        self.screen_saver_enabled = screen_saver_enabled
        self.screen_saver_idle_time = screen_saver_idle_time
        self.screen_saver_text = screen_saver_text
        self.screen_rotation = screen_rotation
        self.touchscreen_rotation = touchscreen_rotation
        self.plugin_config_options = plugin_config_options

    @staticmethod
    def from_chromium_kiosk_config(chromium_kiosk_config: dict, plugin_config_options: List[PluginConfigOption]) -> 'PluginConfigItem':
        return PluginConfigItem(
            name='Main config',
            clean_start=chromium_kiosk_config.get('CLEAN_START', True),
            kiosk=chromium_kiosk_config.get('KIOSK', True),
            touchscreen=chromium_kiosk_config.get('TOUCHSCREEN', True),
            home_page=chromium_kiosk_config.get('HOME_PAGE', 'https://salamek.cz'),
            idle_time=chromium_kiosk_config.get('IDLE_TIME', 0),

            white_list_enabled=chromium_kiosk_config.get('WHITE_LIST', {}).get('ENABLED', False),
            white_list_urls=chromium_kiosk_config.get('WHITE_LIST', {}).get('URLS', []),
            white_list_iframe_enabled=chromium_kiosk_config.get('WHITE_LIST', {}).get('IFRAME_ENABLED', []),

            nav_bar_enabled=chromium_kiosk_config.get('NAV_BAR', {}).get('ENABLED', False),
            nav_bar_enabled_buttons=chromium_kiosk_config.get('NAV_BAR', {}).get('ENABLED_BUTTONS', ['home', 'reload']),
            nav_bar_vertical_position=chromium_kiosk_config.get('NAV_BAR', {}).get('VERTICAL_POSITION', 'bottom'),
            nav_bar_horizontal_position=chromium_kiosk_config.get('NAV_BAR', {}).get('HORIZONTAL_POSITION', 'center'),
            nav_bar_width=chromium_kiosk_config.get('NAV_BAR', {}).get('WIDTH', 100),

            virtual_keyboard_enabled=chromium_kiosk_config.get('VIRTUAL_KEYBOARD', {}).get('ENABLED', False),

            screen_saver_enabled=chromium_kiosk_config.get('SCREEN_SAVER', {}).get('ENABLED', False),
            screen_saver_idle_time=chromium_kiosk_config.get('SCREEN_SAVER', {}).get('IDLE_TIME', False),
            screen_saver_text=chromium_kiosk_config.get('SCREEN_SAVER', {}).get('TEXT', False),

            screen_rotation=chromium_kiosk_config.get('SCREEN_ROTATION', 'normal'),
            touchscreen_rotation=chromium_kiosk_config.get('TOUCHSCREEN_ROTATION', 'normal'),
            plugin_config_options=plugin_config_options
        )

    @staticmethod
    def from_dict(data: dict) -> 'PluginConfigItem':
        del data['key']
        del data['is_deletable']
        del data['is_editable']
        return PluginConfigItem(**data)

    def to_chromium_kiosk_config(self) -> dict:
        return {
            'CLEAN_START': self.clean_start,
            'KIOSK': self.kiosk,
            'TOUCHSCREEN': self.touchscreen,
            'HOME_PAGE': self.home_page,
            'IDLE_TIME': self.idle_time,
            'WHITE_LIST': {
                'ENABLED': self.white_list_enabled,
                'URLS': self.white_list_urls,
                'IFRAME_ENABLED': self.white_list_iframe_enabled,
            },
            'NAV_BAR': {
                'ENABLED': self.nav_bar_enabled,
                'ENABLED_BUTTONS': self.nav_bar_enabled_buttons,
                'VERTICAL_POSITION': self.nav_bar_vertical_position,
                'HORIZONTAL_POSITION': self.nav_bar_horizontal_position,
                'WIDTH': self.nav_bar_width,
            },
            'VIRTUAL_KEYBOARD': {
                'ENABLED': self.virtual_keyboard_enabled
            },
            'SCREEN_SAVER': {
                'ENABLED': self.screen_saver_enabled,
                'IDLE_TIME': self.screen_saver_idle_time,
                'TEXT': self.screen_saver_text,
            },
            'SCREEN_ROTATION': self.screen_rotation,
            'TOUCHSCREEN_ROTATION': self.touchscreen_rotation,
        }

    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'key': self.key,
            'is_deletable': self.is_deletable,
            'is_editable': self.is_editable,
            'plugin_config_options': self.plugin_config_options,
            'clean_start': self.clean_start,
            'kiosk': self.kiosk,
            'touchscreen': self.touchscreen,
            'home_page': self.home_page,
            'idle_time': self.idle_time,
            'white_list_enabled': self.white_list_enabled,
            'white_list_urls': self.white_list_urls,
            'white_list_iframe_enabled': self.white_list_iframe_enabled,
            'nav_bar_enabled': self.nav_bar_enabled,
            'nav_bar_enabled_buttons': self.nav_bar_enabled_buttons,
            'nav_bar_vertical_position': self.nav_bar_vertical_position,
            'nav_bar_horizontal_position': self.nav_bar_horizontal_position,
            'nav_bar_width': self.nav_bar_width,
            'virtual_keyboard_enabled': self.virtual_keyboard_enabled,
            'screen_saver_enabled': self.screen_saver_enabled,
            'screen_saver_idle_time': self.screen_saver_idle_time,
            'screen_saver_text': self.screen_saver_text,
            'screen_rotation': self.screen_rotation,
            'touchscreen_rotation': self.touchscreen_rotation,
        }

