
##########################
# TODO: REMEMBER TO ADD A HEIGHT FIELD TO THE NODES TO CALCULATING THE RANGES AND SUCH
# THen get the range by using just 2 traversals O(log(n))
##########################

# NOTE: Make sure to test every type of rotation (insertion and deletion) to make sure balance factors and such are correct

class AVLTree:
    def __init__(self):
        self.root = None

    def get(self, key):
        track_node = self.root

        # Search the tree for the item with the given key
        while track_node is not None:
            if key == track_node.key:
                return track_node.element
            elif key < track_node.key:
                track_node = track_node.left_child
            else:
                track_node = track_node.right_child
        
        # Called if the search falls off the tree, meaning the item was not found
        return None
    
    def __get_node(self, key):
        track_node = self.root

        # Search the tree for the item with the given key
        while track_node is not None:
            if key == track_node.key:
                return track_node
            elif key < track_node.key:
                track_node = track_node.left_child
            else:
                track_node = track_node.right_child
        
        # Called if the search falls off the tree, meaning the item was not found
        return None
    
    def get_range(self, key_low, key_high, min_case = False, max_case = False):
        if self.root is not None:
            return self.__get_range_recursive(self.root, key_low, key_high, min_case, max_case)
        else:
            return []
        
    def __get_range_recursive(self, current_node, key_low, key_high, min_case, max_case):
        if current_node is None:
            return []

        key = current_node.key
        if key > key_high and not max_case:
            # Key is out of range, check left subtree
            sub_items = self.__get_range_recursive(current_node.left_child, key_low, key_high, min_case, max_case)
            return sub_items
        elif key < key_low and not min_case:
            # Key is out of range, check right subtree
            sub_items = self.__get_range_recursive(current_node.right_child, key_low, key_high, min_case, max_case)
            return sub_items
        else:
            # Key must be in the range, so we should add it to the items list
            left_items = self.__get_range_recursive(current_node.left_child, key_low, key_high, min_case, max_case)

            right_items = self.__get_range_recursive(current_node.right_child, key_low, key_high, min_case, max_case)

            left_items.append((current_node.key, current_node.element))

            left_items.extend(right_items)
            return left_items
        
    def delete_all_le(self, key):
        items = self.get_range(0, key, min_case = True)
        for item in items:
            last_item = item
            self.remove(item[0])
        
        return items
    
    # def increase_keys_in_range(self):


    def get_smallest_ge(self, key):
        smallest_ge = self.__get_smallest_ge_helper(key, self.root)
        if smallest_ge is None:
            return None
        return smallest_ge.element

    def __get_smallest_ge_helper(self, key, current_node):
        if current_node is None:
            return
        elif key == current_node.key:
            return current_node.right_child
        elif key < current_node.key:
            # Must be in left child
            prev_smallest = self.__get_smallest_ge_helper(key, current_node.left_child)
            
            if prev_smallest is not None and prev_smallest.key <= current_node.key:
                return prev_smallest
            else:
                return current_node
        else:
            # Must be in right child
            return self.__get_smallest_ge_helper(key, current_node.right_child)

    def put(self, key, element):
        # Node to be inserted
        insert_node = self.Node(key, element)

        # If there is no root yet, make this new node the root
        if self.root is None:
            self.root = insert_node
        else:
            # Otherwise, start traversing down the tree
            update_bf = self.__put_helper(self.root, insert_node)

            # Finally, check if root itself has a balance factor of 2 or -2
            if self.root.balance_factor == 2 or self.root.balance_factor == -2:
                self.root = self.__perform_rotation(self.root, insert_node.key, at_root = True)
     

    """
        Returns update_bf : bool
    """

    def __put_helper(self, start_node, insert_node):
        start_key = start_node.key
        insert_key = insert_node.key

        if insert_key < start_key:
            # New item is in the left branch of this node
            if start_node.left_child is None:
                # Left child of this node is empty, add the new node here
                start_node.left_child = insert_node
                # Update the balance factor of this node to account for this
                start_node.balance_factor += 1
                # Return this node to a higher level up
                return True
            else:
                # There already is a left child of this node
                update_bf = self.__put_helper(start_node.left_child, insert_node)

                if update_bf:
                    child_bf = start_node.left_child.balance_factor
                    if child_bf == 0:
                        # There is no need to update any more balance factors afterwards
                        return False
                    elif child_bf == 1 or child_bf == -1:
                        # Update the balance factor for this node
                        start_node.balance_factor += 1
                        return True
                    elif child_bf == 2 or child_bf == -2:
                        # Will need to perform a rotation here
                        new_child = self.__perform_rotation(start_node, insert_key)
                        start_node.left_child = new_child
                        return False
        else:
            # New item is in the right branch of this node
            if start_node.right_child is None:
                # Right child of this node is empty, add the new node here
                start_node.right_child = insert_node
                # Update the balance factor of this node to account for this
                start_node.balance_factor -= 1
                # Return this node to a higher level up
                return True
            else:
                # There already is a right child of this node
                update_bf = self.__put_helper(start_node.right_child, insert_node)

                if update_bf:
                    child_bf = start_node.right_child.balance_factor
                    if child_bf == 0:
                        # There is no need to update any more balance factors afterwards
                        return False
                    elif child_bf == 1 or child_bf == -1:
                        # Update the balance factor for this node
                        start_node.balance_factor -= 1
                        return True
                    elif child_bf == 2 or child_bf == -2:
                        # Will need to perform a rotation here
                        new_child = self.__perform_rotation(start_node, insert_key)
                        start_node.right_child = new_child
                        return False

    def remove(self, key):
        if self.root is None:
            # There are no elements to delete, return failure
            return None
        if key == self.root.key:
            if self.root.left_child is None and self.root.right_child is None:
                # Delete root element
                root_key = self.root.key
                root_element = self.root.element
                self.root = None
                return (root_key, root_element)
            
            elif self.root.left_child is None:
                root_key = self.root.key
                root_element = self.root.element
                self.root = self.root.right_child

                return (root_key, root_element)
            elif self.root.right_child is None:
                root_key = self.root.key
                root_element = self.root.element
                self.root = self.root.left_child

                return (root_key, root_element)
            else:
                replace_node = self.__get_largest_in_tree(self.root.left_child)

                update_bf = self.__remove_helper(self.root.left_child, replace_node.key)

                special_delete = False

                # TODO: Figure out what is going on here: UPDATE< NEEDED TO ROTATE AFTER THAT DELETE SOMEWHERE, PROBABLY BELOW
                if self.root.left_child is not None and self.root.left_child.key == replace_node.key and self.root.left_child.element == replace_node.element:
                    if self.root.left_child.left_child is not None:
                        self.root.left_child = self.root.left_child.left_child
                    else:
                        self.root.left_child = None

                    self.root.balance_factor -= 1
                    update_bf = True
                    special_delete = True

                self.root.key = replace_node.key
                self.root.element = replace_node.element

                if update_bf:
                    if self.root.left_child is not None and self.root.left_child.balance_factor == 0:
                        self.root.balance_factor -= 1

                    if self.root.balance_factor == 2 or self.root.balance_factor == -2:
                        self.root = self.__delete_rotation(self.root, replace_node.key, at_root = True, special_delete = special_delete)


        else:
            update_bf = self.__remove_helper(self.root, key)

            if self.root.balance_factor == 2 or self.root.balance_factor == -2:
                self.root = self.__delete_rotation(self.root, key, at_root = True)

    def __remove_helper(self, start_node, target_key):

        if target_key < start_node.key:
            next_child = start_node.left_child
        else:
            next_child = start_node.right_child

        if next_child is None:
            # We have fallen off the tree, and so the element does not exist in the tree
            return False
        elif target_key == next_child.key:
            # We have found the node we need to delete
            if next_child.left_child is None and next_child.right_child is None:
                # A degree 0 node, so deletion is easy
                if target_key < start_node.key:
                    start_node.left_child = None

                    start_node.balance_factor -= 1
                else:
                    start_node.right_child = None

                    start_node.balance_factor += 1
                return True
            elif next_child.left_child is None:
                # Only the left child is None, so a degree 1 node
                if target_key < start_node.key:
                    start_node.left_child = next_child.right_child
                    start_node.balance_factor -= 1
                else:
                    start_node.right_child = next_child.right_child
                    start_node.balance_factor += 1
                return True
            elif next_child.right_child is None:
                # Only the right child is None, so again a degree 1 node
                if target_key < start_node.key:
                    start_node.left_child = next_child.left_child
                    start_node.balance_factor -= 1
                else:
                    start_node.right_child = next_child.left_child
                    start_node.balance_factor += 1
                return True
            else:
                # The node must be a degree 2 node
                # Find the largest node less than the current node
                replace_node = self.__get_largest_in_tree(next_child.left_child)
                # if target_key < start_node.key:
                #     start_node.left_child.key = replace_node.key
                #     start_node.left_child.element = replace_node.element
                # else:
                #     start_node.right_child.key = replace_node.key
                #     start_node.right_child.element = replace_node.element

                # Now delete the new item with this new key
                update_bf = self.__remove_helper(next_child, replace_node.key)

                # TODO: Figure out what is going on here
                # PROBLEM WAS THAT YOU WERE DELETING WITHOUT ROTATING AFTER!!!!!!!!!!! FIX THAT!

                special_delete = False

                if next_child.left_child is not None and next_child.left_child.key == replace_node.key and next_child.left_child.element == replace_node.element:
                    if next_child.left_child.left_child is not None:
                        next_child.left_child = next_child.left_child.left_child
                    else:
                        next_child.left_child = None

                    next_child.balance_factor -= 1
                    update_bf = True
                    special_delete = True

                next_child.key = replace_node.key
                next_child.element = replace_node.element

                if update_bf:

                    # print('In the heres', start_node, child_node)
                    # The deleted node must have been in the left subtree
                    # start_node.balance_factor -= 1
                    # if start_node.balance_factor == 1 or start_node.balance_factor == -1:
                    #     return False
                    # else:
                    #     return True
                    if target_key < start_node.key:
                        child_node = start_node.left_child

                        if child_node.balance_factor == 0:
                            # Height of left subtree decreased
                            start_node.balance_factor -= 1
                            return True
                        elif child_node.balance_factor == 1 or child_node.balance_factor == -1:
                            # Height has remained the same, no need to continue up tree
                            return False
                        elif child_node.balance_factor == 2 or child_node.balance_factor == -2:
                            # Must perform a rotation
                            start_node.left_child = self.__delete_rotation(start_node, target_key, special_delete = special_delete)
                            if start_node.left_child.balance_factor == 1 or start_node.left_child.balance_factor == -1:
                                return False
                            else:
                                start_node.balance_factor -= 1
                                return True
                    else:
                        child_node = start_node.right_child

                        if child_node.balance_factor == 0:
                            # Height of right subtree decreased
                            start_node.balance_factor += 1
                            return True
                        elif child_node.balance_factor == 1 or child_node.balance_factor == -1:
                            # Height has remained the same, no need to continue up tree
                            return False
                        elif child_node.balance_factor == 2 or child_node.balance_factor == -2:
                            # Must perform a rotation
                            start_node.right_child = self.__delete_rotation(start_node, target_key, special_delete = special_delete)
                            if start_node.right_child.balance_factor == 1 or start_node.right_child.balance_factor == -1:
                                return False
                            else:
                                start_node.balance_factor += 1
                                return True
                            

        else:
            update_bf = self.__remove_helper(next_child, target_key)

            if update_bf:
                if target_key < start_node.key:
                    child_node = start_node.left_child

                    if child_node.balance_factor == 0:
                        # Height of left subtree decreased
                        start_node.balance_factor -= 1
                        return True
                    elif child_node.balance_factor == 1 or child_node.balance_factor == -1:
                        # Height has remained the same, no need to continue up tree
                        return False
                    elif child_node.balance_factor == 2 or child_node.balance_factor == -2:
                        # Must perform a rotation
                        start_node.left_child = self.__delete_rotation(start_node, target_key)
                        if start_node.left_child.balance_factor == 1 or start_node.left_child.balance_factor == -1:
                            return False
                        else:
                            start_node.balance_factor -= 1
                            return True
                else:
                    child_node = start_node.right_child

                    if child_node.balance_factor == 0:
                        # Height of left subtree decreased
                        start_node.balance_factor += 1
                        return True
                    elif child_node.balance_factor == 1 or child_node.balance_factor == -1:
                        # Height has remained the same, no need to continue up tree
                        return False
                    elif child_node.balance_factor == 2 or child_node.balance_factor == -2:
                        # Must perform a rotation
                        start_node.right_child = self.__delete_rotation(start_node, target_key)
                        if start_node.right_child.balance_factor == 1 or start_node.right_child.balance_factor == -1:
                            return False
                        else:
                            start_node.balance_factor += 1
                            return True


    def get_max(self):
        if self.root is None:
            return None

        max_node = self.__get_largest_in_tree(self.root)
        return (max_node.key, max_node.element)

    def __get_largest_in_tree(self, sub_root):
        track_node = sub_root

        # Traverse the tree until you fall off, at which point you must be at the rightmost node
        while track_node is not None:
            prev_node = track_node
            track_node = track_node.right_child


        return prev_node
    
    def fix_max(self):
        max_item = self.get_max()
        max_node = self.__get_node(max_item[0])
        # Set to a very large literal so that it will stay as the max
        max_node.key = 10000000000000000
    
    def __delete_rotation(self, start_node, key, at_root = False, special_delete = False):
        direction = ''

        if at_root:
            gp = self.root
        else:
            if key < start_node.key:
                gp = start_node.left_child
            else:
                gp = start_node.right_child

        if key < gp.key or special_delete or gp.left_child is None:
            # Note that because we are deleting, we want to look down the opposite branch this time
            p = gp.right_child
            direction = 'L'
        else:
            p = gp.left_child
            direction = 'R'

        # if p is None:
        #     self.print_tree()
        #     print('key:', key, 'start_node:', start_node)
        #     print('gp:', gp, "left:", gp.left_child, "right:", gp.right_child, "key:", key, "gp key:", gp.key, 'special:', special_delete)
            
        if p is None:
            gp.balance_factor = 0
            return gp

        if p.balance_factor == 0:
            if direction == 'L':
                # L0 Rotation
                sub_root = self.__L0_rotation(gp, p)
            elif direction == 'R':
                # R0 Rotation
                sub_root = self.__R0_rotation(gp, p)
        elif p.balance_factor == 1:
            if direction == 'L':
                # L1 Rotation
                sub_root = self.__L1_rotation(gp, p)
            elif direction == 'R':
                # R1 Rotation
                sub_root = self.__R1_rotation(gp, p)
        elif p.balance_factor == -1:
            if direction == 'L':
                # L-1 Rotation
                sub_root = self.__Lminus_rotation(gp, p)
            elif direction == 'R':
                # R-1 Rotation
                sub_root = self.__Rminus_rotation(gp, p)

        return sub_root

    def __L0_rotation(self, gp, p):
        # gp's left child is unchanged
        # gp right child becomes p's left child
        gp.right_child = p.left_child

        # p's left child becomes gp
        p.left_child = gp
        # p's right child is unchanged

        gp.balance_factor = -1
        p.balance_factor = 1

        # p becomes the new subtree root
        return p

    def __R0_rotation(self, gp, p):
        # gp left child becomes p's right child
        gp.left_child = p.right_child
        # gp's right child is unchanged

        # p's left child is unchanged
        # p's right child becomes gp
        p.right_child = gp

        gp.balance_factor = 1
        p.balance_factor = -1

        # p becomes the new subtree root
        return p
    
    def __Lminus_rotation(self, gp, p):
        # gp's left child is unchanged
        # gp right child becomes p's left child
        gp.right_child = p.left_child

        # p's left child becomes gp
        p.left_child = gp
        # p's right child is unchanged

        gp.balance_factor = 0
        p.balance_factor = 0

        # p becomes the new subtree root
        return p
    
    def __R1_rotation(self, gp, p):
        gp.left_child = p.right_child
        # gp's right child is unchanged

        # p's left child is unchanged
        # p's right child becomes gp
        p.right_child = gp

        gp.balance_factor = 0
        p.balance_factor = 0

        # p becomes the new subtree root
        return p
    
    def __L1_rotation(self, gp, p):
        c = p.left_child

        # gp left child is unchanged
        # Right child of gp is left child of c
        gp.right_child = c.left_child

        # Left child of p is right child of c
        p.left_child = c.right_child
        # Right child of p is unchanged

        # Left child of c is gp
        c.left_child = gp
        # Right child of c is p
        c.right_child = p

        if c.balance_factor == 0:
            gp.balance_factor = 0
            p.balance_factor = 0
        elif c.balance_factor == 1:
            gp.balance_factor = 0
            p.balance_factor = -1
        elif c.balance_factor == -1:
            gp.balance_factor = 1
            p.balance_factor = 0
        c.balance_factor = 0

        return c

    def __Rminus_rotation(self, gp, p):
        c = p.right_child

        # Left child of gp is right child of c
        gp.left_child = c.right_child
        # gp right child is unchanged
        
        # Left child of p is unchanged
        # Right child of p is left child of c
        p.right_child = c.left_child

        # Left child of c is p
        c.left_child = p
        # Right child of c is gp
        c.right_child = gp

        if c.balance_factor == 0:
            gp.balance_factor = 0
            p.balance_factor = 0
        elif c.balance_factor == 1:
            gp.balance_factor = -1
            p.balance_factor = 0
        elif c.balance_factor == -1:
            gp.balance_factor = 0
            p.balance_factor = 1
        c.balance_factor = 0

        return c
        
    def __perform_rotation(self, start_node, key, at_root = False):
        # Need to determine the type of rotation to perform
        # Note that the left and right children of the grandparent and parent here cannot be None (otherwise balance factors are wrong)
        path = ''

        # Find the grandparent node to start with
        if at_root:
            gp = self.root
        else:
            if key < start_node.key:
                gp = start_node.left_child
            else:
                gp = start_node.right_child

        # Get the parent node (child of the grandparent)
        if key < gp.key:
            p = gp.left_child
            path += 'L'
        else:
            p = gp.right_child
            path += 'R'

        # Get the child node (child of the parent)
        if key < p.key:
            c = p.left_child
            path += 'L'
        else:
            c = p.right_child
            path += 'R'
        
        if path == 'LL':
            # Perform an LL Rotation
            sub_root = self.__LL_rotation(gp, p)
        elif path == 'RR':
            # Perform an RR Rotation
            sub_root = self.__RR_rotation(gp, p)
        elif path == 'LR':
            # Perform an LR Rotation
            sub_root = self.__LR_rotation(gp, p, c)
        else:
            # Perform an RL Rotation
            sub_root = self.__RL_rotation(gp, p, c)

        return sub_root
            
    def __LL_rotation(self, gp, p):
        # Start with gp
        # Left child of gp becomes old right child of p
        gp.left_child = p.right_child
        # Right child of gp remains unchanged

        # Finish with p
        # Left child of p remains unchanged
        # Right child of p becomes gp
        p.right_child = gp

        # Both balance factors become 0
        gp.balance_factor = 0
        p.balance_factor = 0

        # p is the new root of this subtree
        return p

    def __RR_rotation(self, gp, p):
        # Start with gp
        # Left child of gp remains unchanged
        # Right child of gp becomes old left child of p
        gp.right_child = p.left_child

        # Finish with p
        # Left child of p becomes gp
        p.left_child = gp
        # Right child of p remains unchanged

        # Both balance factors become 0
        gp.balance_factor = 0
        p.balance_factor = 0

        # p is the new root of this subtree
        return p

    def __LR_rotation(self, gp, p, c):
        # Start with gp
        # Left child of gp becomes old right child of c
        gp.left_child = c.right_child
        # Right child of gp remains unchanged

        # Continue with p
        # Left child of p remains unchanged
        # Right child of p becomes old left child of c
        p.right_child = c.left_child

        # Finish with c
        # Left child of c becomes p
        c.left_child = p
        # Right child of c becomes gp
        c.right_child = gp

        # Update balance factors as necessary
        if c.balance_factor == 1:
            gp.balance_factor = -1
        else:
            gp.balance_factor = 0

        if c.balance_factor == -1:
            p.balance_factor = 1
        else:
            p.balance_factor = 0
        
        c.balance_factor = 0

        # c is the new root of this subtree
        return c

    def __RL_rotation(self, gp, p, c):
        # Start with gp
        # Left child of gp remains unchanged
        # Right child of gp becomes old left child of c
        gp.right_child = c.left_child

        # Continue with p
        # Left child of p becomes old right child of c
        p.left_child = c.right_child
        # Right child of p remains unchanged

        # Finish with c
        # Left child of c becomes gp
        c.left_child = gp
        # Right child of c becomes p
        c.right_child = p

        # Update balance factors as necessary
        if c.balance_factor == -1:
            gp.balance_factor = 1
        else:
            gp.balance_factor = 0

        if c.balance_factor == 1:
            p.balance_factor = -1
        else:
            p.balance_factor = 0
        
        c.balance_factor = 0

        # c is the new root of this subtree
        return c
    
    def print_tree(self):
        if self.root is None:
            print('Tree is empty...')
        else:
            print('Inorder:')
            self.__print_inorder(self.root)

            print('\nPreorder:')
            self.__print_preorder(self.root)

            print('\nPostorder:')
            self.__print_postorder(self.root)

            print()

    def __print_inorder(self, current_node):
        if current_node.left_child is not None:
            self.__print_inorder(current_node.left_child)
        
        print(str(current_node) + ' ', end='')

        if current_node.right_child is not None:
            self.__print_inorder(current_node.right_child)
    
    def __print_preorder(self, current_node):
        print(str(current_node) + ' ', end='')

        if current_node.left_child is not None:
            self.__print_preorder(current_node.left_child)

        if current_node.right_child is not None:
            self.__print_preorder(current_node.right_child)

    def __print_postorder(self, current_node):
        if current_node.left_child is not None:
            self.__print_postorder(current_node.left_child)

        if current_node.right_child is not None:
            self.__print_postorder(current_node.right_child)

        print(str(current_node) + ' ', end='')

    class Node:
        def __init__(self, key, element, balance_factor = 0, left_child = None, right_child = None):
            self.key = key
            self.element = element
            self.balance_factor = balance_factor
            self.left_child = left_child
            self.right_child = right_child

        def __str__(self):
            left_key = None
            if self.left_child is not None:
                left_key = self.left_child.key
            
            right_key = None
            if self.right_child is not None:
                right_key = self.right_child.key
            return f'[{self.key}, {self.balance_factor}, {left_key}, {right_key}, {self.element}]'