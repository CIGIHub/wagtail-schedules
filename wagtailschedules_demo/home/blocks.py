
from wagtail.core.blocks import (CharBlock, ChoiceBlock, RichTextBlock,
                                 StreamBlock, StructBlock, TextBlock)
from wagtail.images.blocks import ImageChooserBlock

class ContentBlocks(StreamBlock):
    title = CharBlock()
    image = ImageChooserBlock(template='blocks/image.html')
