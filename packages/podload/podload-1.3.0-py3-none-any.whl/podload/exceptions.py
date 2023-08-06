'''
Podload exceptions module.
'''


class PodloadError(Exception):
    '''
    Exception which is thrown when a podload error occurs.
    '''


class ParserError(PodloadError):
    '''
    Exception which is thrown when a parsing error occurs.
    '''


class PodcastNotFoundError(PodloadError):
    '''
    Exception which is thrown when a podcast with a certain title wasn't found.
    '''
