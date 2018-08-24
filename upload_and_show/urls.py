"""upload_and_show URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.views.generic import TemplateView, RedirectView
from django.conf.urls import url
from django.contrib import admin

from show import Work as work_views
from show import expre as expr_views
from show import doExer as Do_Views
from show import views as show_views
from show import sets as sets_views
from show import gen as gens_views

from makeSet import views as Set_views
from upload import views as upload_views
from login import views as login_views

from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import staticfiles

urlpatterns = [
                  # 账户登录 注册 设置
                  url(r'^admin/', admin.site.urls),
                  url(r'^login/', login_views.login),
                  url(r'^logout/', login_views.logout),
                  url(r'^register/', login_views.nregister),
                  url(r'^set_sound/', login_views.viewSetSound),
                  url(r'^save_sound/', login_views.saveSoundSetting),
                  url(r'^get_sound/', login_views.getSound),

                  # 页面显示
                  url(r'^index/', show_views.index),
                  url(r'^show/', show_views.showAllEx),
                  url(r'^submit_arr/', show_views.submit_arr, name="submit_arr"),
                  url(r'^get_patient_account/', show_views.get_patient_account, name="get_patient_account"),
                  url(r'^save_patient_account/', show_views.save_patient_account, name="save_patient_account"),

                  url(r'^allGen/', gens_views.allGen, name="allGen"),
                  url(r'^gen_detail/', gens_views.gen_detail, name="gen_detail"),
                  url(r'^get_allGen/', gens_views.get_allGen, name="get_allGen"),
                  url(r'^chart/',gens_views.gen_chart,name="gen_chart"),
                  url(r'^word_fam/',gens_views.word_fam,name="word_fam"),

                  url(r'^get_allMyDoneSet/', work_views.get_allMyDoneSet, name="get_allMyDoneSet"),
                  url(r'^view_allMyToDoSet/', work_views.view_allMyToDoSet, name="view_allMyToDoSet"),
                  url(r'^get_allMyToDoSet/', work_views.get_allMyToDoSet, name="get_allMyToDoSet"),
                  url(r'^view_allMyDoneSet/', work_views.view_allMyDoneSet, name="view_allMyDoneSet"),

                  url(r'^upload_snap/', expr_views.upload_snap, name="upload_snap"),
                  url(r'^get_feeling/', expr_views.get_feeling, name="get_feeling"),

                  url(r'^set_detail/', sets_views.set_detail, name="set_detail"),
                  url(r'^setDisplay/', sets_views.setDisplay, name="setDisplay"),
                  url(r'^get_allSets/', sets_views.get_allSets, name="get_allSets"),
                  url(r'^setArrange/', sets_views.setArrange, name="setArrange"),

                  url(r'^get_nextToDo/', Do_Views.get_nextToDo, name="get_nextToDo"),
                  url(r'^error_answer/', Do_Views.error_answer, name="error_answer"),
                  url(r'^doEx/', Do_Views.doEx, name="doEx"),

                  # 操作：做题/分配/上传等
                  url(r'^upload/', upload_views.upload),
                  url(r'^get_specificGuide/', upload_views.get_specificGuide, name="get_specificGuide"),
                  url(r'^viewGuideline/', upload_views.viewGuideline, name="viewGuideline"),
                  url(r'^guide_upload/', upload_views.guide_upload),
                  url(r'^addGuideline/', upload_views.addGuideline, name="addGuideline"),
                  url(r'^delGuideline/', upload_views.delGuideline, name="delGuideline"),
                  url(r'^submit_GuideDel/', upload_views.submit_GuideDel, name="submit_GuideDel"),

                  url(r'^get_all/', Set_views.get_all_set, name="get_all"),
                  url(r'^submit_set/', Set_views.submit_set, name="submit_set"),
                  url(r'^makeSet/', Set_views.makeSet),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
