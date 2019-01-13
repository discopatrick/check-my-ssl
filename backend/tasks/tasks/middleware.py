import dramatiq


class SentryMiddleware(dramatiq.Middleware):
    def __init__(self, capture_exception):
        self.capture_exception = capture_exception

    def after_process_message(self, broker, message, *, result=None, exception=None):
        if exception is not None:
            self.capture_exception()
