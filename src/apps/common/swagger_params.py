from drf_yasg import openapi


limit_params = openapi.Parameter(
    'limit',
    in_=openapi.IN_QUERY,
    type=openapi.TYPE_INTEGER,
    description="Pagination Limit parameter",
)

offset_params = openapi.Parameter(
    'offset',
    in_=openapi.IN_QUERY,
    type=openapi.TYPE_INTEGER,
    description="Pagination Offset parameter",
)
