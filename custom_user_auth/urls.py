from django.conf.urls import url,patterns,include

urlpatterns = patterns('',
	url(r'^$','custom_user_auth.views.index',name='home'),
	)