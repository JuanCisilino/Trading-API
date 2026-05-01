# trading/views.py

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Trade
from .serializers import TradeSerializer
from .services.iq import IQService


@api_view(['GET'])
def balance_view(request):
    try:
        iq = IQService(mode="PRACTICE")

        # traer ambos balances
        iq.api.change_balance("PRACTICE")
        practice_balance = iq.api.get_balance()

        iq.api.change_balance("REAL")
        real_balance = iq.api.get_balance()

        return Response({
            "practice_balance": practice_balance,
            "real_balance": real_balance
        })

    except Exception as e:
        return Response({"error": str(e)}, status=500)


# 🔥 Ejecutar trade
@api_view(['POST'])
def execute_trade_view(request):
    try:
        asset = request.data.get("asset", "EURUSD")
        direction = request.data.get("direction", "call")
        amount = float(request.data.get("amount", 10))
        mode = request.data.get("mode", "PRACTICE")

        trade = Trade.objects.create(
            asset=asset,
            direction=direction,
            amount=amount,
            status="pending",
            mode=mode
        )

        iq = IQService(mode=mode)

        result = iq.execute_trade(asset, direction, amount)

        trade.result = result["result"]
        trade.profit = result["profit"]
        trade.status = "executed"
        trade.save()

        return Response({
            **TradeSerializer(trade).data,
            "mode": mode
        })

    except Exception as e:
        return Response({"error": str(e)}, status=500)


# 📊 Stats + BALANCE REAL
@api_view(['GET'])
def stats_view(request):
    try:
        mode = request.GET.get("mode", "PRACTICE")

        iq = IQService(mode=mode)
        balance = iq.get_balance()

        trades = Trade.objects.filter(mode=mode)

        return Response({
            "trades": trades.count(),
            "wins": trades.filter(result="win").count(),
            "loss": trades.filter(result="loss").count(),
            "errors": trades.filter(result="error").count(),
            "profit": sum(t.profit for t in trades),
            "balance": balance,
            "mode": mode
        })

    except Exception as e:
        return Response({"error": str(e)}, status=500)

@api_view(['GET'])
def trades_list_view(request):
    mode = request.GET.get("mode", "PRACTICE")
    trades = Trade.objects.filter(mode=mode).order_by('-created_at')[:20]
    return Response(TradeSerializer(trades, many=True).data)