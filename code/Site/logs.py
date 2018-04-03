# Copyright (c) 2017 Jonathan Bassen, Stanford University

import logging


def get_app_logger(log_path):
    app_logger = logging.getLogger("tornado.application")
    gen_logger = logging.getLogger("tornado.general")
    acc_logger = logging.getLogger("tornado.access")
    app_fh = logging.FileHandler(log_path + '/app.log')
    gen_fh = logging.FileHandler(log_path + '/gen.log')
    acc_fh = logging.FileHandler(log_path + '/acc.log')
    app_logger.addHandler(app_fh)
    gen_logger.addHandler(gen_fh)
    acc_logger.addHandler(acc_fh)
    return app_logger
