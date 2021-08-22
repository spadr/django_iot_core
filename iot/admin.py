from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import ugettext_lazy as _
from iot.models import User, DeviceModel, NumberModel, ImageModel

# Register your models here.

admin.site.register(DeviceModel)
admin.site.register(NumberModel)
admin.site.register(ImageModel)



class MyUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'
  
  
class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email',)
  
  
class MyUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),

        (_('Personal info'), {'fields': ('first_name', 
                                         'last_name', 
                                         'alive_monitoring', 
                                         'send_message_to_email', 
                                         'line_token', 
                                         'send_message_to_line',
                                         'slack_token',
                                         'slack_channel',
                                         'send_message_to_slack',
                                         )}),
        
        (_('Permissions'), {'fields': ('is_active', 'function_level', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    form = MyUserChangeForm
    add_form = MyUserCreationForm
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
  
  
admin.site.register(User, MyUserAdmin)