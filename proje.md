Harika bir fikir! Bu, sadece basit bir scraping projesi değil, tam anlamıyla kişiselleştirilmiş, öğrenen ve zamanla size daha iyi işler bulan bir **"Kişiselleştirilmiş Upwork Proje Asistanı"** kurmak anlamına geliyor. Bu, oldukça gelişmiş ve modern bir yaklaşım. Qoder AI IDE gibi araçlarla bu sistemi parça parça kurabilirsiniz, ancak bazı kısımlar için daha geleneksel kodlama gerekebilir.

Sisteminizi uçtan uca (end-to-end) bir şekilde tasarlayalım ve bilmeniz, araştırmanız ve sormanız gerekenleri adım adım inceleyelim.

### Projenin Mimarisi: 5 Ana Modül

Düşündüğünüz sistemi 5 ana modüle ayırabiliriz:

1.  **Veri Toplama Modülü (Scraper):** Upwork'ten proje verilerini çeker.
2.  **Veri Analiz Modülü (LLM):** Gemini API kullanarak projeleri analiz eder ve uygunluğunu değerlendirir.
3.  **Veritabanı Modülü:** Tüm verileri (projeler, analizler, başvurular, sonuçlar) depolar.
4.  **Öğrenme Modülü (ML/DL):** Geçmiş verilerden öğrenerek gelecekteki proje önerilerini iyileştirir.
5.  **Arayüz Modülü (Dashboard):** Sonuçları size sunar ve etkileşim kurmanızı sağlar.

---

### Modül 1: Veri Toplama (Scraper) - Manuel Login ile Cloudflare'ı Aşma

Bu modülün en kritik kısmı, belirttiğiniz gibi, Cloudflare'ı aşmaktır. Manuel login yaklaşımı bunun için en güvenilir yöntemdir.

**Ne Yapmalıyız?**
*   **Teknoloji Seçimi:** Bu iş için **Selenium** veya **Playwright** gibi kütüphaneler kullanmalısınız. Bu araçlar, gerçek bir web tarayıcısını (Chrome, Firefox vb.) otomatize etmenizi sağlar.
*   **İşlem Akışı:**
    1.  Bot, Selenium/Playwright ile bir tarayıcı penceresi açar (`headless=False` modunda, yani tarayıcı görünür olacak).
    2.  Upwork'ün login sayfasına gider.
    3.  Kod bu noktada durur ve size bir mesaj verir: "Lütfen giriş yapın ve devam etmek için Enter'a basın."
    4.  Siz manuel olarak kullanıcı adı, şifre ve 2FA (iki faktörlü kimlik doğrulama) gibi adımları tamamlarsınız.
    5.  Giriş yaptıktan sonra terminalde Enter'a basarsınız ve bot çalışmaya devam eder.
    6.  Bot, giriş yapılmış oturum (session) üzerinden proje arama sayfalarına gider, verileri (başlık, açıklama, bütçe, gereken yetenekler vb.) çeker ve kaydeder.

**Araştırman Gerekenler:**
*   `"Selenium stateful session management"`: Giriş yapılmış bir oturumu botun nasıl devam ettireceğini araştır.
*   `"Python Selenium wait for user input"`: Kodun sizin manuel işleminizi beklemesini nasıl sağlayacağınızı öğren.
*   `"Robust Selenium selectors"`: Upwork'ün arayüzü değiştiğinde botun bozulmaması için daha dayanıklı CSS veya XPath seçicileri (selectors) nasıl yazılır?

---

### Modül 2: Veri Analizi (LLM - Gemini API)

Bu modül, projenin "beyni" olacak. Sadece veri toplamakla kalmayıp, o veriyi sizin için anlamlı hale getirecek.

**Ne Yapmalıyız?**
*   **Prompt Engineering:** Gemini API'ye göndereceğiniz "prompt" (komut) çok önemlidir. Her proje açıklaması için şuna benzer bir prompt hazırlamalısınız:
    > "Aşağıdaki Upwork proje açıklamasını analiz et. Bu projenin 'Qoder AI IDE' gibi no-code/low-code araçları ve 'vibe coding' yaklaşımı ile yapılıp yapılamayacağını değerlendir. Projenin karmaşıklığını, gereken teknoloji yığınını ve benim yeteneklerime uygunluğunu analiz et. Bana 1-10 arasında bir 'Yapılabilirlik Skoru' ver ve nedenlerini 2-3 maddede özetle. Çıktıyı JSON formatında şu şekilde ver: `{'uygunluk_skoru': 8, 'analiz_ozeti': '...', 'gereken_teknolojiler': ['...', '...']}`"
