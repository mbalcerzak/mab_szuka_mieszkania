import pandas as pd


def load_dataframe(file):
    df = pd.read_pickle(f"../../data/{file}.pkl")
    return df #[:100]


def main(flats, prices):
    print(flats['flat_area'].value_counts())

    # TODO Why ID in flats is not unique



if __name__ == "__main__":
    prices = load_dataframe("prices")
    flats = load_dataframe("flats")

    assert len(prices) > 0, "Prices DataFrame is empty"
    assert len(flats) > 0, "Flats DataFrame is empty"

    main(flats, prices)

