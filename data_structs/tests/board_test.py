from os import path

from data_structs.board import *
import unittest
from copy import copy

# id len sclad amount min_per max_per




boards = [
    [1, 100, 0, 5, 0, 0],
    [1, 200, 0, 10, 0, 0],
    [2, 200, 0, 5, 0, 0],
    [2, 300, 0, 10, 0, 0]
]


store_boards = [
    [1, 520, 1, 2, 40, 400],
    [1, 2040, 2, 2, 40, 600],
    [1, 2580, 3, 2, 40, 800],
    [2, 1020, 1, 2, 40, 600],
    [2, 1540, 2, 2, 40, 800],
    [2, 3040, 3, 2, 40, 1200],
    [1, 6000, 4, 10, 40, 1200],
    [2, 6000, 4, 10, 40, 1200],
]


b0 = Board(*boards[0])
b1 = Board(*boards[1])
b2 = Board(*boards[2])
b3 = Board(*boards[3])

se0 = StackElement(b0, boards[0][3])
se1 = StackElement(b1, boards[1][3])
se2 = StackElement(b2, boards[2][3])
se3 = StackElement(b3, boards[3][3])

bs1 = BoardStack([se0, se1])
bs_1 = BoardStack([se0, se0])
bs2 = BoardStack([se3, se2])
bs_2 = BoardStack([se2, se2])

ec1 = ElementCutsaw(Board(*store_boards[0]), [BoardStack([se0]), BoardStack([se0, se0]),
                                              BoardStack([se1])])
ec2 = ElementCutsaw(Board(*store_boards[2]), [BoardStack([se0, se1]), BoardStack([se2]),
                                              BoardStack([se1])])

cs = Cutsaw([(ec1, 1), (ec2,1)])
pass

class BoardTests(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_equality(self):

        self.assertEqual(b1, copy(b1))

    def test_sstr(self):
        print(b1)
        self.assertNotIn('object at', str(b1))



class StackElementTests(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_copy(self):
        s_t = copy(se0)
        self.assertEqual(str(se0) == str(se0), True)
        self.assertIsNot(se0, s_t)

    def test_identity(self):
        se_0 = copy(se0)
        se_0.amount += 1
        self.assertEqual(str(se_0)== str(se0), False)
        self.assertEqual(se0, se_0)

    def test___add__(self):

        se_sum = se0 + se0
        self.assertEqual(
            se_sum.amount, se0.amount + se0.amount)
        self.assertIsNot(se1, se_sum)
        self.assertIsNot(se0, se_sum)

    def test___sub__(self):
        se_1 = copy(se1)
        se_1.amount = se1.amount+1
        se_sub = se_1 - se1
        self.assertEqual(se_sub.amount, 1)
        self.assertIsNot(se1, se_sub)
        self.assertIsNot(se_1, se_sub)

    def test___eq__(self):
        self.assertEqual(se0, copy(se0))
        self.assertNotEqual(se0, se1)

    def test_sstr(self):
        self.assertNotIn('object at', str(se0))


class BoardStackTests(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test___copy__(self):
        els_t = copy(bs1)
        els = zip(els_t, bs1)
        for el in els:
            self.assertIsNot(el[0], el[1])

    def test___len__(self):
        stack1 = BoardStack([se0, se1])
        self.assertEqual(len(se0) + len(se1), len(stack1))

    def test___sub__(self):
        self.assertEqual(len(bs1 - bs1), 0)
        self.assertEqual(len(bs1 - StackElement(b1, 1)), len(se1)+len(se0) - len(b1))

    def test_eq(self):
        self.assertEqual(bs1, copy(bs1))
        self.assertEqual(BoardStack(), BoardStack())

    def test___add__(self):
        self.assertEqual(bs1 + bs1 - bs1, copy(bs1))
        self.assertEqual(1, bs_1.element_count)
    def test_sstr(self):
        s= str(bs1)
        self.assertNotIn('object at', s)
    


class ElementCutsawTests(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test___copy__(self):
        ec1_t = copy(ec1)
        els = zip(ec1_t, ec1)
        for el in els:
            self.assertIsNot(el[0], el[1])

    def test___eq__(self):
        self.assertEqual(ec1, copy(ec1))

    def test_thick_off_stack_boards(self):
        ec_ = copy(ec1)
        ec_.thick_off_stack_boards({1: False, 2: False}, 4)
        self.assertEqual(1, len(ec_))

    def test__can_to_saw(self):
        pass

    def test_sstr(self):
        s= str(ec1)
        self.assertNotIn('object at', s)
       




class CutsawTests(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass
    def test__iter(self):
        pass
    def test___copy__(self):
        self.assertIsNot(copy(cs), cs)

    def test___eq__(self):
        ccs = copy(cs)
        els = zip(ccs, cs)
        for el in els:
            if __debug__:
                print(str(el[0]))
                print(str(el[1]))
            self.assertIsNot(el[0], el[1])

    def test_thick_off_cutsaw_elements(self):
        css = copy(cs)
        css.thick_off_cutsaw_elements({1:True, 2:True, 3:True, 4:True, 5:False}, 4)
    def test___add__(self):
        css = cs + cs + cs
        self.assertTrue( True, all(x == 2 for x in css.values()))
    def test__can_to_saw(self):
        pass
    def test_toJSON(self):
        with open(path.join(path.dirname(__file__), 'cutsaw.json'), 'w') as f:
            css = cs+cs
            f.write(str(css))
            # f.write(str(css))


if __name__ == '__main__':
    
    unittest.main()