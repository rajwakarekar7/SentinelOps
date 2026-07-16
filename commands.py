from utils import has_enough_parts, get_word
import os
import time
from logger import log
import threading

def help_command(parts, brain):

    line = "=" * 50
    section = "-" * 50

    print("\n" + line)
    print("                 SENTINELOPS HELP")
    print(line)

    print("\nSYSTEM MONITORING")
    print(section)
    print(f"{'/dashboard':<22}View system dashboard")
    print(f"{'/system':<22}View system resource information")
    print(f"{'/live':<22}Start live monitoring")
    print(f"{'/telemetry':<22}View telemetry history")

    print("\nSERVICE MANAGEMENT")
    print(section)
    print(f"{'/services':<22}List monitored services")
    print(f"{'/service <name>':<22}View service status")
    print(f"{'/monitor':<22}Start background monitoring engine")
    print(f"{'/recover <name>':<22}Restart a monitored service")
    print(f"{'/kill <process>':<22}Safely terminate a process")

    print("\nRESOURCE ANALYSIS")
    print(section)
    print(f"{'/average <metric>':<22}Average resource usage")
    print(F"{'/peak <metric>':<22}Peak resource usage")
    print(f"{'/stability <metric>':<22}Resource stability analysis")

    print("\nINCIDENT MANAGEMENT")
    print(section)
    print(f"{'/alerts':<22}View active alerts")
    print(f"{'/incidentstats':<22}View incident statistics")
    print(f"{'/resolvedstats':<22}View resolved incidents")
    print(f"{'/audit':<22}View audit trail")
    print(f"{'/notifications':<22}View notification history")

    print("\nREPORTING")
    print(section)
    print(f"{'/report':<22}Generate operational report")
    print(f"{'/savereport':<22}Export report")

    print("\nRELIABILITY")
    print(section)
    print(f"{'/reliability':<22}View service reliability report")
    print(f"{'/recoveryrate':<22}View recovery success rate")
    print(f"{'/clear-audit':<22}Clear audit history")

    print("\nSYSTEM")
    print(section)
    print(f"{'/help':<22}Show help")
    print(f"{'/exit':<22}Shut down SentinelOps")

    print("\n" + line)


#SYSTEM_RESOURCE_USAGE

def system_command(parts, brain):

    system_info = brain.get_system_info()

    top_cpu = brain.get_top_cpu_processes()

    top_memory = brain.get_top_memory_processes()

    line = "=" * 50
    section = "-" * 50

    print("\n" + line)
    print("              SYSTEM INFORMATION")
    print(line)

    print("\nSYSTEM OVERVIEW")
    print(section)

    print(f"CPU Usage           : {system_info['cpu']}%")
    print(f"CPU Cores           : {system_info['cpu_cores']}")
    print(f"Running Processes   : {system_info['process_count']}")
    print(f"Memory Usage        : {system_info['memory_percent']}%")
    print(f"Total RAM           : {system_info['total_ram']} GB")
    print(f"Available RAM       : {system_info['available_ram']} GB")
    print(f"Disk Usage          : {system_info['disk_percent']}%")
    print(f"System Uptime       : {system_info['uptime']}")

    if top_cpu["warning"]:

        print("\nCPU WARNING")
        print(section)
        print(top_cpu["warning"])

    print("\nTOP CPU PROCESSES")
    print(section)
    print(f"{'Process':<35}{'CPU %':>8}")
    print(section)

    for process in top_cpu["processes"]:

        print(f"{process[0]:<35}{process[1]:>8}%")

    if top_memory["warning"]:

        print("\nMEMORY WARNING")
        print(section)
        print(top_memory["warning"])

    print("\nTOP MEMORY PROCESSES")
    print(section)
    print(f"{'Process':<35}{'Memory %':>10}")
    print(section)

    for process in top_memory["processes"]:

        print(f"{process[0]:<35}{process[1]:>10}%")

    print("\n" + line)

#LIVE MONITORING TOOL

