import json
import os
import time
from enum import Enum
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select

# 大分類の種類定義
# サイトの表示順に定義
class MajorClassificationKind(Enum):

    # バレーボール
    Volleyball = 0  
    
    # バスケットボール
    Basketball = 1 
    
    # バドミントン 
    Badminton = 2  
    
    # 卓球
    TableTennis = 3  

    # テニス
    Tennis = 4

    # 体操
    Gymnastics = 5

    # ダンス、エクササイズ 
    Dance = 6  

    # 武道
    MartialArts = 7

    # 野球、ソフトボール
    Baseball = 8  

    # サッカー
    Soccer = 9

    # ニュースポーツ
    NewSports = 10  

    # 競技会、運動会
    Competition = 11  

    # 文化利用、会議
    CulturalUse = 12

    # その他球技
    OtherBallGames = 13

    # その他
    Other = 14  

    # 未指定
    NoSelection = 99

    @classmethod
    def findValue(cls, targetName: str):
        targetName = targetName.replace('MajorClassificationKind.', '')
        for e in MajorClassificationKind:
            if e.name == targetName:
                return e
            
        raise ValueError('{} は有効な値ではありません'.format(targetName))

# 体育館の種類定義
# サイトの表示順に定義
class FacilityKind(Enum):

    # 中央体育館
    CentralGym = 0

    # 千島体育館
    ChishimaGym = 1

    # 東淀川体育館
    HigashiyodogawaGym = 2

    # 北スポーツセンター
    NorthSportsCenter = 3

    # 都島スポーツセンター
    MiyakojimaSportsCenter = 4

    # 福島スポーツセンター
    FukushimaSportsCenter = 5

    # 此花スポーツセンター
    KonohanaSportsCenter = 6

    # 中央スポーツセンター
    CentralSportsCenter = 7

    # 西スポーツセンター
    WestSportsCenter = 8

    # 港スポーツセンター
    MinatoSportsCenter = 9

    # 大正スポーツセンター
    TaishoSportsCenter = 10

    # 天王寺スポーツセンター
    TemnojiSportsCenter = 11

    # 浪速スポーツセンター
    NaniwaSportsCenter = 12

    # 西淀川スポーツセンター
    NishiyodogawaSportsCenter = 13

    # 淀川スポーツセンター
    YodogawaSportsCenter = 14

    # 東淀川スポーツセンター
    HigashiyodogawaSportsCenter = 15

    # 東成スポーツセンター
    HigashinariSportsCenter = 16

    # 生野スポーツセンター
    IkunoSportsCenter = 17

    # 旭スポーツセンター
    AsahiSportsCenter = 18

    # 城東スポーツセンター
    JotoSportsCenter = 19

    # 鶴見スポーツセンター
    TsurumiSportsCenter = 20

    # 阿倍野スポーツセンター
    AbenoSportsCenter = 21

    # 住之江スポーツセンター
    SuminoeSportsCenter = 22

    # HOS住吉スポーツセンター
    HOSSumiyoshiSportsCenter = 23

    # 東住吉スポーツセンター
    HigashisumiyoshiSportsCenter = 24

    # 平野スポーツセンター
    HiranoSportsCenter = 25

    # フィットネス21西成スポーツセンター
    Fitness21NishinariSportsCenter = 26

    # NASAquaPark扇町プール
    NasAquaParkOgimachiPool = 27

    @classmethod
    def findValue(cls, targetName: str):

        targetName = targetName.replace('FacilityKind.', '')
        for e in FacilityKind:
            if e.name == targetName:
                return e
            
        raise ValueError('{} は有効な値ではありません'.format(targetName))

