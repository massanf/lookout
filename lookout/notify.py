import requests
import datetime
import time


def slack_notify(
    link,
    type,
    cmd,
    starttime,
    lastline,
    endtime=0,
    errmsg="",
    returncode=0,
    regex="",
    hangth=2
):
    blocks = []
    cmdline = " ".join(cmd)
    if lastline == "" or lastline == "\n":
        lastline = "No output yet"
    else:
        lastline = f"```{lastline}```"

    if errmsg == "" or errmsg == "\n":
        errmsg = "No error message"
    else:
        errmsg = f"```{errmsg}```"

    if type == "regex_notify":
        notificationline = "🔔 Regex match"
        blocks = [
            {
                "type": "divider"
            },
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": ":bell: Regex match"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"Detected regex match for `{regex}`."
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"```\n $ {cmdline}```",
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": "*Started on:*\n<!date^" + str(int(starttime))
                                + "^ {date_num} {time_secs}|Date and time not available>\n"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Duration:*\n {datetime.timedelta(seconds=int(time.time() - starttime))}\n"
                    }
                ]
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Last line:*\n {lastline}",
                }
            }
        ]

    if type == "successful":
        notificationline = "✅ Process successfully completed"
        blocks = [
            {
                "type": "divider"
            },
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": ":white_check_mark: Process successfully completed"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"```\n $ {cmdline}```",
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Return code:*\n `{returncode}`\n"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Duration:*\n {datetime.timedelta(seconds=int(endtime - starttime))}\n"
                    },
                    {
                        "type": "mrkdwn",
                        "text": "*Started on:*\n<!date^" + str(int(starttime))
                                + "^ {date_num} {time_secs}|Date and time not available>\n"
                    },
                    {
                        "type": "mrkdwn",
                        "text": "*Ended on:*\n<!date^" + str(int(endtime))
                                + "^ {date_num} {time_secs}|Date and time not available>\n"
                    }
                ]
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Last line:*\n {lastline}",
                }
            }
        ]

    if type == "timeout":
        notificationline = "⚠️ Process may be hanging"
        blocks = [
            {
                "type": "divider"
            },
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": ":warning: Process may be hanging"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"Process has not been outputting for {hangth} seconds.\nYou can change this threshold with `--hangthreshold` argument."
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"```\n $ {cmdline}```",
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": "*Started on:*\n<!date^" + str(int(starttime))
                                + "^ {date_num} {time_secs}|Date and time not available>\n"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Duration:*\n {datetime.timedelta(seconds=int(time.time() - starttime))}\n"
                    }
                ]
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Last line:*\n {lastline}",
                }
            }
        ]

    if type == "ended with error":
        notificationline = "❌ Process ended with error"
        blocks = [
            {
                "type": "divider"
            },
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": ":x: Process ended with error"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"```\n $ {cmdline}```",
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Return code:*\n `{returncode}`\n"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Duration:*\n {datetime.timedelta(seconds=int(endtime - starttime))}\n"
                    },
                    {
                        "type": "mrkdwn",
                        "text": "*Started on:*\n<!date^" + str(int(starttime))
                                + "^ {date_num} {time_secs}|Date and time not available>\n"
                    },
                    {
                        "type": "mrkdwn",
                        "text": "*Ended on:*\n<!date^" + str(int(endtime))
                                + "^ {date_num} {time_secs}|Date and time not available>\n"
                    }
                ]
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Last line:*\n {lastline}",
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Error:*\n {errmsg}",
                }
            }
        ]

    requests.post(link,
                  json={
                      "title": "Lookout notification",
                      "blocks": blocks,
                      "text": notificationline,
                  }
                  )
