import notificator


class ConsoleNotificator(notificator.Notificator):
    def notify(self, cameras):
        print('DANGER!', cameras)
