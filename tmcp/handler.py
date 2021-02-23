from time import perf_counter
from queue import Empty
from typing import List, Optional

from rlbot.agents.base_agent import BaseAgent
from rlbot.matchcomms.client import MatchcommsClient

from tmcp import TMCP_VERSION
from .message import TMCPMessage


MAX_PACKETS_PER_TICK: int = 50
TIME_BETWEEN_MESSAGES: float = 0.1


class TMCPHandler:
    """The class for handling TMCP.

    Create an instance by just passing your agent in:

    ```
    def initialize_agent(self):
        self.tmcp_handler = TMCPHandler(self)
    ```

    Usage is also very straightforward:

    ```
    def get_output(self, packet: GameTickPacket) -> SimpleControllerState:
        # Receive and parse all new matchcomms messages into TMCPMessage objects.
        new_messages: List[TMCPMessage] = self.tmcp_handler.recv()
        # Handle TMCPMessages.
        for message in new_messages:
            if message.action_type == ActionType.BALL:
                print(message.time)
        
        ...

        # You can send messages like this.
        self.tmcp_handler.send_boost_action(pad_index)

        # Or you can create them and send them more directly:
        my_message = TMCPMessage.ball_action(self.team, self.index, estimated_time_of_arrival)
        self.tmcp_handler.send(my_message)
    ```
    """

    def __init__(self, agent: BaseAgent):
        self.matchcomms: MatchcommsClient = agent.matchcomms
        self.index: int = agent.index
        self.team: int = agent.team
        self.last_time: float = 0.0 
        self.enabled: bool = True

    def disable(self):
        """Disable the handler. It will not send or receive any messages."""
        self.enabled = False

    def send(self, message: TMCPMessage) -> bool:
        """Send a TMCPMessage over match comms. Will not send messages if they are coming too quickly.
        Returns whether a message was sent."""

        # If disabled, pretend all messages are sent.
        # This is done so that people don't try to resend messages if the handler is disabled.
        if not self.enabled:
            return True

        current_time = perf_counter()
        if current_time - self.last_time < TIME_BETWEEN_MESSAGES:
            return False

        self.matchcomms.outgoing_broadcast.put_nowait(message.to_dict())
        self.last_time: float = current_time
        return True

    def recv(self) -> List[TMCPMessage]:
        messages = []

        # Return empty message list if disabled.
        if not self.enabled:
            return messages

        # Receive messages until we reach the maximum packets per tick or the queue is empty.
        for _ in range(MAX_PACKETS_PER_TICK):
            try:
                message = self.parse(self.matchcomms.incoming_broadcast.get_nowait())
                if message is not None:
                    messages.append(message)
            except Empty:
                break
        return messages

    def parse(self, message: dict) -> Optional[TMCPMessage]:
        # Ignore messages using a different version of the protocol.
        if message.get("tmcp_version") != TMCP_VERSION:
            return None
        # Ignore messages by opposing team.
        if message.get("team") != self.team:
            return None

        return TMCPMessage.from_dict(message)

    def send_ball_action(self, time: Optional[float] = None) -> bool:
        """The bot is going for the ball.

        `time` - Game time that your bot will arrive at the ball.
        """
        if time is None:
            msg = TMCPMessage.ball_action(self.team, self.index)
        else:
            msg = TMCPMessage.ball_action(self.team, self.index, time)
        return self.send(msg)

    def send_boost_action(self, target: int) -> bool:
        """The bot is going for boost.

        `target` - Index of the boost pad the bot is going to collect.
        """
        return self.send(TMCPMessage.boost_action(self.team, self.index, target))

    def send_demo_action(self, target: int, time: Optional[float] = None) -> bool:
        """The bot is going to demolish another car.

        `target` - Index of the bot that will be demoed.
        `time` - Game time that the bot will demo the other bot.
        """
        if time is None:
            msg = TMCPMessage.demo_action(self.team, self.index, target)
        else:
            msg = TMCPMessage.demo_action(self.team, self.index, target, time)
        return self.send(msg)

    def send_wait_action(self, ready: float) -> bool:
        """The bot is waiting for a chance to go for the ball.
        Some examples are positioning (retreating/shadowing) and recovering.

        `ready` - A value of -1 signifies that the bot is NOT ready to go for the ball.
        Otherwise, the ready value indicates the projected intercept time in game time
        if the bot was to go for the ball.
        """
        return self.send(TMCPMessage.wait_action(self.team, self.index, ready))

    def send_defend_action(self) -> bool:
        """The bot is in a position to defend the goal and is not planning to move up.
        If the bot decides to leave net, signal this using either "BALL" (if going for a touch) or "WAIT" (if moving upfield).

        A bot should use "DEFEND" to let its teammates know it is safe to move up a bit without worrying about an open net.
        """
        return self.send(TMCPMessage.defend_action(self.team, self.index))
