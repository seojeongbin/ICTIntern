DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # 사용할 엔진 설정
        'NAME': 'django_teamproject',  # 연동한 MYSQL의 데이터베이스 이름
        'USER': 'newuser_jeongbin',  # db 접속 계정명
        'PASSWORD': 'y18122606',  # 계정 비밀번호
        'HOST': 'localhost',  # 실제 db 주소
        'PORT': '3306',  # 포트번호
    }
}
SECRET_KEY = '9+-@6r^j5x)k-u+-25hi)t*k_94=yhft-8kv!8dk!5fmaen#u1'
