import random
import argparse


# A class to represent items.
class Item:
    def __init__(self, colour):
        self._colour_ = colour

    def get_color(self) -> int:
        return self._colour_


# A class to hold items.
class Container:
    def __init__(self, colour: int, max_items: int = 7):
        self._colour_ = colour
        self._max_item_count_ = max_items
        self._inside_ = []

    def add_item(self, p_item: Item) -> None:
        if self.check_item_color(p_item):
            if not self.is_full():
                self._inside_.append(p_item)
            else:
                raise Exception("The container is full.")
        else:
            raise Exception("Given item has different colour.")

    def is_full(self) -> bool:
        if len(self) >= self._max_item_count_:
            return True
        return False

    def get_color(self) -> int:
        return self._colour_

    def check_item_color(self, p_item: Item) -> bool:
        if self.get_color() == p_item.get_color():
            return True
        return False

    def __len__(self) -> int:
        return len(self._inside_)


# A class to hold containers.
class ContainerList:
    def __init__(self):
        self._containers_ = []
        self._colour_indices_ = [-1, -1, -1]

    def add_item(self, p_item: Item) -> None:
        item_colour = p_item.get_color()
        container_index = self._get_container_from_colour_(item_colour)

        # If there is a container
        if container_index >= 0 and not (self._containers_[container_index]).is_full():
            container = self._containers_[container_index]
            container.add_item(p_item)
            return
        # Create a new container.
        new_container = Container(item_colour)
        self._add_container_(new_container)
        # Add item into that container.
        new_container.add_item(p_item)

    def show(self) -> str:
        print_text_header = '\n############## ContainerList ##############\n'
        print_text_body = ''
        print_text_footer = '###########################################\n'

        # Print each container
        for container in self._containers_:
            if container.get_color() == 0:
                colour_name = 'Yellow'
            elif container.get_color() == 1:
                colour_name = 'Red'
            else:
                colour_name = 'White'
            print_text_body += f'- {colour_name} Container: {len(container)} items\n'

        return print_text_header + print_text_body + print_text_footer

    def small_log(self) -> str:
        log_text = ''
        for container in self._containers_:
            log_text += f'{container.get_color()}({len(container)}) '
        return log_text

    def _add_container_(self, p_container: Container) -> None:
        prev_container_index = self._get_container_from_colour_(p_container.get_color())

        # If there is no previous container for that colour
        if prev_container_index > 0:
            prev_container = self._containers_[prev_container_index]
            if not prev_container.is_full():
                raise Exception("For the same colour, the previous container is not full yet.")

        self._containers_.append(p_container)
        self._change_colour_index_(p_container.get_color(), len(self._containers_) - 1)

    def _get_container_from_colour_(self, p_colour: int) -> int:
        index = self._colour_indices_[p_colour]
        return index

    def _change_colour_index_(self, p_colour: int, p_index: int) -> None:
        self._colour_indices_[p_colour] = p_index

    def __len__(self):
        return len(self._containers_)


def init_argument_parser():
    parser = argparse.ArgumentParser(
        description="This script lets you to experiment the Bin Packing problem with Color constraint.")
    parser.add_argument("-e", "--experiment", nargs="+", required=True, help="Provide the experiment count.")
    parser.add_argument("-i", "--items", nargs="+", required=True, help="Provide the item count as number.")
    parser.add_argument("-f", "--file", nargs="+", required=True, help="Provide a file name to save logs/results.")

    return parser.parse_args()


if __name__ == "__main__":
    # Init the argument parser for flag system.
    args = init_argument_parser()

    # CONFIGURATIONS #
    EXPERIMENT_COUNT = int(args.experiment[0])
    ITEM_COUNT = int(args.items[0])
    FILENAME_TO_SAVE = args.file[0]
    array_to_store_data = []
    ##################

    # Start the simulation.
    print("Experiments are started.")

    file_to_save = open(FILENAME_TO_SAVE, "a")
    # Do experiments.
    for test in range(EXPERIMENT_COUNT):
        # Create a container to hold items.
        container_list = ContainerList()
        item_count = 0
        for _ in range(0, ITEM_COUNT):
            item_count += 1
            random_colour = random.randint(0, 2)
            item = Item(random_colour)
            container_list.add_item(item)

        # Store results
        array_to_store_data.append(len(container_list))
        short_results_log = f'{item_count} in {len(container_list)}: {container_list.small_log()}\n'
        file_to_save.write(short_results_log)

    file_to_save.close()

    print(f'Minimum container count: {min(array_to_store_data)}\n'
          f'Maximum container count: {max(array_to_store_data)}')

    print("Experiments are finished.")
