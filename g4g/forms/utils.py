from .models import EventImage


def upload_images(images, event):
    for image in images:
        EventImage.objects.create(image=image, event=event)