# 抽出オプション定義
class Option : 

    # オプションのエンコードクラス
    class OptionEncoder(json.JSONEncoder):
        def default(self, o):
            if isinstance(o, Option):
                return o.__dict__
            if isinstance(o, MajorClassificationKind):
                return o.name
            if isinstance(o, FacilityKind):
                return o.name
        
            return super(Option.OptionEncoder, self).default(o)
    
    # コンストラクタ
    def __init__(self):
        self._majorClassification = MajorClassificationKind.NoSelection
        self._minorClassification = 0
        self._facilities = []
        self._weekCount = 1
        self._year = None
        self._month = None
        self._day = None
        self._isHeadless = False

    # 設定が適切に行われているか判定する
    def isValid(self) -> bool:
        if self._majorClassification == MajorClassificationKind.NoSelection:
            print("大分類が設定されていません。")
            return False
        
        if(self._minorClassification < 0):
            print("小分類に負の値が設定されています。")
            return False
        
        if(len(self._facilities) <= 0):
            print("施設が設定されていません。")
            return False
        
        return True

    # 日にちを設定する
    # 設定されない場合はデフォルト（検索時の日にち）として処理される
    def setDate(self, year: int, month: int, day: int):
        self._year = year
        self._month = month
        self._day = day

    # オプション設定をJSONで保存する
    def storeOption(self, option):
        dataPath = os.getcwd() + '/setting.txt'
        with open(dataPath, 'w') as f:
            json.dump(
                option.__dict__, 
                f, 
                ensure_ascii = False, 
                indent = 4, 
                sort_keys = True, 
                separators=(',', ': '),
                cls = Option.OptionEncoder)
            
    # 設定からオプションインスタンスを生成する
    @classmethod
    def createOption(self):
        option = Option()
        '''
        option._facilities = [
            FacilityKind.AbenoSportsCenter,
            FacilityKind.CentralGym,
            FacilityKind.HigashinariSportsCenter,
            FacilityKind.HigashisumiyoshiSportsCenter,
        ]
        option._majorClassification = MajorClassificationKind.Basketball
        option._minorClassification = 0
        option._isHeadless = True
        '''
    
        dataPath = os.getcwd() + '/setting.txt'
        with open(dataPath, 'r') as f:
            jsonDict = json.loads(f.read())

            # 施設の設定を取り出す
            for facilityName in jsonDict['_facilities']:
                facility = FacilityKind.findValue(facilityName)

                # 一応既に登録されているか確認
                if not facility in option._facilities:
                    option._facilities.append(facility)

            # 大分類を取り出す
            option._majorClassification = MajorClassificationKind.findValue(jsonDict['_majorClassification'])
            option._minorClassification = jsonDict['_minorClassification']
            option._weekCount = jsonDict['_weekCount']
            option._year = jsonDict['_year']
            option._month = jsonDict['_month']
            option._day = jsonDict['_day']
            option._isHeadless = jsonDict['_isHeadless']
    
        return option

