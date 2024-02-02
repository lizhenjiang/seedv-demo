from celery_app import app

if __name__ == '__main__':
    argv = [
        'worker',
        '--loglevel=info',
        '--concurrency=4',  # 例如，设置并发的worker数量
    ]
    app.worker_main(argv)