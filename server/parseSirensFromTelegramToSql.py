from bs4 import BeautifulSoup
import requests, pendulum, mysql.connector, time;

lastCheckedPost = ""

def checkMessage():
    global lastCheckedPost
    soup = BeautifulSoup(requests.get("https://t.me/s/air_alert_ua").text, 'html.parser')
    postId = soup.select_one("body > main > div > section > div:last-child > div.tgme_widget_message.text_not_supported_wrap.js-widget_message")['data-post']


    if postId != lastCheckedPost:
        lastCheckedPost = postId
        unixTime = int(pendulum.parse(soup.select_one("body > main > div > section > div:last-child > div.tgme_widget_message.text_not_supported_wrap.js-widget_message > div.tgme_widget_message_bubble > div.tgme_widget_message_footer.compact.js-message_footer > div > span.tgme_widget_message_meta > a > time")["datetime"]).int_timestamp)
        text = soup.select_one("body > main > div > section > div:last-child > div.tgme_widget_message.text_not_supported_wrap.js-widget_message > div.tgme_widget_message_bubble > div.js-message_text > b").text;
        element = soup.select_one("body > main > div > section > div:last-child > div.tgme_widget_message.text_not_supported_wrap.js-widget_message > div.tgme_widget_message_bubble > div.js-message_text > a").text;

        proccessTheDB(getInfoAboutSiren(text, element), unixTime);

def getInfoAboutSiren(text, element):
    InfoAboutSiren = {}
    if "повітряна тривога" in text.lower():
        InfoAboutSiren.update({'sirenType': 'airAlarm'})
        InfoAboutSiren.update({'sirenElement': convertElement(element)})
    elif "загроза артобстрілу" in text.lower():
        InfoAboutSiren.update({'sirenType': 'artAlarm'})
        InfoAboutSiren.update({'sirenElement': convertElement(element)})
    elif "відбій тривоги" in text.lower():
        InfoAboutSiren.update({'sirenType': 'airRebound'})
        InfoAboutSiren.update({'sirenElement': convertElement(element)})
    elif "відбій загрози" in text.lower():
        InfoAboutSiren.update({'sirenType': 'artRebound'})
        InfoAboutSiren.update({'sirenElement': convertElement(element)})

    return InfoAboutSiren

def convertElement(element):
    if element == "#Запорізька_область":
        element = "zaporizhzhia"
    elif element == "#Донецька_область":
        element = "donetsk"
    elif element == "#Дніпропетровська_область":
        element = "dnipropetrovsk"
    elif element == "#Київська_область":
        element = "kyiv"
    elif element == "#Вінницька_область":
        element = "vinnytsia"
    elif element == "#Чернігівська_область":
        element = "chernihiv"
    elif element == "#Кіровоградська_область":
        element = "kirovohradsk"
    elif element == "#Черкаська_область":
        element = "cherkasy"
    elif element == "#Полтавська_область":
        element = "poltava"
    elif element == "#Житомирська_область":
        element = "zhytomyr"
    elif element == "#Харківська_область":
        element = "kharkiv"
    elif element == "#Одеська_область":
        element = "odesa"
    elif element == "#Сумська_область":
        element = "sumy"
    elif element == "#ІваноФранківська_область":
        element = "ivano-frankivsk"
    elif element == "#Волинська_область":
        element = "volyn"
    elif element == "#Закарпатська_область":
        element = "transcarpathia"
    elif element == "#Луганська_область":
        element = "luhansk"
    elif element == "#Львівська_область":
        element = "lviv"
    elif element == "#Миколаївська_область":
        element = "mykolaiv"
    elif element == "#Рівненська_область":
        element = "rivne"
    elif element == "#Тернопільська_область":
        element = "ternopil"
    elif element == "#Херсонська_область":
        element = "kherson"
    elif element == "#Хмельницька_область":
        element = "khmelnytskyi"
    elif element == "#Чернівецька_область":
        element = "chernivtsi"

    #Треба доробити міста, усі, переклад міста чисто за гуглом і з маленької букви.
    return element

