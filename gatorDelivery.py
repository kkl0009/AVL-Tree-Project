import sys
from AVL_tree import AVLTree

class Order:
    def __init__(self, id, eta, delivery_time, priority, system_time, value):
        self.id = id
        self.eta = eta
        self.delivery_time = delivery_time
        self.priority = priority
        self.system_time = system_time
        self.value = value

    def __str__(self):
        return f'Order: [{self.id}, {self.eta}, {self.delivery_time}, {self.priority}]'

priority_tree = AVLTree()
eta_tree = AVLTree()
id_tree = AVLTree()
current_order = None

def create_order(order_id, current_system_time, order_value, delivery_time):
    global priority_tree, eta_tree, id_tree, current_order

    VALUE_WEIGHT = 0.3
    TIME_WEIGHT = 0.7
    normalized_order_value = order_value / 50
    priority = VALUE_WEIGHT * normalized_order_value - TIME_WEIGHT * current_system_time

    # Delete all the orders up until this point
    deleted_orders = eta_tree.delete_all_le(current_system_time)

    # current_order = None
    # Also remove these orders from the priority tree
    for order in deleted_orders:
        current_order = order[1]
        priority_tree.remove(order[1].priority)
        id_tree.remove(order[1].id)
    
    # priority_tree.print_tree()

    if current_order is not None and current_order.eta + current_order.delivery_time > current_system_time:
        # No items currently in transit, but return time is currently happening
        buffer_time = (current_order.eta + current_order.delivery_time) - current_system_time
    else:
        # An item may be in transit, check if this is the case
        buffer_time = 0

        max_priority_item = priority_tree.get_max()
        if max_priority_item is not None and max_priority_item[1].eta - max_priority_item[1].delivery_time < current_system_time:
            # This order is currently in transit, so give it the highest priority
            max_priority_item[1].priority = 10000000000000000
            priority_tree.fix_max()

    # priority_tree.put(priority, order_id)
    higher_priority_item = priority_tree.get_smallest_ge(priority)
    if higher_priority_item is None:
        # This item is now the highest priority in the entire system
        eta = current_system_time + delivery_time + buffer_time
    else:
        # There is at least 1 order with a higher priority
        # Make sure to take return time into account by adding delivery time
        eta = higher_priority_item.eta + higher_priority_item.delivery_time + delivery_time

    new_order = Order(order_id, eta, delivery_time, priority, current_system_time, order_value)
    priority_tree.put(priority, new_order)
    eta_tree.put(eta, new_order)
    id_tree.put(order_id, new_order)

    updated_orders = []
    lower_priority_items = priority_tree.get_range(0, priority, min_case = True)
    for item in lower_priority_items:
        order = item[1]
        if order.id != order_id:
            eta_tree.remove(order.eta)
            order.eta = order.eta + 2 * delivery_time
            eta_tree.put(order.eta, order)
            updated_orders.append(order)

    # Start output here
    print(f'Order {order_id} has been created - ETA: {new_order.eta}')

    if len(updated_orders) > 0:
        output_str = '['
        for order in updated_orders:
            output_str += f'{order.id}: {order.eta}, '
        output_str = output_str[:-2] + ']'
        print(f'Updated ETAs: {output_str}')

    for order in deleted_orders:
        print(f'Order {order[1].id} has been delivered at time {order[1].eta}')

def cancel_order(order_id, current_system_time):
    global priority_tree, eta_tree, id_tree, current_order

    old_order = id_tree.get(order_id)

    # Delete all the orders up until this point
    deleted_orders = eta_tree.delete_all_le(current_system_time)

    # Also remove these orders from the priority tree
    for order in deleted_orders:
        current_order = order[1]
        priority_tree.remove(order[1].priority)
        id_tree.remove(order[1].id)

    if old_order is None or old_order.eta - old_order.delivery_time < current_system_time:
        # Order was either already processed or is in transit
        print(f'Cannot cancel. Order {order_id} has already been delivered if the order is out for delivery or is already delivered')
    else:
        priority_tree.remove(old_order.priority)
        eta_tree.remove(old_order.eta)
        id_tree.remove(old_order.id)

        updated_orders = []
        lower_priority_items = priority_tree.get_range(0, old_order.priority, min_case = True)
        for item in lower_priority_items:
            order = item[1]
            eta_tree.remove(order.eta)
            order.eta = order.eta - 2 * old_order.delivery_time
            eta_tree.put(order.eta, order)
            updated_orders.append(order)

        print(f'Order {old_order.id} has been canceled')

        if len(updated_orders) > 0:
            output_str = '['
            for order in updated_orders:
                output_str += f'{order.id}: {order.eta}, '
            output_str = output_str[:-2] + ']'
            print(f'Updated ETAs: {output_str}')

    for order in deleted_orders:
        print(f'Order {order[1].id} has been delivered at time {order[1].eta}')

