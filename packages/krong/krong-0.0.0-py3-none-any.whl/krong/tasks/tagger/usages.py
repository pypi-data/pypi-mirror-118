USAGE_EN = f"""
Tagger is the morpheme analyzer provided by Krong and is based on Pynori, the pure Python morpheme analyzer.
For more details, please visit: https://github.com/gritmind/python-nori

1. The basic usage of Tagger is as follows.
>>> from krong import Krong
>>> tagger = Krong(task="tagger")
>>> tagger("아버지가방에들어가신다")
[('아버지', 'NNG'), ('가', 'JKS'), ('방', 'NNG'), ('에', 'JKB'), ('들어가', 'VV'), ('신다', 'EP+EC')]

2. Tagger has an option called `decomposition`. If you set this value to `True', you can decompose words into smaller units.
>>> from krong import Krong
>>> tagger = Krong(task="tagger", decomposition=True)
>>> tagger("아버지가방에들어가신다")
[('아버지', 'NNG'), ('가', 'JKS'), ('방', 'NNG'), ('에', 'JKB'), ('들어가', 'VV'), ('시', 'EP'), ('ㄴ다', 'EC')]
"""

USAGE_KO = f"""
Tagger는 Krong에서 제공하는 형태소 분석기로, 순수 파이썬 형태소 분석기인 Pynori를 기반으로 합니다.
Pynori에 대해 더 자세히 알아보려면 다음 주소로 접속하세요: https://github.com/gritmind/python-nori

1. Tagger의 기본적인 사용법은 아래와 같습니다.
>>> from krong import Krong
>>> tagger = Krong(task="tagger")
>>> tagger("아버지가방에들어가신다")
[('아버지', 'NNG'), ('가', 'JKS'), ('방', 'NNG'), ('에', 'JKB'), ('들어가', 'VV'), ('신다', 'EP+EC')]

2. Tagger는 `decomposition`이라는 옵션을 가지고 있는데, `True`로 설정하면 어절을 더 작은 단위로 분해할 수 있습니다.
>>> from krong import Krong
>>> tagger = Krong(task="tagger", decomposition=True)
>>> tagger("아버지가방에들어가신다")
[('아버지', 'NNG'), ('가', 'JKS'), ('방', 'NNG'), ('에', 'JKB'), ('들어가', 'VV'), ('시', 'EP'), ('ㄴ다', 'EC')]
"""
