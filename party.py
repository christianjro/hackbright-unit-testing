"""Flask site for Balloonicorn's Party."""

from flask import Flask, session, render_template, request, flash, redirect

app = Flask(__name__)
app.secret_key = "SECRETSECRETSECRET"


def is_mel(name, email):
    """Is this user Mel?
    For example: 

    >>> is_mel('Mel Melitpolski', 'mel@ubermelon.com')
    True
    >>> is_mel('Judith Butler', 'judith@awesome.com')
    False
    >>> is_mel('Mel Melitpolski', 'random@ubermelon.com')
    True
    >>> is_mel('Random Name', 'mel@ubermelon.com')
    True
    """

    return name == "Mel Melitpolski" or email == "mel@ubermelon.com"


def most_and_least_common_type(treats):
    """Given list of treats, return most and least common treat types.

    Return most and least common treat types in tuple of format (most, least).

    For example:

    Testcase_1: Displays "dessert" as most common and "drink" as least common:
    >>> treats = [
    ...     {'type': 'dessert'},
    ...     {'type': 'dessert'},
    ...     {'type': 'appetizer'},
    ...     {'type': 'dessert'},
    ...     {'type': 'appetizer'},
    ...     {'type': 'drink'},
    ... ]
    >>> most_and_least_common_type(treats)
    ('dessert', 'drink')

    Testcase_2: In the case that all treats are the same, return treat type for both:
    >>> treats = [
    ...     {'type': 'dessert'},
    ...     {'type': 'dessert'},
    ...     {'type': 'dessert'},
    ...     {'type': 'dessert'},
    ... ]
    >>> most_and_least_common_type(treats)
    ('dessert', 'dessert')

    Testcase_3: In the case that there is a tie for most common treat type, return the first one:
    >>> treats = [
    ...     {'type': 'dessert'},
    ...     {'type': 'dessert'},
    ...     {'type': 'appetizer'},
    ...     {'type': 'appetizer'},
    ... ]
    >>> most_and_least_common_type(treats)
    ('dessert', 'appetizer')

    Testcase_4: If an empty list is given, return None for both:
    >>> treats = []
    >>> most_and_least_common_type(treats)
    (None, None)
    """

    types = {}

    # Count number of each type
    for treat in treats:
        types[treat['type']] = types.get(treat['type'], 0) + 1

    most_count = most_type = None
    least_count = least_type = None

    # Find most, least common
    for treat_type, count in types.items():
        if most_count is None or count > most_count:
            most_count = count
            most_type = treat_type

        if least_count is None or count < least_count:
            least_count = count
            least_type = treat_type

    return (most_type, least_type)


def get_treats():
    """Return treats being brought to the party.

    One day, I'll move this into a database! -- Balloonicorn
    """

    return [
        {'type': 'dessert',
         'description': 'Chocolate mousse',
         'who': 'Leslie'},
        {'type': 'dessert',
         'description': 'Cardamom-Pear pie',
         'who': 'Joel'},
        {'type': 'appetizer',
         'description': 'Humboldt Fog cheese',
         'who': 'Meggie'},
        {'type': 'dessert',
         'description': 'Lemon bars',
         'who': 'Bonnie'},
        {'type': 'appetizer',
         'description': 'Mini-enchiladas',
         'who': 'Katie'},
        {'type': 'drink',
         'description': 'Sangria',
         'who': 'Anges'},
        {'type': 'dessert',
         'description': 'Chocolate-raisin cookies',
         'who': 'Henry'},
        {'type': 'dessert',
         'description': 'Brownies',
         'who': 'Sarah'}
    ]


@app.route("/")
def homepage():
    """Show homepage."""

    return render_template("homepage.html")


@app.route("/treats")
def show_treats():
    """Show treats people are bringing."""

    treats = get_treats()

    most, least = most_and_least_common_type(get_treats())

    return render_template("treats.html",
                           treats=treats,
                           most=most,
                           least=least)


@app.route("/rsvp", methods=['POST'])
def rsvp():
    """Register for the party."""

    name = request.form.get("name")
    email = request.form.get("email")

    if not is_mel(name, email):
        session['rsvp'] = True
        flash("Yay!")
        return redirect("/")

    else:
        flash("Sorry, Mel. This is kind of awkward.")
        return redirect("/")


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=3030)
