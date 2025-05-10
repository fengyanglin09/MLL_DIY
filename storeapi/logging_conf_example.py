import logging

# Get the logger and set its level
logger = logging.getLogger("myLogger")
logger.setLevel(logging.DEBUG)

# Create the handlers
console = logging.StreamHandler()
file_handler = logging.FileHandler("storeapi.log")

# Create the formatter
formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(name)s:%(lineno)d - %(message)s"
)

# Add the formatter to the handlers
console.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(console)
logger.addHandler(file_handler)


# Actually use the logger
logger.debug("Debug message")
logger.info("Info message")