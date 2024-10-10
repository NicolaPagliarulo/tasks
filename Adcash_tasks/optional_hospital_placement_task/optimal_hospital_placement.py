from math import dist
from typing import List, Tuple

# assign the coordinates to the "city_coordinates" variable in the following format - [(int, int), (int, int) ...]
city_coordinates = [tuple(map(int, input().split(', '))) for _ in range(10)]

def place_hospitals(city_coordinates: List[Tuple]):
    """
    Function which places 2 hospitals in the most optimal places inside 2 of 10 cities.

    :param city_coordinates: list of tuples where each tuple is a coordinate for a city on a 1000 by 1000 matrix.
    :return first_hospital_location, second_hospital_location: two tuples representing the two hospital locations.
    """
    # splitting the list of coordinates into 2 halves.
    first_half_of_cities = city_coordinates[:5]
    second_half_of_cities = city_coordinates[5:]
    # calling the "get_optimal_hospital_location" function for both halves to get the hospitals coordinates.
    first_hospital_location = get_optimal_hospital_location(first_half_of_cities)
    second_hospital_location = get_optimal_hospital_location(second_half_of_cities)
    return [first_hospital_location, second_hospital_location]


def get_optimal_hospital_location(cities: List[Tuple]):
    """
    Function which stores all the longest distances for each city and returns the one with the shortest longest one.

    :param cities: list of tuples where each tuple is a coordinate for a city.
    :return most_optimal_city_for_hospital: the most optimal location to place a hospital from the cities provided.
    """
    # store all the longest distances for each city.
    longest_distances = []
    # check the distance from the "main_city" to the rest. e.g(city1 -> city2, city1 -> city3, city1 -> city4 ...)
    for main_city in cities:
        longest_distance = 0
        for city in cities:
            distance = dist(main_city, city)
            if distance > longest_distance:
                longest_distance = distance
        # store the longest distance found for the main_city.
        longest_distances.append((longest_distance, main_city))
    # get the shortest longest distance found from all the cities.
    most_optimal_city_for_hospital = sorted(longest_distances, key=lambda e: e[0])[0][1]
    return most_optimal_city_for_hospital

hospital_locations = place_hospitals(city_coordinates)

# print out the locations without any brackets.
[print(f"{hospital_location[0]}, {hospital_location[1]}") for hospital_location in hospital_locations]


# example input to test
"""
0, 4
0, 9
2, 1
2, 9
3, 6
4, 2
5, 2
7, 1
9, 1
9, 9
"""
# example output.
"""
3, 6
9, 1
"""
