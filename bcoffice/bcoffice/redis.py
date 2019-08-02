from django_redis.client import DefaultClient

def key_prefix(key, key_prefix, version):
    return key

class RedisCustomClient (DefaultClient):
    def encode(self, value):
        # """
        # Decode the given value.
        # """
        try:
            value = float(value)
        except (ValueError, TypeError):
            try:
                value = value.decode("utf-8")
                if value == 'N/A':
                    value = 0
            except:
                pass
            # try:
            #     value = self._compressor.decompress(value)
            # except CompressorError:
            #     # Handle little values, chosen to be not compressed
            #     pass
            # value = self._serializer.loads(value)

        return value
    def decode(self, value):
        # """
        # Decode the given value.
        # """
        try:
            value = float(value)
        except (ValueError, TypeError):
            try:
                value = value.decode("utf-8")
                if value == 'N/A':
                    value = 0
            except:
                pass
            # try:
            #     value = self._compressor.decompress(value)
            # except CompressorError:
            #     # Handle little values, chosen to be not compressed
            #     pass
            # value = self._serializer.loads(value)

        return value