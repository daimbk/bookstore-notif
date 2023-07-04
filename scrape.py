from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup


def open_link(link):
    """provide option to open the link to book"""

    url = "https://readings.com.pk" + link
    permission = input("Open the link to this book? (Y/N): ")
    while permission not in ('Y', 'N', 'y', 'n'):
        permission = input("Please enter correct option. Y or N: ").upper()

    if permission == "Y" or permission == "y":
        browser = webdriver.Firefox()
        browser.maximize_window()
        browser.get(url)


def check_book():
    """search using only book title (cannot detect specific versions such as special editions)"""
    # get user input of book to check
    book = input("Enter book name: ").title()
    print("\nPlease wait while details are fetched")

    # result page upon searching
    url = f'https://readings.com.pk/Pages/searchresult.aspx?Keyword={book}'

    options = Options()
    options.add_argument("-headless")  # run Firefox in headless mode
    service = Service("geckodriver-v0.33.0-win64")  # path to gecko webdriver
    driver = webdriver.Firefox(service=service, options=options)

    driver.get(url)
    # get page html
    html_content = driver.page_source

    # parse html with BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    """ find and filter the list of results """
    # find the relevant <div> elements and extract information
    div_elements = soup.find_all(
        'div', class_='product_detail_page_left_colum_author_name')

    book_links = {}
    book_author = ""
    for div_element in div_elements:
        title = div_element.find('h5').find(
            'a').text.strip().title()  # name of book
        link = div_element.find('h5').find('a')['href']  # link to book page
        book_author = div_element.find(
            'h6').text.strip().title()  # name of author

        if title == book:
            book_links[link] = book_author

    # exit if no book is found
    if len(book_links) == 0:
        print("No books of such name found.")
        return

    print("Displaying all versions of the book on website.")
    # open result pages
    for page in book_links:
        print()  # newline
        url = "https://readings.com.pk" + f"{page}"
        driver.get(url)
        # get new page html
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, "html.parser")

        # get book details
        title = soup.find('div', class_='books_detail_page_left_colum_author_name').find(
            'h5').contents[0].strip()
        price = soup.find('div', class_='books_our_price').find(
            'span', class_='linethrough').find_next_sibling('span')
        price = price.text.strip()

        # search if book is available
        try:
            driver.find_element(By.CLASS_NAME, "book_availability")
            print("Book is available.")

        except:
            try:
                # check if book is out of stock
                driver.find_element(By.CLASS_NAME, "out_off_stock")
                print("Out of Stock")

            except:
                # check if available for pre-order
                driver.find_element(By.CLASS_NAME, "pree_order")
                print("Available for Pre-Order")

        print(f"Title: {title}")
        print(f"Author: {book_links[page]}")
        print(f"Price: {price}")

        # provide option to open link in browser
        open_link(page)

    driver.quit()


def check_book_author():
    """search using book title and author (more precise)"""

    # get user input of book to check
    book = input("Enter book name: ").title()
    author = input("Enter author's full name: ").title()
    print("\nPlease wait while details are fetched")

    # result page upon searching
    url = f'https://readings.com.pk/Pages/searchresult.aspx?Keyword={book}'

    options = Options()
    options.add_argument("-headless")  # run Firefox in headless mode
    service = Service("geckodriver-v0.33.0-win64")  # path to gecko webdriver
    driver = webdriver.Firefox(service=service, options=options)

    driver.get(url)
    # get page html
    html_content = driver.page_source

    # parse html with BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    """ find and filter the list of results """
    # find the relevant <div> elements and extract information
    div_elements = soup.find_all(
        'div', class_='product_detail_page_left_colum_author_name')

    book_links = {}
    book_author = ""
    for div_element in div_elements:
        title = div_element.find('h5').find(
            'a').text.strip().title()  # name of book
        link = div_element.find('h5').find('a')['href']  # link to book page
        book_author = div_element.find(
            'h6').text.strip().title()  # name of author

        if book_author == author:
            book_links[link] = book_author

    # exit if no book is found
    if len(book_links) == 0:
        print("No books of such name found.")
        return

    print("Displaying all versions of the book on website.")
    # open result pages
    for page in book_links:
        print()  # newline
        url = "https://readings.com.pk" + f"{page}"
        driver.get(url)
        # get new page html
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, "html.parser")

        # get book details
        title = soup.find('div', class_='books_detail_page_left_colum_author_name').find(
            'h5').contents[0].strip()
        price = soup.find('div', class_='books_our_price').find(
            'span', class_='linethrough').find_next_sibling('span')
        price = price.text.strip()

        # search if book is available
        try:
            driver.find_element(By.CLASS_NAME, "book_availability")
            print("Book is available.")

        except:
            try:
                # check if book is out of stock
                driver.find_element(By.CLASS_NAME, "out_off_stock")
                print("Out of Stock")

            except:
                # check if available for pre-order
                driver.find_element(By.CLASS_NAME, "pree_order")
                print("Available for Pre-Order")

        print(f"Title: {title}")
        print(f"Author: {book_links[page]}")
        print(f"Price: {price}")

        # provide option to open link in browser
        open_link(page)

    driver.quit()
