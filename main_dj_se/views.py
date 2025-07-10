from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
from PIL import Image
from io import BytesIO
import os
from django.conf import settings

# Create your views here.
def main_view(request):
    template =loader.get_template('main_dj_se.html')
    return HttpResponse(template.render())

def scrap(request):
    context = {}

    if request.method == 'POST':
        url = request.POST.get('url')
        print(f"[DEBUG] URL recebida: {url}")

        options = Options()
        options.add_argument('--headless')
        options.add_argument("--window-size=1920x1080")
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        options.add_argument('--incognito')
        options.add_argument('--disable-extensions')

        driver = webdriver.Chrome(options=options)

        try:
            driver.get(url)

            title = driver.find_element(By.ID, 'productTitle').text
            description = (driver.find_element(By.ID, 'bookDescription_feature_div')
                           .text.replace("Leia mais", ""))
            reviwe = driver.find_element(By.ID, 'acrPopover').text
            price_digital = driver.find_element(By.ID, 'tmm-grid-swatch-KINDLE').text
            price_fisical = driver.find_element(By.ID, 'tmm-grid-swatch-PAPERBACK').text

            img_element = driver.find_element(By.ID, 'landingImage')
            print(img_element.get_attribute('outerHTML'))

            cover = driver.find_element(By.ID, 'landingImage').get_attribute('src')

            response = requests.get(cover)
            img = Image.open(BytesIO(response.content))

            file_name = 'cover_book.jpg'
            complete_path = os.path.join(settings.MEDIA_ROOT, 'covers', file_name)

            os.makedirs(os.path.dirname(complete_path), exist_ok=True)
            img.save(complete_path)

            context = {
                'title_book': title,
                'description_book': description,
                'price_digital': price_digital,
                'price_audio': "Indisponível",
                'price_fisical': price_fisical,
                'reviwe': reviwe,
                'cover': f"{settings.MEDIA_URL}covers/cover_book.jpg",
            }

        except Exception as e:
            context['erro'] = f"Erro ao extrair dados: {str(e)}"
        finally:
            driver.quit()

    return render(request, 'scrap.html', context)
