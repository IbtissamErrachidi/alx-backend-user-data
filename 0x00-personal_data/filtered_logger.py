#!/usr/bin/env python3
"""
Returns an obfuscated log message
"""
from typing import List
import re
import logging
import os
import mysql.connector


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    Return an obfuscated log message
    """
    for field in fields:
        message = re.sub(field+'=.*?'+separator,
                         field+'='+redaction+separator, message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"


    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields



    def format(self, record: logging.LogRecord) -> str:
        message = super(RedactingFormatter, self).format(record)
        redacted = filter_datum(self.fields, self.REDACTION,
                                message, self.SEPARATOR)
        return redacted

def get_logger() -> logging.Logger:
    """
    logging.Logger object
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    handler = logging.StreamHandler()

    formatter = RedactingFormatter(PII_FIELDS)

    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

def get_db()-> mysql.connector.connection.MySQLConnection:
    """
    get_db
    """
    db_user = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    db_password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    db_host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME")

    return mysql.connector.connect(
        user=db_user,
        password=db_password,
        host=db_host,
        database=db_name
    )


def main():
   """
    main
    """
    logger = get_logger()
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()

    for row in rows:
        message = f"name={row[0]}; email={row[1]}; phone={row[2]}; ssn={row[3]}; password={row[4]}; ip={row[5]}; last_login={row[6]}; user_agent={row[7]}"
        logger.info(message)

    cursor.close()
    db.close()

if __name__ == "__main__":
    main()
