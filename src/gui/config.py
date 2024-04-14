import tomli


def parse_config(filepath: str) -> dict:
    """
    Charge le fichier de configuration TOML.

    :param filepath: Chemin du fichier de configuration.
    :return: Dictionnaire de la configuration.
    :except tomli.TOMLDecodeError: Si le fichier est invalide.
    :except AssertionError: Si un champ est manquant.
    """
    # Parsing du fichier de configuration
    with open(filepath, "rb") as f:
        res = tomli.load(f)

    # Vérification des champs
    assert 'schema' in res
    assert 'currency' in res['schema']
    assert 'invoice' in res
    assert 'seller' in res['invoice']
    assert str == type(res['invoice']['seller'])
    assert 'customer' in res['invoice']
    assert str == type(res['invoice']['customer'])
    assert 'tva' in res['invoice']
    assert float == type(res['invoice']['tva'])
    assert 0. <= res['invoice']['tva'] <= 1.

    return res
