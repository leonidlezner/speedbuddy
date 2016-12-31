import notificator


class RgbLedNotificator(notificator.Notificator):
    def notify(self, cameras):
        print('DANGER! color...')
