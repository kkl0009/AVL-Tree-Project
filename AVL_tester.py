from AVL_tree import AVLTree

if __name__ == "__main__":
    avl_tree = AVLTree()

    # Test R0 Rotation
    # avl_tree.put(5, 10)
    # avl_tree.put(3, 10)
    # avl_tree.put(6, 10)
    # avl_tree.put(1, 10)
    # avl_tree.put(4, 10)
    # avl_tree.remove(6)

    # Test R0 Special Case
    # avl_tree.put(5, 10)
    # avl_tree.put(3, 10)
    # avl_tree.put(6, 10)
    # avl_tree.put(1, 10)
    # avl_tree.put(4, 10)
    # avl_tree.remove(5)

    # Test L0 Rotation
    # avl_tree.put(5, 10)
    # avl_tree.put(1, 10)
    # avl_tree.put(7, 10)
    # avl_tree.put(6, 10)
    # avl_tree.put(8, 10)
    # avl_tree.remove(1)

    # Test L0 Special Case
    # avl_tree.put(5, 10)
    # avl_tree.put(1, 10)
    # avl_tree.put(7, 10)
    # avl_tree.put(6, 10)
    # avl_tree.put(8, 10)
    # avl_tree.remove(5)

    # Test R1 Rotation
    # avl_tree.put(5, 10)
    # avl_tree.put(3, 10)
    # avl_tree.put(6, 10)
    # avl_tree.put(1, 10)
    # avl_tree.remove(6)

    # Test R-1 Rotation
    # avl_tree.put(5, 10)
    # avl_tree.put(3, 10)
    # avl_tree.put(6, 10)
    # avl_tree.put(4, 10)
    # avl_tree.remove(6)

    # Test L1 Rotation
    # avl_tree.put(5, 10)
    # avl_tree.put(3, 10)
    # avl_tree.put(7, 10)
    # avl_tree.put(6, 10)
    # avl_tree.remove(3)

    # Test L1 Special Case
    # avl_tree.put(5, 10)
    # avl_tree.put(3, 10)
    # avl_tree.put(7, 10)
    # avl_tree.put(6, 10)
    # avl_tree.remove(5)

    # Test L-1 Rotation
    # avl_tree.put(5, 10)
    # avl_tree.put(3, 10)
    # avl_tree.put(7, 10)
    # avl_tree.put(8, 10)
    # avl_tree.remove(3)

    # Test L-1 Special Case
    # avl_tree.put(5, 10)
    # avl_tree.put(3, 10)
    # avl_tree.put(7, 10)
    # avl_tree.put(8, 10)
    # avl_tree.remove(5)

    # Multiple Rotation Case
    # avl_tree.put(50, 10)
    # avl_tree.put(25, 10)
    # avl_tree.put(75, 10)
    # avl_tree.put(15, 10)
    # avl_tree.put(40, 10)
    # avl_tree.put(60, 10)
    # avl_tree.put(80, 10)
    # avl_tree.put(35, 10)
    # avl_tree.put(55, 10)
    # avl_tree.put(65, 10)
    # avl_tree.put(90, 10)
    # avl_tree.put(62, 10)

    # print(avl_tree.get_range(16, 89))
    # print(avl_tree.get_smallest_ge(88))
    # print(avl_tree.delete_all_le(49))
    # avl_tree.remove(15)

    # Broken test case?
    # avl_tree.put(56, 10)
    # avl_tree.put(44, 10)
    # avl_tree.put(73, 10)
    # avl_tree.put(49, 10)
    # avl_tree.put(64, 10)
    # avl_tree.put(83, 10)
    # avl_tree.put(90, 10)
    # avl_tree.remove(73)

    # General test cases
    # avl_tree.put(21, 10)
    # avl_tree.put(23, 20)
    # avl_tree.put(27, 30)
    # avl_tree.put(26, 40)
    # avl_tree.put(24, 50)
    # avl_tree.put(25, 60)
    # avl_tree.put(22, 70)
    # avl_tree.put(19, 80)
    # avl_tree.put(20, 90)
    # avl_tree.put(24.5, 100)

    # avl_tree.remove(27)
    # avl_tree.remove(25)
    # avl_tree.remove(24.5)
    # avl_tree.remove(20)
    # avl_tree.remove(22)
    # avl_tree.remove(19)
    # avl_tree.remove(24)
    # avl_tree.remove(21)
    # avl_tree.remove(23)
    # avl_tree.remove(26)

    # Debug test
    # avl_tree.put(50, 10)
    # avl_tree.put(30, 10)
    # avl_tree.put(70, 10)
    # avl_tree.put(25, 10)
    # avl_tree.put(35, 10)
    # avl_tree.put(65, 10)
    # avl_tree.put(75, 10)
    # avl_tree.put(20, 10)
    # avl_tree.put(28, 10)
    # avl_tree.put(40, 10)
    # avl_tree.put(60, 10)
    # avl_tree.put(26, 10)

    # avl_tree.remove(30)
    # Large scale testing
    for i in range(0, 15313):
        avl_tree.put(i, 10)
    
    # for i in range(0, 50000):
    #     avl_tree.put(i, 10)

    # avl_tree.remove(2500)
    for i in range(2500, 7500):
        avl_tree.remove(i)
    #     # avl_tree.print_tree()

    avl_tree.print_tree()
