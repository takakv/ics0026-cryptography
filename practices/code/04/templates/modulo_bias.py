import matplotlib.pyplot as plt
import pandas

BIT_LENGTH = 8


def plot(nums: list[int], title: str) -> None:
    """Plot the numbers on a graph.

    :param nums: The numbers to plot.
    :param title: The title of the plot.
    """
    df = pandas.DataFrame({"nums": nums})
    ordered = df["nums"].value_counts().sort_index()
    plot_width = 2 * len(ordered) // 10  # renders a bit more neatly this way
    ordered.plot(figsize=(plot_width, 10), title=title, kind="bar")
    plt.show()


def sample_reject(lim: int, out_count: int) -> list[int]:
    """ Uniformly sample integers in the range [0, lim).

    :param lim: The exclusive upper bound.
    :param out_count: The number of integers to generate.
    :return: A list of integers below the upper bound.
    """
    nums: list[int] = []
    # TODO: implement the naive rejection sampling.
    return nums


def main():
    n_samples = 10 ** 7

    # Generate n random 8-bit integers.
    nums: list[int] = []
    for _ in range(n_samples):
        # TODO: sample n random 8-bit integers.
        pass

    # Wrap integers below the upper bounds.
    mod_100 = ...
    mod_150 = ...
    mod_200 = ...

    # Plot the integers obtained via modulo wrap.
    plot(mod_100, "x mod 100")
    plot(mod_150, "x mod 150")
    plot(mod_200, "x mod 200")

    # This part will take some time due to the three separate generation
    # processes and the naive rejection sampling.
    rej_100 = sample_reject(100, n_samples)
    rej_150 = sample_reject(150, n_samples)
    rej_200 = sample_reject(200, n_samples)

    # In practice, you should sample with secrets.randbelow() as this uses a
    # more performant unbiased or debiased algorithm.
    # e.g. rej_100 = [secrets.randbelow(100) for _ in range(n_samples)]

    # Plot the integers obtained via rejection sampling.
    plot(rej_100, "Rejection sampling below 100")
    plot(rej_150, "Rejection sampling below 150")
    plot(rej_200, "Rejection sampling below 200")


if __name__ == "__main__":
    main()
