from apscheduler.schedulers.background import BackgroundScheduler
from drones.views import createAuditLogWithScheduler

def startAuditLogWithScheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(createAuditLogWithScheduler(),'interval',minutes=1,id='batteryLogger',replace_existing=True)
    scheduler.start()



