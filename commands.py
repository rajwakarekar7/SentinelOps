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
    print("/dashboard         View system dashboard")
    print("/system            View system resource information")
    print("/live              Start live monitoring")
    print("/telemetry         View telemetry history")

    print("\nSERVICE MANAGEMENT")
    print(section)
    print("/services          List monitored services")
    print("/service <name>    View service status")
    print("/monitor           Start background monitoring engine")
    print("/recover <name>    Restart a monitored service")
    print("/kill <process>    Safely terminate a process")

    print("\nRESOURCE ANALYTICS")
    print(section)
    print("/average <metric>  Average resource usage")
    print("/peak <metric>     Peak resource usage")
    print("/stability <metric> Resource stability analysis")

    print("\nINCIDENT MANAGEMENT")
    print(section)
    print("/alerts            View active alerts")
    print("/incidentstats     View incident statistics")
    print("/resolvedstats     View resolved incidents")
    print("/audit             View audit trail")
    print("/notifications     View notification history")

    print("\nREPORTING")
    print(section)
    print("/report            Generate operational report")
    print("/savereport        Export report")

    print("\nRELIABILITY")
    print(section)
    print("/reliability       View service reliability report")
    print("/recoveryrate      View recovery success rate")
    print("/clear-audit       Clear audit history")

    print("\nSYSTEM")
    print(section)
    print("/help              Show help")
    print("/exit              Exit SentinelOps")

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
    print(f"{'Process':<30}{'CPU %':>8}")
    print(section)

    for process in top_cpu["processes"]:

        print(f"{process[0]:<30}{process[1]:>8}%")

    if top_memory["warning"]:

        print("\nMEMORY WARNING")
        print(section)
        print(top_memory["warning"])

    print("\nTOP MEMORY PROCESSES")
    print(section)
    print(f"{'Process':<30}{'Memory %':>10}")
    print(section)

    for process in top_memory["processes"]:

        print(f"{process[0]:<30}{process[1]:>10}%")

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
            print("                    LIVE MONITOR")
            print(line)

            print(f"\nLast Updated        : {time.strftime('%Y-%m-%d %H:%M:%S')}")

            print("\nSYSTEM HEALTH")
            print(section)

            print(f"Health Score        : {dashboard['health_score']}/100 ({dashboard['health']})")
            print(f"System Health       : {dashboard['health']}")
            print(f"Health Trend        : {dashboard['trend']}")
            print(f"Predictive Status   : {dashboard['predictive']}")
            print(f"Active Alerts       : {dashboard['active_alerts']}")

            print("\nSYSTEM RESOURCES")
            print(section)

            print(f"CPU Usage           : {system_info['cpu']}%")
            print(f"Memory Usage        : {system_info['memory_percent']}%")
            print(f"Disk Usage          : {system_info['disk_percent']}%")
            print(f"CPU Cores           : {system_info['cpu_cores']}")
            print(f"Running Processes   : {system_info['process_count']}")
            print(f"Total RAM           : {system_info['total_ram']} GB")
            print(f"Available RAM       : {system_info['available_ram']} GB")
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

            print(section)
            print("Monitoring Active | Refresh Interval: 5 seconds")
            print("Press Ctrl+C to stop monitoring")
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

    print(f"PID                : {result['pid']}")
    print(f"CPU Usage          : {result['cpu']}%")
    print(f"Memory Usage       : {result['memory']}%")
    print(f"Uptime             : {result['uptime']}")

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


def kill_command(parts , brain):

    if not has_enough_parts(parts, 2):

        print("USAGE: /kill service_name")

        return
    
    service_name = get_word(parts)

    results = brain.kill_service(service_name)

    print("\n[KILL SERVICE]\n")

    print("SERVICE:" , results["service"])
    print("STATUS:" , results["status"] )


def monitor_command(parts ,brain):

    if brain.monitoring:

        print("MONITOR ALREADY RUNNING")

        return

    monitor_thread = threading.Thread(
            
        target= brain.start_background_monitor,

        daemon = True
            
    )

    monitor_thread.start()

    print("\n[BACKGROUND MONITOR STARTED]\n")


