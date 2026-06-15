print("STARTING")

from brain import Brain

from commands import *

from nlp import process_natural_language

brain = Brain()

commands = {

    "/help": help_command,
    "/learn": learn_command,
    "/ask": ask_command,
    "/search": search_command,
    "/delete": delete_command,
    "/show": show_command,
    "/history": history_command,
    "/category": category_command,
    "/stats": stats_command,
    "/update": update_command,
    "/backup": backup_command,
    "/system": system_command,
    "/live": live_monitor,
    "/service": service_command,
    "/services": services_command,
    "/kill": kill_command,
    "/monitor": monitor_command,
    "/telemetry": telemetry_command,
    "/average": average_command,
    "/peak": peak_command,
    "/stability": stability_command,
    "/alerts" : alerts_command,
    "/incidentstats" : incident_stats_command,
    "/resolvedstats" : resolved_stats_command,
    "/recover": recover_command,
    "/dashboard": dashboard_command,
    "/report": report_command,
    "/savereport": save_report_command


}

print("Smart Brain Assistant Started")

while True:

    sentence = input(">>>").strip()
    
    if sentence == "/exit":

        brain.stop_monitor()

        print("Shutting down...")

        break

    if not sentence.startswith("/"):

       sentence = process_natural_language(sentence)

       print("AFTER NLP:", sentence)

       if not sentence:

           continue


    parts = sentence.split()

    if len(parts) == 0:

        continue

    command = parts[0].lower()

    if command in commands:

        commands[command](parts , brain)

    else:

        print("Unknown command")


