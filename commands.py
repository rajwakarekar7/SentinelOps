from utils import *
import os
import time
from logger import log
import threading

#HELP
def help_command(parts , brain):

    print("/learn word meaning category")
    print("/ask word")
    print("/search text")
    print("/show")
    print("/history")
    print("/exit")
    print("/delete word")
    print("/category name")
    print("/stats")
    print("/word meaning category")
    print("/backup")
    print("/system")
    print("/live")
    print("/service")
    print("/services")
    print("/kill")
    print("/monitor")
    print("/telemetry")
    print("/average cpu")
    print("/peak cpu")
    print("/stability cpu")
    print("/alerts")
    print("/incidentstats")
    print("/resolvedstats")
    print("/recover service")
    print("/dashboard data")
    print("/report")
    print("/savereport")


#LEARN
def learn_command(parts , brain):        

    if not has_enough_parts(parts , 2):

        print("Usage: /learn word meaning category")

    else:

        word = get_word(parts)

        meaning = " ".join(parts[2:-1]).lower()

        category = parts[-1].lower()

        brain.learn(word, meaning , category)

        print("Learned successfully")


# ASK
def ask_command(parts , brain):

    if not has_enough_parts(parts , 2):

        print("Usage: /ask word")

    else:

        word = get_word(parts)

        print(brain.answer(word))


# SEARCH
def search_command(parts , brain):

    if not has_enough_parts(parts, 2):

        print("Usage: /search text")

    else:

        text = get_text(parts)

        print(brain.search(text))


# SHOW MEMORY
def show_command(parts , brain):

    brain.show_memory()


# HISTORY
def history_command(parts , brain):

    brain.show_history()


#CATEGORY
def category_command(parts , brain):

    if not has_enough_parts(parts , 2):

        print("Usage: /category name")

    else:

        category = get_word(parts)

        print(brain.show_category(category))


#STATS
def stats_command(parts , brain):

    print(brain.stats())


#DELETE
def delete_command(parts , brain):

    if not has_enough_parts(parts , 2):

        print("Usage: /delete word")

    else:

        word =get_word(parts)

        print(brain.delete(word))


#UPDETE
def update_command(parts , brain):

    if len(parts) < 4 :

        print("Usage: /update word meaning category")

    else:

        word = parts[1].lower()

        meaning = " ".join(parts[2:-1]).lower()

        category = parts[-1].lower()

        print(brain.update(word , meaning , category))


#BACKUP
def backup_command(parts , brain):

    print(brain.backup())


#SYSTEM_RESOURCE_USAGE
def system_command(parts , brain):
    
    system_info = brain.get_system_info()

    top_cpu = brain.get_top_cpu_processes()

    top_memory = brain.get_top_memory_processes()

    print("\n[SYSTEM INFO]")

    print()

    print("CPU USAGE:" , system_info["cpu"] , "%")
    print("CPU CORES:" , system_info["cpu_cores"] )
    print("RUNNING PROCESSES:" , system_info["process_count"])

    if top_cpu["warning"]:

        print("\n[WARNING]")

        print(top_cpu["warning"])

    print("\nTOP CPU PROCESSES:\n")

    for process in top_cpu["processes"]:

        print(

            f"{process[0]:30} {process[1]} %" 
 
        )

    print()

    print("MEMORY USAGE:" , system_info["memory_percent"] , "%")
    print("TOTAL_RAM:" , system_info["total_ram"] , "GB")
    print("AVAILABLE_RAM:" , system_info["available_ram"] , "GB")

    if top_memory["warning"]:

        print("\n[WARNING]")

        print(top_memory["warning"])

    print("\nTOP MEMORY PROCESSES:\n")

    for process in top_memory["processes"]:

        print(

            f"{process[0]:30} {process[1]}%"
        )


    print()

    print("DISK USAGE:" ,  system_info["disk_percent"] , "%")

    print()

    print("UPTIME: " , system_info["uptime"])
    

