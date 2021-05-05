import time

from core.foobartory import Foobartory


def main():
    simulation = Foobartory()
    try:
        simulation.start()
        while simulation.scheduler.running:
            time.sleep(1)
    except KeyboardInterrupt:
        simulation.stop()
if __name__ == '__main__':
    main()
