from bs4 import BeautifulSoup
import json
import os
import datetime

# 時間と予約ステータスを保持するクラス
class TimeStatus : 

    # 利用可能か
    def canAvailable(self):
        return self.status == "空いています"
    
    # コンストラクタ
    def __init__(self, parent, dayIndex):
        tds = parent.find_all('td')

        self.time = tds[0].text

        # 0番目のtdは時刻表示なので無視する
        if(dayIndex + 1 < len(tds)):
            td = tds[dayIndex + 1]
            img = td.find('img')
            if img != None:
                self.status = img.get('alt')
            else:
                self.status = 'データなし'
        else: 
            self.status = "データなし"

# 日毎の予約状況を保持するクラス
class DayStatus : 
    
    # 利用可能時間のリスト -> str
    def availableTimes(self):
        result = []
        for status in self.timeStatus:
            if(status.canAvailable()):
                result.append(status.time)

        return result

    # 引数の日程よりも新しいか判定する
    def isNewDate(self, date):
        # self.dayは [ ◯月◯日 ]になる想定
        month = int(self.day.split('月')[0])
        day = int(self.day.split('月')[-1].split('日')[0])

        if(month < date.month):
            return False
        
        if(month == date.month):
            # 当日は判定外
            if(day < date.day):
                return False
        
        return True

    # コンストラクタ
    def __init__(self, facilityboxItem, dayIndex):
        days = facilityboxItem.findAll(class_ = 'day')
        
        self.day = days[dayIndex].text

        dayKind = days[dayIndex].find('img').get('title')
        self.isHoliday = False
        if dayKind == '土曜日' or dayKind == '日曜日' or dayKind == '祝日':
            self.isHoliday = True

        # 時間と予約可否状況の取得
        # facmdstime は9:00 ~ 12:00のその週全ての可否
        times = facilityboxItem.find_all(class_ = 'facmdstime')
        self.timeStatus = []

        #times[dayIndex]がその日の9:00の状態
        timeIndex = 0
        
        for time in times:
            #print(time.text)
            self.timeStatus.append(TimeStatus(time.parent, dayIndex))
            timeIndex += 1

    # 予約情報の要約を作成する
    def createSummary(self):
        
        times = self.availableTimes()
        summary = self.day + ' 利用可能時間 ' + ('あり' if len(times) > 0 else 'なし') + '\n'
        for time in times:
            summary += time + '\n'

        return summary

# 施設ごとの予約情報を保持するクラス
class FacilityStatus : 
    
    def hasAvailableTime(self):
        for day in self.dayStatus:
            if(len(day.availableTimes()) > 0):
                return True
            
        return False
    
    # BeautifulSoupで id = 'facilitiesbox'で抽出されたアイテム
    def __init__(self, facilityboxItem):

        # 施設名の取得
        self.facilityName = self.getFacilityName(facilityboxItem)

        # アリーナ名の取得
        facilityArea = facilityboxItem.find(class_ = 'shisetu_name')
        self.facilityAreaName = facilityArea.text

        # 日程ごとの情報を操作しやすいように変更
        self.dayStatus = []
        self.addStatus(facilityboxItem)

    # 日程ごとの情報を追加
    def addStatus(self, facilityboxItem):

        date = datetime.datetime.today()
        for i in range(7):

            newDayStatus = DayStatus(facilityboxItem, i)
            
            # 土日祝でフィルタリングする
            if newDayStatus.isHoliday == False:
                continue
            
            # 実行した日よりも前の場合は無視する
            if newDayStatus.isNewDate(date) == False:
                print(f'過ぎた日なので検索から除外します。 除外日: { newDayStatus.day }')
                continue

            exists = False
            for dayStatus in self.dayStatus:
                if newDayStatus.day == dayStatus.day:
                    exists = True
                    break
            
            if exists == False:
                self.dayStatus.append(newDayStatus)

    # 予約情報の要約を作成する
    def createSummary(self):
        summary = ''
        summary += '施設名: ' + self.facilityName + '\n'
        summary += '施設エリア名: ' + self.facilityAreaName + '\n'

        isAvailable = False
        for day in self.dayStatus:
            if(len(day.availableTimes()) > 0):
                summary += day.createSummary()
                isAvailable = True

        if(isAvailable == False):
            summary += '予約可能な日時がありません。'

        return summary
    
    # HTMLから施設名を取得する
    @classmethod
    def getFacilityName(self, facilityboxItem):
        facility = facilityboxItem.find(class_ = 'clearfix kaikan_title')
        return facility.text


# 予約可能情報のエンコードクラス
class StatusEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, TimeStatus):
            return o.__dict__
        if isinstance(o, DayStatus):
            return o.__dict__
        if isinstance(o, FacilityStatus):
            return 'FacilityStatus'
        
        return super(StatusEncoder, self).default(o)
    
# 抽出した情報をJSONで保存する
def store(statuses):

    dataPath = os.getcwd() + '/available.txt'
    with open(dataPath, 'w') as f:
        for status in statuses:
            json.dump(
                status.__dict__, 
                f, 
                ensure_ascii = False, 
                indent = 4, 
                sort_keys = True, 
                separators=(',', ': '),
                cls = StatusEncoder)

# HTMLから情報を抽出する
# 週ごとのHTML分の配列が引数に指定される想定
def extract(htmls):  

    print('HTMLを解析し、予約可能情報を抽出します。')

    if htmls == None or len(htmls) <= 0:
        print("HTML文がないため情報を抽出できません。")
        return
    
    # 施設ごとの予約情報
    facilityStatuses = []

    for html in htmls:
        soup = BeautifulSoup(html, 'html.parser')
    
        # 施設に関する全体情報
        facilitiesBox = soup.find(id = 'facilitiesbox')
        if facilitiesBox == None:
            print("施設の利用可能カレンダーを取得できませんでした。抽出処理をスキップします。")
            continue
    
        # 一つ一つのtrに施設ごとの情報が格納されている
        facilities = facilitiesBox.findAll(class_ = 'clearfix kaikan_title')
    
        for facility in facilities:
            sameStatus = None
            for status in facilityStatuses:
                if(status.facilityName == FacilityStatus.getFacilityName(facility.parent)):
                    sameStatus = status
                    break
            
            if sameStatus != None:
                # 既にリスト内に同じ施設情報が入っている場合は情報を追加する
                sameStatus.addStatus(facility.parent)
            else:
                # まだ追加されていない施設情報なので新規追加
                facilityStatuses.append(FacilityStatus(facility.parent))

    #store(facilityStatuses)
    print('予約可能情報の解析が完了しました。')

    return facilityStatuses