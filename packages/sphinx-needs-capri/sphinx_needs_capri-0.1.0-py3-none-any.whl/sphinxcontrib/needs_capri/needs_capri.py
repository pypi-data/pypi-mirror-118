from sphinxcontrib.needs_capri.service import CodebeamerService


def setup(app):
    # Register sphinx-needs stuff after it has been initialised.
    app.connect("env-before-read-docs", prepare_env)


def prepare_env(app, env, _docname):
    app.needs_services.register("codebeamer", CodebeamerService)
