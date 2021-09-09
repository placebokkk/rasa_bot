#!/bin/bash
docker run -v $(pwd):/app rasa/rasa:latest-full train nlu -d data/  --fixed-model-name nlu.model
#rasa rasa/rasa:latest-full train nlu -d data/  --fixed-model-name nlu.model
