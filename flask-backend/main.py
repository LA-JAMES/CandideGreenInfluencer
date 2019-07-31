import flask
import cv2
import glob
import json
import Levenshtein

from random import randrange

import time
import os

IMAGES_DIRECTORY = 'images/'
INPUT_JSON_FILE = 'data.json'
FEATURE_MATCH_OUTPUT_LOCATION = 'static/react/media/feature-match.jpg'


def load_json(file):
    """
    Use the Python json module to load the provided data set into memory and return is as a list of JSON objects.

    :param file: The relative file location of the json file (data.json) provided.
    :return: A list containing the json data.
    """

    json_data = None

    if file:
        with open(file, 'r') as file:
            json_data = json.load(file)

    return json_data


def get_submitted_image_json(image_file, all_image_json):
    """
    Take the file name as a string (given with parent directory) and strip the directory from the
    string.  Return the result of this operation as well as the object associated with this file name.

    :param image_file: File name + parent directory (e.g. images/1.jpg) of the submitted file.
    :param all_image_json: List of json objects for all images in the data set.
    :return: A string matching the JSON object pertaining to the submitted image & it's associated JSON object.
    """

    json_object_string = image_file.replace('images/', '')

    return json_object_string, all_image_json[json_object_string]


def rank_matches_by_category(similar_image_names, similar_image_categories, similar_image_totals, algorithm='timsort'):
    """
    This function will sort the best matched images (matched by category comparison).

    By default this function will use the sorted() function which is based on Timsort.

    :param similar_image_names: List of similar image file names matched by category.
    :param similar_image_categories: List of similar image categories matched using the comparison algorithm.
    :param similar_image_totals: List of similar image totals (topicality+score) matched by category.
    :param algorithm: Default timsort.  Any other value will use unoptimized bubblesort.
    :return: List of sorted similar image names, categories and totals.
    """

    if algorithm == 'timsort':
        similar_image_totals, similar_image_categories, similar_image_names = \
            zip(*sorted(zip(similar_image_totals, similar_image_categories, similar_image_names), reverse=True))
    else:
        for i in range(len(similar_image_totals)):
            for j in range(i + 1, len(similar_image_totals)):
                if similar_image_totals[j] > similar_image_totals[i]:
                    tmp_total, tmp_name, tmp_categories = \
                        similar_image_totals[i], similar_image_names[i], similar_image_categories[i]

                    similar_image_totals[i], similar_image_names[i], similar_image_categories[i] = \
                        similar_image_totals[j], similar_image_names[j], similar_image_categories[j]

                    similar_image_totals[j], similar_image_names[j], similar_image_categories[j] = \
                        tmp_total, tmp_name, tmp_categories

    return similar_image_names, similar_image_categories, similar_image_totals


def find_related_images_by_category(submitted_json_object_string, submitted_json, all_images_json):
    """
    Find up to 5 similar images to the submitted image.  Use SequenceMatcher on the categories of the submitted
    image & images under comparison.  If an image matches with >4 categories, it is considered a good match.
    Images should be ranked by the sum of score & topicality. Only the data for the submitted image and top 5
    matched images are returned.

    :param submitted_json_object_string: String pertaining to the object name for the submitted image.
    :param submitted_json: Key/Value pairs of the json object for the submitted image.
    :param all_images_json: List of all image json objects.
    :return: Categories for the submitted image & file names, total scores & categories for the top 5 matching
             images.
    """

    submitted_image_categories = []
    submitted_image_total_topicality = 0
    submitted_image_total_score = 0

    similar_images_objects = {}

    for key in submitted_json:
        submitted_image_categories.append(key["description"])
        submitted_image_total_topicality += key["topicality"]
        submitted_image_total_score += key["score"]

    similar_image_categories = []
    similar_image_names = []
    similar_image_totals = []

    for image_json_object in all_images_json:
        if image_json_object != submitted_json_object_string:
            matched_categories = 0
            similar_categories = []
            similar_name = ''
            total_rating = 0
            for key in all_images_json[image_json_object]:
                for category in submitted_image_categories:
                    similarity = Levenshtein.ratio(category, key["description"])
                    if similarity > 0.7:
                        matched_categories += 1
                        similar_categories.append(key["description"])
                        similar_name = image_json_object
                        total_rating += key["topicality"] + key["score"]

            if matched_categories > 4:
                similar_images_objects.update({image_json_object: all_images_json[image_json_object]})
                similar_image_categories.append(similar_categories)
                similar_image_names.append(similar_name)
                similar_image_totals.append(total_rating)

    similar_image_names, similar_image_categories, similar_image_totals = \
        rank_matches_by_category(similar_image_names, similar_image_categories, similar_image_totals)

    return submitted_image_categories, similar_image_names[0:5], similar_image_totals[0:5], \
        similar_image_categories[0:5]