# 対象のHTMLを取得する
# 週ごとのHTMLを取得するので、戻り値は指定されている週の数によって変動する
def getHtml(option: Option):

    # 選択設定が適切か確認
    if option.isValid() == False:
        return

    driver = settingDriver()
    waitTime = 20

    # WebドライバーでQiitaログインページを起動
    driver.get('https://reserve.opas.jp/osakashi/menu/Login.cgi')
    driver.implicitly_wait(waitTime)

    # [空き状況照会]をクリック
    checkButton = driver.find_element(By.CLASS_NAME,"menu_button")
    if checkButton == None:
        print('空き状況照会ボタンを取得できなかったので処理を中断します')
        return
    
    checkButton.click()
    print("「空き状況照会」をクリックしました")
    
    driver.implicitly_wait(waitTime)

    # [利用目的から絞り込む]をクリック
    purposeButton = driver.find_element(By.XPATH, '//*[@id="mmaincolumn"]/div/table/tbody/tr[2]')
    if purposeButton == None:
        print('利用目的ボタンを取得できなかったので処理を中断します')
        return
    
    purposeButton.click()
    print("「利用目的から絞り込む」をクリックしました")
    
    driver.implicitly_wait(waitTime)

    # 大分類を選択
    # バレーボールのtr[2]なのでインデックスを調整
    majorClassifacationIndex = 2 + option._majorClassification.value
    majorButton = driver.find_element(By.XPATH, '//*[@id="mmaincolumn"]/div/table/tbody/tr[' + str(majorClassifacationIndex) + ']')
    if majorButton == None:
        print(f'大分類の{ str(majorClassifacationIndex) }のボタンを取得できなかったので処理を中断します。')
        return
    
    majorButton.click()
    print('大分類から' + option._majorClassification.name + 'を選択しました')
    
    driver.implicitly_wait(waitTime)

    # 小分類のバスケットボールを選択
    minorClassifacationIndex = 2 + option._minorClassification
    minorButton = driver.find_element(By.XPATH, '//*[@id="mmaincolumn"]/div/table/tbody/tr[' + str(minorClassifacationIndex) + ']')
    if minorButton == None:
        print('小分類ボタンを取得できなかったので処理を中断します。')
        return
    
    minorButton.click()
    print('小分類から ' + str(minorClassifacationIndex + 1) + '番目の小分類を選択しました')
    
    driver.implicitly_wait(waitTime)

    # 施設の選択
    for facility in option._facilities:
        # 複数の施設を選ぶ場合はここで一気に選択する
        # 中央体育館はtr[2]なのでインデックスを調整
        facilityIndex = 2 + facility.value
        driver.find_element(By.XPATH, '//*[@id="mmaincolumn"]/div/table/tbody/tr[' + str(facilityIndex) + ']').click()
        print(facility.name + "を選択しました")

    # 「次に進む」を選択
    # 複数の施設を選ぶ場合はここで一気に選択する
    driver.find_element(By.XPATH, '//*[@id="pagerbox"]/a[2]').click()
    print("「次に進む」を選択しました")

    driver.implicitly_wait(waitTime)

    # 時間が設定されているなら設定する
    if option._year != None and option._month != None and option._day != None:
        print('日時を ' + str(option._year) + '/'+ str(option._month) + '/' + str(option._day) + ' に設定します')

        isSet = True
        if trySetSelection(driver, '//*[@id="optYear"]', str(option._year)) != True:
            print(str(option._year) + "年と値を設定できませんでした。")
            isSet = False

        if trySetSelection(driver, '//*[@id="optMonth"]', str(option._month).zfill(2)) != True:
            print(str(option._month) + "月と値を設定できませんでした。")
            isSet = False

        if trySetSelection(driver, '//*[@id="optDay"]', str(option._day)) != True:
            print(str(option._day) + "日と値を設定できませんでした。")
            isSet = False
            
        # 日にちを更新
        if isSet == True:
            driver.find_element(By.XPATH, '//*[@id="selectbox"]/ul/li[1]/div/a[2]').click()

    htmls = [] 
    htmls.append(driver.page_source)
    for i in range(option._weekCount - 1):
        # 指定回数次の週も抽出する
        print("次の週の情報を取得します。")
        nextWeekButton = driver.find_element(By.XPATH, '//*[@id="facilitiesbox"]/tbody/tr[1]/td/table/tbody/tr[2]/th[1]/p/a[2]')
        if nextWeekButton == None:
            print("次の週に進むボタンを取得できませんでした。")
            break
        
        nextWeekButton.click()

        driver.implicitly_wait(waitTime)

        htmls.append(driver.page_source)

    # セッションを終了
    driver.quit()

    return htmls

# リストボックスに設定可能かを判定後に値を設定する
def trySetSelection(driver, xpath, value) -> bool:
    selection = Select(driver.find_element(By.XPATH, xpath))
    for option in selection.options:
        if option.text == value:
            selection.select_by_visible_text(value)
            return True
        
    return False

def settingDriver():
    print("webdriverのセットアップを行います。")

    chrome_options = webdriver.ChromeOptions()

    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1280x1696")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--hide-scrollbars")
    chrome_options.add_argument("--enable-logging")
    chrome_options.add_argument("--log-level=0")
    chrome_options.add_argument("--v=99")
    chrome_options.add_argument("--single-process")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    return webdriver.Chrome(options = chrome_options)