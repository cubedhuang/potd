# scraper borrowed from https://github.com/ryanrudes/amc/tree/main

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from PIL import Image
from io import BytesIO
import os
import shutil
import numpy as np

LEVEL = "12"

# if os.path.exists("./downloads/"):
#     shutil.rmtree("./downloads/")
if not os.path.exists("./problems/"):
    os.mkdir("./problems/")
if not os.path.exists(f"./problems/{LEVEL}/"):
    os.mkdir(f"./problems/{LEVEL}/")

options = Options()
options.add_argument("--headless")
options.add_argument("--window-size=720,1080")

options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

# set userAgent
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
)

browser = webdriver.Chrome(options=options)

for year in range(2002, 2021):
    year_path = f"./problems/{LEVEL}/{year}/"
    os.mkdir(year_path)
    for exam in "AB":
        exam_path = year_path + exam + "/"
        os.mkdir(exam_path)
        for problem in range(1, 26):
            url = f"https://artofproblemsolving.com/wiki/index.php/{year}_AMC_{LEVEL}{exam}_Problems/Problem_{problem}"
            browser.get(url)
            try:
                # div = browser.find_element_by_class_name("mw-parser-output")
                div = browser.find_element(By.XPATH, "//div[@class='mw-parser-output']")
                # elements = (element for element in div.find_elements_by_xpath("*"))
                elements = (element for element in div.find_elements(By.XPATH, "*"))

                while next(elements).tag_name != "h2":
                    pass

                ims = []
                while True:
                    element = next(elements)
                    if element.tag_name == "h2":
                        break
                    location = element.location
                    size = element.size
                    png = browser.get_screenshot_as_png()
                    im = Image.open(BytesIO(png))
                    left = location["x"]
                    top = location["y"]
                    right = location["x"] + size["width"]
                    bottom = location["y"] + size["height"]
                    im = im.crop((left, top, right, bottom))
                    ims.append(im)
                image = np.vstack(
                    [
                        np.pad(
                            np.asarray(im),
                            ((4, 4), (4, 4), (0, 0)),
                            "constant",
                            constant_values=255,
                        )
                        for im in ims
                    ]
                )
                image = np.pad(
                    image, ((12, 12), (12, 12), (0, 0)), "constant", constant_values=255
                )
                image = Image.fromarray(image)
                image.save(exam_path + str(problem) + ".png")
            except KeyboardInterrupt:
                exit()
            except Exception as e:
                print("ERROR:", str(e))
                continue

browser.close()
