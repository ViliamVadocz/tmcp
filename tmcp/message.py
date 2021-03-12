from enum import Enum
from typing import Optional

from tmcp import TMCP_VERSION


class ActionType(Enum):
    BALL = "BALL"
    BOOST = "BOOST"
    DEMO = "DEMO"
    READY = "READY"
    DEFEND = "DEFEND"


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
    def ready_action(cls, team: int, index: int, time: float = -1.0) -> "TMCPMessage":
        self = cls(team, index, ActionType.READY)
        self.time = time
        return self

    @classmethod
    def defend_action(cls, team: int, index: int) -> "TMCPMessage":
        self = cls(team, index, ActionType.DEFEND)
        return self

    @classmethod
    def from_dict(cls, message: dict) -> Optional["TMCPMessage"]:
        try:
            team: int = message["team"]
            index: int = message["index"]
            assert isinstance(team, int)
            assert isinstance(index, int)

            action: dict = message["action"]
            action_type: ActionType = ActionType(action["type"])

            if action_type == ActionType.BALL:
                assert isinstance(action["time"], (float, int))
                msg = cls.ball_action(team, index, float(action["time"]))
            elif action_type == ActionType.BOOST:
                assert isinstance(action["target"], int)
                msg = cls.boost_action(team, index, action["target"])
            elif action_type == ActionType.DEMO:
                assert isinstance(action["target"], int)
                assert isinstance(action["time"], (float, int))
                msg = cls.demo_action(team, index, action["target"], float(action["time"]))
            elif action_type == ActionType.READY:
                assert isinstance(action["time"], (float, int))
                msg = cls.ready_action(team, index, float(action["time"]))
            elif action_type == ActionType.DEFEND:
                msg = cls.defend_action(team, index)
            else:
                raise NotImplementedError
            return msg

        except (KeyError, ValueError, AssertionError):
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
        elif self.action_type == ActionType.READY:
            action = {
                "type": "READY",
                "time": self.time,
            }
        elif self.action_type == ActionType.DEFEND:
            action = {
                "type": "DEFEND"
            }
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
