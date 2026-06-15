from memory import load_memory , save_memory
from logger import log
import shutil
import datetime
import psutil
import time
import json
import os
import subprocess

class Brain:

    def __init__(self):

        self.memory = load_memory()

        self.history = []

        self.monitoring = False

        self.cpu_history = []

        self.memory_history = []

        self.disk_history = []

        self.last_cpu_alert = 0

        self.last_memory_alert = 0

        self.last_disk_alert = 0

        self.active_alerts = self.load_alerts()

        self.config = self.load_config()

        self.resolved_alerts = []

        self.recoverable_services ={

            "nginx" ,

            "apache" ,

            "mysql"

        }

        self.monitored_services =[

            "nginx" ,

            "mysql" ,

            "apache"
        ]

        self.health_histroy = []
         


    def learn(self, word ,meaning , category):

        self.memory[word]= {

            "meaning": meaning ,
            "category": category
        }

        save_memory(self.memory)

        log("Learned "+ word)


    def answer(self ,word):

        if word in self.memory:

            message = word.capitalize()+ " is " + self.memory[word]["meaning"]

            self.history.append("question: " + word)
            self.history.append("Answer: " + message)

            log("Asked "+ word)

            return message
        
        return "i don't Know"
    
    
    def search(self ,text):

        results = []

        for key in self.memory:

            meaning = self.memory[key]["meaning"]

            if text in key or text in meaning:

                results.append(key + "=" + meaning)
            
        if len(results) == 0:

            return "No match found"
        
        return "\n".join(results)

    
    def show_memory(self):

        for key in self.memory:

            print(key + "=" + self.memory[key]["meaning"])


    def show_history(self):

        for item in self.history:

            print(item)


    def delete(self , word):

        if word in self.memory:

            del self.memory[word]

            save_memory(self.memory)

            log("Deleted "+ word)

            return "Deleted Successfully"
        
        return " word not found"
    

    def show_category(self , category):

        results= []

        for key in self.memory:

            current_category= self.memory[key]["category"]

            if current_category == category:

               meaning = self.memory[key]["meaning"]

               results.append(key + "=" + meaning)

        if len(results) == 0:

            return " No words found"
    
        return "\n".join(results)
    

    def stats(self):

        total = len(self.memory)

        category_count = {}

        for key in self.memory:

            category = self.memory[key]["category"]

            if category in category_count:

                category_count[category] += 1

            else:

                category_count[category] = 1

        result = "Total Memeories: " + str(total) + "\n\n"

        for category in category_count:

            count = category_count[category]

            result += category + ":" +str(count) + "\n"

        return result
    

    def update(self , word , meaning , category):

        if word in self.memory:

            self.memory[word]["meaning"] = meaning

            self.memory[word]["category"] = category

            save_memory(self.memory)

            log("updated " + word)

            return word + " updated"
        
        return "Word not found"
    
    
    def backup(self):

        now = datetime.datetime.now()

        timestamp = now.strftime("%Y_%m_%d_%H_%M_%S")

        backup_name = "backup_" + timestamp + ".json"

        shutil.copy("memory.json" , backup_name)

        log("Backup created: " + backup_name)

        return "Backup created " + backup_name
    
    
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

            except:
              
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

            except:

                continue

        processes.sort(key=lambda x:x[1] , reverse=True)

        return{

            "processes":processes[:5],

            "warning": warning
        }
    

    def check_service(self , service_name):

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

        except:

            service_status = "unknow"
            

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
                        "status": "RUNNING",
                        "pid": process.pid,
                        "cpu": cpu,
                        "memory": memory,
                        "health": health,
                        "uptime": uptime
                    }
                 
            except:
                continue

        return{
           "service": service_name,
            "status": "NOT RUNNING"
        }
    

    def check_critical_services(self):

        services = [

            "sshd" ,

            "docker" ,

            "nginx" ,

            "mysql" ,

            "httpd"

        ]

        results = []

        for service in services:

            result = self.check_service(service)

            results.append(result)

        return results
    
    
    def kill_service(self , service_name):

        service_name = service_name.lower()

        protected =[

            "system",

            "explorer" ,

            "wininit" ,

            "csrss",

            "python"
        ]

        for process in psutil.process_iter():

            try:

                name = process.name().lower()

                if service_name in name:

                    for item in protected:

                        if item in name:

                            log("Blocked protected process: " + name)

                            return{

                                "service": service_name,
                                "status": "PROTECTED PROCESS"
                            }
                             
                    process.kill()

                    log("Killed process: " + name)

                    return{

                        "service" : service_name,
                        "status" : "TERMINATED"
                    }
            except:

                continue

        log("Processes not found: " + service_name)

        return{

            "service" : service_name,
            "status" : "NOT FOUND"
        }
    
    def start_background_monitor(self):

        self.monitoring = True

        while self.monitoring:

            system_info = self.get_system_info()

            health_score = self.calculate_health_score()

            self.health_histroy.append(health_score)

            if len(self.health_histroy) > 100:

                self.health_histroy.pop(0)

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

                         "message": (

                            "[WARNING] CPU USAGE: "

                            +str(cpu)

                            + "%"
                        )
                    }

                    self.active_alert.append(alert)

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

                         "message": (

                            "[CRITICAL] MEMORY USAGE: "

                            +str(memory)

                            + "%"
                        )
                    }

                    self.active_alert.append(alert)

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

                         "message": (

                            "[WARNING] MEMORY USAGE: "

                            +str(memory)

                            + "%"
                        )
                    }

                    self.active_alert.append(alert)

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

                        "message": (

                            "[CRITICAL] DISK USAGE: "

                            +str(disk)

                            + "%"
                        )
                    }

                    self.active_alert.append(alert)

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

                        "message": (

                            "[WARNING] DISK USAGE: "

                            +str(disk)

                            + "%"
                        )
                    }

                    self.active_alert.append(alert)

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


            time.sleep(30)

    
    def stop_monitor(self):

        self.monitoring = False

        log("Background monitor stooped")


    def get_average_cpu(self):

        if len(self.cpu_history) == 0:

            return 0
        
        total = sum(self.cpu_history)

        average = total / len(self.cpu_history)

        average = round(average, 2)

        return average
    
    
    def get_peak_cpu(self):

        if len(self.cpu_history) == 0:

            return 0
        
        peak = max(self.cpu_history)

        peak = round(peak, 2 )

        return peak
    
    
    def get_cpu_stability(self):

        if len(self.cpu_history) == 0:

            return "NO DATA"
        
        average = self.get_average_cpu()

        diffrences = []

        for value in self.cpu_history:

            diffrence = abs(value - average)

            diffrences.append(diffrence)

        instability = sum(diffrences) / len(diffrences)

        if instability < 10:

            return "STABLE"
        
        elif instability < 30:

            return "MODERATE"
        
        else:

            return "UNSTABLE"
        

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

                    "Monitor RAM usage "
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

                alert["duration"] = "resolved"

                self.resolved_alerts.append(alert)

        self.active_alerts = updated_alerts

        self.save_alerts()


    def load_config(self):

        file = open("config.json" , "r")

        config = json.load(file)

        file.close()

        return config
    

    def save_alerts(self):

        file = open("alerts.json" , "w")

        json.dump(self.active_alerts , file)

        file.close()

    
    def load_alerts(self):

        file = open("alerts.json" , "r")

        alters = json.load(file)

        file.close()

        return alters


    def get_incident_stats(self):

        cpu_count = 0

        memory_count = 0

        disk_count = 0

        critical_count = 0

        warning_count =  0

        for alerts in self.active_alerts:

            if alerts["resource"] == "cpu":

                cpu_count += 1

            elif alerts["resource"] == "memory":

                memory_count += 1

            elif alerts["resource"] == "disk":

                disk_count += 1

            elif alerts["severity"] == "critical":

                critical_count += 1

            elif alerts["severity"] == "warning":

                warning_count += 1

        return {

            "cpu" : cpu_count,

            "memory" : memory_count,

            "disk" : disk_count,

            "critical" : critical_count ,

            "warning" : warning_count
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

            "total": len(self.resolved_alerts),

            "cpu": cpu_count,

            "memory": memory_count,

            "disk": disk_count,

            "critical": critical_count,

            "warning": warning_count

        }
    

    def restart_service(self , service_name):

        if service_name not in self.recoverable_services:

            return "SERVICE NOT APPROVED FOR AUTO-RECOVERY"
        
        os.system(

            "net start"

            + service_name
        )

        result =self.check_service(service_name)

        if result["status"] == "RUNNING":

            return "SERVICE RECOVERRD SUCCESSFULLY"
        
        return "SERVICE RECOVEREY FAILED"
    
    
    def monitor_services(self):

        for service in self.monitored_services:

            result = self.check_service(service)

            if result["status"] == "NOT RUNNING":

                log(

                    "SERVICE FAILURE"

                    + service

                    + "is not running"
                )

                recovery_result = self.restart_service(service)

                log(

                    "[AUTO RECOVERY]"

                    + service

                    + "->"

                    + recovery_result
                )


    def get_dashboard_data(self):

        system_info =self.get_system_info()

        trend = self.get_health_trend()

        predictive = self.predictive_analysis()

        services = []

        for service in self.monitored_services:

            result = self.check_service(service)

            services.append({

                "name" : service ,

                "status" : result["status"]
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

            result = self.check_service(service)

            if result["status"] == "NOT RUNNING":

                score -= 15

        if score < 0:

            score = 0

        return score
    
    
    def get_health_trend(self):

        if len(self.health_histroy) < 2:

            return "STABLE"
        
        first = self.health_histroy[0]

        last = self.health_histroy[-1]

        if last > first:

            return "IMPROVING"
        
        elif last < first:

            return "DEGRADING"
        
        return "STABLE"
    
    
    def predictive_analysis(self):

        if len(self.health_histroy) < 5:

            return "STABLE"
        
        first = self.health_histroy[0]

        last = self.health_histroy[-1]

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

        report = "\n[SYSTEM REPORT]\n\n"

        report += (

            "HEALTH SCORE: "

            + str(dashboard["health_score"])

            + "/100\n"
        )

        report += (

            "HEALTH TREND: "

            + dashboard["trend"]

            + "\n"
        )

        report += (

            "PREDICTIVE STATUS: "

            + dashboard["predictive"]

            + "\n\n"
            
        )

        report += (

            "ACTIVE ALERTS: "

            + str(dashboard["active_alerts"])

            + "\n"

        )

        report += (

            "RESOLVED INCIDENTS: "

            + str(dashboard["resolved_alerts"])

            + "\n\n"

        )

        report += (

            "CPU INCIDENTS: "

            + str(resolved["cpu"])

            + "\n"

        )

        report += (

            "MEMORY INCIDENTS: "

            + str(resolved["memory"])

            + "\n"

        )

        report += (

            "DISK INCIDENTS: "

            + str(resolved["disk"])

            + "\n"

        )

        return report
    
    
    def save_report(self):

        report = self.generate_report()

        filename = "system_report.txt"

        file = open(filename , "w")

        file.write(report)

        file.close()

        return filename
    
















           



            
                    

            



       

      
        
    

        
    



          
        