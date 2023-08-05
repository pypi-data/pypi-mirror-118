# pytype: skip-file
from typing import Optional

from slack_sdk import WebClient

from slack_bolt.context.ack import Ack
from slack_bolt.context.base_context import BaseContext
from slack_bolt.context.respond import Respond
from slack_bolt.context.say import Say


class BoltContext(BaseContext):
    """Context object associated with a request from Slack."""

    @property
    def client(self) -> Optional[WebClient]:
        """The `WebClient` instance available for this request.

            @app.event("app_mention")
            def handle_events(context):
                context.client.chat_postMessage(
                    channel=context.channel_id,
                    text="Thanks!",
                )

            # You can access "client" this way too.
            @app.event("app_mention")
            def handle_events(client, context):
                client.chat_postMessage(
                    channel=context.channel_id,
                    text="Thanks!",
                )

        Returns:
            `WebClient` instance
        """
        if "client" not in self:
            self["client"] = WebClient(token=None)
        return self["client"]

    @property
    def ack(self) -> Ack:
        """`ack()` function for this request.

            @app.action("button")
            def handle_button_clicks(context):
                context.ack()

            # You can access "ack" this way too.
            @app.action("button")
            def handle_button_clicks(ack):
                ack()

        Returns:
            Callable `ack()` function
        """
        if "ack" not in self:
            self["ack"] = Ack()
        return self["ack"]

    @property
    def say(self) -> Say:
        """`say()` function for this request.

            @app.action("button")
            def handle_button_clicks(context):
                context.ack()
                context.say("Hi!")

            # You can access "ack" this way too.
            @app.action("button")
            def handle_button_clicks(ack, say):
                ack()
                say("Hi!")

        Returns:
            Callable `say()` function
        """
        if "say" not in self:
            self["say"] = Say(client=self.client, channel=self.channel_id)
        return self["say"]

    @property
    def respond(self) -> Optional[Respond]:
        """`respond()` function for this request.

            @app.action("button")
            def handle_button_clicks(context):
                context.ack()
                context.respond("Hi!")

            # You can access "ack" this way too.
            @app.action("button")
            def handle_button_clicks(ack, respond):
                ack()
                respond("Hi!")

        Returns:
            Callable `respond()` function
        """
        if "respond" not in self:
            self["respond"] = Respond(response_url=self.response_url)
        return self["respond"]
