from typing import List
from .onehot import (
    assign_two_ctx, assign_one_ctx_and_trgt, assign_missing_ctx,
    assign_random_to_unused)
import numpy as np


def eiei_crossed(encoded: List[int],
                 tokenlist_size: int,
                 embed_dim: int = 300,
                 max_context_size: int = 10,
                 max_patience: int = 5,
                 sigma: float = None,
                 dtype=np.float16,
                 random_state: int = None,
                 shuffle: str = None,
                 fill: bool = True
                 ) -> np.ndarray:
    """Extreme Input Embedding Initialization (EIEI) for Multi-Label Inputs
    """
    # Initialize embedding weight matrix with 0s
    emb = np.zeros(shape=(tokenlist_size, embed_dim), dtype=dtype)

    # scale the std. dev. of the random number depending on the embedding size
    if sigma is None:
        sigma = 0.1 / embed_dim

    # set random seed
    if random_state is not None:
        np.random.seed(random_state)

    # Number of columns available for each context size
    maxcols = embed_dim // (max_context_size // 2)
    n_block = 0

    # read dimensions
    n_seqlen, k = encoded.shape

    # (1) The outer For-loop to increment `context_size`
    for context_size in range(2, max_context_size + 1, 2):
        # (1b) Position Indicies of the Target ID and Context IDs
        ctx_pos = list(range(context_size + 1))
        trgt_pos = ctx_pos.pop(context_size // 2)

        # (1c.1) Create new training examples (multi-label)
        num = context_size + 1
        examples = [encoded[i:(i + num), :] for i in range(n_seqlen - num)]
        examples, freq = np.unique(examples, axis=0, return_counts=True)

        # (1d) Context Vector Weights
        t = np.arange(context_size) - context_size // 2 + .5
        t = np.exp(-np.abs(t) * 1. / 3.)
        v = t / t.sum()

        # (1/2) Reset counter
        cnt = np.zeros((len(examples),), dtype=int)
        patience = 0
        offset = 0

        while patience < max_patience:
            # (1/2b) only select unused examples, i.e. use each example once!
            idx = np.where(cnt == 0)[0]

            if idx.size == 0:
                break

            # (2d) shuffle indicies
            if shuffle in (True, 'equal'):
                idx = np.random.permutation(idx)
            elif shuffle in ('frequent', 'most_common'):
                idx = np.random.choice(
                    idx, size=len(idx), replace=False,
                    p=freq[idx] / freq[idx].sum())
            elif shuffle in ('rare', 'edge_cases'):
                idx = np.random.choice(
                    idx, size=len(idx), replace=False,
                    p=(1. / freq[idx]) / (1. / freq[idx]).sum())

            # (2) Loop over training examples
            offset = offset % maxcols
            for a in idx:
                exbase = examples[a]
                for shift in range(k):
                    # create new combinations by replacing the target ID
                    ex = exbase.copy()
                    colidx = np.roll(np.arange(k), shift)
                    ex[trgt_pos, :] = exbase[trgt_pos, colidx]

                    # Assign embedding weights in the next column
                    e = (shift + offset) % maxcols + n_block * maxcols

                    # (3) loop over each dimension
                    for m in range(k):
                        # (3a) read target ID `i` and context IDs `j`
                        i = ex[trgt_pos, m]
                        j = ex[ctx_pos, m]

                        # (3b) initialize the first example always randomly
                        if (emb[:, e] == 0).all():
                            cnt[a] += 1
                            emb[j, e] = np.random.normal(
                                0.0, sigma, (context_size,))
                            emb[i, e] = np.dot(v, emb[j, e])
                            continue  # next example

                        # (3c) Example consists of just 1 type of input
                        if (j == i).all():
                            emb[i, e] = np.random.normal(0.0, sigma, (1, ))
                            continue  # next example

                        # (3d) Solve for missing target/context vectors/weights
                        num_ctx_missing = (emb[j, e] == 0).sum()  # `m`
                        flag_trgt_exist = emb[i, e] != 0

                        if flag_trgt_exist and (num_ctx_missing == 2):
                            cnt[a] += 1
                            try:
                                emb = assign_two_ctx(emb, e, i, j, v, sigma)
                            except Exception:
                                print(f"ERROR: e:{e} i:{i} j:{j}")

                        elif (not flag_trgt_exist) and (num_ctx_missing == 1):
                            cnt[a] += 1
                            emb = assign_one_ctx_and_trgt(
                                emb, e, i, j, v, sigma)

                        elif flag_trgt_exist and (num_ctx_missing == 1):
                            cnt[a] += 1
                            emb = assign_missing_ctx(emb, e, i, j, v)

                        # DON'T. NEVER use `assign_missing_target` here.

                        # assign random weights
                        # (the algorithm wouldn't work without this!)
                        elif (not flag_trgt_exist) and (num_ctx_missing > 1):
                            cnt[a] += 1
                            mask = emb[j, e] == 0
                            idx = np.unique(j[mask])
                            if len(idx) > 0:
                                emb[idx[:-1], e] = np.random.normal(
                                    0.0, sigma, (len(idx) - 1, ))
                                emb[i, e] = np.dot(v, emb[j, e])

                # (2x) start in the next column for the next example
                offset += 1

            # (1/2)
            patience += 1

        # (1z) Move to next block
        n_block += 1
        # print(context_size)

    # Assign random numbers to uninitialized IDs in the remaining columns
    if fill:
        emb = assign_random_to_unused(emb, sigma)

    # done
    return emb
