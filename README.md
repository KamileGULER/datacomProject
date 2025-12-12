# DataCom Project 

## 1. Projenin Amacı

Bu projenin amacı, veri iletimi sırasında oluşan hataları tespit edebilen basit bir haberleşme sistemi tasarlamaktır.

Bunun için üç farklı program birlikte çalışmaktadır:

1. **Sender (Client 1 – Veri Gönderici)**
2. **Server (Aracı + Veri Bozucu)**
3. **Receiver (Client 2 – Veri Alıcı + Hata Denetleyici)**

Gönderici, kullanıcıdan aldığı metin için bir hata tespit bilgisi (parity biti) üretir ve bu bilgiyi veriyle birlikte sunucuya gönderir. Sunucu, paketin veri kısmını (DATA) çeşitli yöntemlerle bozarak alıcıya iletir. Alıcı, gelen veri üzerinden aynı kontrol bilgisini tekrar hesaplar ve gönderilen bilgi ile karşılaştırarak verinin yolda bozulup bozulmadığını anlar.

Proje **Python dili** ve **TCP soketleri** kullanılarak gerçekleştirilmiştir.

---

## 2. Sistem Mimarisi

Sistem üç ana bileşenden oluşur:

- **Sender (`sender.py`)**  
  Kullanıcıdan metin alır, parity hesaplar, paketi oluşturup sunucuya gönderir.

- **Server (`server.py`)**  
  Sender’dan paketi alır, DATA kısmını bozar, METHOD ve CHECKSUM alanlarını değiştirmeden paketi Receiver’a iletir.

- **Receiver (`receiver.py`)**  
  Server’dan paketi alır, parity bilgisini yeniden hesaplar ve gönderilen kontrol bilgisi ile karşılaştırarak hata olup olmadığını raporlar.

Bu üç program aynı bilgisayarda (localhost) çalışır ve TCP üzerinden haberleşir:

- Sender → Server: **127.0.0.1:5000**  
- Server → Receiver: **127.0.0.1:6000**

Hata tespit fonksiyonları ise ortak bir modülde tutulur:

- **`error_methods.py`** – Parity hesaplama fonksiyonlarını içerir ve hem Sender hem Receiver tarafından kullanılır.

---

## 3. Paket Formatı

Sistemde tüm mesajlar aşağıdaki formatta gönderilir:

