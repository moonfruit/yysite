# -*- coding: utf-8 -*-
from django.contrib.admin import ModelAdmin, site
from django.forms import ModelForm, Textarea

from .models import Feed, FeedItem


class FeedForm(ModelForm):
    class Meta:
        model = Feed
        exclude = ()
        widgets = {
            'fetcher': Textarea({'cols': 80, 'rows': 1}),
            'description': Textarea({'cols': 80})
        }


class FeedAdmin(ModelAdmin):
    form = FeedForm
    list_display = ('name', 'title', 'fetcher', 'link', 'description')
    search_fields = ('name', 'title')
    actions = ['refresh']

    def refresh(self, request, queryset):
        for feed in queryset:
            count = feed.fetch()
            self.message_user(request, "Refresh feed [%s] with [%d]" % (feed, count))
    refresh.short_description = "Refresh the selected feeds"


class FeedItemAdmin(ModelAdmin):
    readonly_fields = ('feed', 'item_id', 'title', 'publish_date', 'link', 'description')
    list_display = ('feed', 'item_id', 'title', 'publish_date', 'link')
    list_display_links = ('item_id',)
    search_fields = ('feed__name', 'feed__title', 'item_id', 'title')

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        extra_context['show_save'] = False
        return super().changeform_view(request, object_id, extra_context=extra_context)

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


site.register(Feed, FeedAdmin)
site.register(FeedItem, FeedItemAdmin)
