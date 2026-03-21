from src.utils import hash256

def merkle_root(transaction_ids):
    if (len(transaction_ids) == 1):
        return transaction_ids[0]
    elif (len(transaction_ids) % 2 == 1):
        transaction_ids.append(transaction_ids[-1])

    new_level = []
    for i in range(0, len(transaction_ids), 2):
        hash = hash256(transaction_ids[i] + transaction_ids[i + 1])
        new_level.append(hash)

    return merkle_root(new_level)