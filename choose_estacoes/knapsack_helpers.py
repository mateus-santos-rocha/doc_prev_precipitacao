import itertools
from random import randint
import heapq

def all_combs(lst):
    for r in range(1, len(lst)+1):
        for comb in itertools.combinations(lst, r):
            yield comb

def all_items_combinations(items):
    return [list(comb) for comb in all_combs(items)]

def compute_profit(combination):
    profit = 0
    for item in combination:
        profit+=item.profit
    return profit

def compute_weight(combination):
    weight = 0
    for item in combination:
        weight+=item.weight
    return weight

def initialize_random_items(n_items,min_profit,max_profit,min_weight,max_weight):
    items = []
    for i in range(n_items):
        items.append(Item(id=i,profit=randint(min_profit,max_profit),weight=randint(min_weight,max_weight)))
    return items

class Item:
    def __init__(self,id,profit,weight):
        self.id=id
        self.profit=profit
        self.weight=weight
        self.efficiency = profit/weight
    
    def print(self):
        print(f"ID: {self.id}")
        print(f'Profit: {self.profit}')
        print(f'Weight: {self.weight}')
        pass

    def as_dict(self):
        item_dict = {
            'profit':self.profit,
            'weight':self.weight
        }
        return item_dict
    
class Node:
    def __init__(self, level, profit, weight, bound, selected_items):
        self.level = level
        self.profit = profit
        self.weight = weight
        self.bound = bound
        self.selected_items = selected_items 

     # Define comparison for max-heap
    def __lt__(self, other):
        return self.bound > other.bound  # Greater bound has higher priority


def calculate_bound(node, capacity, ordered_items):
    if node.weight >= capacity:
        return 0

    bound = node.profit
    total_weight = node.weight
    j = node.level + 1

    while j < len(ordered_items) and total_weight + ordered_items[j].weight <= capacity:
        total_weight += ordered_items[j].weight
        bound += ordered_items[j].profit
        j += 1

    if j < len(ordered_items):
        bound += (capacity - total_weight) * ordered_items[j].efficiency

    return bound

def branch_and_bound_solution(items,capacity):
    ordered_items = sorted(items, reverse=True, key=lambda x: x.efficiency)
    max_profit = 0
    selected_items_optimal = []

    # Priority queue for nodes

    queue = []
    start_node = Node(-1, 0, 0, 0, [])
    start_node.bound = calculate_bound(start_node, capacity, ordered_items)
    heapq.heappush(queue, start_node)

    while queue:
        current_node = heapq.heappop(queue)

        if current_node.bound <= max_profit:
            continue

        level = current_node.level + 1

        if level < len(ordered_items):
            item = ordered_items[level]

            # Taking the item
            if current_node.weight + item.weight <= capacity:
                next_node_with_item = Node(
                    level,
                    current_node.profit + item.profit,
                    current_node.weight + item.weight,
                    0,
                    current_node.selected_items + [level]
                )
                next_node_with_item.bound = calculate_bound(next_node_with_item, capacity, ordered_items)

                if next_node_with_item.profit > max_profit:
                    max_profit = next_node_with_item.profit
                    selected_items_optimal = next_node_with_item.selected_items

                if next_node_with_item.bound > max_profit:
                    heapq.heappush(queue, next_node_with_item)

            # Not taking the item
            next_node_without_item = Node(
                level,
                current_node.profit,
                current_node.weight,
                0,
                current_node.selected_items
            )
            next_node_without_item.bound = calculate_bound(next_node_without_item, capacity, ordered_items)

            if next_node_without_item.bound > max_profit:
                heapq.heappush(queue, next_node_without_item)

    selected_items = []
    for i in selected_items_optimal:
        selected_items.append(ordered_items[i])

    return selected_items
