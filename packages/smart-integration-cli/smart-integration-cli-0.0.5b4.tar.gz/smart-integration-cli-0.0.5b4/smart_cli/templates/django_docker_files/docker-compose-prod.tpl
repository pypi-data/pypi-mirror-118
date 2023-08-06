version: '3'
services:
  python: &python
    networks:
      - {{ params['network'] }}
    image: {{ params['registry'] }}/{{ params['project_name'] }}/{{ params['project_name'] }}
    build:
      context: .
      dockerfile: docker/prod/python/Dockerfile
    environment:
      - DJANGO_SETTINGS_MODULE={{ params['project_name'] }}.settings.prod
    volumes:
     - ~/.aws/:/root/.aws
    command: gunicorn -w 4 {{ params['project_name'] }}.wsgi -b 0.0.0.0:8000
    depends_on:
      - {{params['project_name'] }}_rabbitmq
      - {{params['project_name'] }}_celery_worker_default
  celery_worker_default:
    networks:
      - {{ params['network'] }}
    image: {{ params['registry'] }}/{{ params['project_name'] }}/{{ params['project_name'] }}_celery_worker_default
    <<: *python # up to copy of instance
    command: celery -A {{params['project_name'] }} worker --loglevel=info --max-tasks-per-child=1
    ports: []
    depends_on:
      - {{ params['project_name'] }}_rabbitmq
  celery_beat:
    networks:
      - {{ params['network'] }}
    image: {{ params['registry'] }}/{{ params['project_name'] }}/{{ params['project_name'] }}_celery_beat
    <<: *python # up to copy of instance
    command: celery -A {{params['project_name'] }} beat --loglevel=info
    ports: []
    depends_on:
      - celery_worker_default

networks:
  {{ params['network'] }}:
    external: true