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
    logger.exception(error)
    logger.info(body)


@app.event("app_mention")
def handle_mention_event(event, say, ack):
    """Triggered by StackRequestHandler.handle in start_slack_app
            the event that the triggering event is an app_message.
    Validates record in the attached file (if they exist) and sends them on to be processed"""

    logger.info("Handling mention event...")
    text = event.get("text")
    if text is None or len(text) == 0:
        ack(":x: Usage: /start-process (description here)")
    else:
        ack("Csv file found, beginning processing")

    thread_ts = event["ts"]
    channel = event["channel"]
    if "files" not in event.keys():
        logger.info("No files found, terminating analysis")
        message = """Please provide a csv file in the chat to have it processed"""
        say(message, thread_ts=thread_ts)
    else:
        logger.info("Files found attached to event, starting analysis.")
        app.client.reactions_add(
            token=BOT_TOKEN, channel=channel, name="eyes", timestamp=thread_ts
        )
        message = "Processing file(s)..."
        say(message, thread_ts=thread_ts)
        # Attempt to analyze files in parallel
        # Send an error message if analysis fails
        try:
            logger.info("Starting to process record...")
            match_file = process_file_urls(event["files"], BOT_TOKEN, app.executor)
        except Exception as error:
            logger.error("Exception while attempting to process record (error)")
            if error == "UnicodeDecodeError":
                msg = """File Extension Error"""
            else:
                msg = f"""File Format Error: {error}"""
        blocks = [{"type": "section", "text": {"type": "mrkdwn", "text": f"{msg}"}}]
        say(blocks, text=f"{msg} file spec here", thread_ts=thread_ts)
        app._client.reactions_add(
            token=BOT_TOKEN, channel=channel, name="exclamation", timestamp=thread_ts
        )

        app._client.reactions_remove(
            token=BOT_TOKEN, channel=channel, name="eyes", timestamp=thread_ts
        )
        try:
            app._client.files_upload(
                token=BOT_TOKEN,
                file=str(match_file) + ".csv",
                filename=str(match_file) + ".csv",
                channels=channel,
                thread_ts=thread_ts,
            )
            logger.info("Files uploaded to slack")
        except Exception as e:
            say(text="Error uploading files: (filepath)", thread_ts=thread_ts)
            logger.error(f"Could not upload file {match_file}, error message: {e}")

        full_path = str(match_file) + ".csv"
        try:
            os.remove(full_path)
        except Exception as e:
            logger.info(f"Removal of file (filepath) failed: {e}")

        app._client.reactions_add(
            token=BOT_TOKEN,
            channel=channel,
            name="white_check_mark",
            timestamp=thread_ts,
        )
        app._client.reactions_remove(
            token=BOT_TOKEN, channel=channel, name="eyes", timestamp=thread_ts
        )


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