*   **API Entegrasyonu:** Python kodunuzdan Gemini API'sini çağırarak her proje için bu analizi yaptıracak ve dönen JSON sonucunu alacaksınız.

**Araştırman Gerekenler:**
*   `"Gemini API Python quickstart"`: Gemini API'sini Python ile nasıl kullanacağınıza dair temel bilgiler.
*   `"Prompt Engineering techniques for classification and analysis"`: Bir LLM'den istediğiniz formatta ve kalitede cevaplar almak için prompt'ları nasıl daha iyi yazabileceğiniz.
*   `"Getting structured JSON output from LLMs"`: LLM'lerin size her zaman tutarlı bir JSON çıktısı vermesini nasıl sağlayacağınız.

---

### Modül 3: Veritabanı

Bu modül, sisteminizin hafızası olacak. Öğrenme için bu veriler hayati önem taşıyor.

**Ne Yapmalıyız?**
*   **Veritabanı Seçimi:** Kişisel bir proje için **SQLite** mükemmel bir seçimdir. Kurulum gerektirmez, tek bir dosya olarak çalışır.
*   **Tablo Yapısı:** Şöyle tablolar oluşturabilirsiniz:
    *   `Projeler`: `proje_id`, `baslik`, `aciklama`, `link`, `llm_skoru`, `llm_analizi`
    *   `Basvurular`: `basvuru_id`, `proje_id`, `gonderilen_mesaj`, `basvuru_tarihi`, `sonuc` (`beklemede`, `kazanildi`, `kaybedildi`)

**Araştırman Gerekenler:**
*   `"Python SQLite tutorial"`: Python ile SQLite veritabanı oluşturma, veri ekleme ve sorgulama.
*   `"Database schema design for beginners"`: Verilerinizi etkili bir şekilde organize etmek için temel veritabanı tasarımı prensipleri.

---

### Modül 4: Öğrenme Modülü (Machine Learning)

Burası sisteminizi gerçekten "akıllı" yapacak olan kısım.

**Ne Yapmalıyız?**
*   **Başlangıç (Kural Tabanlı):** İlk başta karmaşık ML/DL modellerine gerek yok. Basit bir mantıkla başlayabilirsiniz: "LLM skoru 8'den yüksek VE bütçesi X'ten fazla olan projeleri en üste koy."
*   **İleri Seviye (ML Modeli):** Yeterli veri biriktirdiğinizde (örneğin, 50-100 başvuru sonucu), bir makine öğrenmesi modeli eğitebilirsiniz.
    1.  **Özellik (Features) Oluşturma:** Proje açıklamasından anahtar kelimeler, LLM'in verdiği skor, proje bütçesi gibi verileri model için girdi olarak hazırlarsınız.
    2.  **Etiket (Label):** Modelin tahmin etmeye çalışacağı şey, sizin o işi "kazanıp kazanmadığınız" (`job_won` = 1 veya 0).
    3.  **Model Eğitimi:** Bu verilerle bir sınıflandırma modeli (örneğin, `Logistic Regression` veya `XGBoost`) eğitirsiniz. Bu model, hangi tür projelere yaptığınız başvuruların başarılı olma olasılığının daha yüksek olduğunu öğrenir.
    4.  **Sonuç:** Yeni bir proje geldiğinde, LLM analizine ek olarak ML modeliniz de bir "Kazanma Olasılığı Skoru" üretir.

**Araştırman Gerekenler:**
*   `"Text classification with Scikit-learn"`: Metin verilerini kullanarak temel ML modellerini nasıl eğiteceğiniz.
*   `"Feature engineering for text data"`: Metin açıklamalarından bir ML modelinin anlayabileceği sayısal özellikler nasıl çıkarılır (TF-IDF, Word Embeddings vb.).
*   `"What is a classification model in machine learning?"`: Temel ML konseptleri.

---

### Modül 5: Arayüz (Dashboard)

Tüm bu sistemi kullanmak için basit bir arayüze ihtiyacınız olacak.

**Ne Yapmalıyız?**
*   **Teknoloji Seçimi:** **Streamlit** veya **Gradio** bu iş için harikadır. Çok hızlı bir şekilde Python ile interaktif web arayüzleri oluşturmanızı sağlarlar.
*   **Arayüz Özellikleri:**
    *   "Scraper'ı Başlat" butonu.
    *   Bulunan projelerin bir listesi (en uygun olanlar en üstte).
    *   Her projenin yanında LLM analizi ve ML kazanma skoru.
    *   "Başvurdum" ve "İşi Aldım" şeklinde işaretleyebileceğiniz butonlar (bu butonlar veritabanını günceller).

