import logging

from core.actions import MOVE_ACTION_NAME
from core.actions import Move
from settings import BAR_NAME
from settings import FOOBAR_NAME
from settings import FOO_NAME


logger = logging.getLogger('foobartory')


class DuplicatedProductException(Exception):
    pass


class NotEnoughProductException(Exception):
    pass


class NotEnoughCurrencyException(Exception):
    pass


class IdleRobotException(Exception):
    pass


class HasProductsStocksMixin():
    def __init__(self):
        self.product_stocks_history = {
            FOO_NAME: set(),
            BAR_NAME: set(),
            FOOBAR_NAME: set(),
        }

        self.product_stocks = {
            FOO_NAME: [],
            BAR_NAME: [],
            FOOBAR_NAME: [],
        }

    def get_product_stock_amount(self, product_name):
        return len(self.product_stocks[product_name])

    def get_total_disctinct_product_stored(self, product_name):
        return len(self.product_stocks_history[product_name])

    def get_products(self, product_name, quantity):
        return [self.get_product(product_name) for i in range(quantity)]

    def get_product(self, product_name):
        stock_left = self.get_product_stock_amount(product_name)
        if stock_left > 0:
            return self.product_stocks[product_name].pop()
        raise NotEnoughProductException(f'No stock left for {product_name}')

    def add_products(self, product_name, products):
        for product in products:
            self.add_product(product_name, product)

    def add_product(self, product_name, product):
        for stored_product in self.product_stocks[product_name]:
            if stored_product.id == product.id:
                raise DuplicatedProductException()

        self.product_stocks[product_name].append(product)
        self.product_stocks_history[product_name].add(product.id)


class Warehouse(HasProductsStocksMixin):
    def __init__(self):
        self.currency = 0
        super().__init__()

    def consume_currency(self, quantity):
        new_currency = self.currency - quantity
        if new_currency < 0:
            raise NotEnoughCurrencyException()

        self.currency = new_currency


class Robot(HasProductsStocksMixin):
    def __init__(self, robot_id):
        self.id = robot_id
        self.actions_queue = []
        logger.info('New robot #%s has been bought.', self.id)
        super().__init__()

    def plan_work(self, action):
        logger.info('Robot plan to do: %s.', action.name)
        self.actions_queue.append(Move())
        self.actions_queue.append(action)
        return action.get_input()

    def do_work(self):
        if len(self.actions_queue) == 0:
            raise IdleRobotException()

        current_action = self.actions_queue[0]
        current_action.resolve_tick()

        action_output = self._resolve_action(current_action)
        if current_action.name == MOVE_ACTION_NAME and current_action.is_done():
            return self._resolve_action(self.actions_queue[0])
        return action_output

    def _resolve_action(self, action):
        logger.info('Robot #%s working on: %s. %s ticks left', self.id, action.name, action.nb_tick_left)

        if action.is_done():
            logger.info('Robot #%s finish: %s.', self.id, action.name)
            self.actions_queue.pop(0)
            return action.get_output()
        return {}
