import argparse
import os, tarfile
from urllib.request import urlretrieve
from typing import Optional

from YBIGTA.tokenizers import BPETokenizer, WordTokenizer


def load_corpus(
    url: str = "https://huggingface.co/datasets/cnn_dailymail/resolve/main/data/cnn_stories.tgz",
    dl_name: str = "dataset.tgz",
    text_dir: str = "cnn/stories/",
    n: Optional[int] = None
) -> list[str]:
    if not os.path.exists(text_dir):
        if not os.path.exists(dl_name):
            urlretrieve(url, dl_name)
        tarfile.open(dl_name).extractall()

    ls = os.listdir(text_dir)[:n]
    dir_to_text = lambda f: open(text_dir + f, encoding='utf-8').read()
    dataset = [*map(dir_to_text, ls)]
    return dataset


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--use_bpe", type=bool, default=False)
    parser.add_argument("-c", "--n_corpus", type=int, default=40000)
    parser.add_argument("-i", "--n_iter", type=int, default=30000)
    args = parser.parse_args()

    use_bpe = args.use_bpe
    n_corpus = args.n_corpus
    n_iter = args.n_iter

    corpus = load_corpus(n=n_corpus)

    SelectedTokenizer = BPETokenizer if use_bpe else WordTokenizer
    tokenizer = SelectedTokenizer(corpus[2:n_corpus//2])
    tokenizer.add_corpus(corpus[n_corpus//2:])
    tokenizer.train(n_iter=n_iter)

    input_ids = tokenizer.tokenize(
        corpus[:10],
        padding=True,
        max_length=1024
    )

    print(input_ids)

