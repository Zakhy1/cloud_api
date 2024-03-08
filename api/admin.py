from django.contrib import admin

from api.models import Access, File, User

admin.site.register(File)
admin.site.register(User)
admin.site.register(Access)
