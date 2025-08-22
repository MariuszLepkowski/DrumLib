from django import template
import re

register = template.Library()


@register.filter(name='split_paragraphs')
def split_paragraphs(value, num_sentences=3):
    """
    Splits the text into paragraphs every `num_sentences` sentences.
    """
    sentences = re.split(r'(?<=[.!?]) +', value)
    paragraphs = [' '.join(sentences[i:i + num_sentences]) for i in range(0, len(sentences), num_sentences)]
    return '</p><p>'.join(paragraphs)
