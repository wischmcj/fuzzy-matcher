from log_utils import logger

from concurrent.futures import ProcessPoolExecutor
from slack_app import start_slack_app


def main():
    logger.info("Creating process pool...")
    executor = ProcessPoolExecutor()
    logger.info("Starting Slack app...")

    start_slack_app(executor=executor)
    logger.info("started slack app")

    # If app fails or finished processing, stop pending tasks
    executor.shutdown(wait=False, cancel_futures=True)


if __name__ == "__main__":
    main()