```text
DATA|METHOD|CONTROL
DATA : Gönderilmek istenen metin (örneğin: deneme 12345555).

METHOD : Kullanılan hata tespit yöntemi. Bu projede "PARITY".

CONTROL : Gönderici tarafından hesaplanan kontrol bilgisi (even parity biti). "0" veya "1" şeklindedir.

Örneğin:
deneme 12345555|PARITY|0
bozmaz umarım|PARITY|1
Bu format, hem server hem receiver tarafından kullanılır. Server DATA kısmını bozsa bile METHOD ve CONTROL alanları değiştirilmez.

4. Hata Tespit Yöntemi: Even Parity (Çift Parite)
Projede hata tespiti için even parity (çift parite) kullanılmıştır.

Temel mantık:

Metin önce UTF-8 ile bytes haline getirilir.

Tüm byte’larda kaç tane 1 biti olduğu sayılır.

Eğer 1’lerin sayısı çift ise parity biti 0 seçilir.

Eğer 1’lerin sayısı tek ise parity biti 1 seçilir.

Gönderici bu parity bitini CONTROL alanına yazar. Alıcı, gelen veri için aynı hesabı tekrar yapar:

Gönderilen parity == Hesaplanan parity → Hata yok

Gönderilen parity != Hesaplanan parity → Hata var

Bu hesaplama fonksiyonu error_methods.py içinde tanımlıdır ve hem sender hem receiver tarafından ortak kullanılır. Böylece iki tarafta da aynı algoritma çalışmış olur.

5. Dosyaların Görevleri
5.1 error_methods.py
Hata tespiti fonksiyonlarının bulunduğu modüldür.

Ana fonksiyon örneği:
calculate_checksum(data: bytes, method: str) -> str
Şu anda yalnızca "PARITY" yöntemini destekler:

method == "PARITY" ise parity hesaplanır ve "0" veya "1" string’i döndürülür.

İleride CRC, Hamming, Checksum gibi yöntemler eklenmek istenirse aynı fonksiyon genişletilebilir.

5.2 sender.py – Client 1 (Veri Gönderici)
Görev adımları:

Kullanıcıdan şu şekilde metin alır:

Göndermek istediğin metni gir: deneme 12345555
Hata tespit yöntemi olarak "PARITY" seçilir.

Metin UTF-8 ile bytes’a çevrilir.

calculate_checksum fonksiyonu çağrılarak parity biti hesaplanır.

Paket şu formatta oluşturulur:

deneme 12345555|PARITY|0
Sender, TCP soketi ile 127.0.0.1:5000 adresine bağlanır ve bu paketi server’a gönderir.

"Paket server'a gönderildi." mesajını yazar ve bağlantıyı kapatır.

Sender, verinin yolda bozulup bozulmadığını bilmez; sadece doğru kontrol bilgisiyle paket üretmekten sorumludur.

5.3 server.py – Server (Aracı + Veri Bozucu)
Görev adımları:

127.0.0.1:5000 adresinde sender’dan gelecek bağlantıyı dinler.
Ekranda şu mesaj görülür:

Server dinlemede: 127.0.0.1:5000
Sender bağlandığında gelen paketi alır ve ekrana yazar:

Sender'dan gelen paket: deneme 12345555|PARITY|0
packet.rsplit("|", 2) kullanarak paketi üç parçaya ayırır:

data_str → deneme 12345555

method → PARITY

checksum → 0

Sadece DATA kısmını bozar. Bunun için çeşitli hata enjeksiyon fonksiyonları kullanılır:

char_substitution – Rastgele bir karakteri başka bir karakterle değiştirir.

char_deletion – Rastgele bir karakteri siler.

char_insertion – Rastgele bir yere yeni bir karakter ekler.

char_swapping – Yan yana iki karakterin yerini değiştirir.

flip_random_bit_in_char – Bir karakterin bir bitini çevirir (bit flip).

multiple_bit_flips – Birden fazla bit çevirir.

burst_error – Bir blok veri üzerinde toplu bozulma yapar.

Hangi yöntemin kullanılacağı corrupt_data_randomly fonksiyonu içinde rastgele seçilir.
Bazı çalıştırmalarda hiç hata uygulanmaması için "No error applied" seçeneği de bulunmaktadır.

Bozulmuş veriyi ekrana yazar:

Asıl DATA: deneme 12345555
Bozulmuş DATA: de4o{e 12345555
Yeni paketi oluşturur:

de4o{e 12345555|PARITY|0
Burada METHOD ve CHECKSUM aynen korunur.

127.0.0.1:6000 adresine bağlanarak bu yeni paketi receiver’a gönderir.

5.4 receiver.py – Client 2 (Veri Alıcı + Hata Denetleyici)
Görev adımları:

127.0.0.1:6000 adresinde server’dan gelecek bağlantıyı dinler:

Listening on 127.0.0.1:6000...
Server bağlandığında gelen paketi alır:

Received package: de4o{e 12345555|PARITY|0
Paketi data_str, method, received_checksum olarak ayırır:

Received Data : de4o{e 12345555

Method : PARITY

Sent Check Bits : 0

data_str tekrar UTF-8 ile bytes’a çevrilir.

calculate_checksum(data_bytes, method) fonksiyonu ile parity yeniden hesaplanır:

Computed Check Bits : 1 (örnek senaryoda böyle çıkmıştır)

Gönderilen ve hesaplanan parity karşılaştırılır:

Eşit değilse:

Error detected in the received data!
Eşitse:

No error detected in the received data.
Bu şekilde alıcı, verinin iletim sırasında bozulup bozulmadığına karar verir.

6. Örnek Çalışma ve Çıktılar
Aşağıdaki iki örnek, sistemin hem “hata var” hem de “hata yok” durumlarında nasıl çalıştığını göstermektedir.
Ekran görüntüleri sender, server ve receiver çıktılarından alınmıştır.

6.1 Senaryo 1 – Veri Bozuluyor, Hata Tespit Ediliyor
Sender girdisi: deneme 12345555

Gönderilen paket: deneme 12345555|PARITY|0

Server tarafında:

Paket şu şekilde alınır:

Sender'dan gelen paket: deneme 12345555|PARITY|0
METHOD : PARITY, CHECKSUM: 0 olarak görüntülenir.

Hata enjeksiyon yöntemi olarak burst_error seçilmiştir:

[DEBUG] Error method used: burst_error
Bozulmuş veri:

Bozulmuş DATA: de4o{e 12345555
Receiver’a gönderilen yeni paket:

de4o{e 12345555|PARITY|0
Receiver tarafında:

Gelen paket:

Received package: de4o{e 12345555|PARITY|0
Gönderilen parity:

Sent Check Bits : 0
Hesaplanan parity:

Computed Check Bits : 1
Sonuç:

Error detected in the received data!
Bu senaryoda server veriyi değiştirdiği için parity değeri değişmiş, alıcı da bu farkı tespit etmiştir.

6.2 Senaryo 2 – Veri Değişmiyor, Hata Tespit Edilmiyor
Sender girdisi: bozmaz umarım

Gönderilen paket: bozmaz umarım|PARITY|1

Server tarafında:

Paket:

Sender'dan gelen paket: bozmaz umarım|PARITY|1
Asıl DATA: bozmaz umarım, CHECKSUM: 1

Bu çalıştırmada hata uygulanmamıştır:

[DEBUG] No error applied.
Bozulmuş veri aynı kalır:

Bozulmuş DATA: bozmaz umarım
Receiver’a gönderilen paket:

bozmaz umarım|PARITY|1
Receiver tarafında:

Gelen paket:

Received package: bozmaz umarım|PARITY|1
Gönderilen parity:

Sent Check Bits : 1
Hesaplanan parity:

Computed Check Bits : 1
Sonuç:

No error detected in the received data.
Bu senaryoda server veriyi bozmadığı için parity değişmemiş, alıcı da verinin doğru iletildiğini kabul etmiştir.

7. Sonuç
Bu projede, Python ve TCP soketleri kullanılarak üç bileşenli bir haberleşme sistemi geliştirilmiştir:

Sender, kullanıcıdan aldığı metin için even parity kullanarak kontrol biti üretmiş ve paketi DATA|METHOD|CONTROL formatında sunucuya göndermiştir.

Server, paketlerin DATA kısmını çeşitli hata enjeksiyon yöntemleriyle bozarak, gerçek hayattaki “hatalı kanal (noisy channel)” davranışını simüle etmiştir.

Receiver, gelen veri için parity’yi yeniden hesaplamış, gönderilen kontrol bitleriyle karşılaştırmış ve verinin bozulup bozulmadığına başarılı bir şekilde karar vermiştir.

Ekran görüntüleriyle gösterilen örneklerde:

Veri bozulduğunda: Error detected in the received data!

Veri bozulmadığında: No error detected in the received data.

mesajlarının üretildiği açıkça görülmektedir.

Kod yapısı modüler olduğu için, bu altyapı üzerine CRC, Hamming kodu, 2D parity gibi daha gelişmiş hata tespit ve düzeltme yöntemleri de kolayca eklenebilir
