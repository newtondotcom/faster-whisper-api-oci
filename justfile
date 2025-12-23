duration:
    curl -X POST "http://localhost:5000/duration" \
        -H "Authorization: Bearer ${API_KEY:-your-api-key}" \
        -F "file=@test/videoplayback.mp3"

transcribe:
    time curl -X POST "http://localhost:5000/transcribe" \
        -H "Authorization: Bearer ${API_KEY:-your-api-key}" \
        -F "file=@test/videoplayback.mp3"
        
dev: 
    uv run main.py

generate-key:
    uv run python scripts/generate_key.py

health-prod:
    curl -X GET "https://fwao.myr-project.eu/health"

duration-prod: 
    curl -X POST "https://fwao.myr-project.eu/duration" \
        -H "Authorization: Bearer ${API_KEY:-your-api-key}" \
        -F "file=@test/videoplayback.mp3"

transcribe-prod: 
    curl -X POST "https://fwao.myr-project.eu/transcribe" \
        -H "Authorization: Bearer ${API_KEY:-your-api-key}" \
        -F "file=@test/videoplayback.mp3"