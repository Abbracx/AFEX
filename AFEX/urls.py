from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from chat import views as chat_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('chats/', include("chat.urls")),
    path('signup', chat_views.signup, name="signup"),
    path('login', auth_view.LoginView.as_view(template_name='chat/signIn.html'), name="signIn"),
   path('logout', auth_view.LogoutView.as_view(template_name='chat/signout.html'), name="signout")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
