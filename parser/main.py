# Run: uvicorn main:app --reload

from enum import Enum, unique
import logging
import random
from time import sleep
from typing import Any, Generator, Literal, Union
from urllib.parse import quote_plus, urlencode

from pydantic import BaseModel, Field
from fastapi import Depends, FastAPI, status
from fastapi.responses import JSONResponse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.support.ui import WebDriverWait
from selenium_stealth import stealth

DEBUG_MODE = True


class ErrorMessage(BaseModel):
    """Ошибка в полученном запросе"""

    message: str = Field(description="Текст ошибки")


class PageDTO(BaseModel):
    """Модель успешного ответа парсера"""

    ste_name: str = Field(description="Наименование СТЕ")
    data: str = Field(description="HTML страницы с характеристиками из источника")


def get_driver() -> Generator[WebDriver, Any, None]:
    """
    Зависимость для хендлера
    """
    options = Options()
    ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    options.add_argument(f"user-agent={ua}")
    options.add_argument("--ignore-certificate-errors")
    # options.add_argument("--headless")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()

    stealth(
        driver,
        languages=["ru-RU", "ru", "en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Google Inc. (NVIDIA)",
        renderer="ANGLE (NVIDIA, NVIDIA GeForce GTX 650 Ti Direct3D11 vs_5_0 ps_5_0, D3D11-27.21.14.5671)",
        fix_hairline=True,
    )

    yield driver


try:
    app = FastAPI(title="Парсер данных по наименованию СТЕ", version="0.0.1")
except KeyboardInterrupt:
    logging.info("Завершение работы")
    get_driver().close()


def in_page_time(start: float, end: float) -> None:
    """
    Время ожидания на странице в диапазоне (секунды)
    """
    sleep(random.uniform(start, end))


def get_search_results(driver, req_text: str, limit: int = 1) -> list[str]:
    """
    Получение списка URL по запросу (из Яндекс)

    Платные API и иностранные сервисы нельзя использовать.
    Выкручиваемся как можем🌚👌
    """
    payload = {"text": req_text, "lr": 213}
    queries = urlencode(payload, quote_via=quote_plus)
    base_url = f"https://yandex.ru/yandsearch?{queries}"
    if DEBUG_MODE:
        with open("search_page.html", "r", encoding="utf-8") as rf:
            page = rf.read()
    else:
        driver.get(base_url)
        in_page_time(10, 20)
        page = driver.page_source
        # with open('search_page.html', 'w', encoding='utf-8') as wf:
        #     wf.write(page)

    # Чистые костыли, лучше уже не будет
    # TODO: переписать на селекторах

    site_url_split = page.split('" tabindex="0" href="')

    url_list = []

    i = 0
    for x, site_split in enumerate(site_url_split):
        if i == 14:
            break
        if x % 2:
            try:
                url_list.append(site_split.split('"')[0])
                # print(i+1, site_split.split('"')[0])
            except:  # noqa: E722
                continue
            i += 1

    url_list = url_list[:limit]
    # print(url_list)
    return url_list


def parse_vseinstrumenti(driver, req_text: str) -> str | Literal[""]:
    """
    Получение данных из Все инструменты
    """

    driver.get("https://www.vseinstrumenti.ru/")

    search_input = driver.find_element(
        By.XPATH, '//*[@id="__layout"]/div/div[1]/div[2]/div/div[3]/div/div/label/input'
    )
    search_input.click()
    search_input.send_keys(req_text)

    first_result = driver.find_element(
        By.XPATH, '//*[@id="__layout"]/div/div[1]/div[2]/div/div[3]/div/button'
    ).click()

    in_page_time(3, 5)
    WebDriverWait(driver, 20).until(
        EC.frame_to_be_available_and_switch_to_it(
            (
                By.XPATH,
                "//iframe[@title='Widget containing a Cloudflare security challenge']",
            )
        )
    )
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//label[@class='ctp-checkbox-label']"))
    ).click()

    try:
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="product-listing-top"]/div[1]/div[1]/p')
            )
        )
    except:  # noqa: E722
        logging.error("Не получилось загрузить страницу поиска")

    try:
        first_result = driver.find_element(  # noqa: F841
            By.XPATH, '//*[@id="product-listing-top"]/div[2]/div/a[2]'
        ).click()
    except:  # noqa: E722
        logging.error("СТЕ не найден на сайте")
        return ""

    try:
        element = WebDriverWait(driver, 5).until(  # noqa: F841
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    '//*[@id="__layout"]/div/div[2]/div/div[1]/section[1]/div[3]/div/button',
                )
            )
        )
    except:  # noqa: E722
        logging.error("Не получилось загрузить страницу товара")

    try:
        result = driver.find_element(
            By.XPATH, '//*[@id="description"]/div[3]/div[1]/div[1]/div[2]'
        ).get_attribute("outerHTML")
    except:  # noqa: E722
        result = driver.find_element(
            By.XPATH, '//*[@id="description"]/div[2]/div[1]/div[1]/div[2]'
        ).get_attribute("outerHTML")
    return result


