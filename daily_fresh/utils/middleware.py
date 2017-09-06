class UrlRecordMiddleware(object):
    exclude_path = ['/user/login/', '/user/login_check/', '/user/logout/',
                    '/user/register/', '/user/check_username_exist/',
                    '/user/check_email_exist/', '/cart/count/', '/cart/add/',
                    '/user/set_address/', '/goods/get_image_list/',
                    '/user/del_address', '/cart/del_cart_goods/', '/cart/update/', ]

    def process_view(self, request, view_func, *view_args, **view_kwargs):
        if request.path not in UrlRecordMiddleware.exclude_path:
            request.session['pre_url_path'] = request.get_full_path()
