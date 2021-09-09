'''
This tools could output intermediate result of each component
'''
from rasa.cli.utils import get_validated_path
from rasa.model import get_model, get_model_subdirectories
from rasa.core.interpreter import RasaNLUInterpreter
from rasa.shared.nlu.training_data.message import Message
import pathlib
from rasa.shared.nlu.constants import TEXT

def load_interpreter(model_dir, model):
    path_str = str(pathlib.Path(model_dir) / model)
    model = get_validated_path(path_str, "model")
    model_path = get_model(model)
    _, nlu_model = get_model_subdirectories(model_path)
    return RasaNLUInterpreter(nlu_model)

# Loads the model
model_dir='./models'
model='nlu.model.tar.gz'
mod = load_interpreter(model_dir, model)
# Parses new text
text="上海天气"
msg = Message({TEXT: text})
for p in mod.interpreter.pipeline:
    p.process(msg)
    print(msg.as_dict())
