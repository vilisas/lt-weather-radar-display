#!/usr/bin/python3
# -*- coding:utf-8 -*-
#
# E-Ink weather display.
# Sutemos 2023
# based on WaveShare epd examples.
#
# 800 x 480 display simulator. Because e-ink display is sloooow, we can generate png file instead.
# Display has two 1-bit canvases - one for black color, another for red or yellow.
# There is ~16 sec refresh time for EVERY canvas.
#

import os, sys, time, traceback, logging, json, requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

libdir = "../lib/"
if os.path.exists(libdir):
    sys.path.append(libdir)
# from waveshare_epd import epd7in5b_V2


width = 800
height = 480
radar_url = "https://beta.meteo.lt/meteo-data/radar/radarlarge+36.gif"

# API info: https://api.meteo.lt
# observed data for Vilnius
weather_json_url = "https://api.meteo.lt/v1/stations/vilniaus-ams/observations/latest"

logging.basicConfig(level=logging.DEBUG)
# epd = epd7in5b_V2.EPD()


def display_black(buffer):
    # epd.display(epd.getbuffer(buffer),epd.getbuffer(buffer))
#    epd.send_command(0x10)
    for i in range(len(buffer)):
        buffer[i] ^= 0xFF
#    epd.send_data2(buffer)
#    epd.send_command(0x12)
#    time.sleep(0.5)
#    epd.ReadBusy()


try:
    str_time = time.strftime("%Y-%m-%d %H:%M")

    # radar_src = Image.open("lib/radarlarge+36.gif")
    response = requests.get(radar_url)
    radar_src = Image.open(BytesIO(response.content))

    radar_img = radar_src.crop((50, 70, 530, 420))

    response = requests.get(weather_json_url)
    weather_json = json.loads(response.content)
    observatons = dict.get(weather_json,'observations')
    # print(("Type: ", type(weather_json)))
    # print(len(observatons))
    # latest_observation = dict(observatons, len(observatons) - 1)
    latest = observatons[len(observatons) - 1]
    airTemperature = dict.get(latest, 'airTemperature')
    feelsLikeTemperature = dict.get(latest, 'feelsLikeTemperature')
    windSpeed = dict.get(latest, 'windSpeed')
    windGust = dict.get(latest, 'windGust')
    windDirection = dict.get(latest, 'windDirection')
    precipitation = dict.get(latest, 'precipitation')
    conditionCode = dict.get(latest, 'conditionCode')
    seaLevelPressure = dict.get(latest, 'seaLevelPressure')
    relativeHumidity = dict.get(latest, 'relativeHumidity')
    observationTimeUtc = dict.get(latest, 'observationTimeUtc')


    print(("Temp: ", airTemperature, "Feels like", feelsLikeTemperature, "relativeHumidity", relativeHumidity))
    print(("conditionCode", conditionCode))
    # print(latest)
    # print(weather_json)
    # json.dumps(weather_json).find("observations")    
    logging.info("epd7in5b_V2 meteo radar")

    font24 = ImageFont.truetype(libdir + r'Font.ttc', 24)
    font18 = ImageFont.truetype(libdir + r'Font.ttc', 18)
    font64 = ImageFont.truetype(libdir + r'Font.ttc', 64)

#    width  = epd.width
#    height = epd.height
#    logging.info(("EPD width=", width, " height=", height))
    logging.info("init and Clear")
#    epd.init()
#    epd.Clear()  # optional

    # Drawing on the Horizontal image
    logging.info("1.Drawing on the Horizontal image...")
    black_image = Image.new('1', (width, height), 255)  # 255: clear the frame
    red_image = Image.new('1', (width, height), 255)  # 255: clear the frame

    draw_black = ImageDraw.Draw(black_image)  # black image canvas
    draw_red = ImageDraw.Draw(red_image)

    radar_offset_x = 10
    radar_offset_y = 105

    # paste to specific location
    black_image.paste(radar_img, (radar_offset_x, radar_offset_y))
    draw_black.rectangle((radar_offset_x, radar_offset_y,
                         480+radar_offset_x, 350 + radar_offset_y), outline=0)

    draw_black.text((10, height-25), ("Atnaujinta " + str_time),
                    font=font24, fill=0)
    draw_red.text((10, height-25), ("Atnaujinta " + str_time),
                    font=font24, fill=0)
    draw_black.text((5, 1), 'Orai', font=font64, fill=0)
    
    text = "%0.1f°C \n%d%% \n%d m/s \n%0.1f mm" % (airTemperature, relativeHumidity, windSpeed, (0 if precipitation == None else precipitation))
    draw_black.text((510, 90), text, font=font64, fill=0)
    draw_black.text((10, 75), 'Radaras', font=font24, fill=0)
    draw_black.rectangle((0, 0, width-1, height-1), outline=0)

    # You can output the results to png file here
    black_image.save("output.png", format="png")
    ## black_image.show()

#    display_black(epd.getbuffer(black_image))
#    epd.display(epd.getbuffer(black_image),epd.getbuffer(red_image))

    logging.info("Goto Sleep...")
#    epd.sleep()

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
#    epd7in5b_V2.epdconfig.module_exit()
    exit()
