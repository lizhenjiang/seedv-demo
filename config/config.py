DATABASE_CONFIG = {
    'connections': {
        'default': 'mysql://root:@localhost:3306/seedv2',
    },
    'apps': {
        'models': {
            'models': ['app.models.apply','app.models.process', 'aerich.models'],
            'default_connection': 'default',
        },
    },
}