def telemetry_command(parts, brain):

    line = "=" * 60
    section = "-" * 60

    print("\n" + line)
    print("                  TELEMETRY HISTORY")
    print(line)

    telemetry = [

        ("CPU", brain.cpu_history),

        ("MEMORY", brain.memory_history),

        ("DISK", brain.disk_history)

    ]

    for name, history in telemetry:

        print(f"\n{name} TELEMETRY")
        print(section)

        if not history:

            print("No telemetry recorded.")
            print("Start monitoring using: /monitor")
            continue

        print(f"Samples Recorded   : {len(history)}")
        print(f"Latest Reading     : {history[-1]}%")
        print(f"Highest Reading    : {max(history)}%")
        print(f"Lowest Reading     : {min(history)}%")
        print(f"Average Usage      : {round(sum(history)/len(history),2)}%")

        print("\nRecent History")
        print(section)

        recent_history = history[-20:]

        start_sample = len(history) - len(recent_history) + 1

        for index, value in enumerate(recent_history, start=start_sample):

            print(f"Sample {index:02}          {value}%")

    print("\n" + line)

def average_command(parts ,brain):

    if not has_enough_parts(parts , 2):

        print("USAGE: /average cpu")

        return
    
    metric = parts[1].lower()

    if metric == "cpu":

        average = brain.get_average_cpu()

        print("\n[CPU ANALYTICS]\n")

        print("AVERAGE CPU :" ,average , "%")

    else:

        print("Unknown metric")
    

def peak_command(parts ,brain):

    if not has_enough_parts(parts ,2):

        return
    
    metric = parts[1].lower()

    if metric == "cpu":

        peak = brain.get_peak_cpu()

        print("\n[CPU PEAK ANALYTICS]\n")

        print("CPU PEAK: " , peak , "%")
    
    else:

        print("Unknown metric")


def stability_command(parts ,brain):

    if not has_enough_parts(parts , 2):

        print("USAGE: /stability cpu")

        return
      
    metric = parts[1].lower()

    if metric == "cpu":

        stability = brain.get_cpu_stability()

        print("\n[CPU STABILITY ANALYTICS]\n")

        print("CPU STABILITY:" , stability)

    else:

        print("Unknown metric")


def alerts_command(parts , brain):

    print("\n[ACTIVE ALERTS]\n")

    if len(brain.active_alerts) == 0:

        print("No active alerts")

        return
    
    for alert in brain.active_alerts:

        print(

            alert["start_time"],

            "|",

            alert["message"])


def incident_stats_command(parts , brain):

    stats = brain.get_incident_stats()

    print("\n[INCIDENT ANALYTICS]\n")

    print("CPU INCIDENT: " , stats["cpu"])
    print("MEMORY INCIDENT: " , stats["memory"])
    print("DISK INCIDENT: " , stats["disk"])

    print()

    print("CRITICAL INCIDENT: " , stats["critical"])
    print("WARNING INCIDENT: ", stats["warning"])


def resolved_stats_command(parts , brain):

    stats = brain.get_resolved_stats()

    print("\n[RESOLVED INCIDENT ANALYTICS]\n")

    print("TOTAL INCIDENTS:", stats["total"])

    print()

    print("CPU INCIDENTS:", stats["cpu"])

    print("MEMORY INCIDENTS:", stats["memory"])

    print("DISK INCIDENTS:", stats["disk"])

    print()

    print("CRITICAL INCIDENTS:", stats["critical"])

    print("WARNING INCIDENTS:", stats["warning"])


def recover_command(parts , brain):

    if not has_enough_parts(parts ,2):

        print("USAGE /recover service")

        return
    
    service = parts[1].lower()

    result = brain.restart_service(service)

    print("\n[SERVICE RECOVERY]\n")

    print(result)


def dashboard_command(parts, brain):

    data = brain.get_dashboard_data()

    line = "=" * 50
    section = "-" * 50

    print("\n" + line)
    print("            SENTINELOPS DASHBOARD")
    print(line)

    print("\nSYSTEM HEALTH")
    print(section)

    print(f"Health Score        : {data['health_score']}/100 ({data['health']})")
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
    print(f"{'Service':<18} Status")
    print(section)

    for service in data["services"]:
        print(f"{service['name']:<18} {service['status']}")

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


def reliability_command(parts , brain):

    print(brain.service_reliability_report())


def recoveryrate_command(parts, brain):

    print(brain.recovery_success_rate())


def clear_audit_command(parts ,brain):

    result = brain.clear_audit_trail()

    print(result)


def notifications_command(parts ,brain):

    print(brain.show_notifications())


    
    



    
