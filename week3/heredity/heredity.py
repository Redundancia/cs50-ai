import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    individual_probabilities = {}
    for person in people:
        if person not in individual_probabilities:
            calculate_probability(people, one_gene, two_genes, have_trait, person, individual_probabilities)
    print(individual_probabilities)
    joint_probability = 1
    for prob in individual_probabilities.values():
        joint_probability *= prob
    print(joint_probability)
    return joint_probability


def calculate_probability(people, one_gene, two_genes, have_trait, person, individual_probabilities):
    """
    Calculate the probability for given person and ancestors that she/he has/does not have the trait.
    """

    gene_probability = 1
    trait_probability = 1

    # If he doesn't have mother, he doesn't have father either, and we can calculate from the global values PROBS
    if people[person]['mother'] == None:
        if person in one_gene:
            gene_probability = PROBS["gene"][1]
            trait_probability = PROBS["trait"][1][True] if person in have_trait else PROBS["trait"][1][False]
        elif person in two_genes:
            gene_probability = PROBS["gene"][2]
            trait_probability = PROBS["trait"][2][True] if person in have_trait else PROBS["trait"][2][False]
        else:
            gene_probability = PROBS["gene"][0]
            trait_probability = PROBS["trait"][0][True] if person in have_trait else PROBS["trait"][0][False]
    
    # We calculate probabilities according to the amount of copy of genes person has
    else:
        # If parent's probability is not yet calculated, we calculate it first
        if people[person]['mother'] not in individual_probabilities:
            calculate_probability(people, one_gene, two_genes, have_trait, people[person]['mother'], individual_probabilities)
            calculate_probability(people, one_gene, two_genes, have_trait, people[person]['father'], individual_probabilities)

        # Person has 1 gene, two ways this can happen:
        if person in one_gene:
            # First way: gets one from mother
            if people[person]["mother"] in one_gene:
                gene_probability *= 0.5
            elif people[person]["mother"] in two_genes:
                gene_probability *= 1 - PROBS["mutation"]
            else:
                gene_probability *= PROBS["mutation"]
            # No gene from father
            if people[person]["father"] in one_gene:
                gene_probability *= 0.5
            elif people[person]["father"] in two_genes:
                gene_probability *= PROBS["mutation"]
            else:
                gene_probability *= 1 - PROBS["mutation"]

            # Second way: gets one from father, but not from mother, this might be redundant, but for sure could be refactored with the one above
            if people[person]["father"] in one_gene:
                gene_probability *= 0.5
            elif people[person]["father"] in two_genes:
                gene_probability *= 1 - PROBS["mutation"]
            else:
                gene_probability *= PROBS["mutation"]
            # No gene from mother
            if people[person]["mother"] in one_gene:
                gene_probability *= 0.5
            elif people[person]["mother"] in two_genes:
                gene_probability *= PROBS["mutation"]
            else:
                gene_probability *= 1 - PROBS["mutation"]
        
            # Person with 1 gene trait probability
            trait_probability = PROBS["trait"][1][True] if person in have_trait else PROBS["trait"][1][False]

        # Person has 2 genes, gets one from both parents
        elif person in two_genes:
            if people[person]["mother"] in one_gene:
                gene_probability *= 0.5
            elif people[persong]["mother"] in two_genes:
                gene_probability *= 1 - PROBS["mutation"]
            else:
                gene_probability *= PROBS["mutation"]

            if people[person]["father"] in one_gene:
                gene_probability *= 0.5
            elif people[person]["father"] in two_genes:
                gene_probability *= 1 - PROBS["mutation"]
            else:
                gene_probability *= PROBS["mutation"]

            # Person with 2 genes trait probability
            trait_probability = PROBS["trait"][2][True] if person in have_trait else PROBS["trait"][2][False]


        # Person has 0 genes, inherits no genes
        else:
            if people[person]["mother"] in one_gene:
                gene_probability *= 0.5
            elif people[person]["mother"] in two_genes:
                gene_probability *= PROBS["mutation"]
            else:
                gene_probability *= 1 - PROBS["mutation"]

            if people[person]["father"] in one_gene:
                gene_probability *= 0.5
            elif people[person]["father"] in two_genes:
                gene_probability *= PROBS["mutation"]
            else:
                gene_probability *= 1 - PROBS["mutation"]

            # Person with 0 genes trait probability
            trait_probability = PROBS["trait"][0][True] if person in have_trait else PROBS["trait"][0][False]


    individual_probabilities[person] = gene_probability * trait_probability

def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    raise NotImplementedError


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    raise NotImplementedError


if __name__ == "__main__":
    main()
