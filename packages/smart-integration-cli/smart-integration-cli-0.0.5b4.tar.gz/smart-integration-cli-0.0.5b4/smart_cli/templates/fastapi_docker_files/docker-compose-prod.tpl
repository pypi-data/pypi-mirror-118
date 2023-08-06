version: "3"
services:
  python: &python # link to instance
    image: {{ params['registry'] }}/{{ params['project_name'] }}/{{ params['project_name'] }}
    networks:
      - {{ params['network'] }}
    build:
      context: .
      dockerfile: docker/prod/python/Dockerfile
    volumes:
      - ~/.aws/:/root/.aws:ro
    ports:
      - 8000:8000
    environment:
      AWS_PROFILE: "default"
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000
    depends_on:
      - manage_app_rabbitmq
      - manage_app_celery_worker_default
  celery_worker_default:
    <<: *python # up to copy of instance
    image: {{ params['registry'] }}/{{ params['project_name'] }}/{{ params['project_name'] }}_celery_worker_default
    networks:
      - {{ params['network'] }}
    command: celery worker -A app.core.celery --loglevel info -c 3 --max-tasks-per-child 1
    # volumes:
    #   - "./:/src"
    ports: []
  celery_beat:
    <<: *python # up to copy of instance
    networks:
      - {{ params['network'] }}
    image: {{ params['registry'] }}/{{ params['project_name'] }}/{{ params['project_name'] }}_celery_beat
    command: celery -A app.core.celery beat --loglevel=info
    ports: []
      - manage_app_celery_worker_default

networks:
  {{ params['network'] }}:
    external: true