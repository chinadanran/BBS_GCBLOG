from copy import deepcopy

from bs4 import BeautifulSoup
from django import forms

from bbstest1.apps.article.models import Article


class CreateArticleForm(forms.ModelForm):

    desc = forms.CharField(widget=forms.Textarea, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        blog = self.initial.get('user').blog
        categories = blog.category_set.all()
        tags = blog.tag_set.all()
        self.fields['category'].choices = [(category.id, category.title) for category in categories]
        self.fields['tags'].choices = [(tag.id, tag.title) for tag in tags]
        if self.instance:
            self.initial['desc'] = self.instance.articledetail.content
            self.fields['category'].initial = self.instance.category
            self.fields['tags'].initial = self.instance.tags.all()

    def clean_desc(self):
        desc = self.cleaned_data.get('desc')
        soup = BeautifulSoup(desc, "html.parser")
        script_list = soup.select("script")
        for i in script_list:
            i.decompose()

        desc = soup.text
        self.cleaned_data['content'] = desc
        return desc[0:150]

    def save(self, commit=True):
        user = self.initial.get('user')
        self.instance.user = user
        return super().save(commit=commit)

    class Meta:
        model = Article
        fields = ['title', 'desc', 'category', 'tags']


