import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="gets weather data from tsag-agaar.gov.mn"
    )

    parser.add_argument(
        "date",
        default=None,
        type=str,
        help="date to query for",
        nargs="?",
    )

    parser.add_argument(
        "city",
        default=None,
        type=str,
        help="city to query weather data for",
        nargs="?",
    )

    args = parser.parse_args()

    # TODO: implement __main__.py
