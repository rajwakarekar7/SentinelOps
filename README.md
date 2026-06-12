# SentinelOps

SentinelOps is a Python-based observability and infrastructure monitoring platform designed to monitor system health, analyze operational stability, track incidents, generate predictive alerts, and perform autonomous service recovery.

The project simulates real-world observability and DevOps concepts including telemetry collection, incident lifecycle management, health scoring, trend analysis, operational reporting, and self-healing infrastructure workflows.

SentinelOps was built as a practical infrastructure engineering project focused on Linux administration, RHCSA preparation, observability engineering, and infrastructure automation learning.


## Features

### Infrastructure Monitoring

* Real-time CPU monitoring
* Memory utilization tracking
* Disk usage monitoring
* Critical service monitoring

### Observability & Analytics

* Telemetry history tracking
* Average and peak resource analytics
* Infrastructure stability analysis
* Operational health scoring
* Health trend analysis

### Incident Management

* Active incident tracking
* Resolved incident history
* Structured incident lifecycle management
* Timestamp-based incident logging

### Autonomous Remediation

* Safe service recovery workflows
* Automatic service restart attempts
* Controlled recovery policies

### Predictive Intelligence

* Infrastructure degradation detection
* Predictive operational alerts
* Trend-based risk analysis

### Dashboard & Reporting

* Centralized observability dashboard
* Operational report generation
* Persistent report export system

### Persistence & Configuration

* JSON-based persistent storage
* Configuration-driven monitoring policies
* Persistent operational state tracking


## Architecture

SentinelOps is designed using a modular infrastructure-oriented architecture where different components handle monitoring, analytics, incident management, automation, and operational reporting responsibilities.

### Core Components

Components      Responsibility

brain.py	    Core monitoring, analytics, remediation, and observability engine

commands.py	    Command routing and CLI interaction layer

logger.py	    Operational logging system

memory.py	    Persistent memory management

nlp.py	        Natural language command processing

utils.py	    Shared utility functions

config.json 	Configuration-driven monitoring policies

alerts.json  	Persistent active incident storage

memory.json 	Persistent assistant memory storage


### Operational Flow

Telemetry Collection
↓
Infrastructure Analytics
↓
Incident Detection
↓
Health Scoring & Trend Analysis
↓
Predictive Risk Analysis
↓
Autonomous Remediation
↓
Dashboard & Reporting
↓
Persistent Operational Storage

### Monitoring Capabilities

* CPU usage monitoring
* Memory utilization tracking
* Disk usage monitoring
* Critical service monitoring
* Telemetry history collection
* Health trend analysis
* Predictive infrastructure alerting

### Reliability & Remediation

* Structured incident lifecycle tracking
* Active and resolved incident management
* Autonomous service recovery workflows
* Controlled remediation policies
* Persistent operational reporting


## Available Commands


/dashboard  	  Display centralized infrastructure dashboard

/telemetry  	  Show telemetry history for CPU, memory, and disk

/alerts     	  Display active operational incidents

/incidentstats	  Show active incident analytics

/resolvedstats	  Show resolved incident analytics

/average cpu	  Display average CPU utilization

/peak cpu	      Display peak CPU usage

/stability cpu	  Analyze CPU stability trends

/service nginx	  Check service operational status

/recover nginx	  Attempt autonomous service recovery

/report           Generate operational infrastructure report

/savereport	      Export persistent operational report

/kill process	  Terminate non-protected processes safely

/exit	          Shut down SentinelOps monitoring system


Example Usage:

>>> /dashboard
>>> /report
>>> /recover nginx
>>> /service apache
>>> /savereport


## Technologies Used

* Python
* psutil
* threading
* JSON persistence
* File handling
* CLI-based architecture
* Infrastructure monitoring concepts
* Observability engineering concepts
* Incident lifecycle management
* Predictive operational analytics

## Future Improvements

* Linux-native service management using `systemctl`
* Flask-based web dashboard
* Docker container monitoring
* Real-time log analysis
* Email alert integration
* Database-backed incident storage
* Multi-node infrastructure monitoring
* Grafana-style visualization interface
* SSH-based remote infrastructure monitoring
* Authentication and role-based access control

## Project Goals

SentinelOps was developed as a practical infrastructure engineering and observability learning project focused on:

* RHCSA preparation
* Linux administration
* DevOps foundations
* Infrastructure automation
* Observability engineering
* Reliability engineering concepts
* Backend systems thinking

## Author

Developed as a hands-on infrastructure monitoring and observability platform project for practical systems engineering learning and portfolio development.

