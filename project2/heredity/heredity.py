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

    # Keep track of gene and trait probabilities for each person.
    # Create dictionary using dictionary comprehension and set all values to 0.
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

    return probabilities


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = {}
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
    # initialise variables
    gene_prob = 0
    trait_prob = 0
    combined_prob = 1

    for person in people:
        # get names of parents
        mother = people[person]["mother"]
        father = people[person]["father"]

        # if no mother/father data supplied, use unconditional probabilities
        if mother is None and father is None:
            # person has two copies of the gene
            if person in two_genes:
                copies = 2
            # person has 1 copy of the gene
            elif person in one_gene:
                copies = 1
            # person has no copies of the gene
            else:
                copies = 0
            gene_prob = PROBS["gene"][copies]

        else:
            # initialise dict to store probability of getting gene from each parent
            parent_probs = {mother: 0, father: 0}

            # compute probabilities of getting gene from each parent
            for parent in parent_probs:
                # if parent has 2 copies of gene, then the chance of passing it onto child is 1 - probability of mutation,
                # i.e. if parent has 2 copies of gene, the only way they won't pass it on is via mutation.
                if parent in two_genes:
                    parent_probs[parent] = 1 - PROBS["mutation"]
                # if parent has 1 copy of gene, 50/50 chance of whether they pass it on
                elif parent in one_gene:
                    parent_probs[parent] = 0.5
                # else parent has no copy of gene, then the chance of passing it onto child is due to gene mutation probability
                else:
                    parent_probs[parent] = PROBS["mutation"]

            # probability person gets 2 copies of gene is the product of getting it from both parents
            if person in two_genes:
                copies = 2
                gene_prob = parent_probs[mother] * parent_probs[father]

            # probability person gets 1 copy of gene is probability of getting it from one parent but not the other, there are 2 combinations for this
            elif person in one_gene:
                copies = 1
                prob1 = parent_probs[mother] * (1 - parent_probs[father])
                prob2 = parent_probs[father] * (1 - parent_probs[mother])
                gene_prob = prob1 + prob2

            # probability person gets no copy of gene, i.e. does not receive from either parent
            else:
                copies = 0
                gene_prob = (1 - parent_probs[mother]) * (1 - parent_probs[father])

        # probability for trait depends on the number of genes possessed and if person exhibits the trait
        if person in have_trait:
            trait_prob = PROBS["trait"][copies][True]
        else:
            trait_prob = PROBS["trait"][copies][False]

        combined_prob *= gene_prob * trait_prob

    return combined_prob


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities:
        # update gene distribution
        if person in two_genes:
            probabilities[person]["gene"][2] += p
        elif person in one_gene:
            probabilities[person]["gene"][1] += p
        else:
            probabilities[person]["gene"][0] += p

        # update trait distribution
        if person in have_trait:
            probabilities[person]["trait"][True] += p
        else:
            probabilities[person]["trait"][False] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:
        # normalize gene distribution
        gene_sum = sum(probabilities[person]["gene"].values())
        probabilities[person]["gene"] = {key: value / gene_sum for key, value in probabilities[person]["gene"].items()}

        # normalize trait distribution
        trait_sum = sum(probabilities[person]["trait"].values())
        probabilities[person]["trait"] = {key: value / trait_sum for key, value in probabilities[person]["trait"].items()}


if __name__ == "__main__":
    main()
