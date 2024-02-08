# -*- coding: utf-8 -*-
"""
Created on Feb 07 20:02:35 2024

@author: Jerome Yutai Shen

"""
from enum import Enum, unique
from typing import Union, Optional, Tuple, List
from frozendict import frozendict


@unique
class State(Enum):
    authorized = True
    unauthorized = False


@unique
class Action(Enum):
    login = 1
    logout = 2
    deposit = 3
    withdraw = 4
    balance = 5


def login_checker(password: str, atm_password: str, atm_current_balance: int) -> Tuple[bool, int, Optional[None]]:
    if password == atm_password:
        return True, atm_current_balance, None
    else:
        return False, atm_current_balance, None


def logout_checker(action_param: Optional, atm_password: str, atm_current_balance: int) -> Tuple[bool, int, Optional[None]]:
    return True, atm_current_balance, None


def deposit_checker(amount: Optional[int], atm_password: str, atm_current_balance: int) -> Tuple[bool, int, Optional[None]]:
    if amount is not None:
        return True, atm_current_balance + amount, None
    else:
        return False, atm_current_balance, None


def withdraw_checker(amount: Optional[int], atm_password: str, atm_current_balance: int) -> Tuple[bool, int, Optional[None]]:
    if amount is not None:
        if atm_current_balance >= amount:
            return True, atm_current_balance - amount, None
    return False, atm_current_balance, None


def balance_checker(action_param: Optional, atm_password: str, atm_current_balance: int) -> Tuple[bool, int, int]:
    return True, atm_current_balance, atm_current_balance


transition_table = frozendict({
    State["unauthorized"]: (("login", login_checker, State["authorized"]),)
    ,
    State["authorized"]: (
        ("logout", logout_checker, State["unauthorized"]),
        ("deposit", deposit_checker, State["authorized"]),
        ("withdraw", withdraw_checker, State["authorized"]),
        ("balance", balance_checker, State["authorized"])
        )})


class ATM:
    """
    Both __init__ method and next method are modified, otherwise it doesn't work

    """

    def __init__(self,
                 init_state: State = State["unauthorized"],
                 init_balance: int = 0,
                 password: str = "",
                 transition_table: frozendict = transition_table):
        self.state = init_state
        self._balance = init_balance
        self._password = password
        self._transition_table = transition_table

    def __str__(self):
        return self.state.name

    def next(self, action: Action, param: Union[str, int, None]) -> Tuple[bool, Optional[None]]:

        if action.name in (Action(3).name, Action(4).name, Action(5).name) and self.state == State["unauthorized"]:
            return False, None
        try:
            for transition_action, check, next_state in self._transition_table[self.state]:
                if action.name == transition_action:
                    passed, new_balance, res = check(param, self._password, self._balance)
                    if passed:
                        self._balance = new_balance
                        self.state = next_state
                        return True, res
        except KeyError:
            pass
        return False, None


def main(transition_table: frozendict = transition_table) -> List:
    password = input().strip()
    init_balance = int(input().strip())
    num_actions = int(input().strip())

    # Initialize ATM
    atm = ATM(State["unauthorized"], init_balance, password, transition_table)
    response = []
    # Process actions
    for _ in range(num_actions):
        action_input = input().strip().split()
        action = Action[action_input[0]]

        if action in (Action(3), Action(4)):
            assert len(action_input) == 2 and action_input[1].isdigit()
            action_param = int(action_input[1])
        elif action == Action(1):
            assert len(action_input) == 2 and action_input[1].isalpha()
            action_param = action_input[1]
        else:
            action_param = None

        success, result = atm.next(action, action_param)
        if result is None:
            msg = f"Success={success} {atm.state.name}"
        else:
            msg = f"Success={success} {atm.state.name} {result}"
        print(msg)
        response.append(msg)
    print(response)
    return response


if __name__ == "__main__":
    response = main()


