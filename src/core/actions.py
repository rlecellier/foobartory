import random

from settings import BAR_NAME
from settings import CURRENCY_NAME
from settings import FOOBAR_NAME
from settings import FOO_NAME
from settings import ROBOT_NAME
from settings import TICK_DURATION_IN_SECONDS


MOVE_ACTION_NAME = 'move_action'
MINE_FOO_ACTION_NAME = 'mine_foo_action'
MINE_BAR_ACTION_NAME = 'mine_bar_action'
CREATE_FOOBAR_ACTION_NAME = 'create_foobar_action'
SELL_FOOBAR_ACTION_NAME = 'sell_foobar_action'
BUY_ROBOT_ACTION_NAME = 'buy_robot_action'

class Action():
    def __init__(self):
        self.initialize_nb_tick_left()

    def __str__(self):
        return self.__class__.__name__

    def initialize_nb_tick_left(self):
        self.nb_tick_left = int(self.duration_in_second / TICK_DURATION_IN_SECONDS)

    def resolve_tick(self):
        self.nb_tick_left -= 1
        return self.is_done()

    def is_done(self):
        return self.nb_tick_left <= 0

    def get_input(self):
        return {}

    def get_output(self):
        return {}


class Move(Action):
    name = MOVE_ACTION_NAME
    duration_in_second = 5


class MineFoo(Action):
    name = MINE_FOO_ACTION_NAME
    duration_in_second = 1.0
    output_foo = 1

    def get_output(self):
        return { 'products': { FOO_NAME: 1 } }


class MineBar(Action):
    name = MINE_BAR_ACTION_NAME
    min_duration_in_seconds = 0.5
    max_duration_in_seconds = 1.0
    output_bar = 1

    def initialize_nb_tick_left(self):
        self.duration_in_second = round(random.uniform(0.5, 2.0) * 2) / 2
        super().initialize_nb_tick_left()

    def get_output(self):
        return { 'products': { BAR_NAME: 1 } }

class BuyRobot(Action):
    name = BUY_ROBOT_ACTION_NAME
    duration_in_second = 0
    input_foo = 6
    input_currency = 3
    output_robot = 1

    def get_input(self):
        return {
            CURRENCY_NAME: self.input_currency,
            'products': {
                FOO_NAME: self.input_foo,
            }
        }

    def get_output(self):
        return {
            ROBOT_NAME: self.output_robot,
            'consumed_products': self.get_input()['products'],
        }

class SellFoobar(Action):
    name = SELL_FOOBAR_ACTION_NAME
    duration_in_second = 10
    output_min_foobar = 1
    output_max_foobar = 5
    output_currency_by_foobar = 1

    def get_input(self):
        return {
            'products': {
                FOOBAR_NAME: self.output_max_foobar,
            }
        }

    def get_output(self):
        output_foobar = random.randrange(self.output_min_foobar, self.output_max_foobar, 1)
        return {
            CURRENCY_NAME: output_foobar * self.output_currency_by_foobar,
            'consumed_products': {
                FOOBAR_NAME: output_foobar,
            }
        }


class CreateFoobar(Action):
    name = CREATE_FOOBAR_ACTION_NAME
    duration_in_second = 2
    success_rate = 0.6
    input_foo = 1
    input_bar = 1
    output_failure_foo = 1
    output_success_foobar = 1

    def get_input(self):
        return {
            'products': {
                FOO_NAME: self.input_foo,
                BAR_NAME: self.input_bar,
            }
        }

    def get_output(self):
        if random.random() <= self.success_rate:
            return { 'products': { FOOBAR_NAME: self.output_success_foobar } }
        return { 'consume_products': { FOO_NAME: self.output_failure_foo } }
