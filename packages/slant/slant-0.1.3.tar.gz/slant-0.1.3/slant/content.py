# -*- coding: utf-8 -*-
"""Get substantive content in text."""
from functools import partial
from typing import Iterable, List, Union

from multiprocess import Pool, cpu_count

from slant.utils import VALID_WORD_CHARS, build_list_from_file, build_trie_from_wordlist, local_path

stop_words = build_list_from_file(local_path("stop_words.txt"))


def top_words(text: Union[str, Iterable[str]],
              blacklist: Iterable[str] = stop_words,
              top_n: int = 10) -> Union[List[str], List[List[str]]]:
	"""Get top words or list of these in a text or list of texts, excluding a defined blacklist.

	Args:
		text (str | List[str]): Text to parse or list of texts to parse
		blacklist (List[str]): List of words to ignore
		top_n (int): Number of top words to return

	Returns:
		List[str]: List of top N words sorted by most frequently occuring to least frequently occuring

	"""
	blacktrie = build_trie_from_wordlist(blacklist)
	if isinstance(text, str):
		return get_top_words(text, blacktrie, top_n)
	else:
		with Pool(cpu_count()) as pool:
			return pool.map(partial(get_top_words, blacktrie=blacktrie, top_n=top_n), text)


def get_top_words(text: str, blacktrie: dict, top_n: int) -> List[str]:
	"""Get top words in a string, excluding a predefined list of words.

	Args:
		text (str): Text to parse
		blacktrie (dict): Trie built from a blacklist of words to ignore
		top_n (int): Number of top words to return

	Returns:
		List[str]: List of top N words sorted by most frequently occuring to least frequently occuring

	"""
	found_words = {}
	lower_text = text.lower()
	current_word = ""
	current_lower_word = ""
	current_node = blacktrie
	text_len = len(text)
	idx = 0
	while idx < text_len:
		char = text[idx]
		lower_char = lower_text[idx]
		if lower_char in current_node:
			# char in blacktrie, get rest of word and see if that's still true
			current_word += char
			current_lower_word += lower_char
			current_node = current_node[lower_char]
		elif lower_char in VALID_WORD_CHARS:
			# char not in blacktrie and is a valid word char
			current_word += char
			current_lower_word += lower_char
			current_node = blacktrie
		elif None in current_node:
			# Word in blacktrie, ignore
			current_word = ""
			current_lower_word = ""
			current_node = blacktrie
		elif current_word:
			# Non-word char found and not at an end node of the trie, update found_words
			if current_lower_word in found_words:
				found_words[current_lower_word]["count"] += 1
			else:
				found_words[current_lower_word] = {"word": current_word, "count": 1}
			current_word = ""
			current_lower_word = ""
			current_node = blacktrie
		if idx + 1 >= text_len and current_word:
			if current_lower_word in found_words:
				found_words[current_lower_word]["count"] += 1
			else:
				found_words[current_lower_word] = {"word": current_word, "count": 1}
			current_word = ""
			current_lower_word = ""
			current_node = blacktrie
		idx += 1
	sorted_word_list = filter(lambda x: not x.isdigit(), [
	    v["word"] for _, v in sorted(found_words.items(), key=lambda x: x[1]["count"], reverse=True)
	])
	return list(sorted_word_list)[:top_n]
