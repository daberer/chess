from chess.procedure import Game


def test_board():
    g = Game()
    g.create_boards()
    #g.fill_board()
    assert g.board == {
        'A8': [(0, 0), None],
        'B8': [(100, 0), None],
        'C8': [(200, 0), None],
        'D8': [(300, 0), None],
        'E8': [(400, 0), None],
        'F8': [(500, 0), None],
        'G8': [(600, 0), None],
        'H8': [(700, 0), None],
        'A7': [(0, 100), None],
        'B7': [(100, 100), None],
        'C7': [(200, 100), None],
        'D7': [(300, 100), None],
        'E7': [(400, 100), None],
        'F7': [(500, 100), None],
        'G7': [(600, 100), None],
        'H7': [(700, 100), None],
        'A6': [(0, 200), None],
        'B6': [(100, 200), None],
        'C6': [(200, 200), None],
        'D6': [(300, 200), None],
        'E6': [(400, 200), None],
        'F6': [(500, 200), None],
        'G6': [(600, 200), None],
        'H6': [(700, 200), None],
        'A5': [(0, 300), None],
        'B5': [(100, 300), None],
        'C5': [(200, 300), None],
        'D5': [(300, 300), None],
        'E5': [(400, 300), None],
        'F5': [(500, 300), None],
        'G5': [(600, 300), None],
        'H5': [(700, 300), None],
        'A4': [(0, 400), None],
        'B4': [(100, 400), None],
        'C4': [(200, 400), None],
        'D4': [(300, 400), None],
        'E4': [(400, 400), None],
        'F4': [(500, 400), None],
        'G4': [(600, 400), None],
        'H4': [(700, 400), None],
        'A3': [(0, 500), None],
        'B3': [(100, 500), None],
        'C3': [(200, 500), None],
        'D3': [(300, 500), None],
        'E3': [(400, 500), None],
        'F3': [(500, 500), None],
        'G3': [(600, 500), None],
        'H3': [(700, 500), None],
        'A2': [(0, 600), None],
        'B2': [(100, 600), None],
        'C2': [(200, 600), None],
        'D2': [(300, 600), None],
        'E2': [(400, 600), None],
        'F2': [(500, 600), None],
        'G2': [(600, 600), None],
        'H2': [(700, 600), None],
        'A1': [(0, 700), None],
        'B1': [(100, 700), None],
        'C1': [(200, 700), None],
        'D1': [(300, 700), None],
        'E1': [(400, 700), None],
        'F1': [(500, 700), None],
        'G1': [(600, 700), None],
        'H1': [(700, 700), None],
    }

    #'r1bqkb1r/ppp2ppp/2p2n2/8/4p3/8/pppp1ppp/rnbqkb1r'
