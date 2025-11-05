from rest_framework import serializers

from core.models import (DailyChange, DividendPayment, DividendReinvestment,
                         History, Investment, Purchase, Sale)


class InvestmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investment
        fields = "__all__"


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = "__all__"


class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = "__all__"


class DividendReinvestmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DividendReinvestment
        fields = "__all__"


class DividendPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DividendPayment
        fields = "__all__"


class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = "__all__"


class DailyChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyChange
        fields = "__all__"
