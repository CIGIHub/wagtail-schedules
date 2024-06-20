from django.db import models
from wagtail.admin.edit_handlers import (FieldPanel, FieldRowPanel,
                                         InlinePanel, MultiFieldPanel,
                                         PageChooserPanel, StreamFieldPanel)
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Page

from .blocks import ContentBlocks
from wagtail.images.models import Image
from wagtail.images.edit_handlers import ImageChooserPanel

class HomePage(Page):
    header_image = models.ForeignKey(
        Image,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    body = StreamField(ContentBlocks())

    content_panels = Page.content_panels + [
        ImageChooserPanel('header_image'),
        StreamFieldPanel('body'),
    ]
