import operations, query, config


if __name__ == '__main__':

    operations.create_database()
    operations.create_tables()
    operations.parse_phones()
    operations.add_rows_to_names()

    if config.big_base:
        query.lider()
    elif not config.big_base:
        query.rating_numbers()

