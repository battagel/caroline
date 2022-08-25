#!/usr/bin/env python3

from asciimatics.event import KeyboardEvent
from asciimatics.widgets import (
    Frame,
    Layout,
    Widget,
    Label,
    PopUpDialog,
    Text,
    Divider,
    DropdownList,
    Button,
    ListBox,
)
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError, StopApplication

from list_tree import LogLister
import sys
import os

try:
    import magic
except ImportError:
    pass


class Caroline(Frame):
    def __init__(self, screen):
        super(Caroline, self).__init__(
            screen, screen.height, screen.width, has_border=False, name="My Form"
        )

        # Create the (very simple) form layout...
        layout = Layout([1], fill_frame=True)
        self.add_layout(layout)

        # Hierarchical tree of data
        log_lister = LogLister("output.txt")

        self._data = log_lister.generate_data()

        self._list = ListBox(
            Widget.FILL_FRAME,
            self._data,
            name="Logs",
            add_scroll_bar=True,
            on_change=self._on_pick,
            on_select=self._edit,
        )

        # Bottom details
        self._details = Text()
        self._details.disabled = True
        self._details.custom_colour = "field"

        # Constructing layout
        layout.add_widget(Label("Caroline"))
        layout.add_widget(Divider())
        layout.add_widget(self._list)
        layout.add_widget(Divider())
        layout.add_widget(self._details)
        layout.add_widget(Label("Press Enter to select or `q` to quit."))

        # Prepare the Frame for use.
        self.fix()

    def _on_pick(self):
        pass

    def _edit(self):
        pass

    def popup(self):
        # Just confirm whenever the user actually selects something.
        self._scene.add_effect(
            PopUpDialog(
                self._screen, "You selected: {}".format(self._list.value), ["OK"]
            )
        )

    def details(self):
        self._details.value = "--"

    def process_event(self, event):
        # Do the key handling for this Frame.
        if isinstance(event, KeyboardEvent):
            if event.key_code in [ord("q"), ord("Q"), Screen.ctrl("c")]:
                raise StopApplication("User quit")

        # Now pass on to lower levels for normal handling of the event.
        return super(Caroline, self).process_event(event)


def start_app(screen, old_scene):
    screen.play(
        [Scene([Caroline(screen)], -1)], stop_on_resize=True, start_scene=old_scene
    )


last_scene = None
while True:
    try:
        Screen.wrapper(start_app, catch_interrupt=False, arguments=[last_scene])
        sys.exit(0)
    except ResizeScreenError as e:
        last_scene = e.scene


# yes "$(echo -e 's')" | python3 test.py |& tee output.txt
