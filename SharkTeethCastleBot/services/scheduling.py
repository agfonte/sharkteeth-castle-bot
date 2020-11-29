import schedule, time, threading


class SchedulingService:
    __instance = None

    @staticmethod
    def get_instance():
        """ Static access method. """
        if SchedulingService.__instance is None:
            SchedulingService()
        return SchedulingService.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if SchedulingService.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            SchedulingService.__instance = self
            self.set_tasks()

    def set_tasks(self):
        schedule.every(1).seconds.do(self.run_threaded, self.task)

    def start(self):
        while True:
            schedule.run_pending()
            time.sleep(1)

    def run_threaded(self, job_func):
        job_thread = threading.Thread(target=job_func)
        job_thread.start()

    def task(self):
        print("Task")
