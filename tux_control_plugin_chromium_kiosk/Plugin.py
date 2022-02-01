from yaml import load, SafeLoader, dump
from typing import List
from tux_control.plugin.IPlugin import IPlugin

from tux_control.plugin.IPluginConfigItem import IPluginConfigItem
from tux_control.plugin.PluginConfigOption import PluginConfigOption
from tux_control.plugin.GridColumn import GridColumn

from tux_control.plugin.controls.Select import Select
from tux_control.plugin.controls.Text import Text
from tux_control.plugin.controls.Url import Url
from tux_control.plugin.controls.Number import Number
from tux_control.plugin.controls.MultiSelect import MultiSelect
from tux_control.plugin.controls.Chips import Chips
from tux_control.plugin.exceptions import SetException
from tux_control.plugin.SystemUser import SystemUser

from tux_control.plugin.validators.RequiredValidator import RequiredValidator
from tux_control.plugin.validators.UrlValidator import UrlValidator
from tux_control.plugin.validators.NumberValidator import NumberValidator


from tux_control_plugin_chromium_kiosk.PluginConfigItem import PluginConfigItem


class Plugin(IPlugin):
    _chromium_kiosk_config_path = '/etc/chromium-kiosk/config.yml'
    name = 'Chromium Kiosk'
    icon = 'desktop'

    plugin_permissions = {
        'chromium_kiosk.access': 'Allows access to chromium kiosk settings'
    }

    on_set_plugin_config_item_class = PluginConfigItem
    on_new_plugin_config_item_class = PluginConfigItem

    grid_columns = [
        GridColumn('name', 'Name', filter_match_mode='contains'),
        GridColumn('home_page', 'Home page')
    ]

    def __init__(self, plugin_key: str = None, plugin_config: dict = None) -> None:
        self.plugin_key = plugin_key
        self.plugin_config = plugin_config

    @property
    def key(self) -> str:
        return self.__class__.__module__

    @property
    def is_active(self) -> bool:
        if not SystemUser.has_permission('chromium_kiosk.access'):
            return False

        try:
            import chromium_kiosk
            return True
        except ImportError:
            return False

    @property
    def plugin_config_items(self) -> List[IPluginConfigItem]:
        chromium_kiosk_config = self._get_chromium_kiosk_config()

        return [
            PluginConfigItem.from_chromium_kiosk_config(chromium_kiosk_config, plugin_config_options=self.plugin_config_options)
        ]

    def on_get_plugin_config_item(self, plugin_config_item_key: str) -> PluginConfigItem:
        chromium_kiosk_config = self._get_chromium_kiosk_config()
        plugin_config_item = PluginConfigItem.from_chromium_kiosk_config(chromium_kiosk_config, plugin_config_options=self.plugin_config_options)
        if plugin_config_item.key != plugin_config_item_key:
            raise ValueError('WTH? {}'.format(plugin_config_item_key, plugin_config_item.key))
        return plugin_config_item

    def on_set_plugin_config_item(self, plugin_config_item: PluginConfigItem):
        try:
            with open(self._chromium_kiosk_config_path, 'w') as f:
                dump(plugin_config_item.to_chromium_kiosk_config(), f)
        except (FileNotFoundError, PermissionError) as e:
            raise SetException('Failed to save configuration: {}'.format(e)) from e

    @property
    def new_item_plugin_config_options(self) -> List[PluginConfigOption]:
        return [
            PluginConfigOption(
                'name',
                'Name',
                'Name of configuration item',
                Text(),
                [RequiredValidator()]
            ),
        ] + self.plugin_config_options

    @property
    def plugin_config_options(self) -> List[PluginConfigOption]:
        return [
            PluginConfigOption(
                'clean_start',
                'Clean start of kiosk on each boot',
                'Force chromium to clean start on each boot (That simply means do not show "Restore pages" dialog, you want this to be true in 99% of use cases)',
                Select([
                    {'label': 'Yes', 'value': True},
                    {'label': 'No', 'value': False},
                ]),
                [RequiredValidator()],
                default_value=True,
            ),
            PluginConfigOption(
                'kiosk',
                'Kiosk mode',
                'Run in kiosk mode, chromium will use whole screen without any way for user to close it, setting this to false is useful for web application debug (you can access chromium Inspect tool and so on) and initial chromium configuration',
                Select([
                    {'label': 'Yes', 'value': True},
                    {'label': 'No', 'value': False},
                ]),
                [RequiredValidator()],
                default_value=True,
            ),
            PluginConfigOption(
                'touchscreen',
                'Touchscreen mode',
                'Enables support for touchscreen',
                Select([
                    {'label': 'Yes', 'value': True},
                    {'label': 'No', 'value': False},
                ]),
                [RequiredValidator()],
                default_value=True,
            ),
            PluginConfigOption(
                'home_page',
                'Homepage of kiosk',
                'Url to load as homepage',
                Url(),
                [
                    RequiredValidator(),
                    UrlValidator()
                ],
                default_value='https://salamek.github.io/chromium-kiosk/',
            ),
            PluginConfigOption(
                'idle_time',
                'Idle time (s)',
                'How log must be kiosk idle to redirect to HOME_PAGE, 0 to disable',
                Number(),
                [
                    RequiredValidator(),
                    NumberValidator()
                ],
                default_value=0,
            ),
            PluginConfigOption(
                'white_list_enabled',
                'Enable whitelist',
                'Is white list enabled',
                Select([
                    {'label': 'Yes', 'value': True},
                    {'label': 'No', 'value': False},
                ]),
                [RequiredValidator()],
                default_value=False,
            ),
            PluginConfigOption(
                'white_list_urls',
                'Whitelisted URLS',
                'List of whitelisted urls, glob format is supported (eg,: *,google.*/news)',
                Chips(),
                [],
                default_value=[],
            ),
            PluginConfigOption(
                'white_list_iframe_enabled',
                'Enable whitelist iframes',
                'True to enable all iframes, list of urls to specify enabled iframes',
                Chips(),
                [],
                default_value=['true'],
            ),
            PluginConfigOption(
                'nav_bar_enabled',
                'Navbar enabled',
                'Is nav bar enabled',
                Select([
                    {'label': 'Yes', 'value': True},
                    {'label': 'No', 'value': False},
                ]),
                [RequiredValidator()],
                default_value=False,
            ),
            PluginConfigOption(
                'nav_bar_enabled_buttons',
                'Navbar enabled buttons',
                'What buttons shoudl be enabled in navbar',
                MultiSelect([
                    {'label': 'Home', 'value': 'home'},
                    {'label': 'Reload', 'value': 'reload'},
                    {'label': 'Back', 'value': 'back'},
                    {'label': 'Forward', 'value': 'forward'},
                ]),
                [RequiredValidator()],
                default_value=['home', 'reload', 'back', 'forward'],
            ),
            PluginConfigOption(
                'nav_bar_vertical_position',
                'Vertical position',
                'Vertical position on the screen',
                Select([
                    {'label': 'Bottom', 'value': 'bottom'},
                    {'label': 'Top', 'value': 'top'},
                ]),
                [RequiredValidator()],
                default_value='bottom',
            ),
            PluginConfigOption(
                'nav_bar_horizontal_position',
                'Horizontal position',
                'Horizontal position on the screen',
                Select([
                    {'label': 'Center', 'value': 'center'},
                    {'label': 'Left', 'value': 'left'},
                    {'label': 'Right', 'value': 'right'},
                ]),
                [RequiredValidator()],
                default_value='center',
            ),
            PluginConfigOption(
                'nav_bar_width',
                'Width of bar',
                'Width of a bar in %',
                Number(),
                [
                    RequiredValidator(),
                    NumberValidator()
                ],
                default_value=100,
            ),
            PluginConfigOption(
                'virtual_keyboard_enabled',
                'Virtual keyboard enabled',
                'Is virtual keyboard enabled',
                Select([
                    {'label': 'Yes', 'value': True},
                    {'label': 'No', 'value': False},
                ]),
                [RequiredValidator()],
                default_value=False,
            ),

            PluginConfigOption(
                'screen_rotation',
                'Screen rotation',
                'Rotation of the screen',
                Select([
                    {'label': 'Normal', 'value': 'normal'},
                    {'label': 'Left', 'value': 'left'},
                    {'label': 'Right', 'value': 'right'},
                    {'label': 'Inverted', 'value': 'inverted'},
                ]),
                [RequiredValidator()],
                default_value='normal',
            ),
            PluginConfigOption(
                'touchscreen_rotation',
                'Touchscreen rotation',
                'Rotation of the touchscreen',
                Select([
                    {'label': 'Normal', 'value': 'normal'},
                    {'label': 'Left', 'value': 'left'},
                    {'label': 'Right', 'value': 'right'},
                    {'label': 'Inverted', 'value': 'inverted'},
                ]),
                [RequiredValidator()],
                default_value='normal',
            ),
        ]

    def _get_chromium_kiosk_config(self) -> dict:
        try:
            with open(self._chromium_kiosk_config_path, 'r') as f:
                loaded_data = load(f.read(), Loader=SafeLoader)
                if isinstance(loaded_data, dict):
                    return loaded_data
                else:
                    raise Exception('Failed to parse configuration {}'.format(self._chromium_kiosk_config_path))
        except FileNotFoundError:
            return {}
