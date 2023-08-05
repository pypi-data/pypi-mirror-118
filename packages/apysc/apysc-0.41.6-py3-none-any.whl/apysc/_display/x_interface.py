"""Class implementation for the x-coordinate interface.
"""

from typing import Dict

import apysc as ap
from apysc._type.revert_interface import RevertInterface
from apysc._type.variable_name_interface import VariableNameInterface


class XInterface(VariableNameInterface, RevertInterface):

    _x: ap.Int

    def _initialize_x_if_not_initialized(self) -> None:
        """
        Initialize the _x attribute if it hasn't been initialized yet.
        """
        if hasattr(self, '_x'):
            return
        self._x = ap.Int(0)

    @property
    def x(self) -> ap.Int:
        """
        Get a x-coordinate.

        Returns
        -------
        x : Int
            X-coordinate.

        References
        ----------
        - Display object x and y interfaces document
            - https://bit.ly/2ToA5ba
        """
        with ap.DebugInfo(
                callable_='x', locals_=locals(),
                module_name=__name__, class_=XInterface):
            from apysc._type import value_util
            self._initialize_x_if_not_initialized()
            return value_util.get_copy(value=self._x)

    @x.setter
    def x(self, value: ap.Int) -> None:
        """
        Update x-coordinate.

        Parameters
        ----------
        value : int or Int
            X-coordinate value.

        References
        ----------
        - Display object x and y interfaces document
            - https://bit.ly/2ToA5ba
        """
        with ap.DebugInfo(
                callable_='x', locals_=locals(),
                module_name=__name__, class_=XInterface):
            from apysc._type.number_value_interface import NumberValueInterface
            from apysc._validation import number_validation
            if not isinstance(value, NumberValueInterface):
                number_validation.validate_integer(integer=value)
                value = ap.Int(value=value)
            self._x = value
            self._x._append_incremental_calc_substitution_expression()
            self._append_x_update_expression()

    def _append_x_update_expression(self) -> None:
        """
        Append x position updating expression.
        """
        with ap.DebugInfo(
                callable_=self._append_x_update_expression, locals_=locals(),
                module_name=__name__, class_=XInterface):
            from apysc._type import value_util
            self._initialize_x_if_not_initialized()
            value_str: str = value_util.get_value_str_for_expression(
                value=self._x)
            expression: str = (
                f'{self.variable_name}.x({value_str});'
            )
            ap.append_js_expression(expression=expression)

    _x_snapshots: Dict[str, int]

    def _make_snapshot(self, snapshot_name: str) -> None:
        """
        Make a value's snapshot.

        Parameters
        ----------
        snapshot_name : str
            Target snapshot name.
        """
        if not hasattr(self, '_x_snapshots'):
            self._x_snapshots = {}
        if self._snapshot_exists(snapshot_name=snapshot_name):
            return
        self._initialize_x_if_not_initialized()
        self._x_snapshots[snapshot_name] = int(self._x._value)

    def _revert(self, snapshot_name: str) -> None:
        """
        Revert a value if snapshot exists.

        Parameters
        ----------
        snapshot_name : str
            Target snapshot name.
        """
        if not self._snapshot_exists(snapshot_name=snapshot_name):
            return
        self._x._value = self._x_snapshots[snapshot_name]
