from typing import Union
import asyncio
import csv
import re


# get matching regex from content
def get_by_regex(regex, content: str) -> Union[str, None]:
    """Matches content by regex and returns the value captured by the first group, or None if there was no match

    :param regex: A compiled regex to match
    :type regex: re.Pattern
    :param content: The content on which the regex should be applied
    :type content: str
    :rtype: str, None
    """
    match = re.search(regex, content)
    return match.group(1).strip() if match else None


def is_dict(item: dict, ans: Union[None, list] = None) -> list:
    if ans is None:
        ans = []
    tree = []
    for k, v in item.items():
        if isinstance(v, dict):
            ans.append(str(k))
            tree.extend(is_dict(v, ans))
            ans = []
        else:
            if ans:
                ans.append(str(k))
                key = "_".join(ans)
                tree.extend([(key, str(v) if v else "")])
                ans.remove(str(k))
            else:
                tree.extend([(str(k), str(v) if v else "")])
    return tree


def get_tree(item: Union[list, dict]) -> list:
    tree = []
    if isinstance(item, dict):
        tree.extend(is_dict(item, ans=[]))
    elif isinstance(item, list):
        for i in item:
            tree.append(get_tree(i))
    return tree


def render_csv(header: list, data: list, out_path: str = "output.csv") -> None:
    input = []
    with open(out_path, "w") as f:
        dict_writer = csv.DictWriter(f, fieldnames=header)
        dict_writer.writeheader()
        for i in data:
            input.append(dict(i))
        dict_writer.writerows(input)


def ndict_to_csv(obj: list, output_path: str) -> None:
    """Convert nested dictionary to csv.

    :param obj: Stream information list
    :type obj: list
    :param output_path: Path to save the csv file.
    :return: None
    """
    tree = get_tree(obj)
    header = [i[0] for i in tree[0]]
    render_csv(header, tree, output_path)


def run_until_completed(coros):
    futures = [asyncio.ensure_future(c) for c in coros]

    async def first_to_finish():
        while True:
            await asyncio.sleep(0)
            for f in futures:
                if f.done():
                    futures.remove(f)
                    return f.result()

    while len(futures) > 0:
        yield first_to_finish()
