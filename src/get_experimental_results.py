import numpy as np


def get_experimental_results(products, selected_layers, data, u, v, K=5):

    PRODUCT_LINK_PREFIX = "https://www.amazon.com/gp/product/"

    # Get information of the query product
    query_product = None
    record = products.find_one({"Id": data["QueryProductId"]})
    if record is not None:
        query_product = {
            "group": record["group"],
            "title": record["title"],
            "link": PRODUCT_LINK_PREFIX + record["ASIN"],
        }

    # Get top K products for each selected group
    top_K_products = []

    if "GroupNet" in data:  # multi-layered HITS
        for i, g in enumerate(data["GroupDict"]):
            temp = {"group": g, "products": []}
            index2Id = data["WithinLayerNetsDict"][i]
            rank_ui = np.flip(np.argsort(u[i].todense().getA1()), axis=0)
            rank_vi = np.flip(np.argsort(v[i].todense().getA1()), axis=0)
            for r in range(min(K, len(rank_ui))):
                record_authority = products.find_one({"Id": int(index2Id[rank_ui[r]])})
                record_hub = products.find_one({"Id": int(index2Id[rank_vi[r]])})
                temp["products"].append({
                    "rank": r + 1,
                    "authority": {"title": record_authority["title"], "link": PRODUCT_LINK_PREFIX + record_authority["ASIN"]},
                    "hub": {"title": record_hub["title"], "link": PRODUCT_LINK_PREFIX + record_hub["ASIN"]},
                })
            top_K_products.append(temp)
    else:  # regular HITS
        for g in selected_layers:
            temp = {"group": g, "products": []}
            ui = u[data['indices_range_' + g][0]:data['indices_range_' + g][1], 0]
            vi = v[data['indices_range_' + g][0]:data['indices_range_' + g][1], 0]
            rank_ui = np.flip(np.argsort(ui.todense().getA1()), axis=0)
            rank_vi = np.flip(np.argsort(vi.todense().getA1()), axis=0)
            for r in range(min(K, len(rank_ui))):
                record_authority = products.find_one({"Id": int(data['index2Id_' + g][rank_ui[r]])})
                record_hub = products.find_one({"Id": int(data['index2Id_' + g][rank_vi[r]])})
                temp["products"].append({
                    "rank": r + 1,
                    "authority": {"title": record_authority["title"], "link": PRODUCT_LINK_PREFIX + record_authority["ASIN"]},
                    "hub": {"title": record_hub["title"], "link": PRODUCT_LINK_PREFIX + record_hub["ASIN"]},
                })
            top_K_products.append(temp)

    return {
        "query_product": query_product,
        "top_K_products": top_K_products,
    }
