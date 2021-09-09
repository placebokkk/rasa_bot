docker rm -f rasa_nlu_server
docker run -d --name rasa_nlu_server -p 5005:5005 -v $(pwd)/models:/app/models rasa/rasa:latest-full run --enable-api --model models/nlu.model.tar.gz
