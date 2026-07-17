from logger import log
import psutil
import time
import json
import os
import subprocess
from datetime import datetime

class Brain:

    def __init__(self):

        self.monitoring = False

        self.cpu_history = []

        self.memory_history = []

        self.disk_history = []

        self.last_cpu_alert = 0

        self.last_memory_alert = 0

        self.last_disk_alert = 0

        self.audit_file = "audit_trail.json"

        self.notification_file = "notification.json"

        self.alert_file = "alerts.json"

        self.ensure_runtime_files()

        self.active_alerts = self.load_alerts()

        self.notifications = self.load_notification()

        self.config = self.load_config()

        self.resolved_alerts = []

        self.audit_trail = self.load_audit_trail()

        self.recoverable_services ={

            "sshd",

            "firewalld",

            "rsyslog",

            "chronyd",

            "crond"

        }

        self.monitored_services =[

            "sshd",

            "firewalld",

            "rsyslog",

            "chronyd",

            "crond",

            "cups"
        ]

        self.health_history = []

        self.failed_services = set()

        self.monitor_thread = None

        self.protected_processes = {

            "system",
            "systemd",
            "init",
            "explorer",
            "wininit",
            "csrss",
            "python"

        }

       

    
    def ensure_runtime_files(self):

        runtime_files = [

            self.alert_file,

            self.audit_file,

            self.notification_file

        ]

        for file in runtime_files:

            if not os.path.exists(file):

                with open(file, "w") as f:

                    json.dump([],f,indent=4)


    def get_system_info(self):
        
        cpu = psutil.cpu_percent()

        cpu_cores = psutil.cpu_count()

        memory = psutil.virtual_memory().percent

        ram = psutil.virtual_memory()

        total_ram = round(ram.total / (1024 ** 3) , 1)

        available_ram = round(ram.available / (1024 ** 3), 1)

        disk = psutil.disk_usage("/").percent

        uptime = psutil.boot_time()

        process_count = len(psutil.pids())

        current_time= time.time()

        uptime_seconds = current_time - uptime

        days = int(uptime_seconds // 86400)

        hours = int((uptime_seconds % 86400) // 3600)

        minutes = int((uptime_seconds % 3600) // 60)

        uptime = f"{days} days, {hours} hours, {minutes} minutes"

        
        return {

            "cpu": cpu,
            "cpu_cores": cpu_cores,
            "memory_percent": memory,
            "disk_percent": disk,
            "uptime": uptime,
            "total_ram": total_ram,
            "available_ram": available_ram,
            "process_count": process_count

        }
    

    def get_top_cpu_processes(self):

        processes = []

        warning = None

        for process in psutil.process_iter():

            process.cpu_percent()

        time.sleep(1)

        for process in psutil.process_iter():

            try:

                name = process.name()

                if name == "System Idle Process":
                   continue

                cpu = process.cpu_percent()

                if cpu > 90 :

                   warning =(

                       name

                       + " is using high cpu ("

                       + str(cpu)

                       + "%)"
                   )


                processes.append((name , cpu))

            except (psutil.NoSuchProcess,
                    psutil.AccessDenied,
                    psutil.ZombieProcess):
                continue
        
        processes.sort(key=lambda x:x[1] , reverse= True)

        return { 
            
            "processes" : processes[:5],

            "warning" : warning
                            
        }

  
    def get_top_memory_processes(self):

        processes = []

        warning = None

        for process in psutil.process_iter():

            try:

                name = process.name()

                memory = round(process.memory_percent() , 2)

                if memory > 60:

                    warning =(

                        name

                        + " is using high memory ("

                        + str(memory)

                        + "%)"
                    )

                processes.append((name , memory) )

            except (psutil.NoSuchProcess,
                    psutil.AccessDenied,
                    psutil.ZombieProcess):
                continue

        processes.sort(key=lambda x:x[1] , reverse=True)

        return{

            "processes":processes[:5],

            "warning": warning
        }
    

    def get_service_status(self , service_name):

        service_name = service_name.lower()

        try:

            result = subprocess.run(

                ["systemctl" ,"is-active" , service_name],

                capture_output=True,

                text=True
            )

            service_status = result.stdout.strip()

            if service_status != "active":

                return{

                    "service" : service_name,

                    "status" : service_status.upper(),

                    "pid" : "N/A",

                    "cpu" : 0,

                    "memory" : 0,

                    "health" : "SERVICE NOT RUNNING",

                    "uptime" : "N/A"
   
                }

        except (subprocess.SubprocessError, FileNotFoundError):

            return {
                "service": service_name,
                "status": "UNSUPPORTED",
                "pid": "N/A",
                "cpu": 0,
                "memory": 0,
                "health": "SYSTEMCTL NOT AVAILABLE",
                "uptime": "N/A"
            }
            

        for process in psutil.process_iter():

            try:

                name = process.name().lower()

                created_time = process.create_time()

                current_time = time.time()

                uptime_seconds = current_time - created_time

                hours = int(uptime_seconds // 3600)

                minutes = int((uptime_seconds % 3600) // 60)

                uptime = f"{hours} hours , {minutes} minutes"

                if service_name in name:

                    process.cpu_percent()

                    time.sleep(2)

                    cpu = process.cpu_percent()

                    memory = round(process.memory_percent() , 2)

                    health = "NORMAL"

                    if uptime_seconds < 300:

                        health = "RECENTLY RESTARTED"

                    if cpu > 80:

                        health = "HIGH CPU USAGE"

                    elif memory > 10:

                        health = "HIGH MEMORY USAGE"
                    

                    return{

                        "service": service_name,
                        "status": "ACTIVE",
                        "pid": process.pid,
                        "cpu": cpu,
                        "memory": memory,
                        "health": health,
                        "uptime": uptime
                    }
                 
            except (psutil.NoSuchProcess,
                    psutil.AccessDenied,
                    psutil.ZombieProcess):
                continue

        return {
            "service": service_name,
            "status": service_status.upper(),
            "pid": "N/A",
            "cpu": 0,
            "memory": 0,
            "health": "UNKNOWN",
            "uptime": "N/A"
        }
    

    def check_critical_services(self):

        results = []

        for service in self.monitored_services:

            result = self.get_service_status(service)

            results.append(result)

        return results

         
    def kill_service(self, service_name):

        service_name = service_name.lower()

        for process in psutil.process_iter():

            try:

                name = process.name().lower()

                if service_name in name:

                    for protected in self.protected_processes:

                        if protected in name:

                            log("Blocked protected process: " + name)

                            self.log_audit_event(
                                "PROCESS_TERMINATION",
                                name,
                                "BLOCKED"
                            )

                            return {

                                "service": name,
                                "pid": process.pid,
                                "result": "BLOCKED",
                                "reason": "PROTECTED SYSTEM PROCESS",
                                "audit": True

                            }

                    pid = process.pid

                    process.kill()

                    log("Killed process: " + name)

                    self.log_audit_event(
                        "PROCESS_TERMINATION",
                        name,
                        "SUCCESS"
                    )

                    return {

                        "service": name,
                        "pid": pid,
                        "result": "SUCCESS",
                        "reason": "PROCESS TERMINATED",
                        "audit": True

                    }

            except (
                psutil.NoSuchProcess,
                psutil.AccessDenied,
                psutil.ZombieProcess
            ):
                continue

        log("Process not found: " + service_name)

        return {

            "service": service_name,
            "pid": "N/A",
            "result": "FAILED",
            "reason": "PROCESS NOT FOUND",
            "audit": False

        }
    
    def start_background_monitor(self):

        self.monitoring = True

        while self.monitoring:

            system_info = self.get_system_info()

            health_score = self.calculate_health_score()

            self.health_history.append(health_score)

            if len(self.health_history) > 100:

                self.health_history.pop(0)

            current_time =time.time()

            self.cpu_history.append(

                system_info["cpu"]
            )

            self.memory_history.append(

                system_info["memory_percent"]
            )

            self.disk_history.append(

                system_info["disk_percent"]
            )

            if len(self.cpu_history) > 100:

                self.cpu_history.pop(0)

            if len(self.memory_history) > 100:

                self.memory_history.pop(0)

            if len(self.disk_history) > 100:

                self.disk_history.pop(0)

            
            cpu = system_info["cpu"]

            if cpu >= self.config["cpu_critical"]:

                if current_time - self.last_cpu_alert > self.config["cooldown"]:

                    recommendation = self.get_recommendation(

                        "cpu" ,

                        "critical"
                    )

                    alert ={

                         "resource": "cpu",

                         "severity": "critical",

                         "value": cpu,

                         "start_time":time.strftime("%Y-%m-%d %H:%M:%S"),

                         "recommendation": recommendation,

                         "message": (

                            "[CRITICAL] CPU USAGE: "

                            +str(cpu)

                            + "%"
                        )

                    }   

                    self.active_alerts.append(alert)

                    self.save_alerts()

                    log(

                        alert["message"]

                        + " | RECOMMENDATION: "

                        + recommendation

                    )

                    self.last_cpu_alert = current_time

                else:

                    self.resolve_alert("CPU")


            elif cpu >= self.config["cpu_warning"]:

                if current_time - self.last_cpu_alert > self.config["cooldown"]:

                    recommendation = self.get_recommendation(

                        "cpu" ,

                        "warning"

                    )

                    alert ={

                        
                         "resource": "cpu",

                         "severity": "warning",

                         "value": cpu,

                         "start_time":time.strftime("%Y-%m-%d %H:%M:%S"),

                         "recommendation": recommendation,

                         "message": (

                            "[WARNING] CPU USAGE: "

                            +str(cpu)

                            + "%"
                        )
                    }

                    self.active_alerts.append(alert)

                    self.save_alerts()

                    log(

                        alert["message"]

                        + " | RECOMMENDATION: "

                        + recommendation

                    )

                    self.last_cpu_alert = current_time

                else:

                    self.resolve_alert("CPU")


            memory = system_info["memory_percent"]

            if memory >= self.config["memory_critical"]:

                if current_time - self.last_memory_alert > self.config["cooldown"]:

                    recommendation = self.get_recommendation(

                        "memory" ,

                        "critical"

                    )

                    alert ={
                    
                         "resource": "memory",

                         "severity": "critical",

                         "value": memory,

                         "start_time":time.strftime("%Y-%m-%d %H:%M:%S"),

                         "recommendation": recommendation,

                         "message": (

                            "[CRITICAL] MEMORY USAGE: "

                            +str(memory)

                            + "%"
                        )
                    }

                    self.active_alerts.append(alert)

                    self.save_alerts()

                    log(

                        alert["message"]

                        + " | RECOMMENDATION: "

                        + recommendation

                    )

                    self.last_memory_alert = current_time

                else:

                    self.resolve_alert("MEMORY")


            elif memory >= self.config["memory_warning"]:

                if current_time - self.last_memory_alert > self.config["cooldown"]:

                    recommendation = self.get_recommendation(

                        "memory" ,

                        "warning"

                    )

                    alert ={
                    
                         "resource": "memory",

                         "severity": "warning",

                         "value": memory,

                         "start_time":time.strftime("%Y-%m-%d %H:%M:%S"),

                         "recommendation": recommendation,

                         "message": (

                            "[WARNING] MEMORY USAGE: "

                            +str(memory)

                            + "%"
                        )
                    }

                    self.active_alerts.append(alert)

                    self.save_alerts()

                    log(

                        alert["message"]

                        +" | RECOMMENDATION: "

                        + recommendation

                    )

                    self.last_memory_alert = current_time

                else:

                    self.resolve_alert("MEMORY")


            disk = system_info["disk_percent"]

            if disk >= self.config["disk_critical"]:

                if current_time - self.last_disk_alert > self.config["cooldown"]:

                    recommendation = self.get_recommendation(

                        "disk" ,

                        "critical"

                    )

                    alert ={

                        "resource": "disk",

                        "severity": "critical",

                        "value": disk,

                        "start_time":time.strftime("%Y-%m-%d %H:%M:%S"),

                        "recommendation": recommendation,

                        "message": (

                            "[CRITICAL] DISK USAGE: "

                            +str(disk)

                            + "%"
                        )
                    }

                    self.active_alerts.append(alert)

                    self.save_alerts()

                    log(

                        alert["message"]

                        +" | RECOMMENDATION: "

                        + recommendation
                    )

                    self.last_disk_alert = current_time

                else:

                    self.resolve_alert("DISK")


            elif disk >= self.config["disk_warning"]:

                if current_time - self.last_disk_alert > self.config["cooldown"]:

                    recommendation = self.get_recommendation(

                        "disk" ,

                        "warning"

                    )

                    alert ={

                        "resource": "disk",

                        "severity": "warning",

                        "value": disk,

                        "start_time":time.strftime("%Y-%m-%d %H:%M:%S"),

                        "recommendation": recommendation,

                        "message": (

                            "[WARNING] DISK USAGE: "

                            +str(disk)

                            + "%"
                        )
                    }

                    self.active_alerts.append(alert)

                    self.save_alerts()

                    log(

                        alert["message"]

                        +" | RECOMMENDATION: "

                        + recommendation

                    )

                    self.last_disk_alert = current_time

                else:

                    self.resolve_alert("DISK")

            
            self.monitor_services()


            time.sleep(self.config["monitor_interval"])

    
    def stop_monitor(self):

        if not self.monitoring:
            return False

        self.monitoring = False

        log("Background monitor stopped")

        return True


    def get_average_usage(self, metric):

        metric = metric.lower()

        history = {

            "cpu": self.cpu_history,
            "memory": self.memory_history,
            "disk": self.disk_history

        }.get(metric)

        if history is None:

            return None

        if len(history) == 0:

            return 0

        return round(sum(history) / len(history), 2)
    
    
    def get_peak_usage(self, metric):

        metric = metric.lower()

        history = {

            "cpu": self.cpu_history,
            "memory": self.memory_history,
            "disk": self.disk_history

        }.get(metric)

        if history is None:

            return None

        if len(history) == 0:

            return 0

        return round(max(history), 2)
    
    
    def get_stability(self, metric):

        metric = metric.lower()

        history = {

            "cpu": self.cpu_history,
            "memory": self.memory_history,
            "disk": self.disk_history

        }.get(metric)

        if history is None:

            return None

        if len(history) == 0:

            return {

                "status": "NO DATA",
                "variation": 0,
                "samples": 0

            }

        average = sum(history) / len(history)

        differences = []

        for value in history:

            differences.append(abs(value - average))

        variation = round(sum(differences) / len(differences), 2)

        if variation < 10:

            status = "STABLE"

        elif variation < 30:

            status = "MODERATE"

        else:

            status = "UNSTABLE"

        return {

            "status": status,
            "variation": variation,
            "samples": len(history)

        }
        

    def get_recommendation(self , resource , severity):

        if resource == "cpu" :

            if severity == "critical" :

                return (

                    "check high cpu processes "
                    "and stop unnecessary applications"
                )
            
            elif severity == "warning" :

                return(

                    "monitor cpu usage "
                    "and reduce background tasks"
                )
            
        elif resource == "memory":

            if severity == "critical":

                return(

                    "close unused applications "
                    "and investigate memory usage"
                )
            
            elif severity == "warning":

                return(

                    "monitor RAM usage "
                    "and avoid opening heavy programs"
                )
            
        elif resource == "disk":

            if severity == "critical" :

                return(

                    "Free disk space immediately "
                    "and remove unnecessary files"
                )
            
            elif severity == "warning":

                return(

                    "check storage usage "
                    "clean temporary files"
                )
            
    
    def resolve_alert(self , keyword):

        end_time = time.strftime("%Y-%m-%d %H:%M:%S")

        updated_alerts = []

        for alert in self.active_alerts:

            if keyword.lower() != alert['resource']:

                updated_alerts.append(alert)

            else:

                alert["end_time"] = end_time

                alert["status"] = "RESOLVED"

                self.resolved_alerts.append(alert)

        self.active_alerts = updated_alerts

        self.save_alerts()


    def load_config(self):

        with open("config.json", "r") as file:
            config = json.load(file)

        return config
    

    def save_alerts(self):

        with open("alerts.json", "w") as file:

            json.dump(self.active_alerts, file, indent=4)



    def log_audit_event(self, event ,target ,status):

        record = {

            "timestamp" : time.strftime("%Y-%m-%d %H:%M:%S"),

            "event" : event,

            "target" : target,

            "status" : status
        }

        self.audit_trail.append(record)

        self.save_audit_trail()


    def show_audit_trail(self):

        if len(self.audit_trail) == 0:

            return "No audit events recorded."

        border = "=" * 75
        section = "-" * 75

        lines = []

        lines.append(border)
        lines.append("                         AUDIT TRAIL")
        lines.append(border)
        lines.append("")
        lines.append(

            f"{'TIMESTAMP':22}"
            f"{'EVENT':18}"
            f"{'TARGET':25}"
            f"{'STATUS':12}"
        )
        lines.append(section)

        for event in self.audit_trail:

            line = (

                f"{event['timestamp']:22}"
                f"{event['event']:18}"
                f"{event['target']:25}"
                f"{event['status']:12}"
            )
            
            lines.append("")
            lines.append(line)

        lines.append(border)

        return "\n".join(lines)

    
    def load_alerts(self):

        try:

            with open(self.alert_file, "r") as file:

                return json.load(file)

        except (FileNotFoundError, json.JSONDecodeError):

            return []


    def get_incident_stats(self):

        cpu_count = 0
        memory_count = 0
        disk_count = 0

        critical_count = 0
        warning_count = 0

        for alert in self.active_alerts:

            if alert["resource"] == "cpu":

                cpu_count += 1

            elif alert["resource"] == "memory":

                memory_count += 1

            elif alert["resource"] == "disk":

                disk_count += 1

            # Separate IF statements
            if alert["severity"] == "critical":

                critical_count += 1

            elif alert["severity"] == "warning":

                warning_count += 1

        return {

            "cpu": cpu_count,

            "memory": memory_count,

            "disk": disk_count,

            "critical": critical_count,

            "warning": warning_count,

            "active": len(self.active_alerts),

            "total": len(self.active_alerts)

        }
    

    def get_resolved_stats(self):

        cpu_count = 0

        memory_count = 0

        disk_count = 0

        critical_count = 0

        warning_count = 0

        for alert in self.resolved_alerts:

            if alert["resource"] == "cpu":

                cpu_count += 1

            elif alert["resource"] == "memory":

                memory_count += 1

            elif alert["resource"] == "disk":

                disk_count += 1

            if alert["severity"] == "critical":

                critical_count += 1

            elif alert["severity"] == "warning":

                warning_count += 1

        return {

            "resolved": len(self.resolved_alerts),

            "cpu": cpu_count,

            "memory": memory_count,

            "disk": disk_count,

            "critical": critical_count,

            "warning": warning_count

        }
    

    def restart_service(self, service_name):

        if service_name not in self.recoverable_services:

            return {

                "service": service_name,
                "previous_status": "UNKNOWN",
                "current_status": "NOT RECOVERABLE",
                "result": "FAILED",
                "reason": "SERVICE NOT APPROVED FOR AUTO-RECOVERY",

                "audit": False,
                "notification": False

            }

        previous = self.get_service_status(service_name)["status"]

        subprocess.run(

            ["sudo", "systemctl", "restart", service_name],

            capture_output=True,
            text=True

        )

        result = self.get_service_status(service_name)

        if result["status"] == "ACTIVE":

            self.failed_services.discard(service_name)

            self.log_audit_event(

                "AUTO_RECOVERY",
                service_name,
                "SUCCESS"

            )

            self.send_notification(

                "INFO",
                service_name,
                service_name + " recovered successfully",
                "SUCCESS"

            )

            return {

                "service": service_name,
                "previous_status": previous,
                "current_status": result["status"],
                "result": "SUCCESS",
                "reason": "SERVICE RESTARTED SUCCESSFULLY",

                "audit": True,
                "notification": True

            }

        self.log_audit_event(

            "AUTO_RECOVERY",
            service_name,
            "FAILED"

        )

        self.send_notification(

            "CRITICAL",
            service_name,
            service_name + " recovery failed",
            "FAILED"

        )

        return {

            "service": service_name,
            "previous_status": previous,
            "current_status": result["status"],
            "result": "FAILED",
            "reason": "SERVICE COULD NOT BE RESTARTED",

            "audit": True,
            "notification": True

        }
    
    
    def monitor_services(self):

        for service in self.monitored_services:

            result = self.get_service_status(service)

            if result["status"] in [ "INACTIVE" , "FAILED"]:

                if service not in self.failed_services:

                    self.failed_services.add(service)

                    log(

                        "SERVICE FAILURE: "

                        + service

                        + " is not running"
                    )

                    self.log_audit_event(

                        "SERVICE_FAILURE" ,

                        service ,

                        result["status"]
                    )

                    self.send_notification(

                        "CRITICAL",

                        service ,

                        service + " service failure detected",

                        "PENDING"
                    )

                    if service not in self.recoverable_services:

                        self.log_audit_event(

                            "RECOVERY_SKIPPED",

                            service,

                            "NOT APPROVED"
                        )

                        log(

                            "[RECOVERY SKIPPED] "

                            + service

                            + " is not approved for auto recovery"
                        )

                        continue

                    recovery_result = self.restart_service(service)

                    log(

                        "[AUTO RECOVERY] "

                        + service

                        + " -> "

                        + recovery_result["result"]

                        + " | "

                        + recovery_result["reason"]
                    )


    def get_dashboard_data(self):

        system_info =self.get_system_info()

        trend = self.get_health_trend()

        predictive = self.predictive_analysis()

        services = []

        for service in self.monitored_services:

            result = self.get_service_status(service)

            services.append({

                "service": result["service"],

                "status": result["status"],

                "health": result["health"]
            })

        health_score = self.calculate_health_score()

        health = "HEALTHY"

        if health_score < 80:

            health = "WARNING"

        if health_score < 50:

            health = "CRITICAL"


        return {

            "health": health,

            "cpu": system_info["cpu"],

            "memory": system_info["memory_percent"],

            "disk": system_info["disk_percent"],

            "active_alerts": len(self.active_alerts),

            "resolved_alerts": len(self.resolved_alerts),

            "services": services,

            "health_score": health_score,

            "trend" : trend,

            "predictive" : predictive


        }
    
    def calculate_health_score(self):

        score = 100

        system_info = self.get_system_info()

        if system_info["cpu"] >= self.config["cpu_critical"]:

            score -= 20

        elif system_info["cpu"] >= self.config["cpu_warning"]:

            score -= 10

        if system_info["memory_percent"] >= self.config["memory_critical"]:

            score -= 20

        elif system_info["memory_percent"] >= self.config["memory_warning"]:

            score -= 10

        if system_info["disk_percent"] >= self.config["disk_critical"]:

            score -= 20

        elif system_info["disk_percent"] >= self.config["disk_warning"]:

            score -= 10

        score -= len(self.active_alerts) * 5

        for service in self.monitored_services:

            result = self.get_service_status(service)

            if result["status"] in ["INACTIVE" , "FAILED"]:

                score -= 15

        if score < 0:

            score = 0

        return score
    
    
    def get_health_trend(self):

        if len(self.health_history) < 2:

            return "STABLE"
        
        first = self.health_history[0]

        last = self.health_history[-1]

        if last > first:

            return "IMPROVING"
        
        elif last < first:

            return "DEGRADING"
        
        return "STABLE"
    
    
    def predictive_analysis(self):

        if len(self.health_history) < 5:

            return "STABLE"
        
        first = self.health_history[0]

        last = self.health_history[-1]

        difference = first - last

        if difference >= 30:

            return (

                "CRITICAL RISK: "

                "Infrastructure health rapidly degrading"
            )
        
        elif difference >=15:

            return (

                "WARNING: "

                "Infrastructure stability decreasing"
            )
        
        return "STABLE"
    

    def generate_report(self):

        dashboard = self.get_dashboard_data()

        resolved = self.get_resolved_stats()

        line = "=" * 60
        section = "-" * 60

        report = "\n" + line + "\n"
        report += "                 OPERATIONAL REPORT\n"
        report += line + "\n"

        report += "\nSYSTEM HEALTH\n"
        report += section + "\n"

        report += (
            f"Health Score        : "
            f"{dashboard['health_score']}/100 "
            f"({dashboard['health']})\n"
        )
        report += f"System Health       : {dashboard['health']}\n"
        report += f"Health Trend        : {dashboard['trend']}\n"
        report += f"Predictive Status   : {dashboard['predictive']}\n"

        report += "\nRESOURCE SUMMARY\n"
        report += section + "\n"

        report += f"CPU Usage           : {dashboard['cpu']}%\n"
        report += f"Memory Usage        : {dashboard['memory']}%\n"
        report += f"Disk Usage          : {dashboard['disk']}%\n"

        report += "\nINCIDENT SUMMARY\n"
        report += section + "\n"

        report += f"Active Alerts       : {dashboard['active_alerts']}\n"
        report += f"Resolved Incidents  : {dashboard['resolved_alerts']}\n"

        report += "\nRESOLVED INCIDENTS\n"
        report += section + "\n"

        report += f"CPU Incidents       : {resolved['cpu']}\n"
        report += f"Memory Incidents    : {resolved['memory']}\n"
        report += f"Disk Incidents      : {resolved['disk']}\n"

        report += "\nSERVICE RELIABILITY\n"
        report += section + "\n"

        report += self.service_reliability_report()

        report += "\n\nRECENT AUDIT EVENTS\n"
        report += section + "\n"

        report += self.get_recent_audit_events()

        report += "\n\nRECENT NOTIFICATIONS\n"
        report += section + "\n"

        report += self.get_recent_notifications()

        report += "\n\n" + line

        return report
    
    
    def save_report(self):

        report = self.generate_report()

        filename = datetime.now().strftime(

            "system_report_%Y%m%d_%H%M%S.txt"
        )

        with open(filename, "w") as file:

            file.write(report)

        return filename
    

    def save_audit_trail(self):

        with open(self.audit_file , "w") as file:

            json.dump(

                self.audit_trail,

                file,

                indent=4
            )


    def load_audit_trail(self):

        try:

            with open(self.audit_file, "r") as file:

                self.audit_trail = json.load(file)

        except (FileNotFoundError, json.JSONDecodeError):

            self.audit_trail = []

        return self.audit_trail


    def service_reliability_report(self):

        failure_counts = {}

        for event in self.audit_trail:

            if event["event"] == "SERVICE_FAILURE":

                service = event["target"]

                failure_counts[service] = failure_counts.get(service, 0) + 1

        if len(failure_counts) == 0:

            return "\nNo service failures recorded.\n"

        report = ""

        report += "\nSERVICE FAILURE SUMMARY\n"
        report += "-" * 60 + "\n"

        report += f"{'Service':<20}{'Failures':<15}{'Health'}\n"

        report += "-" * 60 + "\n"

        for service, count in failure_counts.items():

            if count <= 2:

                health = "GOOD"

            elif count <= 5:

                health = "FAIR"

            else:

                health = "POOR"

            report += f"{'Service':<20}{'Failures':<15}{'Reliability'}\n"

        most_unstable = max(
            failure_counts,
            key=failure_counts.get
        )

        report += f"\nMost Unstable Service : {most_unstable} ({failure_counts[most_unstable]} failures)\n"

        recovery = self.recovery_success_rate()

        report += "\n"
        report += "-" * 60
        report += "\nRECOVERY ANALYTICS\n"
        report += "-" * 60 + "\n"

        report += f"Total Recoveries      : {recovery['total']}\n"
        report += f"Successful Recoveries : {recovery['success']}\n"
        report += f"Failed Recoveries     : {recovery['failed']}\n"
        report += (
            f"Success Rate          : "
            f"{recovery['rate']}% "
            f"({recovery['success']}/{recovery['total']})\n"
        )
        report += f"Recovery Health       : {recovery['health']}\n"

        return report
    

    def recovery_success_rate(self):

        total_recoveries = 0
        successful_recoveries = 0

        for event in self.audit_trail:

            if event["event"] == "AUTO_RECOVERY":

                total_recoveries += 1

                if event["status"] == "SUCCESS":

                    successful_recoveries += 1

        if total_recoveries == 0:

            return {

                "total": 0,
                "success": 0,
                "failed": 0,
                "rate": 0,
                "health": "NO DATA"

            }

        failed = total_recoveries - successful_recoveries

        success_rate = round(

            (successful_recoveries / total_recoveries) * 100,

            2

        )

        if success_rate >= 90:

            health = "EXCELLENT"

        elif success_rate >= 75:

            health = "GOOD"

        elif success_rate >= 50:

            health = "FAIR"

        else:

            health = "POOR"

        return {

            "total": total_recoveries,
            "success": successful_recoveries,
            "failed": failed,
            "rate": success_rate,
            "health": health

        }

    def clear_audit_trail(self):

        if len(self.audit_trail) == 0:

            return {

                "result": "NO ACTION",
                "message": "AUDIT TRAIL IS ALREADY EMPTY"

            }

        self.audit_trail = []

        self.save_audit_trail()

        return {

            "result": "SUCCESS",
            "message": "AUDIT TRAIL CLEARED SUCCESSFULLY"

        }
    

    def load_notification(self):

        try:

            with open(self.notification_file , "r") as file:

                self.notifications = json.load(file)

        except (FileNotFoundError, json.JSONDecodeError):
            self.notifications = []

        return self.notifications


    def save_notifications(self):

        with open(self.notification_file , "w") as file:

            json.dump(

                self.notifications ,

                file ,

                indent=4
            )


    def send_notification(
            
            self,

            severity ,

            service,

            message,

            recovery_status
            
    ):
        
        notificaton = {

            "timestamp": time.strftime(

                "%Y-%m-%d %H:%M:%S"
            ),

            "severity": severity,

            "service": service,

            "message": message,

            "recovery_status": recovery_status
        }

        self.notifications.append(

            notificaton
        )

        self.save_notifications()


    def show_notifications(self):

        if len(self.notifications) == 0:

            return "No notifications recorded."

        line = "=" * 110
        section = "-" * 110

        lines = []

        lines.append(line)
        lines.append("NOTIFICATIONS".center(110))
        lines.append(line)
        lines.append("")

        lines.append(

            f"{'Timestamp':<25}"
            f"{'Severity':<12}"
            f"{'Service':<15}"
            f"{'Recovery':<15}"
            f"{'Message'}"

        )

        lines.append(section)

        recent_notifications = self.notifications[-20:]

        for notification in reversed(recent_notifications):

            lines.append(

                f"{notification['timestamp']:<25}"
                f"{notification['severity']:<12}"
                f"{notification['service']:<15}"
                f"{notification['recovery_status']:<15}"
                f"{notification['message']}"

            )

        lines.append("")
        lines.append(line)

        return "\n".join(lines)

    def get_recent_audit_events(self):

        recent_events = self.audit_trail[-5:]

        lines = []

        for event in recent_events:

            line = (

                event["timestamp"]

                + " | "

                + event["event"]

                + " | "

                + event["target"]

                + " | "

                + event["status"]

            )

            lines.append(line)

        return "\n".join(lines)
    

    def get_recent_notifications(self):

        recent_notifications = self.notifications[-5:]

        lines = []

        for event in recent_notifications:

            line = (

                event["timestamp"]

                + " | "

                + event["severity"]

                + " | "

                + event["service"]

                + " | "

                + event["recovery_status"]

                + " | "

                + event["message"]

            )

            lines.append(line)

        return "\n".join(lines)






    
















           



            
                    

            



       

      
        
    

        
    



          
        