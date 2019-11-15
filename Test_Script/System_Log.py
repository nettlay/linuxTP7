import logging


def file_log(root, message):
    logging.basicConfig(filename=root+'/Test_Report/systeminformation.log', level=logging.DEBUG,
                        format='%(asctime)s - %(message)s.', datefmt='')
    logger = logging.getLogger()
    logger.info(message)

