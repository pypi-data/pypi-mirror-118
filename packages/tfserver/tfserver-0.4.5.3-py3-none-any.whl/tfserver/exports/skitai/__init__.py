from atila import Atila
from rs4 import tc

def __config__ (pref):
    import tfserver

    if "TF_MODELS" in pref.config:
        for alias, model in pref.config.TF_MODELS.items ():
            config = {}
            if isinstance (model, (list, tuple)):
                model, config = model
            tfserver.add_model (alias, model, **config)

    if "GPU_LIMIT" not in pref.config:	# Mb or None
        pref.config.GPU_LIMIT = 'growth'

    if "GPU_DEVICES" not in pref.config:
        pref.config.GPU_DEVICES = []

    assert pref.config.GPU_LIMIT == 'growth' or isinstance (pref.config.GPU_LIMIT, (int, float)), 'GPU_LIMIT should be growth or Memory Mbytes'
    assert isinstance (pref.config.GPU_DEVICES, (list, tuple)), 'GPU_DEVICES should be GPU index list'

def __app__ ():
    return Atila (__name__)

def __setup__ (app, mntopt):
    from . import services
    import tfserver
    assert mntopt ['point'] == '/', 'must be mounted on root for gRPC methods'
    app.mount ('/', services)
    @app.before_mount
    def before_mount (wasc):
        import dnn
        dnn.setup_gpus (app.config.GPU_LIMIT, app.config.GPU_DEVICES) # this call must be in a child process
        for alias, model_dir in tfserver.load_models ():
            wasc.logger ("app", "- loading tensorflow model '{}' from {}".format (tc.cyan (alias), tc.white (model_dir)), 'info')

    @app.umounted
    def umounted (wasc):
        tfserver.close_models ()
