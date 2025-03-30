import requests

# 個人トークン
#token = 'ib3LFzBsiDbq0MeD8I8T1YBZeQ26bTXctCIB6JJAxbl'

# グループトークン
#token = 'ybYQw9LSWVmVTWb9fawRniBIH5c55YRvJbzgvdClMps'

# ユーザーID
userID = 'U3314a9a6c7835f0a283faa8ffa79e097'
# Line Messaging APIのアクセストークン
accessToken = '3Dkkn7oBDBHY5nI60yv1REKcFXu43fxkETPDunbBkHyJFmH23fkoRScgFiLM6YCJR22jkqNq/gUlbdgMOk5Ts71MMTX38kKnPsQtgc/xL0WSlsQqM9sz1kn+WcfFAj8+NqsF+SHpHuIMU3qWeFn1lQdB04t89/1O/w1cDnyilFU='

# Lineにメッセージを送信する
def sendMessage(message: str):
   
    headers = {
        'Authorization': f'Bearer {accessToken}',
        'Content-Type': 'application/json'
        }

    data = {
        'to': userID,
        'messages': [
           {
                'type': 'text',
                'text': message
           } 
        ]
    }

    #line_notify_api = 'https://notify-api.line.me/api/notify'
    #requests.post(line_notify_api, headers = headers, data = data)

    url = 'https://api.line.me/v2/bot/message/push'
    response = requests.post(url, headers = headers, json = data)

    if response.status_code == 200:
        print('メッセージが送信されました \n' + message)
    else:
        print(f'エラーが発生しました: {response.status_code}, {response.text}')