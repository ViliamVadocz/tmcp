from enum import Enum
from typing import Optional

from tmcp import TMCP_VERSION
from .convert import try_convert_direction
from .type_check import type_check


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

    @type_check
    def __init__(self, team: int, index: int, action_type: ActionType):
        self.team = team
        self.index = index
        self.action_type = action_type

    @classmethod
    @type_check
    def ball_action(
        cls, team: int, index: int, time: float = -1.0, direction = [0.0, 0.0, 0.0]
    ):  # -> TMCPMessage:
        self = cls(team, index, ActionType.BALL)
        self.time = time
        self.direction = try_convert_direction(direction)
        return self

    @classmethod
    @type_check
    def boost_action(cls, team: int, index: int, target: int):  # -> TMCPMessage:
        self = cls(team, index, ActionType.BOOST)
        self.target = target
        return self

    @classmethod
    @type_check
    def demo_action(
        cls, team: int, index: int, target: int, time: float = -1.0
    ):  # -> TMCPMessage:
        self = cls(team, index, ActionType.DEMO)
        self.target = target
        self.time = time
        return self

    @classmethod
    @type_check
    def ready_action(cls, team: int, index: int, time: float = -1.0):  # -> TMCPMessage:
        self = cls(team, index, ActionType.READY)
        self.time = time
        return self

    @classmethod
    @type_check
    def defend_action(cls, team: int, index: int):  # -> TMCPMessage:
        self = cls(team, index, ActionType.DEFEND)
        return self

    @classmethod
    def from_dict(cls, message: dict) -> Optional["TMCPMessage"]:
        try:
            team: int = message["team"]
            index: int = message["index"]
            assert isinstance(team, int)
            assert isinstance(index, int)

            version = message["tmcp_version"]
            assert isinstance(version, (list, tuple))
            assert len(version) == 2
            
            action: dict = message["action"]
            action_type: ActionType = ActionType(action["type"].upper())

            if action_type == ActionType.BALL:
                action_time = action.get("time", -1)
                assert isinstance(action_time, (float, int))
                direction = action.get("direction", [0.0, 0.0, 0.0])
                assert isinstance(direction, (list, tuple))
                assert len(direction) in (2, 3)
                assert all(isinstance(elem, (int, float)) for elem in direction)
                msg = cls.ball_action(team, index, float(action_time), direction)
            elif action_type == ActionType.BOOST:
                assert isinstance(action["target"], int)
                msg = cls.boost_action(team, index, action["target"])
            elif action_type == ActionType.DEMO:
                assert isinstance(action["target"], int)
                action_time = action.get("time", -1)
                assert isinstance(action_time, (float, int))
                msg = cls.demo_action(
                    team, index, action["target"], float(action_time)
                )
            elif action_type == ActionType.READY:
                action_time = action.get("time", -1)
                assert isinstance(action_time, (float, int))
                msg = cls.ready_action(team, index, float(action_time))
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
                "direction": self.direction
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
