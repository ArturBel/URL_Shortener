from apscheduler.schedulers.background import BackgroundScheduler
import atexit
from api.models import Urls
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os


load_dotenv()
scheduler = BackgroundScheduler()



# setting up scheduler for periodic deletion of unused urls
def periodic_deletion(app, db):
    with app.app_context():
        # time range
        cutoff = datetime.now() - timedelta(hours=os.getenv("REFRESH_HOURS"))
        
        # delete all urls not accessed withing timeframe
        urls = Urls.query.filter(Urls.last_access < cutoff).yield_per(100)

        for url in urls:
            db.session.delete(url)

        db.session.commit()


def init_scheduler(app, db):
    # setting up periodic deletion
    scheduler.add_job(
        func=lambda: periodic_deletion(app, db),
        trigger="interval",
        seconds=30,
    )

    # scheduler behaviour: starts and ends with app
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())
