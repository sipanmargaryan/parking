from rest_framework import serializers

import core.models

__all__ = (
    'CountrySerializer'
)


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = core.models.Country
        fields = '__all__'
