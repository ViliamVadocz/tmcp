from enum import Enum
from typing import Optional

from .handler import TMCP_VERSION


class ActionType(Enum):
    BALL = "BALL"
    BOOST = "BOOST"
    DEMO = "DEMO"
    WAIT = "WAIT"


class TMCPMessage:
    """
    A TMCP compliant message object.
    All messages contain a `team`, `index`, and `action_type`.
    
    Based on the `action_type`, this object will have other attributes.
    For example, if the `action_type` equals `ActionType.BALL`,
    this object will have a `time` attribute.
    """

    def __init__(self, team: int, index: int, action_type: ActionType):
        self.team = team
        self.index = index
        self.action_type = action_type

    @classmethod
    def ball_action(cls, team: int, index: int, time: float = -1.0) -> "TMCPMessage":
        self = cls(team, index, ActionType.BALL)
        self.time = time
        return self

    @classmethod
    def boost_action(cls, team: int, index: int, target: int) -> "TMCPMessage":
        self = cls(team, index, ActionType.BOOST)
        self.target = target
        return self

    @classmethod
    def demo_action(
        cls, team: int, index: int, target: int, time: float = -1.0
    ) -> "TMCPMessage":
        self = cls(team, index, ActionType.DEMO)
        self.target = target
        self.time = time
        return self

    @classmethod
    def wait_action(cls, team: int, index: int) -> "TMCPMessage":
        self = cls(team, index, ActionType.WAIT)
        return self

    @classmethod
    def from_dict(cls, message: dict) -> Optional["TMCPMessage"]:
        try:
            team: int = message["team"]
            index: int = message["index"]

            action: dict = message["action"]
            action_type: ActionType = ActionType(action["type"])

            if action_type == ActionType.BALL:
                msg = cls.ball_action(team, index, action["time"])
            elif action_type == ActionType.BOOST:
                msg = cls.boost_action(team, index, action["target"])
            elif action_type == ActionType.DEMO:
                msg = cls.demo_action(team, index, action["target"], action["time"])
            elif action_type == ActionType.WAIT:
                msg = cls.wait_action(team, index)
            else:
                raise NotImplementedError
            return msg

        except (KeyError, ValueError):
            return None

    def to_dict(self) -> dict:
        if self.action_type == ActionType.BALL:
            action = {
                "type": "BALL",
                "time": self.time,
            }
        elif self.action_type == ActionType.BOOST:
            action = {
                "type": "BOOST",
                "target": self.target,
            }
        elif self.action_type == ActionType.DEMO:
            action = {
                "type": "DEMO",
                "target": self.target,
                "time": self.time,
            }
        elif self.action_type == ActionType.WAIT:
            action = {"type": "WAIT"}
        else:
            raise NotImplementedError

        return {
            "tmcp_version": TMCP_VERSION,
            "team": self.team,
            "index": self.index,
            "action": action,
        }

    def __repr__(self):
        return str(self.to_dict())
