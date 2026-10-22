"""The newsgroups data for the Lab 4 example.

This is the newsgroups example from the scikit-learn text tutorial (Week 3), with two of
its newsgroups changed: posts from comp.graphics, rec.sport.hockey, sci.med and
talk.religion.misc. To show what happens when one class is rare, load_newsgroups() keeps
only 75 of the 377 religion posts for training and 50 of the 251 for testing. The other
newsgroups keep all of their posts.

The first run downloads the data, which scikit-learn keeps for later runs.
"""

from sklearn.datasets import fetch_20newsgroups


def keep_fewer(newsgroups, small_group, how_many):
    """Return the posts and their labels, keeping only the first how_many posts of small_group."""
    small_label = newsgroups.target_names.index(small_group)
    posts = []
    labels = []
    small_count = 0
    for i in range(len(newsgroups.data)):
        label = newsgroups.target[i]
        if label == small_label:
            small_count = small_count + 1
        if label != small_label or small_count <= how_many:
            posts.append(newsgroups.data[i])
            labels.append(label)
    return posts, labels


def load_newsgroups():
    """Returns the training and test posts, their labels, and the names of the newsgroups."""
    categories = ["talk.religion.misc", "rec.sport.hockey", "comp.graphics", "sci.med"]
    twenty_train = fetch_20newsgroups(subset="train", categories=categories, shuffle=True, random_state=42)
    twenty_test = fetch_20newsgroups(subset="test", categories=categories, shuffle=True, random_state=42)

    train_posts, train_groups = keep_fewer(twenty_train, "talk.religion.misc", 75)
    test_posts, test_groups = keep_fewer(twenty_test, "talk.religion.misc", 50)
    return train_posts, test_posts, train_groups, test_groups, twenty_test.target_names
