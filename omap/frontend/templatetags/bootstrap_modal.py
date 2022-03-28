import re

from django import template
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from tag_parser.basetags import BaseNode


def camel_to_snake(s):
    return re.sub(r"(?<!^)(?=[A-Z])", "-", s).lower()


register = template.Library()


@register.tag("modalform")
class ModalFormNode(BaseNode):
    max_args = None
    allowed_kwargs = None
    end_tag_name = "endmodalform"

    def render_tag(self, context, *tag_args, **tag_kwargs):
        # Render contents inside
        return render_to_string(
            "omap/frontend/modalform.html",
            context={"content": self.nodelist.render(context)},
        )


@register.simple_tag()
def open_modal(url=None, title=None):
    url_mark = ""
    if url is not None:
        url_mark = f' data-url="{url}"'
    data_title = ""
    if title is not None:
        data_title = f' data-title="{title}"'
    return mark_safe(f'data-action="click->modalform#showForm"{url_mark}{data_title}')


def get_data_attributes(tag_kwargs):
    data_attributes_dict = {
        camel_to_snake(k): tag_kwargs[k]
        for k in tag_kwargs.keys()
        if re.match("data[A-Z]", k)
    }
    data_attributes = " ".join([f'{k}="{v}"' for k, v in data_attributes_dict.items()])
    return data_attributes


@register.tag("modal")
class ModalNode(BaseNode):
    max_args = None
    allowed_kwargs = None  # ('title', 'modal_id', 'turbo', 'form')
    end_tag_name = "endmodal"

    def render_tag(self, context, *tag_args, **tag_kwargs):
        # Render contents inside
        modal_id = tag_kwargs.get("modal_id", "modal")
        title = tag_kwargs.get("title", "")

        big = tag_kwargs.get("big", False)

        # Fetch all data attributes
        data_attributes = get_data_attributes(tag_kwargs)

        return render_to_string(
            "omap/frontend/modal.html",
            context={
                "modal_id": modal_id,
                "data_attributes": data_attributes,
                "title": title,
                "body": self.nodelist.render(context),
                "big": big,
            },
        )
