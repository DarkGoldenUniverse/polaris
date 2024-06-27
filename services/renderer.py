from rest_framework.renderers import JSONRenderer


class CustomJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        if renderer_context["response"].status_code >= 400:
            return super().render({"errors": data}, accepted_media_type, renderer_context)

        return super().render(data, accepted_media_type, renderer_context)
