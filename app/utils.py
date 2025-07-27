from rest_framework.views import exception_handler
from rest_framework.response import Response

def custom_exception_handler(exc, context):
    # 標準のハンドラを呼び出して、標準のレスポンスを取得
    response = exception_handler(exc, context)

    # レスポンスがある場合（DRFが処理できる例外の場合）
    if response is not None:
        # エラーレスポンスを標準化
        if 'detail' in response.data:
            # 単一のエラーメッセージの場合
            error_message = response.data['detail']
            response.data = {'errors': {'non_field_errors': [str(error_message)]}}
        elif isinstance(response.data, dict):
            # フィールドごとのエラーの場合
            response.data = {'errors': response.data}

    return response