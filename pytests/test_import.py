import sqlalchemy_continuum
print("SQLAlchemy Continuum import successful")


try:
    import sqlalchemy_continuum
    print("sqlalchemy_continuum import successful")
except ModuleNotFoundError:
    print("ModuleNotFoundError: sqlalchemy_continuum")
