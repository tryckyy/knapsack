import argparse
import itertools


def load_items(file_name):
    items = []
    with open(file_name, "r") as file:
        for line in file:
            value, weight, item = line.strip().split(";")
            items.append((int(value), int(weight), item))
    return items


def knapsack_brute_force(items, max_weight):
    best_value = 0
    best_combination = []
    for r in range(1, len(items) + 1):
        for combination in itertools.combinations(items, r):
            total_weight = sum(item[1] for item in combination)
            total_value = sum(item[0] for item in combination)
            if total_weight <= max_weight and total_value > best_value:
                best_value = total_value
                best_combination = combination
    return best_value, best_combination


def knapsack_value_first(items, max_weight):
    total_weight = 0
    total_value = 0
    chosen_items = []

    for value, weight, item in sorted(items, key=lambda x: x[0], reverse=True):
        if total_weight + weight <= max_weight:
            total_weight += weight
            total_value += value
            chosen_items.append((value, weight, item))

    return total_value, chosen_items


def knapsack_ratio_value_weight(items, max_weight):
    items = sorted(items, key=lambda x: x[0] / x[1], reverse=True)
    total_weight = 0
    total_value = 0
    chosen_items = []
    for value, weight, item in items:
        if total_weight + weight <= max_weight:
            total_weight += weight
            total_value += value
            chosen_items.append((value, weight, item))
    return total_value, chosen_items


def worst_case_scenarios(items, max_weight):
    # Instance pour l'heuristique valeur-first
    items_value_first = [(10, 8, 'item1'), (4, 2, 'item2'), (7, 5, 'item3')]
    value_first_result = knapsack_value_first(items_value_first, max_weight)

    # Instance pour l'heuristique ratio valeur/poids
    items_ratio = [(10, 8, 'item1'), (4, 2, 'item2'), (7, 5, 'item3')]
    ratio_result = knapsack_ratio_value_weight(items_ratio, max_weight)

    return value_first_result, ratio_result


def main():
    parser = argparse.ArgumentParser(
        description="Solve the knapsack problem with different methods."
    )
    parser.add_argument(
        "-b", "--brute-force", action="store_true", help="Use brute force method"
    )
    parser.add_argument(
        "-v", "--value-first", action="store_true", help="Use value-first method"
    )
    parser.add_argument(
        "-r",
        "--ratio-value-weight",
        action="store_true",
        help="Use ratio value/weight method",
    )
    parser.add_argument(
        "-W", type=int, required=True, help="Maximum weight of the knapsack"
    )
    parser.add_argument("file", type=str, help="Input file containing items")

    args = parser.parse_args()

    items = load_items(args.file)

    if args.brute_force:
        best_value, chosen_items = knapsack_brute_force(items, args.W)
    elif args.value_first:
        best_value, chosen_items = knapsack_value_first(items, args.W)
    elif args.ratio_value_weight:
        best_value, chosen_items = knapsack_ratio_value_weight(items, args.W)
    else:
        print("Please specify a method: -b, -v, or -r.")
        return

    print(f"Best value: {best_value}")
    print("Chosen items:")
    for value, weight, item in chosen_items:
        print(f"  {item}: value={value}, weight={weight}")

        # Afficher les pires cas pour les heuristiques
        print("\nWorst case scenarios:")
        value_first_result, ratio_result = worst_case_scenarios(items, args.W)

        print("\nWorst case for value-first heuristic:")
        print(f"Best value: {value_first_result[0]}")
        for value, weight, item in value_first_result[1]:
            print(f"  {item}: value={value}, weight={weight}")

        print("\nWorst case for ratio-value/weight heuristic:")
        print(f"Best value: {ratio_result[0]}")
        for value, weight, item in ratio_result[1]:
            print(f"  {item}: value={value}, weight={weight}")


if __name__ == "__main__":
    main()