def live_monitor(parts, brain):

    line = "=" * 60
    section = "-" * 60

    try:

        while True:

            os.system("cls" if os.name == "nt" else "clear")

            dashboard = brain.get_dashboard_data()

            system_info = brain.get_system_info()

            top_cpu = brain.get_top_cpu_processes()

            top_memory = brain.get_top_memory_processes()

            print(line)
            print(f"LIVE MONITOR{'':>20}Updated: {time.strftime('%H:%M:%S')}")
            print(line)

            print("\nHEALTH")
            print(section)

            print(f"Health Score        : {dashboard['health_score']}/100")
            print(f"System Health       : {dashboard['health']}")
            print(f"Health Trend        : {dashboard['trend']}")
            print(f"Predictive Status   : {dashboard['predictive']}")
            print(f"Active Alerts       : {dashboard['active_alerts']}")

            print("\nRESOURCES")
            print(section)

            print(f"CPU Usage           : {system_info['cpu']}%")
            print(f"Memory Usage        : {system_info['memory_percent']}%")
            print(f"Disk Usage          : {system_info['disk_percent']}%")
            
            if top_cpu["warning"]:

                print("\nCPU WARNING")
                print(section)
                print(top_cpu["warning"])

            print("\nTOP CPU PROCESSES")
            print(section)
            print(f"{'Process':<40}{'CPU %':>8}")
            print(section)

            for process in top_cpu["processes"]:

                print(f"{process[0]:<40}{process[1]:>8}%")

            if top_memory["warning"]:

                print("\nMEMORY WARNING")
                print(section)
                print(top_memory["warning"])

            print("\nTOP MEMORY PROCESSES")
            print(section)
            print(f"{'Process':<40}{'Memory %':>10}")
            print(section)

            for process in top_memory["processes"]:

                print(f"{process[0]:<40}{process[1]:>10}%")

            print(section)
            print("Monitoring | Refresh: 5s | Ctrl+C to Stop")
            print(line)

            time.sleep(5)

    except KeyboardInterrupt:

        print("\n")
        print("Live monitoring stopped.")


#PROCESSES MONITORING SYSTEM

def service_command(parts, brain):

    if not has_enough_parts(parts, 2):

        print("Usage: /service <service_name>")
        return

    service_name = get_word(parts)

    result = brain.get_service_status(service_name)

    line = "=" * 50
    section = "-" * 50

    print("\n" + line)
    print("                SERVICE STATUS")
    print(line)

    print(f"\nService            : {result['service']}")
    print(f"Status             : {result['status']}")
    print(f"Health             : {result['health']}")

    print("\nPROCESS INFORMATION")
    print(section)

    if result["status"] == "ACTIVE":

        print(f"PID                : {result['pid']}")
        print(f"CPU Usage          : {result['cpu']}%")
        print(f"Memory Usage       : {result['memory']}%")
        print(f"Uptime             : {result['uptime']}")

    else:

        print("No running process found.")

    print("\n" + line)
#SERVICES DASHBOARD

def services_command(parts, brain):

    results = brain.check_critical_services()

    line = "=" * 70
    section = "-" * 70

    print("\n" + line)
    print("                    MONITORED SERVICES")
    print(line)

    print(f"{'Service':<15}{'Status':<15}{'Health'}")
    print(section)

    for service in results:

        print(
            f"{service['service']:<15}"
            f"{service['status']:<15}"
            f"{service['health']}"
        )

    print("\n" + line)


def kill_command(parts, brain):

    if not has_enough_parts(parts, 2):

        print("Usage: /kill <process_name>")
        return

    process = get_word(parts)

    result = brain.kill_service(process)

    line = "=" * 60
    section = "-" * 60

    print("\n" + line)
    print("               PROCESS TERMINATION")
    print(line)

    print(f"\nProcess            : {result['service']}")
    print(f"PID                : {result['pid']}")

    print("\nTERMINATION RESULT")
    print(section)

    print(f"Result             : {result['result']}")
    print(f"Reason             : {result['reason']}")

    audit = "Recorded" if result["audit"] else "Not Recorded"

    print(f"\nAudit Event        : {audit}")

    print("\n" + line)


def monitor_command(parts ,brain):

    if brain.monitoring:

        print("MONITOR ALREADY RUNNING")

        return

    brain.monitor_thread = threading.Thread(
        target=brain.start_background_monitor,
        daemon=True
    )

    brain.monitor_thread.start()

    brain.log_audit_event(
        "MONITOR",
        "BACKGROUND ENGINE",
        "STARTED"
    )

    log("Background monitoring engine started.")

    line = "=" * 50

    print("\n" + line)
    print("      BACKGROUND MONITOR STARTED")
    print(line)

    print("\nTelemetry collection enabled.")
    print("Alert engine activated.")
    print("Service monitoring activated.")

    print("\nMonitoring Interval : 30 seconds")

    print("\n" + line)


