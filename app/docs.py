# Config for open api interactive docs
desc = (
    'Tattoo API to provide database functionality to booking software'
)


error_responses = {
    500: {
        'description': 'Server Error',
        'content': {'application/json': {'example': {'detail': 'error in request schema'}}},
    },
    400: {
        'description': 'Bad Request',
        'content': {'application/json': {'example': {'detail': 'Bad Request'}}},
    },
    401: {
        'description': 'Unauthorized',
        'content': {'application/json': {'example': {'detail': 'Not authenticated'}}},
    },
    409: {
        'description': 'Conflict',
        'content': {'application/json': {'example': {'detail': 'Conflict in resource creation/modification.'}}},
    }
}