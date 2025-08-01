from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtCore import Qt
from krita import Krita, DockWidget, DockWidgetFactory, DockWidgetFactoryBase

DOCKER_NAME = 'layerUtil_CSP'
DOCKER_ID = 'pykrita_layerutil_csp'


class Layerutil_csp(DockWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle(DOCKER_NAME)

        self._main_widget = QWidget(self)
        self.setWidget(self._main_widget)
        self._main_widget.setStyleSheet("background-color: #696969;")
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(2, 2, 2, 2)
        self.layout.setSpacing(1) # vertical spacing 1px between rows
        self._main_widget.setLayout(self.layout)

        # Delay setup until Krita is ready
        app = Krita.instance()
        app.notifier().windowCreated.connect(self._setup_ui)
        app.notifier().setActive(True)

    def _setup_ui(self, *args):
        """Create the docker UI once Krita actions are ready."""

        # Row 1
        row1 = QHBoxLayout()
        row1.setAlignment(Qt.AlignRight)
        row1.setSpacing(5)  # 5px spacing between buttons in the same row
        for action_id, fallback_text, tooltip in [
            ("toggle_layer_inherit_alpha", "IA", "Toggle layer alpha inheritance"),
            ("layer_properties", "P", "Properties (F3)"),
            ("layer_style", "🦚", "Layer Style"),
            ("toggle_layer_lock", "L", "Toggle layer lock"),
            ("create_quick_clipping_group", "📎", "Quick Clipping Group (Ctrl+Shift+G)"),
            ("toggle_layer_alpha_lock", "AL", "Toggle layer alpha"),
        ]:
            btn = self._make_action_button(action_id, fallback_text, tooltip)
            if btn:
                row1.addWidget(btn)
        self.layout.addLayout(row1)

        # Row 2
        row2 = QHBoxLayout()
        row2.setAlignment(Qt.AlignRight)
        row2.setSpacing(5)  # 5px spacing between buttons in the same row
        for action_id, fallback_text, tooltip in [
            ("add_new_paint_layer", "PL", "Add a new Paint Layer (Ins)"),
            ("add_new_adjustment_layer", "FL", "Add a new Filter Layer"),
            ("merge_layer", "M", "Merge with Layer Below (Ctrl+E)"),
            ("new_from_visible", "✅", "New layer from visible"),
            ("remove_layer", "X", "Remove Layer (Shift+Del)"),
        ]:
            btn = self._make_action_button(action_id, fallback_text, tooltip)
            if btn:
                row2.addWidget(btn)
        self.layout.addLayout(row2)

    def _make_action_button(self, action_id, fallback_text, tooltip):
        """Return a small 20x20 borderless QPushButton linked to a Krita action."""
        app = Krita.instance()
        action = app.action(action_id)
        if action is None:
            print(f"[Layerutil_csp] WARNING: action '{action_id}' not found.")
            return None

        btn = QPushButton()
        btn.setFixedSize(20, 20)

        # icon preferred, fallback to tiny text
        if not action.icon().isNull():
            btn.setIcon(action.icon())
            btn.setIconSize(btn.size())
        else:
            btn.setText(fallback_text)

        btn.setToolTip(tooltip)
        btn.clicked.connect(action.trigger)

        # remove borders/padding
        btn.setStyleSheet("""
            QPushButton {
                border: none;
                padding: 0px;
                margin: 0px;
                background: transparent;
            }
            QPushButton:hover {
                background: rgba(255,255,255,30);
            }
        """)

        return btn

    def canvasChanged(self, canvas):
        pass


# Register docker
instance = Krita.instance()
dock_widget_factory = DockWidgetFactory(
    DOCKER_ID,
    DockWidgetFactoryBase.DockRight,
    Layerutil_csp
)
instance.addDockWidgetFactory(dock_widget_factory)