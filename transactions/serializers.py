from rest_framework import serializers
from .models import Category, Transaction, RecurringTransaction


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "type",
            "color",
            "icon",
            "is_default",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]

    def validate(self, data):
        user = self.context["request"].user
        name = data.get("name")

        if Category.objects.filter(user=user, name=name).exists():
            raise serializers.ValidationError(
                "You already have a category with this name."
            )

        return data

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
    
class TransactionCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = [
            "id",
            "category",
            "type",
            "amount",
            "description",
            "transaction_date",
            "is_recurring",
        ]
        read_only_fields = ["id"]

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value

    def validate(self, data):
        user = self.context["request"].user
        category = data.get("category")

        if category and category.user != user:
            raise serializers.ValidationError(
                "You cannot use another user's category."
            )

        return data

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
    
class TransactionDetailSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Transaction
        fields = [
            "id",
            "type",
            "amount",
            "description",
            "transaction_date",
            "is_recurring",
            "category",
            "category_name",
            "created_at",
        ]
        
class RecurringTransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = RecurringTransaction
        fields = [
            "id",
            "category",
            "type",
            "amount",
            "frequency",
            "next_run_date",
            "is_active",
        ]
        read_only_fields = ["id"]

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)