def update_time(order_id, current_system_time, new_delivery_time):
    global eta_tree, current_order

    update_order = id_tree.get(order_id)

    # Delete all the orders up until this point
    deleted_orders = eta_tree.delete_all_le(current_system_time)

    # Also remove these orders from the priority tree
    for order in deleted_orders:
        current_order = order[1]
        priority_tree.remove(order[1].priority)
        id_tree.remove(order[1].id)

    if update_order is None or update_order.eta - update_order.delivery_time < current_system_time:
        # Order was either already processed or is in transit
        print(f'Cannot update. Order {order_id} has already been delivered if the order is out for delivery or is already delivered')

    else:

        eta_tree.remove(update_order.eta)

        old_delivery_time = update_order.delivery_time

        eta = update_order.eta - update_order.delivery_time + new_delivery_time

        updated_orders = []
        lower_priority_items = priority_tree.get_range(0, update_order.priority, min_case = True)
        for item in lower_priority_items:
            order = item[1]
            if order.id != order_id:
                eta_tree.remove(order.eta)
                order.eta = order.eta + 2 * (new_delivery_time - old_delivery_time)
                eta_tree.put(order.eta, order)
                updated_orders.append(order)

        update_order.eta = eta
        update_order.delivery_time = new_delivery_time
        eta_tree.put(update_order.eta, update_order)

        updated_orders.append(update_order)

        if len(updated_orders) > 0:
            output_str = '['
            for order in updated_orders:
                output_str += f'{order.id}: {order.eta}, '
            output_str = output_str[:-2] + ']'
            print(f'Updated ETAs: {output_str}')

    for order in deleted_orders:
        print(f'Order {order[1].id} has been delivered at time {order[1].eta}')

def clear_eta_tree():
    global eta_tree

    all_tree_items = eta_tree.get_range(0, 0, min_case = True, max_case = True)

    for item in all_tree_items:
        order = item[1]
        print(f'Order {order.id} has been delivered at time {order.eta}')

def parse_input_file(input_file_name):
    with open(input_file_name, 'r') as new_file:
        input_data = new_file.read()

    for next_command in input_data.split('\n'):

        if 'print' in next_command:
            args = next_command[next_command.find('(') + 1 : next_command.find(')')]

            if ',' not in args:
                # CASE: print(orderId)
                order_id = args.strip()
                order = id_tree.get(order_id)
                print(f'[{order.id}, {order.system_time}, {order.value}, {order.delivery_time}, {order.eta}]')
            else:
                both_args = args.split(',')
                if len(both_args) != 2:
                    print('Invalid format for \"print(time1, time2)\"')
                else:
                    # CASE: print(time1, time2)
                    time1 = both_args[0].strip()
                    time2 = both_args[1].strip()
                    items = eta_tree.get_range(int(time1), int(time2))
                    # if current_order is not None and current_order.eta == global_system_time:
                    #     items.append((current_order.eta, current_order))
                    if len(items) <= 0:
                        print('There are no orders in that time period')
                    else:
                        output_str = '['
                        for item in items:
                            output_str += f'{item[1].id},'
                        output_str = output_str[:-1] + ']'
                        print(output_str)

        elif 'getRankOfOrder' in next_command:
            arg = next_command[next_command.find('(') + 1 : next_command.find(')')]

            if ',' in arg:
                print('Invalid format for \"getRankOfOrder(orderId)\"')
            else:
                # CASE: getRankOfOrder(orderId)
                order_id = arg.strip()
                order = id_tree.get(order_id)
                if order is not None:
                    orders_before = eta_tree.get_range(0, order.eta, min_case = True)

                    # Subtract 1 to account for the current order being in this list
                    number_before = len(orders_before) - 1
                    print(f'Order {order_id} will be delivered after {number_before} orders')
        elif 'createOrder' in next_command:
            args = next_command[next_command.find('(') + 1 : next_command.find(')')]
            all_args = args.split(',')
            if len(all_args) != 4:
                print('Invalid format for \"createOrder(orderId, currentSystemTime, orderValue, deliveryTime)\"')
            else:
                # CASE: createOrder(orderId, currentSystemTime, orderValue, deliveryTime)
                order_id = all_args[0].strip()
                current_system_time = int(all_args[1].strip())
                order_value = int(all_args[2].strip())
                delivery_time = int(all_args[3].strip())
                create_order(order_id, current_system_time, order_value, delivery_time)
                # print(f'Running createOrder({order_id}, {current_system_time}, {order_value}, {delivery_time})')

        elif 'cancelOrder' in next_command:
            args = next_command[next_command.find('(') + 1 : next_command.find(')')]
            both_args = args.split(',')
            if len(both_args) != 2:
                print('Invalid format for \"cancelOrder(orderId, currentSystemTime)\"')
            else:
                # CASE: cancelOrder(orderId, currentSystemTime)
                order_id = both_args[0].strip()
                current_system_time = int(both_args[1].strip())
                cancel_order(order_id, current_system_time)
        elif 'updateTime' in next_command:
            args = next_command[next_command.find('(') + 1 : next_command.find(')')]
            all_args = args.split(',')
            if len(all_args) != 3:
                print('Invalid format for \"updateTime(orderId, currentSystemTime, newDeliveryTime)\"')
            else:
                # CASE: updateTime(orderId, currentSystemTime, newDeliveryTime)
                order_id = all_args[0].strip()
                current_system_time = int(all_args[1].strip())
                new_delivery_time = int(all_args[2].strip())
                update_time(order_id, current_system_time, new_delivery_time)

        elif 'Quit' in next_command:
            # CASE: Quit()
            clear_eta_tree()
            sys.exit()
        else:
            print('Invalid command entered...')

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print('Please input the correct number of arguments to the program...')
        sys.exit()
    
    input_file_name = sys.argv[1]

    try:
        file_test = open(input_file_name, 'r')
        file_test.close()
    except FileNotFoundError:
        print(f'File with name "{input_file_name}" not found...')
        sys.exit()

    print(f'Running program with input file \"{input_file_name}\"')
    parse_input_file(input_file_name)