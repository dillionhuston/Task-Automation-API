import requests

from app.utils.logger import SingletonLogger


logger = SingletonLogger().get_logger()

def send_discord_notification(
        status = str,
        message = str,
        task_name = str,
        webhook_url = str
):
    try:
        content = f"**Task**{task_name}\n"f"**Status**{status}\n"f"**Info**{message}"
        payload = {"content": content}

        response = requests.post(webhook_url, json=payload)
        if response.status_code == 204: # retrun 204 on success
            return content
        else:
            logger.log(f"Discord message failed to send {response.text}. app.utils.discord ")
    except Exception as e:
        logger.log(f"Error sending Discord message{e}")