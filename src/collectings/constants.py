DISPLAY_VIDEO_ADMIN = '<iframe width="150" height="150" src="{}"></iframe>'
MIN_REQUIRED_AMOUNT = 500
MAX_REQUIRED_AMOUNT = 99_999_999
MIN_PAYMENT_AMOUNT = 50
MAX_PAYMENT_AMOUNT = 999_999
STATUSES = (
    ('pending', 'Ожидает начисление'),
    ('waiting_for_capture', 'Ожидает списание'),
    ('succeeded', 'Успешно'),
    ('canceled', 'Отменено')
)
