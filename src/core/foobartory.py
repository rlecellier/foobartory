
import logging

from apscheduler.schedulers.background import BackgroundScheduler

from core.actions import BuyRobot
from core.actions import CreateFoobar
from core.actions import MineBar
from core.actions import MineFoo
from core.actions import SellFoobar
from core.products import Bar
from core.products import Foo
from core.products import FooBar
from core.warehouse import IdleRobotException
from core.warehouse import Robot
from core.warehouse import Warehouse
from settings import BAR_NAME
from settings import CURRENCY_NAME
from settings import FOOBAR_NAME
from settings import FOOBAR_STOCK_LIMIT
from settings import FOO_NAME
from settings import NB_INITIAL_ROBOTS
from settings import NB_WINING_ROBOTS
from settings import ROBOT_NAME
from settings import TICK_DURATION_IN_SECONDS


logger = logging.getLogger('foobartory')

class Foobartory():
    def __init__(self):
        self.warehouse = Warehouse()
        self.robots = [Robot(i) for i in range(NB_INITIAL_ROBOTS)]
        self.scheduler = BackgroundScheduler()
        self.tick_id = 0

    @property
    def nb_robots(self):
        return len(self.robots)

    def start(self):
        logger.info("Starting simulation")
        self.scheduler.start()
        self.job = self.scheduler.add_job(self.next_tick, 'interval', seconds=TICK_DURATION_IN_SECONDS)

    def check_end_game(self):
        if self.nb_robots >= NB_WINING_ROBOTS:
            print('##')
            print('### Wining condition reached ###')
            print('##')
            self.stop()

    def stop(self):
        logger.info("Ending simulation")
        self.job.remove()
        self.scheduler.shutdown(wait=False)

        print(f'## TOTAL ROBOTS : {self.nb_robots} ##')

        print('Final stocks:')
        print(self._get_log_stocks_row())
        print('History of all stored products')
        print(self._get_log_history_stocks_row())

    def next_tick(self):
        self.tick_id += 1

        print('')
        logger.info('Simulation tick %s starting.', self.tick_id)
        logger.info('Working robots %s.', self.nb_robots)
        print(self._get_log_stocks_row())

        try:
            for robot in self.robots:
                try:
                    action_output = robot.do_work()
                    self.handle_action_output(robot, action_output)
                    self.check_end_game()
                except IdleRobotException:
                    action_input = robot.plan_work(self.get_next_action())
                    self.handle_action_input(robot, action_input)
        except Exception as e:
            self.stop()
            raise e

    def handle_action_input(self, robot, action_input):
        """
        action_input = {
            CURRENCY_NAME: 0,
            'products': {
                NAME_FOO: 0,
                NAME_BAR: 0,
                NAME_FOOBAR: 0,
            }
        }
        """
        if CURRENCY_NAME in action_input:
            self.warehouse.consume_currency(action_input[CURRENCY_NAME])

        if 'products' in action_input:
            for product_name, quantity in action_input['products'].items():
                robot_stock = robot.get_product_stock_amount(product_name)
                if robot_stock < quantity:
                    products = self.warehouse.get_products(product_name, quantity - robot_stock)
                    robot.add_products(product_name, products)


    def handle_action_output(self, robot, action_output):
        """
        action_output = {
            CURRENCY_NAME: 0,
            ROBOT_NAME: 0,
            'products': {
                NAME_FOO: 0,
                NAME_BAR: 0,
                NAME_FOOBAR: 0,
            }
            'consumed_products': {
                NAME_FOO: 0,
                NAME_BAR: 0,
                NAME_FOOBAR: 0,
            }
        }
        """
        if CURRENCY_NAME in action_output:
            self.warehouse.currency += action_output[CURRENCY_NAME]

        if ROBOT_NAME in action_output:
            for _i in range(action_output[ROBOT_NAME]):
                self.robots.append(Robot(self.nb_robots + 1))

        if 'products' in action_output:
            for product_name, quantity in action_output['products'].items():
                products = self._build_products(robot, product_name, quantity)
                self.warehouse.add_products(product_name, products)

        if 'consumed_products' in action_output:
            for product_name, quantity in action_output['consumed_products'].items():
                robot.get_products(product_name, quantity)


    def get_next_action(self):
        next_action = None
        if all([
            self.warehouse.get_product_stock_amount(FOO_NAME) >= BuyRobot.input_foo,
            self.warehouse.currency >= BuyRobot.input_currency,
        ]):
            next_action = BuyRobot()
        elif self.warehouse.get_product_stock_amount(FOOBAR_NAME) >= SellFoobar.output_max_foobar:
            next_action = SellFoobar()
        elif all([
            self.warehouse.get_product_stock_amount(FOOBAR_NAME) <= FOOBAR_STOCK_LIMIT,
            self.warehouse.get_product_stock_amount(FOO_NAME) >= (BuyRobot.input_foo + CreateFoobar.input_foo),
            self.warehouse.get_product_stock_amount(BAR_NAME) >= CreateFoobar.input_bar,
        ]):
            next_action = CreateFoobar()
        elif self.warehouse.get_product_stock_amount(FOO_NAME) > self.warehouse.get_product_stock_amount(BAR_NAME):
            next_action = MineBar()
        else:
            next_action = MineFoo()
        return next_action

    def _build_products(self, robot, product_name, quantity):
        return [self._build_product(robot, product_name) for i in range(quantity)]

    def _build_product(self, robot, product_name):
        product = None
        if product_name == FOO_NAME:
            product = Foo()
        elif product_name == BAR_NAME:
            product = Bar()
        elif product_name == FOOBAR_NAME:
            product_foo = robot.get_product(FOO_NAME)
            product_bar = robot.get_product(BAR_NAME)
            product = FooBar(product_foo, product_bar)
        return product

    def _get_log_stocks_row(self):
        log_stock_parts = [
            f'tick id : {self.tick_id: 3}',
            f'robots : {self.nb_robots: 3}',
        ]
        for name, stocks in self.warehouse.product_stocks.items():
            stock_row = f'#{name}: {len(stocks):02}'
            log_stock_parts.append(stock_row)

        return log_stock_parts

    def _get_log_history_stocks_row(self):
        log_stock_parts = [
            f'tick id : {self.tick_id: 3}',
        ]
        for name, stocks in self.warehouse.product_stocks_history.items():
            stock_row = f'#TOTAL_{name}: {len(stocks):02}'
            log_stock_parts.append(stock_row)

        return log_stock_parts
