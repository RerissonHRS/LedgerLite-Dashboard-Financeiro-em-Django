# django-portfolio-dashboard

Projeto Django pensado para portfólio: autenticação, CRUD de vendas, dashboard com Chart.js, exportação para CSV/Excel e layout moderno com Bootstrap 5.

## Como rodar

```bash
cd backend
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Acesse: http://127.0.0.1:8000

## Dados de exemplo

Você pode popular com alguns registros via admin (/admin) ou criar pelo menu **Vendas**.

## Estrutura
- `dashboard` app com modelos, formulários e views
- templates com Bootstrap 5 e Chart.js
- exportação de dados (CSV/Excel)
- testes básicos

## Deploy rápido (Render/Heroku)
- Adicione `gunicorn` ao `requirements.txt`
- Crie `Procfile` com `web: gunicorn core.wsgi`
- Configure variáveis de ambiente e `ALLOWED_HOSTS`
