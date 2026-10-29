
cd query_assistant
docker-compose up -d

python load_data.py
cd ..

adk web --session_service_uri postgresql://admin:pass123@localhost:5433/adk_sessions
