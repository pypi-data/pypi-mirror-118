"""Implementation of a finite state machine for studies"""
import logging
from study_state_machine.errors import (
    BehaviorNotAllowedException,
    StateNotFoundException,
)

logger = logging.getLogger(__name__)


class Context:
    """
    Only if an initial state is passed to the constructor, the context of the current state is set. Otherwise, call
    :func:`~study_state_machine.context.Context.transition_to` or
    :func:`~study_state_machine.context.Context.load_state` with a name of a State, respectively
    """

    def __init__(self, available_states, initial_state=None):
        """
        available_states need to be provided in a JSON format (list of objects)
        example of a state:
        {
            "name" : "RegisteredState",
            "strategies_create_study": [
                {
                    "name": "expression",
                    "value": "len(kwargs.get('datasets', [])) > 0",
                    "state_if_true": "DatasetState"
                }
            ],
            "strategies_change_state": [
                {
                    "name": "expression",
                    "value": "len(kwargs.get('datasets', [])) > 0",
                    "state_if_true": "DatasetState"
                }
            ]
        }
        """
        self._current_state = initial_state
        self._available_states_map = {
            state["name"]: state for state in available_states
        }

    def __repr__(self):
        return f"<{self.__class__.__name__}" f"(current state: {self._current_state})>"

    def transition_to(self, state_name):
        """Set state as the new current state and set its context

        :param state_name: new current state
        """
        self._current_state = state_name

    def load_state(self, state_name):
        """Load state with given name

        :param state_name: Name of the state
        :raise StateNotFoundException: If the state is not found
        """
        if state_name not in self._available_states_map.keys():
            error_msg = f"Fail to find state (name: {state_name})"
            logger.error(error_msg)
            raise StateNotFoundException(error_msg)

        self.transition_to(state_name)

    def get_state_dict(self, state_name):
        return self._available_states_map[state_name]

    @property
    def current_state(self):
        return self._current_state

    @current_state.setter
    def current_state(self, state_name):
        self.transition_to(state_name)

    @property
    def available_states(self):
        return self._available_states_map.keys(), self._available_states_map.values()

    def parse_strategies(self, strategies, *args, **kwargs):
        """ Parse strategies list and return a state to be transitioned to """
        for strategy in strategies:
            if strategy["name"] == "expression":
                expression_value = eval(strategy["value"])
                if expression_value:
                    if "state_if_true" in strategy:
                        return strategy["state_if_true"]

            elif strategy["name"] == "locked":
                message = f"Not allowed to change to another state in state {self._current_state}."
                message += f" This is a final state where modifications are not allowed anymore"
                raise BehaviorNotAllowedException(message)

        return None

    def create_study(self, *args, **kwargs):
        state_dict = self.get_state_dict(self._current_state)
        new_state = self.parse_strategies(
            state_dict["strategies_create_study"], *args, **kwargs
        )
        if new_state is not None:
            self.transition_to(new_state)

    def add_sample(self, *args, **kwargs):
        raise NotImplementedError(
            f"add_sample not implemented for state {self._current_state}"
        )

    def change_state(self, *args, **kwargs):
        state_dict = self.get_state_dict(self._current_state)
        new_state = self.parse_strategies(
            state_dict["strategies_change_state"], *args, **kwargs
        )
        if new_state is not None:
            self.transition_to(new_state)
