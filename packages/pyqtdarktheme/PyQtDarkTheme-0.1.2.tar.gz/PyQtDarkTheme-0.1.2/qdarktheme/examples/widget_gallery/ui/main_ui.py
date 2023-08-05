from qdarktheme.resource_manager import get_icon
from qdarktheme.Qt.QtCore import Qt
from qdarktheme.Qt.QtGui import QAction
from qdarktheme.Qt.QtWidgets import QMainWindow, QMenuBar, QStackedWidget, QStatusBar, QToolBar, QToolButton, QWidget

from qdarktheme.examples.widget_gallery.ui.dock import DockUI
from qdarktheme.examples.widget_gallery.ui.home import HomeUI


class UI:
    def setup_ui(self, main_win: QMainWindow) -> None:
        # Attribute
        self.central_window = QMainWindow()
        self.stack_widget = QStackedWidget()

        self.action_change_home_window = QAction(get_icon("home"), "Move home")
        self.action_change_dock_window = QAction(get_icon("flip_to_front"), "Move dock")
        self.action_open_folder = QAction(get_icon("folder_open"), "Open folder dialog")
        self.action_open_color_dialog = QAction(get_icon("palette"), "Open color dialog", main_win)
        self.action_enable = QAction(get_icon("circle"), "Enable")
        self.action_disable = QAction(get_icon("clear"), "Disable")
        self.action_toggle_theme = QAction(get_icon("dark_mode"), "Change to a light theme")

        sidebar = QToolBar("Sidebar")
        toolbar = QToolBar("Toolbar")
        statusbar = QStatusBar()
        menubar = QMenuBar()
        tool_button_settings = QToolButton()
        tool_button_enable = QToolButton()
        tool_button_disable = QToolButton()
        tool_button_toggle_theme = QToolButton()

        # ui
        self.action_change_home_window.setCheckable(True)
        self.action_change_dock_window.setCheckable(True)
        self.action_change_home_window.setChecked(True)
        sidebar.setMovable(False)
        sidebar.addActions([self.action_change_home_window, self.action_change_dock_window])

        tool_button_settings.setIcon(get_icon("settings"))
        tool_button_settings.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        tool_button_settings.addActions([self.action_enable, self.action_disable])
        tool_button_enable.setDefaultAction(self.action_enable)
        tool_button_disable.setDefaultAction(self.action_disable)
        tool_button_toggle_theme.setDefaultAction(self.action_toggle_theme)

        toolbar.addActions([self.action_open_folder, self.action_open_color_dialog])
        toolbar.addSeparator()
        toolbar.addWidget(tool_button_settings)
        toolbar.addAction(self.action_toggle_theme)

        statusbar.addPermanentWidget(tool_button_enable)
        statusbar.addPermanentWidget(tool_button_disable)
        statusbar.addPermanentWidget(tool_button_toggle_theme)
        statusbar.showMessage("Enable")

        menu = menubar.addMenu("&Menu")
        menu.addAction(self.action_open_folder)
        menu.addSeparator()
        menu_toggle_status = menu.addMenu("&Toggle Status")
        menu_toggle_status.addActions([self.action_enable, self.action_disable])

        self.action_enable.setEnabled(False)

        # setup qss property
        sidebar.setProperty("type", "sidebar")

        # layout
        stack_1 = QWidget()
        home_ui = HomeUI()
        home_ui.setup_ui(stack_1)
        self.stack_widget.addWidget(stack_1)
        stack_2 = QMainWindow()
        dock_ui = DockUI()
        dock_ui._setup_ui(stack_2)
        self.stack_widget.addWidget(stack_2)

        self.central_window.setCentralWidget(self.stack_widget)
        self.central_window.addToolBar(toolbar)

        main_win.setCentralWidget(self.central_window)
        main_win.addToolBar(Qt.ToolBarArea.LeftToolBarArea, sidebar)
        main_win.setMenuBar(menubar)
        main_win.setStatusBar(statusbar)
