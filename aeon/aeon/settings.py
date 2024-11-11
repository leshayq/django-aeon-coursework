from pathlib import Path
import dotenv
import os

dotenv.load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    #user apps
    'shop.apps.ShopConfig',
    'users.apps.UsersConfig',
    'cart.apps.CartConfig',
    'payment.apps.PaymentConfig',

    #libraries
    'colorfield',
    'django.contrib.humanize',
    'django_email_verification',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'aeon.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'shop.context_processors.get_categories',
            ],
        },
    },
]

WSGI_APPLICATION = 'aeon.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'shop',
        'USER': os.getenv('USER'),
        'PASSWORD': os.getenv('PASSWORD'),
        'HOST':'localhost',
        'PORT': os.getenv('PORT'),
    }   
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'uk'

TIME_ZONE = 'Europe/Kiev'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'users.CustomUser'
AUTHENTICATION_BACKENDS = ['users.backends.EmailBackend']

#EMAIL VERIFICATION AND PASSWORD RECOVERY
def email_verified_callback(user):
    user.is_active = True

def password_change_callback(user, password):
    user.set_password(password)

EMAIL_FROM_ADDRESS = os.getenv('EMAIL_FROM_ADDRESS')  # mandatory
EMAIL_PAGE_DOMAIN = 'http://127.0.0.1:8000/'  # mandatory (unless you use a custom link)
EMAIL_MULTI_USER = False  # optional (defaults to False)

# Email Verification Settings (mandatory for email sending)
EMAIL_MAIL_SUBJECT = 'AEON| Підтвердження пошти'
EMAIL_MAIL_HTML = 'users/email/mail_body.html'
EMAIL_MAIL_PLAIN = 'users/email/mail_body.txt'
EMAIL_MAIL_TOKEN_LIFE = 60 * 60
# 60000 * 60000

# Email Verification Settings (mandatory for builtin view)
EMAIL_MAIL_PAGE_TEMPLATE = 'users/email/email_success_template.html'
EMAIL_MAIL_CALLBACK = email_verified_callback

# # Password Recovery Settings (mandatory for email sending)
# EMAIL_PASSWORD_SUBJECT = 'Change your password {{ user.username }}'
# EMAIL_PASSWORD_HTML = 'password_body.html'
# EMAIL_PASSWORD_PLAIN = 'password_body.txt'
# EMAIL_PASSWORD_TOKEN_LIFE = 60 * 10  # 10 minutes

# # Password Recovery Settings (mandatory for builtin view)
# EMAIL_PASSWORD_PAGE_TEMPLATE = 'password_changed_template.html'
# EMAIL_PASSWORD_CHANGE_PAGE_TEMPLATE = 'password_change_template.html'
# EMAIL_PASSWORD_CALLBACK = password_change_callback

# For Django Email Backend
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = os.getenv('EMAIL_FROM_ADDRESS')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')  # os.environ['password_key'] suggested
EMAIL_USE_TLS = True