def telemetry_command(parts, brain):

    line = "=" * 60
    section = "-" * 60

    print("\n" + line)
    print("                  TELEMETRY HISTORY")
    print(line)

    if brain.monitoring:

        print("\nTelemetry Status    : ACTIVE")

    else:

        print("\nTelemetry Status    : STOPPED")

    print(f"Collection Interval : {brain.config['monitor_interval']} seconds")

    telemetry = [

        ("CPU", brain.cpu_history),

        ("MEMORY", brain.memory_history),

        ("DISK", brain.disk_history)

    ]

    for name, history in telemetry:

        print(f"\n{name} RESOURCE HISTORY")
        print(section)

        if not history:

            print("No telemetry recorded.")
            print("Start monitoring using: /monitor")
            continue

        print(f"Latest Reading      : {round(history[-1], 2)}%")
        print(f"Average Usage       : {round(sum(history) / len(history), 2)}%")
        print(f"Peak Usage          : {round(max(history), 2)}%")
        print(f"Minimum Usage       : {round(min(history), 2)}%")
        print(f"Samples Recorded    : {len(history)}")

        print("\nRecent Samples")
        print(section)

        recent_history = history[-20:]

        start_sample = len(history) - len(recent_history) + 1

        for index, value in enumerate(recent_history, start=start_sample):

            print(

                f"Sample {index:<3}"
                f"{round(value,2):>10}%"

            )

    print(section)

    if brain.monitoring:

        print("Monitoring engine is currently collecting telemetry.")

    else:

        print("Monitoring engine is stopped.")

    print("\n" + line)

def average_command(parts, brain):

    if not has_enough_parts(parts, 2):

        print("Usage: /average <cpu|memory|disk>")
        return

    metric = parts[1].lower()

    average = brain.get_average_usage(metric)

    if average is None:

        print("Unknown metric.")
        print("Available metrics: cpu, memory, disk")
        return

    line = "=" * 50

    print("\n" + line)
    print(f"          {metric.upper()} AVERAGE ANALYTICS")
    print(line)

    print(f"\nAverage {metric.upper()} Usage : {average}%")

    print("\n" + line)
    

def peak_command(parts, brain):

    if not has_enough_parts(parts, 2):

        print("Usage: /peak <cpu|memory|disk>")
        return

    metric = parts[1].lower()

    peak = brain.get_peak_usage(metric)

    if peak is None:

        print("Unknown metric.")
        print("Available metrics: cpu, memory, disk")
        return

    line = "=" * 50

    print("\n" + line)
    print(f"            {metric.upper()} PEAK ANALYTICS")
    print(line)

    print(f"\nPeak {metric.upper()} Usage : {peak}%")

    print("\n" + line)

def stability_command(parts, brain):

    if not has_enough_parts(parts, 2):

        print("Usage: /stability <cpu|memory|disk>")
        return

    metric = parts[1].lower()

    result = brain.get_stability(metric)

    if result is None:

        print("Unknown metric.")
        print("Available metrics: cpu, memory, disk")
        return

    line = "=" * 50

    print("\n" + line)
    print(f"         {metric.upper()} STABILITY ANALYSIS")
    print(line)

    print(f"\nStability Status : {result['status']}")
    print(f"Average Variation: {result['variation']}%")
    print(f"Samples Recorded : {result['samples']}")

    print("\n" + line)


def alerts_command(parts, brain):

    line = "=" * 75
    section = "-" * 75

    print("\n" + line)
    print("                         ACTIVE ALERTS")
    print(line)

    if len(brain.active_alerts) == 0:

        print("\nNo active alerts.")
        print("\n" + line)
        return

    print(
        f"{'Resource':<12}"
        f"{'Severity':<12}"
        f"{'Value':<10}"
        f"{'Since':<22}"
    )

    print(section)

    for alert in brain.active_alerts:

        print(

            f"{alert['resource'].upper():<12}"
            f"{alert['severity'].upper():<12}"
            f"{str(alert['value']) + '%':<10}"
            f"{alert['start_time']:<22}"

        )

    print("\nRecommendations")
    print(section)

    for alert in brain.active_alerts:

        print(

            f"{alert['resource'].upper():<10}"
            f"{alert.get('recommendation', 'No recommendation available')}"

        )

    print("\n" + line)


def incident_stats_command(parts, brain):

    stats = brain.get_incident_stats()

    line = "=" * 60
    section = "-" * 60

    print("\n" + line)
    print("                 INCIDENT STATISTICS")
    print(line)

    print("\nINCIDENT SUMMARY")
    print(section)

    print(f"Total Incidents      : {stats['total']}")
    print(f"Active Incidents     : {stats['active']}")

    print("\nRESOURCE BREAKDOWN")
    print(section)

    print(f"CPU Incidents        : {stats['cpu']}")
    print(f"Memory Incidents     : {stats['memory']}")
    print(f"Disk Incidents       : {stats['disk']}")

    print("\nSEVERITY BREAKDOWN")
    print(section)

    print(f"Critical Incidents   : {stats['critical']}")
    print(f"Warning Incidents    : {stats['warning']}")

    print("\n" + line)


