import unittest
from curseswm import DynamicBox, Window
 
class TestUM(unittest.TestCase):
 
    def setUp(self):
        self.dyn = DynamicBox()
        self.w1 = Window("w1")
        self.w2 = Window("w2")
        self.w3 = Window("w3")

        self.dyn.add_window(self.w1, weight=2,priority=3,min_dimension=4)

        self.assertEqual(len(self.dyn.window_list), 1)

        self.dyn.add_window(self.w1, weight=3,priority=2,min_dimension=4)

        self.assertEqual(len(self.dyn.window_list), 2)

        self.dyn.add_window(self.w1, weight=1,priority=1,min_dimension=4)

        self.assertEqual(len(self.dyn.window_list), 3)
 
    def test(self):
        self.dyn._reset_display_of_windows()

        self.assertEqual(self.dyn._get_weights_list(),[2,3,1])
        self.assertEqual(self.dyn._get_total_weights(),6)

        self.dyn._correct_dimensions(30)
        self.assertEqual(self.dyn._get_total_actual_dim(),30)

        self.assertEqual(self.dyn._solution_is_feasable(),False)
        self.dyn.window_list[0].actual_dim = 4
        self.dyn.window_list[1].actual_dim = 4
        self.dyn.window_list[2].actual_dim = 5
        self.assertEqual(self.dyn._solution_is_feasable(),True)

        self.dyn._reset_display_of_windows()
        self.dyn._shutoff_lowest_priority()
        self.assertEqual(self.dyn.window_list[0].display,True)
        self.assertEqual(self.dyn.window_list[1].display,True)
        self.assertEqual(self.dyn.window_list[2].display,False)

        self.assertEqual(self.dyn._find_first_displayed_window().display,True)




if __name__ == '__main__':
    unittest.main()