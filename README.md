# Instagram Web Scraping With Selenium


![Instagram logo](instagram-logo.jpg)

[![Watch the video](thumbnail.png)](ig-web-scraping-demo.mp4)

Proyek ini adalah proyek intern saya yaitu scraping instagram web menggunakan Anaconda `Python 3.9.12` dan `Selenium 3.141.0`. Script untuk scraping berada di file `scratch_selenium.ipynb`. Script scraping ini mampu mengambil informasi dari data publik dari profike instagram orang, seperti jumlah posting, jumlah followers, jumlah following dan lain-lain. 


Ada beberapa hal yang perlu diperhatikan ketika menjalankan ini. Pastikan anda menonton video demo scraping instagram yang berada di directory yang sama. Teknik scraping yang saya gunakan tidak hanya Selenium, tetapi beberapa melalui hidden API dari instagram. Juga menggunakan script `keyboard` dan `mouse` yang mana script tersebut akan beraksi seperti layaknya kita menggunakan keyboard dan mouse secara fisik. Perlu ditekankan, ketika hendak menjalankan script, tidak jangan melakukan interupsi input berupa menggerakkan mouse, menggunakan keyboard, berpindah tab aplikasi. 


> Please note that web scraping may be against Instagram's terms of service, so use this script responsibly and consider the legal implications.


## Prerequisites
```py
!pip install selenium==3.141.0
!pip install webdriver-manager
!pip install requests==2.30.0
!pip install pygame
!pip install keyboard
!pip install mouse
```
Untuk dapat melakukan Web Scraping, anda perlu mendownload Chrome Driver (untuk kasus ini, saya melakukan scraping menggunakan Google Chrome). Lalu kemudian, letakkan pada lokasi berikut:
```
"C:/SeleniumDrivers/chromedriver.exe"
```
Silahkan membuat file baru di system `C:` dengan nama `SeleniumDrivers`.
Download versi Chrome Driver yang sesuai dengan versi Google Chrome anda.<br>

Download Chrome Driver:<br>
https://chromedriver.chromium.org/downloads

Cek versi Google Chrome:<br>
https://www.lifewire.com/check-version-of-chrome-5222040


## How to Run
Untuk menjalankan script, anda memerlukan akun Instagram dan mempersiapkan `username` & `password`. Saya sarankan akun yang kosong (fake) karena jika menggunakan akun IG anda yang asli MUNGKIN dapat menyebabkan akun anda terblokir atau hal lain yang tak diinginkan. Lalu kemudian untuk menjalankan script ini harus menggunakan VS Code dengan ukuran yang sesuai dengan yang ada di video.
1. Install requirement library
2. Download Chrome Driver
3. Put the Chrome Driver on this path `C:/SeleniumDrivers/chromedriver.exe`
4. You can edit or choose which instagram user you want to scrape, by edit it in variable `list_username`.
5. It's safe to click `run all`