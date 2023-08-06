"""
Copyright 2010-2021 Mikkel Munch Mortensen <3xm@detfalskested.dk>.

This file is part of SMS Gateway.

SMS Gateway is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

SMS Gateway is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with SMS Gateway.  If not, see <http://www.gnu.org/licenses/>.
"""

import getopt
from urllib.parse import urlencode
from urllib.request import urlopen
from typing import Any, Tuple


class Gateway:
    """
    A Python wrapper around the SMS gateway from CPSMS <https://www.cpsms.dk/>.

    Please look at the README for further description.
    """

    options: dict[str, Any] = {}

    @property
    def default_options(self) -> dict[str, Any]:
        return {
            "recipients": [],
            "message": "",
            "callback_url": "",
            "timestamp": "",  # For delaying messages. Format: YYYYMMDDHHMM.
            "utf8": True,
            "flash": False,
            "group": False,
            "gateway_base_url": "https://www.cpsms.dk/sms/?",
        }

    def __init__(
        self,
        username: str,
        password: str,
        sender_name: str,
        options: dict[str, Any] = None,
    ) -> None:
        """Initialize SMS gateway, with some options."""
        self.options = self.default_options
        if options is not None:
            self.options.update(options)

        self.options["username"] = username
        self.options["password"] = password
        self.options["from"] = sender_name

    def add_recipient(self, number: str) -> None:
        """Add a number to the list of recipients."""
        self.options["recipients"].append(number)

    def send(self, message: str = None) -> Tuple[bool, str]:
        """
        Send the message specified in self.options to all recipients.

        Optionally, override the message to be sent.
        """
        # Decide what to send.
        if message is None:
            message = self.options["message"]

        # Raise error if message is empty.
        if message == "":
            raise ValueError("Message empty.")

        # Raise error if message is too long.
        if len(message) > 459:
            raise ValueError(
                "Message not allowed to be more than 459 characters."
                "Current message is %i characters." % len(message)
            )

        # Raise error if recipients is empty.
        if len(self.options["recipients"]) == 0:
            raise ValueError("No recipients.")

        # Construct gateway URL.
        options = [
            ("username", self.options["username"]),
            ("password", self.options["password"]),
            ("message", message),
            ("from", self.options["from"]),
            ("utf8", int(self.options["utf8"])),
            ("flash", int(self.options["flash"])),
            ("group", int(self.options["group"])),
            ("url", self.options["callback_url"]),
        ]

        for r in self.options["recipients"]:
            options.append(("recipient[]", r))

        if self.options["timestamp"] != "":
            options.append(("timestamp", self.options["timestamp"]))

        url = self.options["gateway_base_url"] + urlencode(options)
        print(url)

        # Send SMS.
        remote_call = urlopen(url)
        result = remote_call.read().decode()
        remote_call.close()
        if result.find("<succes>") > -1:
            return True, result
        else:
            return False, result
