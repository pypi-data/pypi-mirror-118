# -*- coding: utf-8 -*-
"""Miscellaneous utility functions."""
from pathlib import Path, PosixPath
from string import ascii_letters, digits
from typing import Callable, Iterable, List

VALID_WORD_CHARS = set(ascii_letters + digits + "'’")

# Get path of file in local dictionaries directory
local_path = lambda path: Path(__file__).parent.joinpath(f"dictionaries/{path}")


def build_list_from_file(path: PosixPath) -> List[str]:
	"""Build list from text file.

	Args:
		path (PosixPath): Path to list-containing text file

	Returns:
		List[str]: List of strings from text file

	"""
	with open(path, "r", encoding="utf-8") as f:
		return list(filter(str.strip, f.read().split("\n")))


def build_dict_from_file(path: PosixPath, value_func: Callable = str) -> dict:
	"""Build dictionary from file of key, value pairs separated by tab character.

	Args:
		path (PosixPath): Path to dictionary-containing text file
		value_func (Callable): Function to run over each value

	Returns:
		output (dict): Dictionary built from file

	"""
	output = {}
	with open(path, "r", encoding="utf-8") as f:
		for line in filter(str.strip, f.read().rstrip().split("\n")):
			key, value = line.strip().split("\t")[:2]
			output[key] = value_func(value)
	return output


def build_trie_from_wordlist(wordlist: Iterable[str]) -> dict:
	"""Build a trie from an iterable of words.

	Args:
		wordlist (Iterable[str]): List of words from which we build a trie

	Returns:
		trie (dict): Trie data structure built from wordlist

	Note:
		Trie's were introduced by Edward Fredkin in his 1960 article "Trie memory."
		https://doi.org/10.1145/367390.367400

	"""
	trie = {}
	for word in wordlist:
		current_node = trie
		for char in word.lower():
			current_node = current_node.setdefault(char, {})
		current_node[None] = word
	return trie


def build_trie_from_file(path: PosixPath) -> dict:
	"""Build a trie from a text file of words.

	Args:
		path (PosixPath): Path to file that contains wordlist

	Returns:
		trie (dict): Trie data structure built from wordlist

	"""
	if not path.exists():
		raise FileNotFoundError(f"File `{path}` does not exist")
	with open(path, "r", encoding="utf-8") as f:
		wordlist = filter(str.strip, f.read().split("\n"))
	return build_trie_from_wordlist(wordlist)
