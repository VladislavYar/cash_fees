<div align="center">
  <h1>cash_fees</h1>
  <h3>Описание</h3>
  <p>Rest API для веб-сервиса групповых денежных сборов.</p>
  <hr>
  <h3>Примечания</h3>
</div>
  <p align="center">Платежи интегрированы через сервис <a href="https://yookassa.ru/">ЮKassa</a>, <a href="https://github.com/yoomoney/yookassa-sdk-python">ссылка на SDK</a>.</p>
  <p align="center">В проекте доступна swagger-документация по адресу <code>/api/v1/docs/</code>.</p>
  <p align="center">Эндпоинты пользователя ограничены для простоты восприятия.</p>
  <p align="center">Поле <code>cover</code> может принимать как <code>base64-строку</code>, так и <code>slug</code> <i>дефолтной обложки</i>.</p>
  <p align="center">Эндпоинт <code>DELETE: /api/v1/collectings/{slug}/</code> не удаляет объект, а делает его неактивным.</p>
<hr>

<h3 align="center">Как запустить</h3>
<details>
  <p align="center"><summary align="center"><ins>Через Docker</ins></summary></p>
  <ul>
    <li align="center">1. Создать и заполнить файл <code>.env</code> в папке 
      <a href="https://github.com/VladislavYar/cash_fees/tree/main/infra"><code>infra</code></a> по шаблону 
        <a href="https://github.com/VladislavYar/cash_fees/blob/main/infra/.env.example"><code>.env.example</code></a>.
    </li>
    <li align="center">
      <p>2. Если имеется утилита <code>Make</code>, в корне проекта выполнить команду <code>make project-init</code>,</p>
      <p>иначе</p>
      <p>выполнить команду <code>docker compose -f ./infra/docker-compose.yml --env-file ./infra/.env up -d</code>.</p>
      <p><code>Docker</code> соберёт контейнеры с <code>postgreSQL</code>, <code>Сelery</code>, <b>приложением</b>, выполнит миграцию,</p>
      <p>заполнит БД тестовыми <i>платежами</i>, <i>групповыми сборами</i>, <i>дефолтными обложками</i>, <i>поводами для сбора</i>, <i>некоммерческими организациями</i>, <i>регионами</i>, <i>решаемыми проблемами</i> и <i>пользователями</i>, создаст superuser-a.</p>
      <p>После сервер будет доступен по адрессу: <code>http://127.0.0.1:8000/</code>.</p>
    </li>
    <li align="center">
      <p><b>Примечание</b></p>
      <p>3. В контейнер с приложением проброшен <code>volume</code> с кодом, изменение кода в проекте обновляет его в контейнере и перезапускает сервер.</p>
      <p>В mock-данныx генерируются изображения, на слабой вычислительной машине это может затянуть сбор контейнера.</p>
      <p>Для корректировки данной ситуации уменьшите количество/размер изображений в <a href="https://github.com/VladislavYar/cash_fees/blob/main/src/core/management/commands/test_data.py"><code>management command</code></a>.</p>
    </li>
    <li align="center">
      <p>4. Последующие запуски проекта осуществляются через команду <code>make project-start</code></p>
      <p>или</p>
      <p><code>docker compose -f ./infra/docker-compose-start.yml --env-file ./infra/.env up -d</code></p>
    </li>
  </ul>
</details>

<details>
  <p align="center"><summary align="center"><ins>Через консоль</ins></summary></p>
  <ul>
    <li align="center">1. Создать и заполнить файл <code>.env</code> в папке 
      <a href="https://github.com/VladislavYar/cash_fees/tree/main/infra"><code>infra</code></a> по шаблону 
        <a href="https://github.com/VladislavYar/cash_fees/blob/main/infra/.env.example"><code>.env.example</code></a>.
    </li>
    <li align="center">
      <p>2. Создать БД в <code>postgreSQL</code>.</p>
    </li>
    <li align="center">
      <p>3. Установить poetry <code>pip install poetry</code>.</p>
    </li>
    <li align="center">
      <p>4. Создать и активировать виртуальную оболочку <code>poetry shell</code>.</p>
    </li>
    <li align="center">
      <p>5. Установить зависимости <code>poetry install</code>.</p>
    </li>
    <li align="center">
      <p>6. Выполнить миграцию БД <code>python src/manage.py migrate</code>.</p>
    </li>
        <li align="center">
      <p>7. Создать superuser-a <code>python src/manage.py createsuperuser --noinput</code>.</p>
    </li>
    </li>
        <li align="center">
      <p>8. Заполнить БД тестовыми данными(<i>платежи, групповые сборы, дефолтные обложки, поводы для сбора, некоммерческие организации, регионы, решаемые проблемы и пользователи</i>) <code>python src/manage.py test_data</code>.</p>
    </li>
    <li align="center">
      <p><b>Примечание</b></p>
      <p>В mock-данныx генерируются изображения, на слабой вычислительной машине это может быть продолжительно.</p>
      <p>Для корректировки данной ситуации уменьшите количество/размер изображений в <a href="https://github.com/VladislavYar/cash_fees/blob/main/src/core/management/commands/test_data.py"><code>management command</code></a>.</p>
      <p>В проекте брокером сообщений и хранилищем для кэша используется <code>Redis</code>.</p>
    </li>
    </li>
        <li align="center">
      <p>9. Запустить сервер <code>python src/manage.py runserver</code>.</p>
    </li>
    <li align="center">
      <p>10. Сервер будет доступен по адрессу: <code>http://127.0.0.1:8000/</code>.</p>
    </li>
    <li align="center">
      <p>11. В новой консоле запустить worker <code>cd src/ && celery -A config worker -l debug --without-gossip --without-mingle --without-heartbeat -Ofair --pool=solo</code>.</p>
    </li>
    <li align="center">
      <p>12. В новой консоле запустить beat <code>cd src/ && celery -A config beat --loglevel=DEBUG</code>.</p>
    </li>
  </ul>
</details>
<hr>

<h3 align="center">Стек</h3>
<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12.3-red?style=flat&logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/Django-5.0.4-red?style=flat&logo=django&logoColor=white">
  <img src="https://img.shields.io/badge/Celery-5.4.0-red?style=flat&logo=celery&logoColor=white">
  <img src="https://img.shields.io/badge/DjangoRestFramework-3.15.1-red?style=flat">
  <img src="https://img.shields.io/badge/PostgreSQL-Latest-red?style=flat&logo=postgresql&logoColor=white">
  <img src="https://img.shields.io/badge/Redis-Latest-red?style=flat&logo=redis&logoColor=white">
  <img src="https://img.shields.io/badge/Docker-Latest-red?style=flat&logo=docker&logoColor=white">
  <img src="https://img.shields.io/badge/Swagger-Latest-red?style=flat&logo=swagger&logoColor=white">
  <img src="https://img.shields.io/badge/Poetry-Latest-red?style=flat&logo=poetry&logoColor=white">
  <img src="https://img.shields.io/badge/YookassaSdkPython-Latest-red?style=flat">
</p>
<hr>
