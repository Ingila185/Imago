from rest_framework import serializers

class MediaSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField()
    MEDIA_ID = serializers.CharField()
    DB = serializers.CharField()
    # Add other relevant fields from your Elasticsearch documents here

    def get_thumbnail_url(self, instance):
        base_url = "https://www.imago-images.de"
        media_id = instance.get('MEDIA_ID', '')  # Get MEDIA_ID directly
        db_value = instance.get('DB', '')        # Get DB directly
        return f"{base_url}/bild/{db_value}/{media_id}"

    thumbnail_url = serializers.SerializerMethodField()


class ImagoSerializer(serializers.Serializer):
    bildnummer = serializers.CharField()
    datum = serializers.DateTimeField()
    suchtext = serializers.CharField()
    fotografen = serializers.CharField()
    hoehe = serializers.CharField()
    breite = serializers.CharField()
    db = serializers.CharField()

class ImagoHitSerializer(serializers.Serializer):
    _index = serializers.CharField()
    _id = serializers.CharField()
    _score = serializers.FloatField()
    _source = ImagoSerializer()

class ImagoHitsListSerializer(serializers.Serializer):
    value = serializers.IntegerField()
    relation = serializers.CharField()

class ImagoHitsSerializer(serializers.Serializer):
    total = ImagoHitsListSerializer()
    max_score = serializers.FloatField()
    hits = ImagoHitSerializer(many=True)

class ImagoSearchResponseSerializer(serializers.Serializer):
    took = serializers.IntegerField()
    timed_out = serializers.BooleanField()
    _shards = serializers.DictField()
    hits = ImagoHitsSerializer()