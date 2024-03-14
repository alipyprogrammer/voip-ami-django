from django.contrib import admin
from .models import *

# Register your models here.



admin.site.register(Forward)


admin.site.register(ActiveChannels)
admin.site.register(Peers)
admin.site.register(Member)
admin.site.register(Callers)

admin.site.register(Peers5040)
admin.site.register(Member5040)
admin.site.register(Callers5040)
admin.site.register(ActiveChannels5040)

admin.site.register(PeersFellows)
admin.site.register(MemberFellows)
admin.site.register(CallersFellows)
admin.site.register(ActiveChannelsFellows)