import scraping
import extraction
import notification

# エントリポイント
def main(argc, argv):

    # 実際のサイトからHTMLを取得する
    option = scraping.Option.createOption()

    htmls = []

    htmls = scraping.getHtml(option)
    
    statuses = extraction.extract(htmls)

    if statuses != None:
        print('解析結果をlineに送信します。')
        summary = ''

        exists = False
        for status in statuses:
            if status.hasAvailableTime():
                summary += status.createSummary()
                summary += '\n'
                exists = True

        # 空いている情報があるなら送る
        if exists == True:
            summary += 'こちらのURLで予約可能です。' + '\n'
            summary += 'https://reserve.opas.jp/osakashi/menu/Login.cgi'+ '\n'
            print(summary)
            notification.sendMessage(summary)
        else:
            print("送信する情報がなかったので、送信処理を終了します。")