# Rasa Bot

A demo bot using rasa

## 环境配置
**方法1**

安装rasa
```
conda create -n rasa python=3.7 
conda activate rasa
pip install rasa
```
可以使用rasa的cli命令进行训练，测试，部署.

**方法2**
直接使用rasa提供的docker镜像rasa/rasa:latest-full, 其中安装好了环境，并且把入口设为'rasa'指令，可以直接使用.
```
docker run -v $(pwd):/app rasa/rasa:latest-full train nlu -d data --fixed-model-name nlu.model
```

注意，docker的方式不能用于本地cli里测试nlu，需要用rasa指令。
```
rasa shell nlu -m models/nlu.model.tar.gz
```

[Rasa nlu pipeline 官方介绍](https://rasa.com/blog/intents-entities-understanding-the-rasa-nlu-pipeline/)

## 训练 NLU 模型
```
./run_train.sh
# rasa train nlu -d data --fixed-model-name nlu.model
```

## 在shell中测试NLU
```
rasa shell nlu -m models/nlu.model.tar.gz
```

## 通过Docker部署NLU http 服务
```
./run_server.sh
```

## 客户端请求
```
curl localhost:5005/model/parse -d '{"text":"明天张家港的出行指数"}'
```


## 数据格式

为了分别构建不同domian的数据，可以intent example, lookup table, regex, synonym map.分开写。但在训练时，data下的所有.yml文件(包括子目录)都会被rasa merge为一个文件。


```
# tree
data
├── chat
│   └── nlu.yml
├── common
│   ├── slot.common.city.yml
│   └── slot.common.date.yml
├── domain.yml
├── location
│   └── nlu.yml
├── movie
│   ├── nlu.yml
│   └── slot.movie.movie_name.yml
├── restaurant
│   └── nlu.yml
└── weather
    ├── nlu.yml
    ├── slot.weather.index.yml
    └── slot.weather.type.yml
```

**语义Schema的设计**:

在nlu的schema的设计上，查找饭店这个意图，可以放到location领域(或者叫skill技能)下面，location.query_restaurant意图, 也可以放在单独的restaurant领域下面，叫做restaurant.query意图。
哪一种方法好，可能要根据具体的应用场景。比如

* 查到了之后，用户说导航到这里。 对于前者，不涉及domain切换，对于后者，涉及domain切换。

* 查到了之后，用户说，这家店的特色菜有什么。对于前者，location下需要放更多意图。对于后者，restaurant是专门用于处理餐厅相关domain，更自然。


## 支持的Intent

Rasa没有多domain的概念，所有intent在同一级进行ranking, 本demo通过`domain.intent`来命名intent。


```
  - chat.greet 你好
  - chat.goodbye 再见
  - location.navi 导航到中关村
  - restaurant.query 我想吃四川菜
  - weather.query 后天苏州的天气
  - movie.query_rank 电影排行榜
  - movie.query_actor 神女的主演是谁
  - movie.query_by_actor 成龙演过的电影
  - movie.query_director 菊豆的导演是谁
  - movie.query_by_director 张艺谋演过的电影
```

## 响应格式

一些entity同时被DIETClassifier和RegexEntityExtractor提取两次。
```
{
    "text": "明天张家港的出行指数",
    "intent": {
        "id": 6897568374531625700,
        "name": "weather.query",
        "confidence": 0.9999915361404419
    },
    "entities": [
        {
            "entity": "common.date",
            "start": 0,
            "end": 2,
            "confidence_entity": 0.9986041188240051,
            "value": "明天",
            "extractor": "DIETClassifier"
        },
        {
            "entity": "common.city",
            "start": 2,
            "end": 5,
            "confidence_entity": 0.9813811779022217,
            "value": "张家港",
            "extractor": "DIETClassifier"
        },
        {
            "entity": "weather.index",
            "start": 6,
            "end": 10,
            "confidence_entity": 0.995211660861969,
            "value": "出行指数",
            "extractor": "DIETClassifier"
        },
        {
            "entity": "common.date",
            "start": 0,
            "end": 2,
            "value": "明天",
            "extractor": "RegexEntityExtractor"
        },
        {
            "entity": "common.city",
            "start": 2,
            "end": 5,
            "value": "张家港",
            "extractor": "RegexEntityExtractor"
        }
    ],
    "intent_ranking": [
        {
            "id": 6897568374531625700,
            "name": "weather.query",
            "confidence": 0.9999915361404419
        },
        {
            "id": 5381259472444820122,
            "name": "movie.query_director",
            "confidence": 4.065560005983571e-6
        },
        {
            "id": 6068329175557841786,
            "name": "movie.query_rank",
            "confidence": 1.1596364402066683e-6
        },
        {
            "id": -7391928109399037888,
            "name": "chat.greet",
            "confidence": 1.0092300044561853e-6
        },
        {
            "id": -7263337550355765766,
            "name": "movie.query_by_actor",
            "confidence": 9.354873782285722e-7
        },
        {
            "id": -1951018134331897348,
            "name": "location.navi",
            "confidence": 5.725630103370349e-7
        },
        {
            "id": -6620148514972248276,
            "name": "chat.goodbye",
            "confidence": 5.30417196387134e-7
        },
        {
            "id": 2850092206877808584,
            "name": "movie.query_actor",
            "confidence": 2.0090494956548355e-7
        },
        {
            "id": 2217385203066872523,
            "name": "location.query_restaurant",
            "confidence": 1.3091992379088424e-8
        },
        {
            "id": -2016087047650602818,
            "name": "location.query_others",
            "confidence": 4.1429810693216496e-9
        }
    ]
}
```

## NLU pipeline配置文件 config.yml
* 使用JiebaTokenizer
* 对于中文，RegexFeaturizer和RegexEntityExtractor均需要使用`use_word_boundaries: False`，否则生成的正则会在`entity`前后加上`\b`,变为`(\bentity1\b|\bentity2\b)`
* RegexFeaturizer仅根据Lookuptable/Regex提取feature，但是不保证该feature一定能将对应的部分标注为对应的Regex Entity Name，需要提供足够的example。
* RegexEntityExtractor直接根据Regex/LookupTable进行正则匹配，提取特征
* 第二个CountVectorsFeaturizer在中文里是否需要待确认？

```
language: zh

pipeline:
    - name: JiebaTokenizer
    - name: RegexFeaturizer 
      use_word_boundaries: False
    - name: CountVectorsFeaturizer
    - name: CountVectorsFeaturizer
      analyzer: "char_wb"
      min_ngram: 1
      max_ngram: 4
    - name: DIETClassifier
      epochs: 100
    - name: RegexEntityExtractor
      use_word_boundaries: False
    - name: EntitySynonymMapper
```

