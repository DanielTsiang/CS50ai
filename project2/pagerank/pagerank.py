import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print("PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = {}

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+[^>]*?href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = {link for link in pages[filename] if link in pages}

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    num_pages = len(corpus)
    num_links = len(corpus[page])
    if num_links:
        # With probability damping_factor, the random surfer randomly chooses
        # one of the links from page with equal probability
        random_surfer = {page: damping_factor / num_links for page in corpus[page]}

        # With probability 1 - damping_factor, the random surfer randomly chooses
        # one of all pages in the corpus with equal probability
        for page in corpus:
            if page in random_surfer:
                random_surfer[page] += (1 - damping_factor) / num_pages
            else:
                random_surfer[page] = (1 - damping_factor) / num_pages

    # If page has no outgoing links, then transition_model chooses randomly among all pages with equal probability.
    else:
        random_surfer = {page: 1 / num_pages for page in corpus}

    # check the probability distribution sums to 1
    surfer_sum = round(sum(random_surfer.values()), 4)
    assert surfer_sum == 1, f"Probabilities in transition_model function adds up to {surfer_sum} and not 1."
    return random_surfer


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # initialise empty dictionary
    samples_count = dict.fromkeys(corpus.keys(), 0)

    # start with a page at random
    initial_random_page = random.choice(list(corpus.keys()))
    transition_probabilities = transition_model(corpus, initial_random_page, damping_factor)
    samples_count[initial_random_page] += 1

    # sample rest of `n` pages
    for _ in range(n - 1):
        random_page = random.choices(
            list(transition_probabilities.keys()),
            weights=list(transition_probabilities.values()),
            k=1
        )[0]
        samples_count[random_page] += 1
        transition_probabilities = transition_model(corpus, random_page, damping_factor)

    # calculate page ranks
    page_rank = {page: samples_count[page] / n for page in samples_count}

    # check the probability distribution sums to 1
    page_rank_sum = round(sum(page_rank.values()), 4)
    assert page_rank_sum == 1, f"Probabilities in sample_pagerank function adds up to {page_rank_sum} and not 1."
    return page_rank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # assign each page an initial rank of 1 / N, where N is the total number of pages in the corpus
    num_pages = len(corpus)
    page_rank = {page: 1 / num_pages for page in corpus}

    # iteratively calculate new rank values based on all of the current rank values
    page_rank_difference = 1
    iterations = 0
    while page_rank_difference >= 0.001:
        # reset PageRank difference and increment iteration count
        page_rank_difference = 0
        iterations += 1

        # copy current state to calculate new PageRanks without influence from newly calculated values
        previous_state = page_rank.copy()

        for page in page_rank:
            # grab "parent" pages that link to current "page" iteration
            parents = [link for link in corpus if page in corpus[link]]

            # 1st part of equation
            first = (1 - damping_factor) / num_pages

            # iterate over parents to add 2nd part of the equation iteratively
            second = []
            if len(parents) != 0:
                for parent in parents:
                    # number of links starting from parent page
                    num_links = len(corpus[parent])
                    value = previous_state[parent] / num_links
                    second.append(value)

            # calculate page rank for this page
            page_rank[page] = first + (damping_factor * sum(second))

            # calculate PageRank difference during this iteration
            new_page_rank_difference = abs(page_rank[page] - previous_state[page])
            page_rank_difference = max(page_rank_difference, new_page_rank_difference)

    # normalise values
    page_rank_sum = sum(page_rank.values())
    normalised_page_rank = {key: value/page_rank_sum for key, value in page_rank.items()}
    print(f"\nPageRank values stable after {iterations} iterations.")
    normalised_page_rank_sum = round(sum(normalised_page_rank.values()), 4)
    assert normalised_page_rank_sum == 1, f"Probabilities in iterate_pagerank function adds up to " \
                                          f"{normalised_page_rank_sum} and not 1."
    return normalised_page_rank


if __name__ == "__main__":
    main()
