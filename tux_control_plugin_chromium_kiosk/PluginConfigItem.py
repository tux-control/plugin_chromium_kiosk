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
                 plugin_config_options: List[PluginConfigOption]
                 ):
        self.name = name
        self.plugin_config_options = plugin_config_options

    @staticmethod
    def from_chromium_kiosk_config(chromium_kiosk_config: dict, plugin_config_options: List[PluginConfigOption]) -> 'PluginConfigItem':
        data = dict(
            full_screen=chromium_kiosk_config.get('FULL_SCREEN', True),
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

            screen_rotation=chromium_kiosk_config.get('SCREEN_ROTATION', 'normal'),
            touchscreen_rotation=chromium_kiosk_config.get('TOUCHSCREEN_ROTATION', 'normal')
        )

        for plugin_config_option in plugin_config_options:
            plugin_config_option._value = data.get(plugin_config_option.key)

        return PluginConfigItem(
            name='Main config',
            plugin_config_options=plugin_config_options
        )

    @staticmethod
    def from_dict(data: dict) -> 'PluginConfigItem':
        plugin_config_options = []
        for item in data.get('plugin_config_options'):
            plugin_config_option = PluginConfigOption.from_dict(item)
            plugin_config_options.append(plugin_config_option)

        name = data.get('name')
        return PluginConfigItem(
            name=name,
            plugin_config_options=plugin_config_options,
        )

    def to_chromium_kiosk_config(self) -> dict:
        data = {}
        for plugin_config_option in self.plugin_config_options:
            data[plugin_config_option.key] = plugin_config_option.value

        return {
            'FULL_SCREEN': data.get('full_screen'),
            'TOUCHSCREEN': data.get('touchscreen'),
            'HOME_PAGE': data.get('home_page'),
            'IDLE_TIME':  data.get('idle_time'),
            'WHITE_LIST': {
                'ENABLED': data.get('white_list_enabled'),
                'URLS': data.get('white_list_urls'),
                'IFRAME_ENABLED': data.get('white_list_iframe_enabled'),
            },
            'NAV_BAR': {
                'ENABLED': data.get('nav_bar_enabled'),
                'ENABLED_BUTTONS': data.get('nav_bar_enabled_buttons'),
                'VERTICAL_POSITION': data.get('nav_bar_vertical_position'),
                'HORIZONTAL_POSITION': data.get('nav_bar_horizontal_position'),
                'WIDTH': data.get('nav_bar_width'),
            },
            'VIRTUAL_KEYBOARD': {
                'ENABLED': data.get('virtual_keyboard_enabled')
            },
            'SCREEN_ROTATION': data.get('screen_rotation'),
            'TOUCHSCREEN_ROTATION': data.get('touchscreen_rotation'),
        }

    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'key': self.key,
            'is_deletable': self.is_deletable,
            'is_editable': self.is_editable,
            'plugin_config_options': self.plugin_config_options
        }

