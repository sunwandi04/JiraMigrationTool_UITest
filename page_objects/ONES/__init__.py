import logging

class LoggerHandler():

    # 初始化 Logger
    def __init__(self,
                 name='root',
                 logger_level= 'DEBUG',
                 file=None,
                 logger_format = '%(asctime)s-%(message)s'
                 # logger_format = '%(asctime)s-%(filename)s-%(lineno)d-%(message)s'
                 ):

        # 1、初始化logger收集器
        logger = logging.getLogger(name)


        # 2、设置日志收集器level级别
        logger.setLevel(logger_level)

        # 5、初始化 handler 格式
        fmt = logging.Formatter(logger_format)

        # 3、初始化日志处理器

        # 如果传递了文件，就会输出到file文件中
        if file:
            file_handler = logging.FileHandler(file)
            # 4、设置 file_handler 级别
            file_handler.setLevel(logger_level)
            # 6、设置handler格式
            file_handler.setFormatter(fmt)
            # 7、添加handler
            logger.addHandler(file_handler)

        # 默认都输出到控制台
        stream_handler = logging.StreamHandler()
        # 4、设置 stream_handler 级别
        stream_handler.setLevel(logger_level)
        # 6、设置handler格式
        stream_handler.setFormatter(fmt)
        # 7、添加handler
        logger.addHandler(stream_handler)

        # 设置成实例属性
        self.logger = logger

    # 返回日志信息

    def debug(self,msg):
        return self.logger.debug(msg)

    def info(self,msg):
        return self.logger.info(msg)

    def warning(self,msg):
        return self.logger.warning(msg)

    def error(self,msg):
        return self.logger.error(msg)

    def critical(self,msg):
        return self.logger.critical(msg)
