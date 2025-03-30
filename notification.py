import requests

# 個人トークン
#token = 'ib3LFzBsiDbq0MeD8I8T1YBZeQ26bTXctCIB6JJAxbl'

# グループトークン
token = 'ybYQw9LSWVmVTWb9fawRniBIH5c55YRvJbzgvdClMps'

# Lineにメッセージを送信する
def sendMessage(message: str):
   
    line_notify_api = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': f'Bearer {token}'}
    data = {'message': '\n' + message }

    requests.post(line_notify_api, headers = headers, data = data)

    print('lineにメッセージを送信しました')
    print('送信内容: \n' + message)
