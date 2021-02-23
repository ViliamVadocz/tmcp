# tmcp
## Helper classes for the Team Match Communication Protocol

Learn more about [TMCP](https://github.com/RLBot/RLBot/wiki/Team-Match-Communication-Protocol).

---

## How to use

Start by creating an instance of the TMCPHandler.
You should pass in your agent.

```py
from tmcp import TMCPHandler

class MyBot(BaseAgent):
    def initialize_agent(self):
        self.tmcp_handler = TMCPHandler(self)
```

Usage is also very straightforward:

```py
from tmcp import TMCPMessage, ActionType

...
    def get_output(self, packet: GameTickPacket) -> SimpleControllerState:
        # Receive and parse all new matchcomms messages into TMCPMessage objects
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

The handler will throttle your messages if you send them too quickly.
If you want to make sure all of your messages are sent, you can create a backlog like this:

```py
# During initialization, create a backlog list.
self.backlog = []

...
# Sending returns false if a message was not sent.
if not self.tmcp_handler.send(message):
    self.backlog.append(message)

...
# In your main loop, check whether you have any messages in the backlog.
if self.backlog:
    backlog_message = self.backlog.pop(0)
    # Try sending the message again. If it doesn't work, return it to the backlog.
    if not self.tmcp_handler.send(backlog_message):
        self.backlog.insert(0, backlog_message)
```
