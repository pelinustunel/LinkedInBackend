from models.message_model import Message

messages = [
    # Pelin Üstünel (id: 2) ↔ Mevsim Gediz (id: 1)
    Message(
        message_id=1,
        sender_id="1",
        sender_name="Mevsim Gediz",
        sender_image="http://127.0.0.1:5003/images/mevsim.jpg",
        receiver_id="2",
        receiver_name="Pelin Üstünel",
        receiver_image="http://127.0.0.1:5003/images/pelin.jpg",
        content="Merhaba, nasılsın?",
        image_url="https://example.com/image1.png",
        timestamp="2025-02-21"
    ),
    Message(
        message_id=2,
        sender_id="2",
        sender_name="Pelin Üstünel",
        sender_image="http://127.0.0.1:5003/images/pelin.jpg",
        receiver_id="1",
        receiver_name="Mevsim Gediz",
        receiver_image="http://127.0.0.1:5003/images/mevsim.jpg",
        content="İyiyim, teşekkürler! Sen nasılsın?",
        image_url="",
        timestamp="2025-02-21"
    ),
    Message(
        message_id=3,
        sender_id="1",
        sender_name="Mevsim Gediz",
        sender_image="http://127.0.0.1:5003/images/mevsim.jpg",
        receiver_id="2",
        receiver_name="Pelin Üstünel",
        receiver_image="http://127.0.0.1:5003/images/pelin.jpg",
        content="Ben de iyiyim. Bootcamp’e katıldın mı bu dönem?",
        image_url="",
        timestamp="2025-02-22"
    ),
    Message(
        message_id=4,
        sender_id="2",
        sender_name="Pelin Üstünel",
        sender_image="http://127.0.0.1:5003/images/pelin.jpg",
        receiver_id="1",
        receiver_name="Mevsim Gediz",
        receiver_image="http://127.0.0.1:5003/images/mevsim.jpg",
        content="Evet, başladım! Proje geliştirme aşamasındayız şu an.",
        image_url="",
        timestamp="2025-02-22"
    ),
    Message(
        message_id=5,
        sender_id="1",
        sender_name="Mevsim Gediz",
        sender_image="http://127.0.0.1:5003/images/mevsim.jpg",
        receiver_id="2",
        receiver_name="Pelin Üstünel",
        receiver_image="http://127.0.0.1:5003/images/pelin.jpg",
        content="Harika, başarılar dilerim! ✨",
        image_url="",
        timestamp="2025-02-22"
    ),

    # Pelin Üstünel (id: 2) ↔ Cihan Kutlu (id: 3)
    Message(
        message_id=6,
        sender_id="3",
        sender_name="Cihan Kutlu",
        sender_image="http://127.0.0.1:5003/images/cihan.jpg",
        receiver_id="2",
        receiver_name="Pelin Üstünel",
        receiver_image="http://127.0.0.1:5003/images/pelin.jpg",
        content="Projeye buradan erişebilirsin.",
        image_url="",
        timestamp="2025-02-21"
    ),
    Message(
        message_id=7,
        sender_id="2",
        sender_name="Pelin Üstünel",
        sender_image="http://127.0.0.1:5003/images/pelin.jpg",
        receiver_id="3",
        receiver_name="Cihan Kutlu",
        receiver_image="http://127.0.0.1:5003/images/cihan.jpg",
        content="Tamamdır, çok teşekkür ederim! İnceleyeceğim.",
        image_url="",
        timestamp="2025-02-22"
    ),
    Message(
        message_id=8,
        sender_id="3",
        sender_name="Cihan Kutlu",
        sender_image="http://127.0.0.1:5003/images/cihan.jpg",
        receiver_id="2",
        receiver_name="Pelin Üstünel",
        receiver_image="http://127.0.0.1:5003/images/pelin.jpg",
        content="Herhangi bir sorun olursa haber ver, yardımcı olurum.",
        image_url="",
        timestamp="2025-02-22"
    ),

    # Pelin Üstünel (id: 2) ↔ Elif Yılmaz (id: 4)
    Message(
        message_id=9,
        sender_id="4",
        sender_name="Elif Yılmaz",
        sender_image="http://127.0.0.1:5003/images/aslihan.jpg",
        receiver_id="2",
        receiver_name="Pelin Üstünel",
        receiver_image="http://127.0.0.1:5003/images/pelin.jpg",
        content="LinkedIn profilin çok başarılı, tebrikler! 👏",
        image_url="",
        timestamp="2025-02-20"
    ),
    Message(
        message_id=10,
        sender_id="2",
        sender_name="Pelin Üstünel",
        sender_image="http://127.0.0.1:5003/images/pelin.jpg",
        receiver_id="4",
        receiver_name="Elif Yılmaz",
        receiver_image="http://127.0.0.1:5003/images/aslihan.jpg",
        content="Çok teşekkür ederim Elif, senin projeni de beğendim! 😊",
        image_url="",
        timestamp="2025-02-21"
    ),
    Message(
        message_id=11,
        sender_id="4",
        sender_name="Elif Yılmaz",
        sender_image="http://127.0.0.1:5003/images/aslihan.jpg",
        receiver_id="2",
        receiver_name="Pelin Üstünel",
        receiver_image="http://127.0.0.1:5003/images/pelin.jpg",
        content="Süpersin, başarılarının devamını dilerim! 🌸",
        image_url="",
        timestamp="2025-02-22"
    ),

    # Pelin Üstünel (id: 2) ↔ Ahmet Kara (id: 5)
    Message(
        message_id=12,
        sender_id="5",
        sender_name="Ahmet Kara",
        sender_image="http://127.0.0.1:5003/images/metehan.jpg",
        receiver_id="2",
        receiver_name="Pelin Üstünel",
        receiver_image="http://127.0.0.1:5003/images/pelin.jpg",
        content="Bootcamp hakkında bilgi verebilir misin? Nasıl ilerliyor?",
        image_url="",
        timestamp="2025-02-20"
    ),
    Message(
        message_id=13,
        sender_id="2",
        sender_name="Pelin Üstünel",
        sender_image="http://127.0.0.1:5003/images/pelin.jpg",
        receiver_id="5",
        receiver_name="Ahmet Kara",
        receiver_image="http://127.0.0.1:5003/images/metehan.jpg",
        content="Tabii ki! Oldukça yoğun ama çok verimli geçiyor 😊",
        image_url="",
        timestamp="2025-02-21"
    )
]

def get_next_message_id():
    """Yeni mesaj ID'sini döndürür."""
    return max(msg.message_id for msg in messages) + 1 if messages else 1