def feature_based_matcher(submitted_image_file, all_images):
    """
    Use OpenCV's integrated SIFT algorithm to compare the similarity of two images.
    The similarity will be calculated by the maximum number 'good' (above a given ratio - 0.8) key point matches
    presented by the image under comparison.  The image with the highest number of good feature matches will be
    returned, along with the number of matches it achieved.

    :param submitted_image_file: Directory/Name of file to load e.g. images/1.jpg.
    :param all_images: A list of all image files that the submitted image will be compared to.
    :return: The file name for the best matched image, and the number of matches it achieved.
    """

    top_number_of_matches = 0
    top_matches = []
    top_matched_image = None
    top_keypoints1 = None
    top_keypoints2 = None
    top_matched_file = ''

    submitted_image = cv2.imread(submitted_image_file)

    for image in all_images:

        if image != submitted_image_file:

            print('Comparing submitted file with image: ', image)

            suggested_img = cv2.imread(image)

            ''' Import sift algorithm from OpenCV '''
            sift = cv2.xfeatures2d.SIFT_create()
            keypoints_1, description_1 = sift.detectAndCompute(submitted_image, None)
            keypoints_2, description_2 = sift.detectAndCompute(suggested_img, None)

            index_params = dict(algorithm=0, trees=5)
            search_params = dict()
            flann = cv2.FlannBasedMatcher(index_params, search_params)

            matches = flann.knnMatch(description_1, description_2, k=2)

            good_matches = []
            match_ratio = 0.8

            [good_matches.append(m) for m, n in matches if m.distance < match_ratio * n.distance]

            if len(good_matches) > top_number_of_matches:
                top_number_of_matches = len(good_matches)
                top_matched_image = suggested_img
                top_matches = good_matches
                top_keypoints1 = keypoints_1
                top_keypoints2 = keypoints_2
                top_matched_file = image.replace('images/', '')
                print('New top match found!')

    print('Most matched photo has ', top_number_of_matches, ' feature matches.')

    result = cv2.drawMatches(submitted_image, top_keypoints1, top_matched_image, top_keypoints2, top_matches, None)

    cv2.imwrite(FEATURE_MATCH_OUTPUT_LOCATION, result)

    '''This wait allows time for the image to be saved before ReactJS loads the front end.'''
    time.sleep(10)

    return top_matched_file, top_number_of_matches


app = flask.Flask("__main__")


@app.route("/")
def my_index():
    """
    Every time the page is loaded, do the following things:
    - Get a list of all images from the images directory.
    - Select a random image from the list.
    - Load the json from the configured file into memory.
    - Get the json object for the submitted image.
    - Find up to 5 similar images by description using the Levenshtein algorithm.
    - Rank the top 5 similar image by a total score (score+topicality).
    - Find the best matched image using the OpenCV SIFT algorithm.
    - Display the calculated information in ReactJS.

    :return: Flask render template containing image data (incl. names, categories etc.) for display in ReactJS.
    """

    try:
        print('Removing old feature match file...')
        os.remove(FEATURE_MATCH_OUTPUT_LOCATION)

    except OSError:
        print('INFO :: Old feature match file not found!')

    image_files = glob.glob(IMAGES_DIRECTORY + '*.jpg')

    submitted_image_number = randrange(len(image_files))
    submitted_image_file = image_files[submitted_image_number]

    dataset_json = load_json(file=INPUT_JSON_FILE)

    submitted_image_json_object_string, submitted_image_json = get_submitted_image_json(image_file=submitted_image_file,
                                                                                        all_image_json=dataset_json)

    submitted_image_categories, chosen_similar_image_names, chosen_similar_image_totals, \
        chosen_image_categories = find_related_images_by_category(submitted_image_json_object_string,
                                                                  submitted_image_json,
                                                                  dataset_json)

    matched_cv_image, number_of_features_matched = feature_based_matcher(submitted_image_file=submitted_image_file,
                                                                         all_images=image_files)

    submitted_img_file = submitted_image_file.replace("images/", "")

    return flask.render_template("index.html", submission=submitted_img_file,
                                 submission_categories=json.dumps(submitted_image_categories),
                                 similar_images=json.dumps(chosen_similar_image_names),
                                 similar_categories=json.dumps(chosen_image_categories), proc_img=matched_cv_image,
                                 proc_img_features=number_of_features_matched)


app.run(debug=True)
