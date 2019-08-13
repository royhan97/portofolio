def configure(app):
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = '<some email>'
    app.config['MAIL_PASSWORD'] = '<the email password>'
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True

    app.secret_key = 'something-really-secret'
    app.config['CACHE_TYPE'] = 'null'
    app.config.update(DEBUG=True,
                      TEMPLATES_AUTO_RELOAD=True)

    return True