def parse_nix(driver, req_text: str) -> str | Literal[""]:
    """
    Получение данных из Никс
    """
    driver.get("https://www.nix.ru/")

    search_input = driver.find_element(By.XPATH, '//*[@id="textfield"]')
    search_input.click()
    search_input.send_keys(req_text)

    in_page_time(2, 4)

    driver.find_element(By.XPATH, '//*[@id="search_button"]').click()

    in_page_time(1, 3)

    driver.find_element(By.XPATH, '//*[@id="good_name_1"]/a').click()

    in_page_time(1, 3)

    result = driver.find_element(
        By.XPATH, '//*[@id="goods_descriptions"]'
    ).get_attribute("outerHTML")

    return result


def parse_sportpoint(driver, req_text: str) -> str | Literal[""]:
    """
    Получение данных из Спортпоинт
    """
    driver.get("https://sportpoint.ru/")

    # Кроссовки волейбольные ASICS 1071A068 002 GEL-RENMA 10  р. 43,5

    search_input = driver.find_element(By.XPATH, '//*[@id="title-search-input"]')
    search_input.click()
    search_input.send_keys(req_text)

    in_page_time(2, 4)

    driver.find_element(By.XPATH, '//*[@id="title-search"]/form/button').click()

    in_page_time(1, 3)

    driver.find_elements(By.CLASS_NAME, "products-product__name")[0].click()

    in_page_time(1, 3)

    result = driver.find_element(
        By.XPATH, "/html/body/div[2]/div/section[2]/div[2]/div[1]/div[4]/div[2]"
    ).get_attribute("outerHTML")

    return result


def parse_notik(driver, req_text: str) -> str | Literal[""]:
    """
    Получение данных из Нотик
    """
    driver.get("https://www.notik.ru/")

    search_input = driver.find_element(By.XPATH, '/*[@id="searchquery"]')
    search_input.click()
    search_input.send_keys(req_text)

    in_page_time(2, 4)

    driver.find_element(By.XPATH, '//*[@id="mainsearchform"]/fieldset/div').click()

    in_page_time(1, 3)

    if "По данному запросу ничего не найдено" in driver.page_source:
        return ""

    div_count = len(
        driver.find_elements(By.XPATH, '//*[@id="search_result"]/div[2]/div[*]')
    )

    driver.find_element(
        By.XPATH, f'//*[@id="results{div_count}"]/ul/li[1]/div[2]/a'
    ).click()

    in_page_time(1, 3)

    result = driver.find_element(By.XPATH, '//*[@id="conts"]/li/div[2]').get_attribute(
        "outerHTML"
    )

    return result


@unique
class Funcs(str, Enum):
    vseinstrumenti = parse_vseinstrumenti
    nix = parse_nix
    sportpoint = parse_sportpoint
    notik = parse_notik

    @classmethod
    def get_func(cls, key):
        return dict(vars(cls)).get(key, None)


@unique
class Source(str, Enum):
    vseinstrumenti = "vseinstrumenti"
    nix = "nix"
    sportpoint = "sportpoint"
    notik = "notik"


@app.get(
    "/",
    tags=["home"],
    summary="Домашняя страница",
    status_code=status.HTTP_200_OK,
)
def default_page() -> JSONResponse:
    """
    Домашняя страница
    """
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"info": "Парсер данных по наименованию СТЕ"},
    )


@app.get(
    "/api/v1/ste",
    tags=["parse"],
    response_model=PageDTO,
    summary="Парсинг HTML с характеристиками СТЕ",
    status_code=status.HTTP_200_OK,
)
def process_ste(
    ste_name: Union[str, None] = None,
    source: Source = None,
    driver=Depends(get_driver),
) -> JSONResponse:
    """
    Получение страницы из источника по названию СТЕ
    """
    page = Funcs.get_func(source.value)(driver, ste_name)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=PageDTO(ste_name=ste_name, data=page).model_dump(),
    )


if __name__ == "__main__":
    logging.basicConfig(
        filename="app.log",
        filemode="a",
        level=logging.DEBUG,
        format="[%(levelname)s]%(asctime)s - %(message)s",
        encoding="utf-8",
        datefmt="%d-%m-%YT%H:%M:%SZ%z",
    )
