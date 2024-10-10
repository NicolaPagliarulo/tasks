from flask import Flask,render_template, request
from functools import reduce
from pyspark.sql import SparkSession, functions as F


# create the spark and flask applications
spark = SparkSession.builder.appName('app').getOrCreate()
app = Flask(__name__)

# read in the data from the .csv files provided and cast the data type of 'opps' from a string to a double
spark.read.csv('archive/browsername.csv', header=True
               ).withColumn("opps", F.col("opps").cast("double")).createOrReplaceTempView('browsername_temp_view')
spark.read.csv('archive/countries.csv', header=True
               ).withColumn("opps", F.col("opps").cast("double")).createOrReplaceTempView('countries_temp_view')
spark.read.csv('archive/platformname.csv', header=True
               ).withColumn("opps", F.col("opps").cast("double")).createOrReplaceTempView('platformname_temp_view')
spark.read.csv('archive/vertical.csv', header=True
               ).withColumn("opps", F.col("opps").cast("double")).createOrReplaceTempView('vertical_temp_view')


# create the home page view
@app.route('/', methods=['GET'])
def index():
    # rendering the 'traffic_estimation.html' without any
    return render_template('traffic_estimation.html', context=None)

# create the '/estimate' page view
@app.route('/estimate', methods=['GET'])
def search():
    # getting the request count provided from the user (this field is mandatory)
    total_request_count = int(request.args.get('request_count'))

    # variable used to map each column with the view associated with it.
    cols_to_temp_view_map = {'browsername': 'browsername_temp_view',
                             'country': 'countries_temp_view',
                             'platformname': 'platformname_temp_view',
                             'publishernewthematic': 'vertical_temp_view'}

    # variable that stores the values from the provided fields in a key, value pairs.
    submitted_fields = {'browsername': request.args.get('browsername', ''),
                        'platformname': request.args.get('platformname', ''),
                        'country': request.args.get('country', ''),
                        'publishernewthematic': request.args.get('vertical', '')}

    # getting the multipliers and messages for each field.
    multipliers_and_messages = [get_multiplier_and_message(cols_to_temp_view_map[key], (key, value))
                               if value != '' else (1, f'No value provided for: {key}')
                               for key, value in submitted_fields.items()]

    # separate the tuples into 2 lists.
    multipliers = [e[0] for e in multipliers_and_messages]
    field_messages = [e[1] for e in multipliers_and_messages]

    # get the total multiplier from all multipliers
    total_multiplier = reduce((lambda x, y: x * y), multipliers)

    estimated_traffic = round(total_request_count * total_multiplier, 2)


    return render_template('traffic_estimation.html', context={'estimated_traffic': estimated_traffic,
                                                                                'field_messages': field_messages,
                                                                                'request_count': total_request_count})


def get_multiplier_and_message(temp_view: str, col_and_value: tuple[str, str]):
    """
    Helper function that is getting the percentage of the provided value from the total values of a given col.
    And a message if there is a match or not.

    :param temp_view: a temporary view. (this could be a regular view)sa
    :param col_and_value: the column name and value on which we do the filtering.
    :return col_multiplier, field_message: the percentage of the value compared to the total values of a given col
                                           and a message for field.
    """

    col = col_and_value[0]
    value = col_and_value[1]

    col_multiplier = 1

    # getting the opps value and the total opps value (opps - opportunities)
    requested_col_opps = spark.sql(f"SELECT opps FROM {temp_view} WHERE {col} = '{value}'").first()
    sum_all_col_opps = spark.sql(f"SELECT SUM(opps) FROM {temp_view}").first()[0]

    # getting the percentage of the opps for the value provided from the total opps.
    # if there isn`t a match we return 1 as a percentage.
    if requested_col_opps:
        col_multiplier = requested_col_opps[0] / sum_all_col_opps
        field_message = f'There was a match for {col} as {value}.'
    else:
        field_message = (f'There were no matches for a {col} with {value} name.\n'
                        f'That`s why it was excluded from the estimation.')
    return col_multiplier, field_message


if __name__ == '__main__':
    app.run(debug=True, port=3000)