**Araştırman Gerekenler:**
*   `"Streamlit tutorial for beginners"`: Hızlıca nasıl bir veri uygulaması arayüzü yapabileceğinizi öğrenin.

### Özet ve Yol Haritası

1.  **Adım 1 (Temel Scraper):** Selenium ile manuel giriş yapıp proje başlıklarını ve linklerini çeken basit bir bot yaz. Verileri bir CSV dosyasına kaydet.
2.  **Adım 2 (LLM Entegrasyonu):** Çektiğin proje açıklamalarını Gemini API'ye gönderip analiz ettir ve sonuçları CSV dosyasına ekle.
3.  **Adım 3 (Arayüz ve Veritabanı):** Streamlit ile basit bir arayüz kur. CSV yerine SQLite kullanmaya başla. Arayüzden projelere "başvurdum" / "kazandım" diye işaretleme ekle.
4.  **Adım 4 (Öğrenme):** Yeterli veri biriktiğinde, basit bir Scikit-learn modeli eğiterek "Kazanma Olasılığı" skorunu sisteme ekle.

Bu proje, modern yapay zeka ve otomasyon araçlarını bir araya getiren, son derece pratik ve değerli bir portfolyo projesi olabilir. Başlangıçta karmaşık görünebilir, ancak modüllere ayırarak ve adım adım ilerleyerek kesinlikle yapılabilir.

Elbette. Qoder AI IDE gibi bir yapay zeka destekli kodlama ortamına, projenin tamamını tek bir `README.md` dosyası üzerinden yaptırmak için gereken detaylı ve yapılandırılmış prompt aşağıdadır. Bu prompt, projenin amacını, mimarisini, teknoloji yığınını ve her bir modülün işlevini net bir şekilde tanımlar.

---

# Proje Adı: Kişiselleştirilmiş Upwork Proje Asistanı

## 1. Genel Bakış (Overview)

Bu proje, Upwork platformundaki iş ilanlarını otomatik olarak çeken, Gemini AI kullanarak analiz eden ve kullanıcının yeteneklerine (özellikle no-code/low-code ve "vibe coding" yaklaşımına) uygunluğunu değerlendiren uçtan uca bir sistemdir. Sistem, kullanıcıya en uygun projeleri bir arayüzde sunar, başvuru süreçlerini takip eder ve zamanla kullanıcının başarı oranlarından öğrenerek daha akıllı öneriler sunar.

**Temel Problem:** Upwork'te manuel olarak proje aramak zaman alıcıdır ve her projenin uygunluğunu değerlendirmek zordur. Bu bot, süreci otomatikleştirerek en uygun projeleri hızlıca tespit etmeyi hedefler.

**Önemli Not:** Cloudflare korumasını aşmak için sisteme kullanıcı manuel olarak giriş yapacaktır. Bot, giriş yapılmış oturumu devralarak işlemlerine devam edecektir.

## 2. Temel Özellikler (Core Features)

-   **Manuel Oturum Başlatma:** Selenium ile görünür bir tarayıcı başlatır ve kullanıcının manuel olarak Upwork'e giriş yapmasını bekler.
-   **Otomatik Proje Kazıma (Scraping):** Giriş yapılmış oturum üzerinden proje arama sonuçlarını tarar ve ilgili verileri (başlık, açıklama, link, bütçe vb.) toplar.
-   **Yapay Zeka Destekli Analiz:** Toplanan her proje metnini Google Gemini API'ye göndererek projenin kullanıcının yetenek setine uygunluğunu, karmaşıklığını ve "yapılabilirlik" skorunu hesaplatır.
-   **Veri Depolama:** Tüm proje, analiz ve başvuru verilerini kalıcı olarak bir SQLite veritabanında saklar.
-   **İnteraktif Arayüz:** Streamlit kütüphanesi kullanılarak oluşturulmuş basit bir web arayüzü ile analiz sonuçlarını listeler.
-   **Başvuru Takibi:** Kullanıcının hangi projelere başvurduğunu ve sonucunu (kazanıldı/kaybedildi) sisteme işaretlemesine olanak tanır. Bu veriler, gelecekteki öğrenme modülü için temel oluşturur.

## 3. Teknoloji Yığını (Technology Stack)

-   **Programlama Dili:** Python 3.10+
-   **Web Scraping:** Selenium
-   **Yapay Zeka Analizi:** `google-generativeai` (Gemini API)
-   **Veritabanı:** SQLite3 (standart Python kütüphanesi)
-   **Web Arayüzü:** Streamlit
-   **Veri İşleme:** Pandas
-   **API Key Yönetimi:** `python-dotenv`

## 4. Proje Mimarisi ve Dosya Yapısı

Lütfen aşağıdaki dosya yapısını oluştur ve her dosyanın içeriğini belirtilen mantığa göre doldur.