#LIVE MONITORING TOOL
def live_monitor( parts , brain):

    while True:

        os.system("cls")

        system_info = brain.get_system_info()

        log(

            "CPU: "
            
            +str(system_info["cpu"])

            + "% |"

            "RAM: "

            +str(system_info["memory_percent"])

            + "% |"

            "DISK: "

            +str(system_info["disk_percent"])

            +"%"

        )

        top_cpu = brain.get_top_cpu_processes()

        top_memory = brain.get_top_memory_processes()

        print("==============================")
        print("     LIVE SYSTEM MONITOR")
        print("==============================\n")

        print(
            "CPU USAGE:",
            system_info["cpu"],
            "%"
        )

        print(
            "CPU CORES:",
            system_info["cpu_cores"]
        )

        print(
            "RUNNING PROCESSES:",
            system_info["process_count"]
        )

        # CPU WARNING

        if top_cpu["warning"]:

            print("\n[WARNING]")

            print(
                top_cpu["warning"]
            )

        # CPU LEADERBOARD

        print("\nTOP CPU PROCESSES:\n")

        for process in top_cpu["processes"]:

            print(

                f"{process[0]:30} "
                f"{process[1]} %"

            )

        # MEMORY

        print("\nMEMORY USAGE:")

        print(
            system_info["memory_percent"],
            "%"
        )

        print(
            "TOTAL RAM:",
            system_info["total_ram"],
            "GB"
        )

        print(
            "AVAILABLE RAM:",
            system_info["available_ram"],
            "GB"
        )

        # MEMORY WARNING

        if top_memory["warning"]:

            print("\n[WARNING]")

            print(
                top_memory["warning"]
            )

        # MEMORY LEADERBOARD

        print("\nTOP MEMORY PROCESSES:\n")

        for process in top_memory["processes"]:

            print(

                f"{process[0]:30} "
                f"{process[1]} %"

            )

        # DISK

        print("\nDISK USAGE:")

        print(
            system_info["disk_percent"],
            "%"
        )

        # UPTIME

        print("\nUPTIME:")

        print(
            system_info["uptime"]
        )

        time.sleep(10)


#PROCESSES MONITORING SYSTEM
def service_command(parts, brain):

    if not has_enough_parts(parts , 2):

        print("USAGE: /service name")

        return

    service_name = get_word(parts)

    result = brain.check_service(service_name)

    print("\n[SERVICE STATUS]\n")
    print("SERVICE:" , result["service"])

    print("STATUS:" , result["status"])

    if result["status"] == "ACTIVE":

        print("PID:" , result["pid"])

        print("CPU USAGE:", result["cpu"],"%")

        print("MEMORY USAGE:", result["memory"], "%")

        print("UPTIME:" , result["uptime"])

        print("HEALTH:" , result["health"])

    else:

        print("HEALTH:" , result["health"])


#SERVICES DASHBOARD
def services_command(parts , brain):

    results = brain.check_critical_services()

    print("\n[CRITICAL SERVICES]\n")

    for result in results:

        print(

            f"{result['service']:15}"
            f"{result['status']}"
        )


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

    monitor_thread = threading.Thread(
        
        target= brain.start_background_monitor
        
    )

    monitor_thread.start()

    print("\n[BACKGROUND MONITOR STARTED]\n")


def telemetry_command(parts , brain):

    print("\n[TELEMETRY HISTORY]\n")

    print("CPU HISTORY:")
    print(brain.cpu_history)

    print("MEMORY HISTORY:")
    print(brain.memory_history)

    print("DISK HISTORY:")
    print(brain.disk_history)

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

            alert["timestamp"],

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


def dashboard_command(parts , brain):

    data = brain.get_dashboard_data()

    print("\n[SYSTEM DASHBOARD]\n")

    print("HEALTH SCORE:", data["health_score"], "/100")

    print("SYSTEM HEALTH:", data["health"])

    print("HEALTH TREND:" , data["trend"])

    print("PREDICTIVE STATUS:" , data["predictive"])

    print()

    print("CPU:", data["cpu"], "%")

    print("MEMORY:", data["memory"], "%")

    print("DISK:", data["disk"], "%")

    print()

    print("ACTIVE ALERTS:", data["active_alerts"])

    print("RESOLVED INCIDENTS:", data["resolved_alerts"])

    print("\n[SERVICES]\n")

    for service in data["services"]:

        print(

            service["name"],

            "->",

            service["status"]

        )


def report_command(parts , brain):

    report = brain.generate_report()

    print(report)


def save_report_command(parts ,brain):

    filename = brain.save_report()

    print("\n[REPORT EXPORT]\n")

    print("REPORT SAVED:", filename)

    
    



    
