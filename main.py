import requests
import json
from PIL import Image, ImageDraw, ImageFont
import ctypes, os
import datetime


def setWallpaper(path):
    ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 3)


def make_image(date, meal):
    img = Image.open("wallpaper_base.png")
    img = img.resize((1920, 1080))
    boldFont = ImageFont.truetype("SpoqaHanSansNeo-Bold.ttf", 50)
    regularFont = ImageFont.truetype("SpoqaHanSansNeo-Regular.ttf", 20)
    mediumFont = ImageFont.truetype("SpoqaHanSansNeo-Medium.ttf", 25)
    draw = ImageDraw.Draw(img)
    draw.text((560, 100), "오늘(" + date + ")의 급식은...", (0, 0, 0), font=boldFont)
    for i in range(len(meal)):
        draw.text((550, 190 + 250 * i), meal[i][0], (0, 0, 0), font=mediumFont)
        for j in range(len(meal[i][1])):
            text = meal[i][1][j]
            x = 550
            y = 220 + 250 * i + 30 * j
            if j == 0:
                _, _, text_width, text_height = regularFont.getbbox(text)
                draw.text((x, y), text, font=regularFont, fill=(0, 0, 0))
            else:
                _, _, text_width, text_height = regularFont.getbbox(text)
                draw.text((x, y), text, font=regularFont, fill=(0, 0, 0))
    draw.text((760, 970), "맛있겠당...", font=boldFont, fill=(0, 0, 0))
    img.save("급식.png")

meal_order = 1  # 0~2
today = datetime.datetime.now()
date = today.strftime('%Y%m%d')

res = requests.get("https://open.neis.go.kr/hub/mealServiceDietInfo?KEY=7c8f58d4e4174b94b96b1aea5fb6fd0d&type=json&&ATPT_OFCDC_SC_CODE=E10&SD_SCHUL_CODE=7310058&MLSV_YMD=" + date)
res = json.loads(res.text)["mealServiceDietInfo"][1]["row"]
changeName = {"조식": "아침", "중식": "점심", "석식": "저녁"}
meal = []
for i in res:
    meal.append((changeName[i["MMEAL_SC_NM"]], i["DDISH_NM"].split("<br/>")))
print(meal)

make_image(date, meal)
path = os.path.abspath('급식.png')
setWallpaper(path)