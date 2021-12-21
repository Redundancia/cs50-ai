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
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    probability_distribution = {}
    number_of_pages= len(corpus)
    number_of_sub_pages = len(corpus[page])

    # adds probability distribution for all pages in case of random page, or in case page has no subpages
    for corpus_page in corpus.keys():
        if len(corpus[page]) > 0:
            probability_distribution[corpus_page] = probability_distribution.get(corpus_page, 0) + ((1 / number_of_pages) * (1 - damping_factor))
        else: 
            probability_distribution[corpus_page] = probability_distribution.get(corpus_page, 0) + ((1 / number_of_pages) * 1)
    
    # adds probability distribution for subpages of page
    for sub_page in corpus[page]:
        probability_distribution[sub_page] = probability_distribution.get(sub_page, 0) + ((1 / number_of_sub_pages) * damping_factor)
    
    if round(sum(probability_distribution.values()),4) != 1:
        print(f"something wrong with transition_model: {round(sum(probability_distribution.values()),4)}")
    return probability_distribution

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    sample_dictionary = {}

    # Pick random page
    page = random.choice(list(corpus.keys()))

    # Do the first calculation outside of loop, loop could be refactored to make this redundant
    transition_probabilities = transition_model(corpus, page, damping_factor)
    sample_dictionary[page] = 1

    for i in range(n-1):
        random_number_to_decide_new_page = random.random()
        probability_calculation = 0
        for sub_page, probability in transition_probabilities.items():
            probability_calculation += probability
            # Check if random picked the given sub_page
            if probability_calculation > random_number_to_decide_new_page:
                
                # Increment dict value for sub_page, these values are occurences, will be calculated into probability
                sample_dictionary[sub_page] = sample_dictionary.get(sub_page, 0) + 1
                transition_probabilities = transition_model(corpus, sub_page, damping_factor)
                break

    # Turn the dictionary values into probabilities(0-1)
    for page, probability in sample_dictionary.items():
        sample_dictionary[page] /= n
    
    if round(sum(sample_dictionary.values()),4) != 1:
        print(f"something wrong with sample_pagerank: {round(sum(sample_dictionary.values()),4)}")

    return sample_dictionary



def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    iterative_dictionary = {}
    number_of_pages = len(corpus)
    
    # Setup starting probabilities
    for page, sub_pages in corpus.items():
        iterative_dictionary[page] = 1 / number_of_pages


if __name__ == "__main__":
    main()
