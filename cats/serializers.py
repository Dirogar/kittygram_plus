import datetime
from rest_framework import serializers
import webcolors
from .models import Cat, Owner, Achievement, AchievementCat, CHOICES


class Hex2NameColor(serializers.Field):
    """Преобразует цвет в формате hex в человекочитаемый"""

    def to_representation(self, value):
        """Возращает текущий цвет при чтении"""
        return value

    def to_internal_value(self, data):
        """
        Возвращает интерпретацию цвета из hex формата
        """
        try:
            data = webcolors.hex_to_name(data)
        except ValueError:
            raise serializers.ValidationError('Для этого цвета нет имени')
        return data


class AchievementSerializer(serializers.ModelSerializer):
    """Класс достижений животного"""
    # Переименуем название говнополя
    achievement_name = serializers.CharField(source='name')
    qwe = serializers.DateField

    class Meta:
        model = Achievement
        fields = ('id', 'achievement_name')


class CatSerializer(serializers.ModelSerializer):
    achievements = AchievementSerializer(many=True, required=False)
    age = serializers.SerializerMethodField()
    #color = Hex2NameColor() # Хуй знает почему не используем
    color = serializers.ChoiceField(choices=CHOICES)

    class Meta:
        model = Cat
        fields = ('id', 'name', 'color', 'birth_year', 'owner', 'achievements',
                  'age')

    def create(self, validated_data):
        if 'achievements' not in self.initial_data:
            cat = Cat.objects.create(**validated_data)
            return cat
        achievements = validated_data.pop('achievements')

        cat = Cat.objects.create(**validated_data)

        for achievement in achievements:
            current_achievement, status = Achievement.objects.get_or_create(
                **achievement
            )
            AchievementCat.objects.create(
                achievement=current_achievement, cat=cat
            )
        return cat

    def get_age(self, obj):
        """
        Получение возраста животного. Хорошей практикой будет не
        перегружать такие методы

        :obf: Объект - кот
        :return: Возраст животного
        """
        return datetime.datetime.now().year - obj.birth_year


class OwnerSerializer(serializers.ModelSerializer):
    cats = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Owner
        fields = ('first_name', 'last_name', 'cats')
