from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('programing', views.programing, name='poopgame_programing'),
    path('poopsub', views.poopsub, name='poopgame_poopsub'),
    path('subtract3/', views.unko_hikizan, name='unko_hikizan'),
    path('multiply', views.multiply, name='multiply'),
        # 追加：解答チェック用エンドポイント
    path('multiply/check/', views.multiply_check, name='multiply_check'),
    path('poopadd/', views.poopadd, name='poopadd'),
    path('poopadd/check/', views.poopadd_check, name='poopadd_check'),
    path('multiply2/', views.poopmultiply2, name='poopmultiply2'),
    path('multiply2/check/', views.poopmultiply2_check, name='poopmultiply2_check'),
    path('multiply3/', views.unko_kakezan, name='unko_kakezan'),

    path('divide/',   views.divide,   name='divide'),
    path('home', views.home, name="home"),
    path('register/', views.poopgame_register, name='poopgame_register'),
    path('login/', LoginView.as_view(
        template_name='poopgame/login.html',
        redirect_authenticated_user=True
    ), name='poopgame_login'),
    path('poopgame_logout/', LogoutView.as_view(next_page='home'), name='poopgame_logout'),
    path('daily-ranking/', views.weekly_ranking, name='weekly_ranking'),
    path('', views.capitalism, name='capitalism'),
    path('parent/', views.parent_page, name='parent_page'),
    path('bonus/', views.bonus_game, name='bonus_game'),
    path('bonus/result/', views.bonus_result, name='bonus_result'),
        # 子ども用お手伝いページ
    path('child-chores/', views.child_chores, name='child_chores'),
    # 親認証（PINがあればここで聞く、なければ高度問題へリダイレクト）
    path('parent-auth/', views.parent_auth, name='parent_auth'),
    # 高度問題チャレンジ
    path('advanced-challenge/', views.advanced_challenge, name='advanced_challenge'),
    path('shop/', views.unko_shop, name='unko_shop'),  # 子ども側ショップ画面
    path('shop/request/<int:item_id>/', views.request_purchase, name='request_purchase'),  # 購入申請  
    path('parent/shop/', views.parent_shop_admin, name='parent_shop_admin'),  # 親用管理画面
    path('parent/shop/approve/<int:request_id>/', views.approve_purchase, name='approve_purchase'),  # 購入承認
    path('parent/shop/delete/<int:item_id>/', views.delete_shop_item, name='delete_shop_item'),  # 商品削除]
    path('unko_programming/', views.unko_programming_view, name='unko_programming'),
    path('unko_hissan/', views.unko_hissan, name='unko_hissan'),
    ]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)