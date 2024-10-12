from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet
from .models import Article, Tag, Scope

class RelationshipInlineFormset(BaseInlineFormSet):
    def clean(self):
        main_tags = 0
        for form in self.forms:
            data = form.cleaned_data

            if data.get('is_main') is True:
                main_tags += 1

        if main_tags == 1:
            return super().clean()
        elif main_tags > 1:
            raise ValidationError('Статья уже имеет основной тэг')
        elif main_tags == 0:
            raise ValidationError('Статья должна имееть основной тэг')
        


class RelationshipInline(admin.TabularInline):
    model = Scope
    formset = RelationshipInlineFormset

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [RelationshipInline]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    ...