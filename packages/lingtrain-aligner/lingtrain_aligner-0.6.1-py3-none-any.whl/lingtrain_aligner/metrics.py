
def chain_score():
    return 1

def get_breaks_count(index, min_len=2):
    """Get amount of breaks"""
    curr_from = index[0]["from"][0]
    curr_to = index[0]["to"]
    curr_from = index[0]["from"][0]
    curr_to = index[0]["to"]
    chains_from = []
    chains_to = []
    
    chain_to = [(curr_to, index[0]["batch_id"], index[0]["sub_id"])]
    chain_from = [(curr_from, index[0]["batch_id"], index[0]["sub_id"])]
    for i in range(1, len(index)):
        val_from = index[i]["from"][0]
        val_to = index[i]["to"]
        if val_to == curr_to + 1:
            chain_to.append((val_to, index[i]["batch_id"], index[i]["sub_id"]))
            chain_from.append((val_from, index[i]["batch_id"], index[i]["sub_id"]))
            curr_to = val_to
            curr_from = val_from
        elif len(chain_to) >= min_len:
            chains_to.append(chain_to)
            chains_from.append(chain_from)
            chain_to = [(val_to, index[i]["batch_id"], index[i]["sub_id"])]
            chain_from = [(val_from, index[i]["batch_id"], index[i]["sub_id"])]
            curr_to = val_to
            curr_from = val_from
        else:
            chain_to = [(val_to, index[i]["batch_id"], index[i]["sub_id"])]
            chain_from = [(val_from, index[i]["batch_id"], index[i]["sub_id"])]
            curr_to = val_to
            curr_from = val_from
    if len(chain_to) >= min_len:
        chains_to.append(chain_to)
        chains_from.append(chain_from)

    return chains_from, chains_to

# def get_good_chains(index, min_len=2, handle_start=False):
#     """Calculate valid alignment chains"""
#     curr_from = index[0]["from"][0]
#     curr_to = index[0]["to"]
#     chains_from = []
#     chains_to = []
#     chain_to = [(curr_to, index[0]["batch_id"], index[0]["sub_id"])]
#     chain_from = [(curr_from, index[0]["batch_id"], index[0]["sub_id"])]
#     for i in range(1, len(index)):
#         val_from = index[i]["from"][0]
#         val_to = index[i]["to"]
#         if val_to == curr_to + 1:
#             chain_to.append((val_to, index[i]["batch_id"], index[i]["sub_id"]))
#             chain_from.append((val_from, index[i]["batch_id"], index[i]["sub_id"]))
#             curr_to = val_to
#             curr_from = val_from
#         elif len(chain_to) >= min_len or handle_start:
#             chains_to.append(chain_to)
#             chains_from.append(chain_from)
#             chain_to = [(val_to, index[i]["batch_id"], index[i]["sub_id"])]
#             chain_from = [(val_from, index[i]["batch_id"], index[i]["sub_id"])]
#             curr_to = val_to
#             curr_from = val_from
#             handle_start = False
#         else:

#             # print(">>:", chain_to)

#             chain_to = [(val_to, index[i]["batch_id"], index[i]["sub_id"])]
#             chain_from = [(val_from, index[i]["batch_id"], index[i]["sub_id"])]
#             curr_to = val_to
#             curr_from = val_from
#     if len(chain_to) >= min_len:
#         chains_to.append(chain_to)
#         chains_from.append(chain_from)

#     return chains_from, chains_to