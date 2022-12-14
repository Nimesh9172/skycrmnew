from app1 import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
        path('test',views.test,name="test"),
        path('b',views.base3,name="base3"),
        
		path("testworking",views.testworking,name="testworking"),
        path('tlcmsresponse',views.tlcmsresponse,name="tlcmsresponse"),
        path('display/',views.display,name="display"),
        path('teamoverall/',views.teamoverall,name="teamoverall"),
        path('',views.home,name="home"),
        path('login/', views.loginuser, name='login'),
        path('logout',views.logoutuser,name="logout"),
        path("qsdash",views.qsdash,name="qsdash"),
        path('dashboard/', views.dashboard, name='dashboard'),
        path('cms/<int:id>/', views.cms, name='cms'),
        path('tlcms/<int:id>/', views.tlcms, name='tlcms'),
        path('incomingcms/', views.incomingcms, name='incoming'),
        path('noncontacted/', views.noncontacted, name='noncontacted'),
        path('listid',views.listid,name='listid'),

        path('notificationCount',views.notificationCount,name="notificationCount"),
        path('misscallednotiCount',views.misscallednotiCount,name="misscallednotiCount"),

        path('nonattempted/',views.nonattempted,name='nonattempted'),
        path('dialstat',views.dialstatus,name="dialstat"),
        path('mob',views.mobno,name="mobilenopopup"),
		path('sms',views.sms,name="sms"),
		path("exportsms",views.exportsms,name="exportsms"),

        path("dailer",views.dialer,name="un"),
        path('search/', views.search, name='s'),
        path('reminder/', views.Reminder, name='r'),
        path('ots/', views.ots, name='o'),
        path('recoverystatus/', views.recovery, name='rs'),
        path('sendfe/', views.SendtoFE, name='sd'),
        path("additional/",views.additional,name='additional'),
        path("dataupload/",views.dataupload,name="dataupload"),
        path('upload',views.upload,name="upload"),
        path("datastatus/",views.datastatus,name="datastatus"),
        path("dataexport/",views.dataexport,name="dataexport"),
        path("connecttocustomer",views.connect),
        path('sf/<int:id>',views.sendfetagging),
        
        
        path("dashtl",views.dashtl,name="dashtl"),
        path("dashtlajax",views.dashtlajax,name="dashtlajax"),
        path("ptp",views.ptp,name="ptp"),
        path("ptpcount",views.ptpcount,name="ptpcount"),
        path("paidcount",views.paidcount,name="paidcount"),
        path("dashtlots",views.dashtlots,name="dashtlots"),


        path("missedcall",views.missedcall,name="missedcall"),
        path("unknown",views.missunknown,name="unknown"),

        path('qualityscore',views.qualityscore,name="qualityscore"),
        path('scoredata',views.scoredata,name='scoredata'),
        path('score/<int:rec>',views.score,name="score"),
        path("qualityexport",views.qualityexport,name="qualityexport"),
        

    	#ajax

	    path('userajax',views.userajax,name="userajax"),
        path('sajax',views.searchajax,name="sajax"),
        path('smsajax',views.smsajax,name="smsajax"),
        path("ptpajax",views.ptpajax,name="ptpajax"),
        path('misscmsajax',views.misscmsajax,name="misscmsajax"),
        path('missedcallajax',views.missedcallajax,name="missedcallajax"),
        path('qsajax',views.qsajax,name='qsajax'),
        # path("teamajax",views.teamajax,name="teamajax"),
        path('tvajax',views.tvajax,name='tvajax'),
   

        #filterurls
        path('filterm',views.filterrm,name='filterrm'),
        path('filterrs',views.filterrs,name='filterrs'),
        path('filterots',views.filterots,name='filterots'),
        

        # dialapi
        path('call',views.dialcal,name="call"),
        path('dispose',views.dispose,name="dispose"),
        path('disconnect',views.disconnectcall,name="disconnect"),
        path("pausecode",views.pausecode,name="pausecode"),
        path("breakcode",views.breakcode,name="breakcode"),
        path("apstatus",views.activepausestatus,name="apstatus"),
        path("callsinqueue",views.callsinqueue,name="callsinqueue"),
        path('pa',views.pa,name="pa"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


