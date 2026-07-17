print("\n" + "=" * 50)
print("                 SENTINELOPS")
print("     Linux Infrastructure Monitoring Platform")
print("=" * 50)
print()
print("Initializing monitoring engine...")
print("Loading configuration...")
print("Loading monitored services...")
print("System ready.")
print()
print("Type /help to view available commands.")
print()

from brain import Brain

from commands import *

brain = Brain()

commands = {

    "/help": help_command,

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

    "/savereport": save_report_command,

    "/audit": audit_command,

    "/reliability": reliability_command,

    "/recoveryrate": recoveryrate_command,

    "/clear-audit" : clear_audit_command,

    "/notifications": notifications_command
}

while True:

    sentence = input(">>>").strip()
    
    if sentence == "/exit":

        stopped = brain.stop_monitor()

        if stopped:
            print("\nStopping monitoring engine...")

        print("SentinelOps shutdown complete.")

        break

    parts = sentence.split()

    if len(parts) == 0:

        continue

    command = parts[0].lower()

    if command in commands:

        commands[command](parts , brain)

    else:

        print("Unknown command")


