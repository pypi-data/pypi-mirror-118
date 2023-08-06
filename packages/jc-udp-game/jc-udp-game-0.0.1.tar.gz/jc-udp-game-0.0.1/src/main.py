def run():
    as_module = False
    try:
        from core import Game
    except:  # noqa
        from .core import Game
        as_module = True

    game = Game(500, 500)
    game.logger.info('As module:' + ('True' if as_module else 'False'))
    game.start('jencat.pro', 4242)


if __name__ == "__main__":
    run()
