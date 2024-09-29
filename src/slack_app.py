from __future__ import annotations

import os
from concurrent.futures import Executor, ProcessPoolExecutor

from slack_bolt import App, SlackRequestHandler

from configuration import logger
from file_tasks import process_file_urls

BOT_TOKEN = ""

app = App()


@app.middleware
def log_request(logger, body, next):
    logger.debug(body)
    return next()


@app.command("/hello-bolt-python")
def hello_command(ack, body):
    user_id = body["user_id"]
    ack(f"Hi <@{user_id}>!")


@app.error
def global_error_handler(error, body, logger):
    logger.error(error)
    logger.info(body)


class Client:
    def __init__(self, token, channel, timestamp, say):
        self.token = token
        self.channel = channel
        self.timestamp = timestamp
        self.say = say

    def do(self, method, *args, **kwargs):
        if method == "say":
            to_run = self.say
        else:
            to_run = getattr(app._client, method)
        return to_run(
            *args,
            token=self.token,
            channel=self.channel,
            timestamp=self.timestamp,
            **kwargs,
        )


@app.event("app_mention")
def handle_mention_event(event, say, ack):
    """Triggered by StackRequestHandler.handle in start_slack_app
            the event that the triggering event is an app_message.
    Validates record in the attached file (if they exist) and sends them on to be processed"""
    msg = "Handling mention event..."
    logger.info(msg)
    ack(msg)
    client = Client(BOT_TOKEN, event["channel"], event["ts"])

    if "files" not in event.keys():
        logger.info("No files found, terminating analysis")
        message = """Please provide a csv file in the chat to have it processed"""
        client.say(message)
    else:
        logger.info("Files found attached to event, starting analysis.")

        client.do("reactions_add", name="eyes")
        client.do("say", "Processing file(s)...")
        # Attempt to analyze files in parallel
        # Send an error message if analysis fails
        try:
            logger.info(message)
            match_file = process_file_urls(event["files"], BOT_TOKEN, app.executor)
        except Exception as error:
            logger.error("Exception while attempting to process record (error)")
            if error == "UnicodeDecodeError":
                msg = """File Extension Error"""
            else:
                msg = f"""File Format Error: {error}"""
            blocks = [{"type": "section", "text": {"type": "mrkdwn", "text": f"{msg}"}}]
            client.do("say", blocks, text=f"{msg}")
            client.do("reactions_remove", name="eyes")
            client.do("reactions_add", name="exclamation")

        try:
            client.do(
                "files_upload",
                file=str(match_file) + ".csv",
                filename=str(match_file) + ".csv",
            )
            logger.info("Files uploaded to slack")
        except Exception as e:
            msg = f"Error uploading files: {match_file}"
            client.do("say", msg)
            logger.error(f"{msg}, error message: {e}")

        full_path = str(match_file) + ".csv"
        try:
            os.remove(full_path)
        except Exception as e:
            logger.info(f"Removal of file {full_path} failed: {e}")

        client.do("reactions_add", name="white_check_mark")
        client.do("reactions_remove", name="eyes")


def start_slack_app(event, context, executor: Executor | None = None):
    logger.info("Application started with executor %s", type(executor))
    app.executor = executor
    logger.info("Handling request...")
    slack_handler = SlackRequestHandler("app-app")
    return slack_handler.handle(event, context)


def main():
    logger.info("Creating process pool...")

    executor = ProcessPoolExecutor()
    start_slack_app(executor=executor)

    # If app fails or finished processing, stop pending tasks
    executor.shutdown(wait=False, cancel_futures=True)


if __name__ == "__main__":
    app.start(3000)
    main()