def resolved_stats_command(parts, brain):

    stats = brain.get_resolved_stats()

    line = "=" * 60
    section = "-" * 60

    print("\n" + line)
    print("                 RESOLVED INCIDENTS")
    print(line)

    print("\nRESOLUTION SUMMARY")
    print(section)

    print(f"Resolved Incidents  : {stats['resolved']}")

    print("\nRESOURCE BREAKDOWN")
    print(section)

    print(f"CPU Incidents       : {stats['cpu']}")
    print(f"Memory Incidents    : {stats['memory']}")
    print(f"Disk Incidents      : {stats['disk']}")

    print("\nSEVERITY BREAKDOWN")
    print(section)

    print(f"Critical Incidents  : {stats['critical']}")
    print(f"Warning Incidents   : {stats['warning']}")

    print("\n" + line)

def recover_command(parts, brain):

    if not has_enough_parts(parts, 2):

        print("Usage: /recover <service_name>")
        return

    service = parts[1].lower()

    result = brain.restart_service(service)

    line = "=" * 60
    section = "-" * 60

    print("\n" + line)
    print("                  SERVICE RECOVERY")
    print(line)

    print(f"\nService            : {result['service']}")
    print(f"Previous Status    : {result['previous_status']}")
    print(f"Current Status     : {result['current_status']}")

    print("\nRECOVERY RESULT")
    print(section)

    print(f"Result             : {result['result']}")
    print(f"Reason             : {result['reason']}")

    audit_status = "Recorded" if result["audit"] else "Not Recorded"

    notification_status = "Sent" if result["notification"] else "Not Sent"

    print(f"\nAudit Event        : {audit_status}")
    print(f"Notification       : {notification_status}")

    print("\n" + line)


def dashboard_command(parts, brain):

    data = brain.get_dashboard_data()

    line = "=" * 50
    section = "-" * 50

    print("\n" + line)
    print("            SENTINELOPS DASHBOARD")
    print(line)

    print("\nSYSTEM HEALTH")
    print(section)

    print(f"Health Score        : {data['health_score']}/100")
    print(f"System Health       : {data['health']}")
    print(f"Health Trend        : {data['trend']}")
    print(f"Predictive Status   : {data['predictive']}")

    print("\nSYSTEM RESOURCES")
    print(section)

    print(f"CPU Usage           : {data['cpu']}%")
    print(f"Memory Usage        : {data['memory']}%")
    print(f"Disk Usage          : {data['disk']}%")

    print("\nINCIDENT SUMMARY")
    print(section)

    print(f"Active Alerts       : {data['active_alerts']}")
    print(f"Resolved Incidents  : {data['resolved_alerts']}")

    print("\nMONITORED SERVICES")
    print(section)
    print(f"{'Service':<15}{'Status':<15}Health")
    print(section)

    for service in data["services"]:

        print(
            f"{service['service']:<15}"
            f"{service['status']:<15}"
            f"{service['health']}"
        )

    print("\n" + line)


def report_command(parts , brain):

    report = brain.generate_report()

    print(report)


def save_report_command(parts, brain):

    filename = brain.save_report()

    line = "=" * 50

    print("\n" + line)
    print("              REPORT EXPORTED")
    print(line)

    print("\nOperational report exported successfully.\n")

    print(f"File Name          : {filename}")

    print("\n" + line)

def audit_command(parts, brain):

    print(brain.show_audit_trail())


def reliability_command(parts, brain):

    report = brain.service_reliability_report()

    line = "=" * 60

    print("\n" + line)
    print("               SERVICE RELIABILITY")
    print(line)

    print(report)

    print(line)


def recoveryrate_command(parts, brain):

    stats = brain.recovery_success_rate()

    line = "=" * 60
    section = "-" * 60

    print("\n" + line)
    print("              RECOVERY SUCCESS RATE")
    print(line)

    if stats["total"] == 0:

        print("\nNo recovery data available.")

        print("\n" + line)

        return

    print("\nRECOVERY SUMMARY")
    print(section)

    print(f"Total Recoveries      : {stats['total']}")
    print(f"Successful Recoveries : {stats['success']}")
    print(f"Failed Recoveries     : {stats['failed']}")

    print("\nPERFORMANCE")
    print(section)

    print(f"Recovery Success Rate : {stats['rate']}%")
    print(f"Recovery Engine       : {stats['health']}")

    print("\n" + line)


def clear_audit_command(parts, brain):

    result = brain.clear_audit_trail()

    line = "=" * 60

    print("\n" + line)
    print("                AUDIT MAINTENANCE")
    print(line)

    print("\nAction            : Clear Audit Trail")
    print(f"Result            : {result['result']}")
    print(f"Message           : {result['message']}")

    print("\nSystem Status     : Ready")

    print("\n" + line)


def notifications_command(parts, brain):

    print()
    print(brain.show_notifications())


    
    



    
