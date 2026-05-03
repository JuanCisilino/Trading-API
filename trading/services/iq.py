# trading/services/iq.py

from iqoptionapi.stable_api import IQ_Option
from django.conf import settings

class IQService:
    def __init__(self, mode="PRACTICE"):
        self.api = IQ_Option(settings.IQ_EMAIL, settings.IQ_PASSWORD)

        connected, reason = self.api.connect()
        if not connected:
            raise Exception(f"Error conectando a IQ Option: {reason}")

        self.api.change_balance(mode)  # PRACTICE o REAL

    def get_balance(self):
        return self.api.get_balance()
    
    def execute_trade(self, asset, direction, amount):
            status, trade_id = self.api.buy(amount, asset, direction, 1)

            if not status:
                    return {"result": "error", "profit": 0, "msg": "buy failed"}

            result = self.api.check_win_v4(trade_id)

        # 🔥 FIX CLAVE
            if isinstance(result, tuple):
                    result = result[0]

            if result is None:
                    return {"result": "error", "profit": 0}

            if result > 0:
                    return {"result": "win", "profit": result}
            elif result < 0:
                    return {"result": "loss", "profit": result}
            else:
                    return {"result": "draw", "profit": 0}