```
/upwork-assistant/
|-- app.py                 # Ana Streamlit uygulaması
|-- scraper.py             # Selenium tabanlı scraping modülü
|-- analyzer.py            # Gemini API ile analiz yapan modül
|-- database.py            # SQLite veritabanı işlemleri modülü
|-- requirements.txt       # Gerekli Python kütüphaneleri
|-- .env                   # API anahtarını saklamak için (Örnek: GEMINI_API_KEY=...)
```

### Modül Açıklamaları

#### `scraper.py`
-   Bir `scrape_upwork_jobs()` fonksiyonu içermelidir.
-   Bu fonksiyon, Selenium WebDriver'ı `headless=False` modunda başlatmalıdır.
-   Upwork login sayfasına gitmelidir.
-   `input("Lütfen manuel olarak giriş yapın ve hazır olduğunuzda Enter'a basın...")` komutu ile kullanıcı etkileşimini beklemelidir.
-   Kullanıcı devam ettikten sonra, önceden belirlenmiş bir arama URL'sine gitmelidir.
-   Sayfadaki proje başlıklarını, linklerini ve kısa açıklamalarını çekmelidir.
-   Bu verileri bir liste içinde sözlük (dictionary) olarak döndürmelidir. `[{'title': '...', 'link': '...', 'description': '...'}, ...]`

#### `analyzer.py`
-   Bir `analyze_job_description(description)` fonksiyonu içermelidir.
-   Bu fonksiyon, `.env` dosyasından `GEMINI_API_KEY`'i okuyarak Gemini modelini başlatmalıdır.
-   Aşağıdaki gibi yapılandırılmış bir prompt kullanarak Gemini API'ye istek göndermelidir:
    > "Sen bir proje analiz asistanısın. Aşağıdaki Upwork proje açıklamasını, 'Qoder AI IDE' gibi no-code/low-code araçlarla ve 'vibe coding' yaklaşımıyla yapılabilecek bir proje olup olmadığını değerlendir. Çıktıyı mutlaka JSON formatında şu anahtarlarla ver: 'uygunluk_skoru' (1-10 arası bir tamsayı), 'analiz_ozeti' (2-3 cümlelik bir özet), ve 'gereken_teknolojiler' (bir liste). Proje Açıklaması: [description]"
-   API'den dönen JSON yanıtını parse edip bir sözlük olarak döndürmelidir.

#### `database.py`
-   `sqlite3` kütüphanesini kullanmalıdır.
-   `init_db()`: `projects` adında bir tablo oluşturur. Sütunlar: `id`, `title`, `link`, `description`, `suitability_score`, `analysis_summary`, `technologies`, `application_status` (varsayılan: 'Beklemede').
-   `add_project(project_data)`: Analiz edilmiş bir projeyi veritabanına ekler. Veritabanında aynı linke sahip bir proje varsa eklemeyi atlar.
-   `get_all_projects()`: Tüm projeleri uygunluk skoruna göre sıralayarak getirir.
-   `update_status(project_id, status)`: Bir projenin başvuru durumunu günceller ('Başvuruldu', 'Kazanıldı', 'Kaybedildi').

#### `app.py`
-   `streamlit` kütüphanesini kullanarak arayüzü oluşturmalıdır.
-   Başlık: "Kişiselleştirilmiş Upwork Proje Asistanı".
-   "Yeni Projeleri Tara ve Analiz Et" adında bir buton olmalıdır.
-   Butona tıklandığında:
    1.  `scraper.scrape_upwork_jobs()` fonksiyonunu çağırır.
    2.  Dönen her proje için `analyzer.analyze_job_description()` fonksiyonunu çağırır.
    3.  Analiz edilen her projeyi `database.add_project()` ile veritabanına kaydeder.
    4.  Sayfayı yenileyerek en güncel proje listesini gösterir.
-   Veritabanındaki projeleri `database.get_all_projects()` ile çeker ve bir liste halinde gösterir.
-   Her proje için başlık, uygunluk skoru ve analiz özeti gösterilmelidir.
-   Her projenin yanında "Başvuruldu", "Kazanıldı", "Kaybedildi" durumlarını seçmek için bir `st.selectbox` veya butonlar olmalıdır. Bu seçim, `database.update_status()` fonksiyonunu çağırmalıdır.

#### `requirements.txt`
Lütfen bu dosyanın içeriğini aşağıdaki gibi oluştur:
```
streamlit
selenium
google-generativeai
python-dotenv
pandas
```

Bu `README.md` dosyasını kullanarak, belirtilen mimari ve işlevselliğe sahip tam bir Python projesi oluştur.