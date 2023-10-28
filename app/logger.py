import logging


import logging

# 루트 로거 설정 초기화 (한 번만 실행)
if not logging.root.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s [%(name)-10s] %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    logging.basicConfig(level=logging.INFO, handlers=[handler])

def logger(mod_name):
    return logging.getLogger(mod_name)
