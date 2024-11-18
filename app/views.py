from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Category, Keyword, ScrapedResult
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
from django.http import HttpResponse
import csv
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm, LoginForm

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')  # Redirect to your home page
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            
            # Redirect to your home page
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('index.html')  # Redirect to your home page


def results(request):
    results = ScrapedResult.objects.all().order_by('scrape_time')
    return render(request, 'results.html', {'results': results})

def download_csv(request):
    results = ScrapedResult.objects.all().values('keyword__name', 'url', 'page_number', 'position', 'scrape_time')

    # Create the CSV response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="scraped_results.csv"'
    writer = csv.writer(response)
    writer.writerow(['Keyword', 'URL', 'Page Number', 'Position', 'Scrape Time'])
    for result in results:
        writer.writerow([result['keyword__name'], result['url'], result['page_number'], result['position'], result['scrape_time']])

    return response

def index(request):
    categories = Category.objects.all()
    return render(request, 'index.html', {'categories': categories})

def create_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        schedule_time = request.POST.get('schedule_time')
        category = Category.objects.create(name=name, schedule_time=schedule_time)
        return redirect('index')

    return render(request, 'create_category.html')

def add_keyword(request):                                    
    if request.method == 'POST':
        category_id = request.POST.get('category')
        keywords = request.POST.getlist('keywords')

        category = Category.objects.get(id=category_id)

        # Save each keyword to the database
        for keyword in keywords:
            Keyword.objects.create(name=keyword, category=category)
        return redirect('index')

    categories = Category.objects.all()
    return render(request, 'add_keyword.html', {'categories': categories})


def run_program(request):
    # Path to ChromeDriver
    chrome_service = Service('chromedriver.exe')  # Update this path
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')  # Optional: runs Chrome in headless mode

    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

    try:
        # Scrape data for all keywords and categories
        categories = Category.objects.all()
        for category in categories:
            print(f"Processing Category: {category.name}")  # Debugging line
            keywords = Keyword.objects.filter(category=category)
            for keyword in keywords:
                print(f"Processing Keyword: {keyword.name}")  # Debugging line
                # Fetch the first result for each keyword from Google
                driver.get(f'https://www.google.com/search?q={keyword.name}')
                time.sleep(2)  # Wait for the page to load

                try:
                    first_result = driver.find_element(By.CSS_SELECTOR, 'h3')
                    url = first_result.find_element(By.XPATH, '..').get_attribute('href')
                    position = 1  # First position
                    page_number = 1  # First page

                    print(f"URL: {url}")  # Debugging line

                    # Check if the result already exists for the same keyword and URL
                    existing_result = ScrapedResult.objects.filter(keyword=keyword, url=url).first()
                    if not existing_result:
                        # Save the result in the database if it doesn't already exist
                        ScrapedResult.objects.create(
                            keyword=keyword,
                            url=url,
                            page_number=page_number,
                            position=position
                            

                        )
                    else:
                        print(f"Result already exists for keyword: {keyword.name} and URL: {url}")  # Debugging line

                except Exception as e:
                    print(f"Error while scraping: {e}")  # Debugging line
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

 
    # Redirect to home page after running the program
    return redirect('index')