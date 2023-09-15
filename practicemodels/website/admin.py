from django.contrib import admin,messages
from website.models import Book,Author
from django import forms
from django.urls import path
from django.http import HttpResponseRedirect





def make_published(modeladmin, request, queryset):
    queryset.update(is_available='True')

def make_unpublished(modeladmin, request, queryset):
    queryset.update(is_available='False')

def show_availabe(modeladmin, request, queryset):
    queryset.filter(is_available='True')


def delete_selected(modeladmin, request, queryset):
    queryset.delete()

class CustomFieldFilter(admin.SimpleListFilter):
    title = 'Custom Field' 
    parameter_name = 'title'  

    def lookups(self, request, model_admin):
        return (
            ('value1', 'Programming Fundaments'),
            ('value2', 'Object Oriented Programming'),
            ('value3', 'Data Structures and Algorithms'),
        )

    def queryset(self, request, queryset):
        # apply the filter to the queryset
        if self.value() == 'value1':
            return queryset.filter(title='pf')
        if self.value() == 'value2':
            return queryset.filter(title='oop')
        if self.value() == 'value3':
            return queryset.filter(title='dsa')

# class YourModelForm(forms.ModelForm):
#     class Meta:
#         model = Book
#         fields = ('added_at', 'publication_date', 'publication_year', 'title') 

class YourModelAdmin(admin.ModelAdmin):

    def custom_list_display(self,obj):
        return f"{obj.title} {obj.publication_year}"

    list_display = ['title', 'publication_year','custom_list_display'] 
    search_fields = ('title',)
    # list_filter = ('title', 'publication_date')
    list_filter = (CustomFieldFilter,)
    date_hierarchy = 'added_at'
    actions = [make_published,show_availabe,make_unpublished, delete_selected]

    # Adding a custom button on admin panel to change the availability to true
    change_list_template = 'admin/Book/change_list.html'

    def changeAvailability(self,request):
        Book.objects.update(is_available=True)
        messages.add_message(request, messages.SUCCESS, 'All books are set to avaibale!')
        return HttpResponseRedirect("../")


    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path (
                "change-avalibity/",
                self.changeAvailability,
                name="change-availability",
            ),
        ]
        return  custom_urls + urls
        


admin.site.register(Book,YourModelAdmin)
admin.site.register(Author)
