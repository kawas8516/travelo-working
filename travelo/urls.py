"""
URL configuration for travelo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
"""
URL configuration for travelo project.
"""

from django.contrib import admin
from django.urls import path, include
from .views import chatbot_response  # Import your view here


urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', chatbot_response, name='chatbot_response'),  # Load chatbot directly at the root
    path('bookings/', include('bookings.urls')),  # Adjust to your bookings app
]



