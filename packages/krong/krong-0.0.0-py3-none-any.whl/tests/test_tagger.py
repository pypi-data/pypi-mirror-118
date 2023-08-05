from krong import Krong

tagger = Kltk(task="tagger", decomposition=False)
output = tagger("아버지가방에들어가신다")
print(output)