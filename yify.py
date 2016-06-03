import requests
import sys
import json
BASE_URL = "http://www.yify.is/api/v2"
DEFAULT_LIMIT = 50


def search_movie(query, results):
    """ Searches a movie using yify search API.
    query is the term to search for and results is the
    number of results, counting from the first, to be returned"""
    limit = min(results, DEFAULT_LIMIT)
    params = {'query_term': query, 'limit': limit}
    response = requests.get('%s/list_movies.json' % BASE_URL, params=params)
    dict_response = json.loads(response.content)
    if dict_response['status'] != 'ok':
        print >> sys.stderr, 'Whoops! Something went wrong with the request'
        print >> sys.stderr, dict_response['status_message']
    # Parsing of the response to get movie data:
    return dict_response['data']['movies']


def show_results(movies):
    # TO(NEVER)DO implement
    return movies


if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option('-s', '--search', dest='query_term', default='',
                      help='Indicates the movie name, director, actor, etc. to search for')
    parser.add_option('-n', '--results-number', type='int', dest='number', default=10,
                      help='Indicates the number of results to display. Defaults to 10')
    parser.add_option('-r', '--raw', action='store_true', dest='raw_data', default=False)
    options, args = parser.parse_args()
    args = " ".join(args)
    if options.query_term == '' and args == '':
        print >> sys.stderr, 'Error: query term not specified'
        sys.exit(-1)
    movies = search_movie(options.query_term or args, options.number)
    if options.raw_data:
        from pprint import pprint
        pprint(json.dumps(movies))
    else:
        show_results(movies)
