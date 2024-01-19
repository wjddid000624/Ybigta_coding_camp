import collections

from typing import Optional, Union, List

class Tokenizer():
    """
    BPE와 WordTokenizer의 공통적인 부분을 뽑아서 만든 class입니다.
    init 함수, add_corpus 함수, tokenize 함수를 구현합니다.
    """
    # corpus에는 문자열 리스트(List[str]) 또는 문자열(str)을 전달할 수 있습니다.
    def __init__(self, corpus: Optional[Union[List[str], str]] = None): 
        self.corpus = corpus if isinstance(corpus, list) else [corpus] if isinstance(corpus, str) else []
        self.vocab = collections.defaultdict(int)

        # corpus가 주어진 경우 vocab을 구축합니다.
        if self.corpus:
            self.build_vocab()

    def add_corpus(self, corpus: Union[List[str], str]) -> None:
        # corpus가 list면 그대로, string이면 리스트로 저장합니다.
        self.corpus = corpus if isinstance(corpus, list) else [corpus] if isinstance(corpus, str) else []
        
        # 기존 vocab에 새로운 corpus를 이용해 vocab을 추가한다.
        self.build_vocab() 

    # corpus를 이용해 vocab을 만든다.
    def build_vocab(self)->None:
        for sentence in self.corpus:
            tokens = sentence.split()
            for token in tokens:
                self.vocab[token] += 1

    # 객체 자체를 call해도 tokenize처럼 사용할 수 있어야 합니다.
    def __call__(self, text:Union[List[str], str], 
            padding: bool = False, 
            max_length: Optional[int] = None
            ) -> Union[List[List[int]], List[int]]:
        return self.tokenize(text, padding, max_length)


class BPETokenizer(Tokenizer):
    def __init__(self, corpus: Optional[Union[List[str], str]] = None): 
        super().__init__(corpus)
        self.bpe_codes = {}
    
    # vocab을 이용해 pair의 빈도수를 계산한다.
    def get_stats(self) -> dict:
        pairs = collections.defaultdict(int)
        for word, freq in self.vocab.items():
            symbols = word.split()
            for i in range(len(symbols) - 1):
                pairs[symbols[i], symbols[i + 1]] += freq
        return pairs

    def merge_tokens(self, pair: str, v_in: str) -> None: 
        merged_token = pair + v_in
        self.bpe_codes[pair, v_in] = merged_token

        new_vocab = collections.defaultdict(int)
        for word in self.vocab:
            new_word = word.replace(pair, merged_token).replace(v_in, merged_token)
            new_vocab[new_word] += self.vocab[word]

        self.vocab = new_vocab
    
    def train(self, n_iter: int) -> None:
        for i in range(n_iter):
            # pair들의 빈도 계산
            pairs = self.get_stats()
            if not pairs:
                break

            # 빈도가 가장 큰 pair 산출
            best = max(pairs, key=pairs.get)
            
            # 산출한 pair를 merge
            self.merge_tokens(*best)
            print(f"Iteration {i + 1}: Merged pair {best}")

    def tokenize(self, 
            text: Union[List[str], str], 
            padding: bool = False,
            max_length: Optional[int] = None
            ) -> Union[List[List[int]], List[int]]:

        if isinstance(text, str):
            text = [text]

        tokenized_texts = []
        for sentence in text:
            tokens = sentence.split()
            token_ids = [self.vocab[token] for token in tokens if token in self.vocab]
            tokenized_texts.append(token_ids)

        if max_length is not None:
            tokenized_texts = [text[:max_length] for text in tokenized_texts]

        if padding:
            max_len = max(len(text) for text in tokenized_texts)
            padded_texts = [text + [0] * (max_len - len(text)) for text in tokenized_texts]
            return padded_texts
        else:
            return tokenized_texts
    
class WordTokenizer(Tokenizer):
    """
    1. Corpus를 전부 whitespace 기준으로 split해서 각각을 token으로 취급하는 아주 간단한 tokenizer를 구현하시면 됩니다.
    2. BPETokenizer 와 거의 동일한 method들을 가지지만, 내부 구현은 당연히 다릅니다.
    3. 또한 WordTokenizer 는 train method를 가지며 동일한 기능을 하지만, iterate 과정이 없으므로 인자를 받지 않아도 됩니다. (단, 임의의 args 또는
    kwargs가 주어진다 해도 오류가 발생하지는 않아야 합니다.)
    가능하다면 상속을 통해 구현해보시기 바랍니다.
    """

    def train(self, n_iter: Optional[int] = None)-> None: 
        self.vocab["[UNK]"] = 1

        self.token2idx = {token: idx for idx, token in enumerate(self.vocab)}
        self.idx2token = {idx: token for idx, token in enumerate(self.vocab)}

    def tokenize(self, text:Union[List[str], str], 
            padding: bool = False, 
            max_length: Optional[int] = None
            ) -> Union[List[List[int]], List[int]]:
        if isinstance(text, str):
            text = [text]
        tokenized_text = []
        for sentence in text:
            tokenized_sentence = []
            for token in sentence.split():
                if token in self.token2idx:
                    tokenized_sentence.append(self.token2idx[token])
                else:
                    tokenized_sentence.append(self.token2idx["[UNK]"])
            tokenized_text.append(tokenized_sentence)

        
        if padding:
            max_len = max(len(text) for text in tokenized_text)
            padded_texts = [text + [0] * (max_len - len(text)) for text in tokenized_text]
            return padded_texts

        return tokenized_text