"""
i18n - Internationalisation des textes fixes
"""

class I18n:
    """Gère les traductions des textes fixes de l'application"""
    
    TRANSLATIONS = {
        'fr': {
            'by': 'Par',
            'chapter': 'Chapitre',
            'introduction': 'Introduction',
            'subtitle': "De 9 ans en CDI plongeur au lancement de Green SEO AI : l'histoire vraie d'un combat contre un faux diagnostic et pour la reconnaissance d'un trauma complexe.",
            'empty_chapter': '[Chapitre vide]'
        },
        'en': {
            'by': 'By',
            'chapter': 'Chapter',
            'introduction': 'Introduction',
            'subtitle': "From 9 years as a dishwasher to launching Green SEO AI: the true story of a fight against a misdiagnosis and for recognition of complex trauma.",
            'empty_chapter': '[Empty chapter]'
        },
        'es': {
            'by': 'Por',
            'chapter': 'Capítulo',
            'introduction': 'Introducción',
            'subtitle': "De 9 años como lavaplatos al lanzamiento de Green SEO AI: la historia real de una lucha contra un diagnóstico erróneo y por el reconocimiento del trauma complejo.",
            'empty_chapter': '[Capítulo vacío]'
        },
        'it': {
            'by': 'Di',
            'chapter': 'Capitolo',
            'introduction': 'Introduzione',
            'subtitle': "Da 9 anni come lavapiatti al lancio di Green SEO AI: la vera storia di una lotta contro una diagnosi errata e per il riconoscimento del trauma complesso.",
            'empty_chapter': '[Capitolo vuoto]'
        },
        'ru': {
            'by': 'Автор',
            'chapter': 'Глава',
            'introduction': 'Введение',
            'subtitle': "От 9 лет посудомойщиком до запуска Green SEO AI: правдивая история борьбы с неправильным диагнозом и за признание сложной травмы.",
            'empty_chapter': '[Пустая глава]'
        },
        'ja': {
            'by': '著者',
            'chapter': '章',
            'introduction': '紹介',
            'subtitle': "皿洗いとしての9年間からGreen SEO AIの立ち上げまで：誤診との闘いと複雑なトラウマの認識のための真実の物語。",
            'empty_chapter': '[空の章]'
        },
        'zh': {
            'by': '作者',
            'chapter': '章节',
            'introduction': '介绍',
            'subtitle': "从9年洗碗工到推出Green SEO AI：与误诊作斗争和争取复杂创伤认可的真实故事。",
            'empty_chapter': '[空章节]'
        },
        'hi': {
            'by': 'द्वारा',
            'chapter': 'अध्याय',
            'introduction': 'परिचय',
            'subtitle': "9 साल बर्तन धोने से लेकर Green SEO AI लॉन्च करने तक: गलत निदान के खिलाफ लड़ाई और जटिल आघात की मान्यता के लिए सच्ची कहानी।",
            'empty_chapter': '[खाली अध्याय]'
        },
        'ar': {
            'by': 'بواسطة',
            'chapter': 'الفصل',
            'introduction': 'مقدمة',
            'subtitle': "من 9 سنوات كغسال أطباق إلى إطلاق Green SEO AI: القصة الحقيقية للنضال ضد التشخيص الخاطئ ومن أجل الاعتراف بالصدمة المعقدة.",
            'empty_chapter': '[فصل فارغ]'
        },
        'de': {
            'by': 'Von',
            'chapter': 'Kapitel',
            'introduction': 'Einführung',
            'subtitle': "Von 9 Jahren als Tellerwäscher bis zur Gründung von Green SEO AI: Die wahre Geschichte eines Kampfes gegen eine Fehldiagnose und für die Anerkennung eines komplexen Traumas.",
            'empty_chapter': '[Leeres Kapitel]'
        },
        'pt': {
            'by': 'Por',
            'chapter': 'Capítulo',
            'introduction': 'Introdução',
            'subtitle': "De 9 anos como lavador de pratos ao lançamento do Green SEO AI: a verdadeira história de uma luta contra um diagnóstico errado e pelo reconhecimento de um trauma complexo.",
            'empty_chapter': '[Capítulo vazio]'
        },
        'tr': {
            'by': 'Yazan',
            'chapter': 'Bölüm',
            'introduction': 'Giriş',
            'subtitle': "9 yıl bulaşık yıkayıcısı olarak çalışmaktan Green SEO AI'ı kurmaya: yanlış teşhise karşı mücadele ve karmaşık travmanın tanınması için gerçek hikaye.",
            'empty_chapter': '[Boş bölüm]'
        },
        'ko': {
            'by': '저자',
            'chapter': '장',
            'introduction': '소개',
            'subtitle': "9년간 설거지부로 일하다 Green SEO AI 출시까지: 오진에 맞서 싸우고 복합 트라우마 인정을 위한 진실한 이야기.",
            'empty_chapter': '[빈 장]'
        },
        'id': {
            'by': 'Oleh',
            'chapter': 'Bab',
            'introduction': 'Pengenalan',
            'subtitle': "Dari 9 tahun sebagai pencuci piring hingga meluncurkan Green SEO AI: kisah nyata perjuangan melawan diagnosis yang salah dan untuk pengakuan trauma kompleks.",
            'empty_chapter': '[Bab kosong]'
        },
        'vi': {
            'by': 'Bởi',
            'chapter': 'Chương',
            'introduction': 'Giới thiệu',
            'subtitle': "Từ 9 năm làm người rửa bát đến ra mắt Green SEO AI: câu chuyện có thật về cuộc đấu tranh chống lại chẩn đoán sai và đòi công nhận chấn thương phức tạp.",
            'empty_chapter': '[Chương trống]'
        },
        'pl': {
            'by': 'Autor',
            'chapter': 'Rozdział',
            'introduction': 'Wprowadzenie',
            'subtitle': "Od 9 lat jako zmywacz naczyń do uruchomienia Green SEO AI: prawdziwa historia walki z błędną diagnozą i o uznanie złożonej traumy.",
            'empty_chapter': '[Pusty rozdział]'
        },
        'th': {
            'by': 'โดย',
            'chapter': 'บท',
            'introduction': 'บทนำ',
            'subtitle': "จากการเป็นล้างจาน 9 ปีสู่การเปิดตัว Green SEO AI: เรื่องราวจริงของการต่อสู้กับการวินิจฉัยที่ผิดและการยอมรับบาดแผลที่ซับซ้อน",
            'empty_chapter': '[บทว่าง]'
        }
    }
    
    @classmethod
    def get(cls, key: str, lang: str = 'fr') -> str:
        """
        Récupère une traduction
        
        Args:
            key: Clé de traduction ('by', 'chapter', etc.)
            lang: Code langue ('fr', 'en', 'es', etc.)
        
        Returns:
            str: Texte traduit
        """
        if lang not in cls.TRANSLATIONS:
            lang = 'fr'  # Fallback to French
        
        return cls.TRANSLATIONS.get(lang, {}).get(key, cls.TRANSLATIONS['fr'].get(key, ''))
    
    @classmethod
    def get_chapter_number(cls, number: int, lang: str = 'fr') -> str:
        """
        Retourne le texte 'Chapitre X' traduit
        
        Args:
            number: Numéro du chapitre
            lang: Code langue
        
        Returns:
            str: "Chapitre X" traduit (ex: "Chapter 1", "Capítulo 1")
        """
        chapter_word = cls.get('chapter', lang)
        return f"{chapter_word} {number}"

