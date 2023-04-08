from .models import EventImage


def get_language(self):
    lang = self.context["request"].headers.get("Accept-Language")

    if lang == "ru":
        return "ru"
    return "ky"


def switch_language(lang):
    if lang == "ky":
        return "ru"
    elif lang == "ru":
        return "ky"


def upload_images(images, event):
    for image in images:
        EventImage.objects.create(image, event=event)
