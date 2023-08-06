# -*- coding: utf-8 -*-
"""Check text for bias words."""
from functools import partial
from pathlib import Path, PosixPath
from typing import Iterable, Union

from multiprocess import Pool, cpu_count

from slant.utils import (VALID_WORD_CHARS, build_list_from_file, build_trie_from_file,
                         build_trie_from_wordlist, local_path)

bias_words = build_list_from_file(local_path("bias_words.txt"))

def has_bias_words(
    text: Union[Iterable[str], str],
    blacklist: Union[Iterable[str], str, PosixPath] = bias_words
) -> bool:
	"""Determine if a given text has bias words in it.

	Args:
		text (str | Iterable[str]): Text or iterable of texts to search for bias words
		blacklist (PosixPath | str | Iterable[str]): List of words to disallow or a file pointing to
			such a list

	Returns:
		bool | Iterable[bool]: True if bias word found, False if none found. If input is an iterable of
			texts, return an iterable of bools for result corresponding to each text

	"""
	# Get trie of bias words
	if isinstance(blacklist, (str, PosixPath)):
		bias_words_trie = build_trie_from_file(Path(blacklist))
	else:
		bias_words_trie = build_trie_from_wordlist(blacklist)

	# Check for bias words
	if isinstance(text, str):
		return find_bias_words(text, bias_words_trie=bias_words_trie, return_all=False)
	else:
		with Pool(cpu_count()) as pool:
			return pool.map(partial(find_bias_words, bias_words_trie=bias_words_trie, return_all=False),
			                text)


def get_bias_words(
    text: Union[Iterable[str], str],
    blacklist: Union[Iterable[str], str, PosixPath] = bias_words
) -> bool:
	"""Get all bias words in a given text or texts.

	Args:
		text (str | Iterable[str]): Text or iterable of texts to search for bias words
		blacklist (PosixPath | str | Iterable[str]): List of words to disallow or a file pointing to
			such a list

	Returns:
		list: List of bias words found in text

	"""
	# Get trie of bias words
	if isinstance(blacklist, (str, PosixPath)):
		bias_words_trie = build_trie_from_file(blacklist)
	else:
		bias_words_trie = build_trie_from_wordlist(blacklist)

	# Check for bias words
	if isinstance(text, str):
		return find_bias_words(text, bias_words_trie=bias_words_trie)
	else:
		with Pool(cpu_count()) as pool:
			return pool.map(partial(find_bias_words, bias_words_trie=bias_words_trie), text)


def find_bias_words(text: str,
                    bias_words_trie: dict,
                    return_all=True) -> Union[Iterable[str], bool]:
	"""Determine if any bias words exist in a given textin a given text.

	The algorithm used to match bias words is adapted from Alfred V. Aho and Margaret J. Corasick's
	1975 article "Efficient string matching: an aid to bibliographic search."
	https://doi.org/10.1145/360825.360855

	Args:
		text (str): Text to search for bias words
		bias_words_trie (dict): Trie data structure of bias words
		return_all (bool): If True, find and return all bias words in text. If False, return boolean
			indicating whether any bias words were found

	Returns:
		found_bias_words (list): List of bias words found in text

	Note:
		While one could logically determine whether any bias words were found by simply wrapping a
		resultant list of found bias words in a `bool()` function, passing false to the `return_all`
		keyword argument yields marginal improvement as it returns `True` at the first occurence of a
		bias word found in its blacklist.

	"""
	found_bias_words = []
	text = text.lower()
	current_word = ""
	current_node = bias_words_trie
	text_len = len(text)
	idx = 0
	while idx < text_len:
		char = text[idx]
		if char in current_node:
			# char still in bias word trie, keep traversing
			current_word += char
			current_node = current_node[char]
		elif char in VALID_WORD_CHARS:
			# char not in bias word trie, but is a valid word char
			current_word += char
			# Advance through rest of word
			idx += 1
			while idx < text_len:
				if text[idx] not in VALID_WORD_CHARS:
					break
				idx += 1
			current_word = ""  # Reset current_word
			current_node = bias_words_trie  # Reset current_node
		elif None in current_node:
			if return_all:
				found_bias_words.append(current_node[None])
			else:
				return True
		elif current_word:
			# Non-word char found, reset current node and current word
			current_node = bias_words_trie
			current_word = ""
		if idx + 1 >= text_len and None in current_node:
			# At end of text with word found
			if return_all:
				found_bias_words.append(current_node[None])
			else:
				return True
		idx += 1
	return found_bias_words if return_all else False
