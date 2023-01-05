

from raspil_rt.data_structs.board import *
import unittest
from copy import copy

# id len sclad amount min_per max_per


class BoardTests(unittest.TestCase):

    def setUp(self):
        self.b1 = Board(1, 100, 0)
        self.b2 = Board(2, 200, 0)

    def tearDown(self):
        pass

    def test___init__(self):
        pass

    def test___hash__(self):
        pass

    def test___eq__(self):

        self.assertEqual(self.b1, self.b1)
        self.assertNotEqual(self.b1, self.b2)

    def test___str__(self):

        self.assertNotIn('object at', str(self.b1))


class BoardStackMix:

    base2 = Board(2, 200, 0)
    base1 = Board(1, 100, 0)
    board_stack = BoardStack([
        (base1, 5),
        (base2, 43),
        (base1, 5),

    ], remain=500)


class BoardStackTests(unittest.TestCase, BoardStackMix):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test___isub__(self):
        pass

    def test___init__(self):
        self.assertEqual(self.board_stack.remain, 500)

    def test_amount(self):
        self.assertEqual(43 + 5*2, self.board_stack.amount)

    def test_total_len(self):
        self.assertEqual(200*43 + 10*100, self.board_stack.total_len)

    def test___contains__(self):
        bs1 = BoardStack([
            (self.base2, 43),
        ])
        bs2 = BoardStack([
            (self.base2, 44),
        ])
        self.assertNotIn(bs2, self.board_stack)
        self.assertIn(bs1, self.board_stack)

    def test___eq__(self):
        board_stack = BoardStack([
            (self.base1, 5),
            (self.base2, 43),
            (self.base1, 5),
        ], remain=500)
        self.assertEqual(board_stack, self.board_stack)

    def test___str__(self):
        s = str(self.board_stack)
        self.assertNotIn('object at', s)

    def test___copy__(self):
        b1 = copy(self.board_stack)
        self.assertIn(b1, self.board_stack)

    def test___sub__(self):
        bs1 = BoardStack([
            (self.base1, 10),
            (self.base2, 15)
        ])
        bs2 = BoardStack([
            (self.base1, 15),
            (self.base2, 7)
        ])

        bs4 = BoardStack([
            (self.base1, 10),
            (self.base2, 15)
        ])
        self.assertEqual((bs1 - bs4).amount, 0)
        self.assertRaises(NegativeValueError, lambda: bs1 - bs2)

    def test___add__(self):
        bs3 = BoardStack([
            (self.base1, 15),
            (self.base2, 7)
        ])
        self.assertEqual((bs3+bs3).amount, 15*2+7*2)


class BoardsWrapperTests(unittest.TestCase, BoardStackMix):
    def setUp(self):
        self.bw = BoardsWrapper(self.board_stack)

    def tearDown(self):
        pass

    def test___init__(self):
        pass

    def test_pop(self):

        self.assertEqual(self.bw.pop()[0], list(self.board_stack.keys())[1])

    def test_shift(self):
        self.bw.pop()
        self.bw.shift()
        self.assertEqual(self.bw.pop()[0], list(self.board_stack.keys())[1])


class ElementCutsawTests(unittest.TestCase, BoardStackMix):
    def setUp(self):
        self.ec = CutsawElement(Board(1, 2000, 3, 1, 200, 600), [
            BoardStack([
                (Board(1, 100, 0), 5),
                (Board(1, 200, 0), 5)
            ], remain=500),
            BoardStack([
                (Board(1, 100, 0), 4),
                (Board(1, 200, 0), 4)
            ], remain=800),
            BoardStack([
                (Board(1, 100, 0), 2),
                (Board(1, 200, 0), 2)
            ], remain=1400),
        ])

    def tearDown(self):
        pass

    def test___init__(self):
        pass

    def test_length(self):
        pass

    def test_sort_stacks(self):
        self.ec.sort_stacks()
        if self.ec.sorted:
            self.assertLess(self.ec.sorted[0].remain, self.ec.sorted[1].remain)

    def test_get_best_stack(self):
        res = self.ec.get_best_stack(self.ec[1])

        self.assertEqual(res[0].remain, self.ec[1].remain)

    def test___iadd__(self):
        pass

    def test___str__(self):
        s = str(self.ec)
        self.assertNotIn('object at', s)

    def test___copy__(self):
        pass

    def test___eq__(self):
        self.assertEqual(self.ec, copy(self.ec))


class CutsawMix():
    el1 = CutsawElement(Board(1, 2000, 2, 1, 200, 600), [
        BoardStack([(Board(1, 100, 0), 4), (Board(1, 200, 0), 4)]),
        BoardStack([(Board(1, 200, 0), 4)]),
        BoardStack([(Board(1, 300, 0), 6)]),
        BoardStack([(Board(1, 200, 0), 9)]),
    ])
    el2 = CutsawElement(Board(1, 6000, 4, 1, 200, 1200), [
        BoardStack([(Board(1, 2000, 0), 2), (Board(1, 200, 0), 9)]),
        BoardStack([(Board(1, 2000, 0), 1)]),
        BoardStack([(Board(1, 1000, 0), 5), (Board(1, 100, 0), 5)]),
    ])
    el3 = CutsawElement(Board(1, 720, 3, 1, 200, 600),  [
        BoardStack([(Board(1, 100, 0), 4)]),
        BoardStack([(Board(1, 150, 0), 4), (Board(1, 100, 0), 1)])
    ])


class CutsawTests(unittest.TestCase, CutsawMix):

    def setUp(self):
        self.cut = Cutsaw([
            (self.el1, 1),
            (self.el2, 1),
            (self.el3, 1),
        ])

    def tearDown(self):
        pass

    def test___init__(self):
        pass

    def test___getitem__(self):
        self.assertEqual(self.cut[self.el2], 1)

    def test___setitem__(self):
        self.cut[self.el1]= 100
        self.assertEqual(self.cut[self.el1], 100)

    def test___delitem__(self):
        del self.cut[self.el1]
        self.assertEqual(len(self.cut), 2)


    def test___iter__(self):
        it =iter(self.cut)
        self.assertEqual(next(it), self.el1)
            

    def test___str__(self):
        s = str(self.cut)
        self.assertNotIn('object at', s)

    def test_get_best_cutsaw_elements(self):
        pass

    def test__iter(self):
        pass

    def test___copy__(self):
        cut2 = copy(self.cut)
        cut2[self.el2] = 100
        self.assertNotEquals(cut2[self.el2], self.cut[self.el2])

 

    def test___add__(self):
        cut2 = self.cut + self.cut
        self.assertEqual(cut2[self.el2],  self.cut[self.el2]*2)





if __name__ == '__main__':

    unittest.main()