def connectToDB():
    connector = []
    connector.append(mysql.connector.connect(host="localhost", user="root", password="---", database="esepar"))
    connector.append(connector[0].cursor())

    return connector

def closeDB(connector):
    connector[1].close()
    connector[0].commit()
    connector[0].close()

def proccessTheDB(sirenArr, uTime):  
    newc = connectToDB()
    conlink = newc[0]
    concursor = newc[1]

    #debug
    #sirenArr["sirenType"] = "artRebound"
    #sirenArr["sirenElement"] = "yakesdrugemisto"
    #uTime = 1240

    if sirenArr["sirenType"] == "airAlarm" or sirenArr["sirenType"] == "airRebound":
        concursor.execute("CREATE TABLE IF NOT EXISTS airSiren (`sirenElement` TEXT NOT NULL, `airAlarmStartTime` INT, `airAlarmEndTime` INT)");
        
        if sirenArr["sirenType"] == "airAlarm":

            concursor.execute(f"SELECT `sirenElement` FROM airSiren WHERE `airAlarmEndTime` = 0 AND `sirenElement`='{sirenArr['sirenElement']}' ORDER BY airAlarmStartTime DESC LIMIT 1");
            notClosed = concursor.fetchall()
            if len(notClosed) != 0:
                print(f"У елементі - {sirenArr['sirenElement']}, з типом - {sirenArr['sirenType']}, зафіксовано дві повітряних тривог підряд. Виконується наступна команда:")
                print(f"UPDATE airSiren SET `airAlarmEndTime` = {uTime} WHERE `airAlarmEndTime` = 0 AND `sirenElement` = '{sirenArr['sirenElement']}'")
                concursor.execute(f"UPDATE airSiren SET `airAlarmEndTime` = {uTime} WHERE `airAlarmEndTime` = 0 AND `sirenElement` = '{sirenArr['sirenElement']}'")
                
            print(f"У елементі - {sirenArr['sirenElement']}, з типом - {sirenArr['sirenType']}, зафіксована нова тривога. Виконується наступна команда:")
            print(f"INSERT INTO airSiren (`sirenElement`, `airAlarmStartTime`, `airAlarmEndTime`) VALUES ('{sirenArr['sirenElement']}', {uTime}, 0)")
            print("---")
            concursor.execute(f"INSERT INTO airSiren (`sirenElement`, `airAlarmStartTime`, `airAlarmEndTime`) VALUES ('{sirenArr['sirenElement']}', {uTime}, 0)")
        
        elif sirenArr["sirenType"] == "airRebound":
        
            concursor.execute(f"SELECT `airAlarmEndTime` FROM airSiren WHERE `sirenElement`= '{sirenArr['sirenElement']}' ORDER BY airAlarmStartTime DESC LIMIT 1");
            notClosed = concursor.fetchall()
            if len(notClosed) != 0:
                notClosed = notClosed[len(notClosed) - 1]
                if int(notClosed[0]) != 0:
                    print(f"У елементі - {sirenArr['sirenElement']}, з типом - {sirenArr['sirenType']}, зафіксовано два відбою повітряної тривоги підряд. Виконується наступна команда:")
                    print(f"INSERT INTO airSiren (`sirenElement`, `airAlarmStartTime`, `airAlarmEndTime`) VALUES ('{sirenArr['sirenElement']}', {int(notClosed[0])}, {uTime})")
                    print("---")
                    concursor.execute(f"INSERT INTO airSiren (`sirenElement`, `airAlarmStartTime`, `airAlarmEndTime`) VALUES ('{sirenArr['sirenElement']}', {int(notClosed[0])}, {uTime})")
                else:
                    print(f"У елементі - {sirenArr['sirenElement']}, з типом - {sirenArr['sirenType']}, зафіксований відбій повітряної тривоги. Виконується наступна команда:")
                    print(f"UPDATE airSiren SET `airAlarmEndTime` = {uTime} WHERE `airAlarmEndTime` = 0 AND `sirenElement`='{sirenArr['sirenElement']}'")
                    print("---")
                    concursor.execute(f"UPDATE airSiren SET `airAlarmEndTime` = {uTime} WHERE `airAlarmEndTime` = 0 AND `sirenElement`='{sirenArr['sirenElement']}'")

    if sirenArr["sirenType"] == "artAlarm" or sirenArr["sirenType"] == "artRebound":
        concursor.execute("CREATE TABLE IF NOT EXISTS artSiren (`sirenElement` TEXT NOT NULL, `artAlarmStartTime` INT, `artAlarmEndTime` INT)");

        if sirenArr["sirenType"] == "artAlarm":

            concursor.execute(f"SELECT `sirenElement` FROM artSiren WHERE `artAlarmEndTime` = 0 AND `sirenElement`='{sirenArr['sirenElement']}' ORDER BY artAlarmStartTime DESC LIMIT 1");
            notClosed = concursor.fetchall()
            if len(notClosed) != 0:
                print(f"У елементі - {sirenArr['sirenElement']}, з типом - {sirenArr['sirenType']}, зафіксовано дві загрози артобстрілу підряд. Виконується наступна команда:")
                print(f"UPDATE artSiren SET `artAlarmEndTime` = {uTime} WHERE `artAlarmEndTime` = 0 AND `sirenElement` = '{sirenArr['sirenElement']}'")
                concursor.execute(f"UPDATE artSiren SET `artAlarmEndTime` = {uTime} WHERE `artAlarmEndTime` = 0 AND `sirenElement` = '{sirenArr['sirenElement']}'")

            print(f"У елементі - {sirenArr['sirenElement']}, з типом - {sirenArr['sirenType']}, зафіксований новий артобстріл. Виконується наступна команда:")
            print(f"INSERT INTO artSiren (`sirenElement`, `artAlarmStartTime`, `artAlarmEndTime`) VALUES ('{sirenArr['sirenElement']}', {uTime}, 0)")
            print("---")
            concursor.execute(f"INSERT INTO artSiren (`sirenElement`, `artAlarmStartTime`, `artAlarmEndTime`) VALUES ('{sirenArr['sirenElement']}', {uTime}, 0)")
        
        elif sirenArr["sirenType"] == "artRebound":
        
            concursor.execute(f"SELECT `artAlarmEndTime` FROM artSiren WHERE `sirenElement`= '{sirenArr['sirenElement']}' ORDER BY artAlarmStartTime DESC LIMIT 1");
            notClosed = concursor.fetchall()
            if len(notClosed) != 0:
                notClosed = notClosed[len(notClosed) - 1]
                if int(notClosed[0]) != 0:
                    print(f"У елементі - {sirenArr['sirenElement']}, з типом - {sirenArr['sirenType']}, зафіксовано два відбою загрози артобстрілу підряд. Виконується наступна команда:")
                    print(f"INSERT INTO artSiren (`sirenElement`, `artAlarmStartTime`, `artAlarmEndTime`) VALUES ('{sirenArr['sirenElement']}', {int(notClosed[0])}, {uTime})")
                    print("---")
                    concursor.execute(f"INSERT INTO artSiren (`sirenElement`, `artAlarmStartTime`, `artAlarmEndTime`) VALUES ('{sirenArr['sirenElement']}', {int(notClosed[0])}, {uTime})")
                else:
                    print(f"У елементі - {sirenArr['sirenElement']}, з типом - {sirenArr['sirenType']}, зафіксований відбій загрози артобстрілу. Виконується наступна команда:")
                    print(f"UPDATE artSiren SET `artAlarmEndTime` = {uTime} WHERE `artAlarmEndTime` = 0 AND `sirenElement`='{sirenArr['sirenElement']}'")
                    print("---")
                    concursor.execute(f"UPDATE artSiren SET `artAlarmEndTime` = {uTime} WHERE `artAlarmEndTime` = 0 AND `sirenElement`='{sirenArr['sirenElement']}'")

    closeDB(newc)

def startP(freez, freezErr):
    print("Процес парсингу початий\n")
    while (True):
        try:
            checkMessage()
            time.sleep(freez);
        except:
            print(f"Фрізінг на {freezErr}, секунд через скоріше всього інтернет помилку")
            time.sleep(freezErr)

startP(5, 60)