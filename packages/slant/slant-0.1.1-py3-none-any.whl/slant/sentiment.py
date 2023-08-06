# -*- coding: utf-8 -*-
"""VADER sentiment analysis"""
from string import punctuation
from typing import Iterable, List, Union

import numpy as np
from multiprocess import Pool, cpu_count

from slant.utils import VALID_WORD_CHARS, build_dict_from_file, local_path

lexicon_dict = build_dict_from_file(local_path("vader_lexicon.txt"), float)
emoji_dict = build_dict_from_file(local_path("emoji_utf8_lexicon.txt"))

NEGATORS = set([
    "aint", "arent", "cannot", "cant", "couldnt", "darent", "didnt", "doesnt", "ain't", "aren't",
    "can't", "couldn't", "daren't", "didn't", "doesn't", "dont", "hadnt", "hasnt", "havent", "isnt",
    "mightnt", "mustnt", "neither", "don't", "hadn't", "hasn't", "haven't", "isn't", "mightn't",
    "mustn't", "neednt", "needn't", "never", "none", "nope", "nor", "not", "nothing", "nowhere",
    "oughtnt", "shant", "shouldnt", "uhuh", "wasnt", "werent", "oughtn't", "shan't", "shouldn't",
    "uh-uh", "wasn't", "weren't", "without", "wont", "wouldnt", "won't", "wouldn't", "rarely",
    "seldom", "despite"
])

# Degree adverb sentiment boosters (https://en.wiktionary.org/wiki/Category:English_degree_adverbs)
incr_degree_adverbs = [
    "absolutely", "amazingly", "awfully", "completely", "considerable", "considerably", "decidedly",
    "deeply", "effing", "enormous", "enormously", "entirely", "especially", "exceptional",
    "exceptionally", "extreme", "extremely", "fabulously", "flipping", "flippin", "frackin",
    "fracking", "fricking", "frickin", "frigging", "friggin", "fully", "fuckin", "fucking",
    "fuggin", "fugging", "greatly", "hella", "highly", "hugely", "incredible", "incredibly",
    "intensely", "major", "majorly", "more", "most", "particularly", "purely", "quite", "really",
    "remarkably", "so", "substantially", "thoroughly", "total", "totally", "tremendous",
    "tremendously", "uber", "unbelievably", "unusually", "utter", "utterly", "very"
]
decr_degree_adverbs = [
    "almost", "barely", "hardly", "just enough", "kind of", "kinda", "kindof", "kind-of", "less",
    "little", "marginal", "marginally", "occasional", "occasionally", "partly", "scarce",
    "scarcely", "slight", "slightly", "somewhat", "sort of", "sorta", "sortof", "sort-of"
]
BOOSTER_DICT = {
    **{adv: 0.293 for adv in incr_degree_adverbs},
    **{adv: -0.293 for adv in decr_degree_adverbs}
}

UPPER_INCR = 0.733  # Sentiment booster for uppercase words
NEGATOR_SCALAR = -0.74  # Sentiment booster for words preceded by negators

# Special case words that are in lexicon, but that are more than one word long
SPECIAL_CASES = {
    "the shit": 3,
    "the bomb": 3,
    "bad ass": 1.5,
    "badass": 1.5,
    "bus stop": 0.0,
    "yeah right": -2,
    "kiss of death": -1.5,
    "to die for": 3,
    "beating heart": 3.1,
    "broken heart": -2.9
}


def is_upper_diff(text: str) -> bool:
	"""Check if some words are all caps while others aren't.

	Args:
		text (str): Text to parse through and check if some words are capitalized while others aren't

	Returns:
		bool: True if some words all caps while others aren't, False otherwise

	"""
	current_word = ""
	upper_word_count = 0
	non_upper_word_count = 0
	text_len = len(text)
	idx = 0
	while idx < text_len:
		char = text[idx]
		if char in VALID_WORD_CHARS:
			current_word += char
		elif current_word:
			upper_word_count += int(current_word.isupper())
			non_upper_word_count += int(not current_word.isupper())
			current_word = ""
		if idx + 1 >= text_len and current_word:
			upper_word_count += int(current_word.isupper())
			non_upper_word_count += int(not current_word.isupper())
		if upper_word_count and non_upper_word_count:
			return True
		idx += 1
	return False


class Sentiment:
	"""Calculate the sentiment of a given text.

	Attributes:
		neg (float | Iterable[float]): Negative sentiment score(s)
		neu (float | Iterable[float]): Neutral sentiment score(s)
		pos (float | Iterable[float]): Positive sentiment score(s)
		compound (float | Iterable[float]): Compound sentiment score(s)
	"""

	def __init__(self, text: Union[str, Iterable[str]]):
		"""Instantiate Sentiment class.

		Args:
			text (str | Iterable[str]): Text to score

		"""
		if isinstance(text, str):
			sentiments = self.score(text)
			self.neg = sentiments["neg"]
			self.neu = sentiments["neu"]
			self.pos = sentiments["pos"]
			self.compound = sentiments["compound"]
		else:
			with Pool(cpu_count()) as pool:
				sentiments = pool.map(self.score, text)
				self.neg = [sentiment["neg"] for sentiment in sentiments]
				self.neu = [sentiment["neu"] for sentiment in sentiments]
				self.pos = [sentiment["pos"] for sentiment in sentiments]
				self.compound = [sentiment["compound"] for sentiment in sentiments]

	def score(self, text: str) -> dict:
		"""Score text.

		Args:
			text (str): Text to score

		Returns:
			dict: Valence scores

		"""
		text_no_emoji = ""
		previous_char = " "
		for char in text:
			if char in emoji_dict:
				if previous_char != " ":
					text_no_emoji += " "
				char = emoji_dict[char]
			text_no_emoji += char
			previous_char = char

		self.text = text_no_emoji.strip()
		self.upper_diff = is_upper_diff(self.text)
		self.tokens = list(map(self.strip_punctuation, self.text.split()))
		self.tokens_lower = list(map(str.lower, (self.tokens)))
		self.n_tokens = len(self.tokens_lower)

		sentiments = []
		for i, item in enumerate(self.tokens_lower):
			# Check for vader_lexicon words that may be used as modifiers or negations
			valence = 0
			if item not in BOOSTER_DICT or i + 1 >= self.n_tokens or (item == "kind" and
			                                                          self.tokens_lower[i + 1] == "of"):
				valence = self.sentiment_valence(self.tokens[i], item, i)
			sentiments.append(valence)

		sentiments = self.but_check(sentiments)
		return self.score_valence(sentiments)

	@staticmethod
	def strip_punctuation(token: str) -> str:
		"""Strip punctuation on words, but leave for possible emoticons of len >= 2.

		Args:
			token (str): Token from which we strip punctuation

		Returns:
			str: Punctuation-stripped token

		"""
		stripped = token.strip(punctuation)
		return token if len(stripped) <= 2 else stripped

	def scalar_inc_dec(self, word: str, valence: float) -> float:
		"""Check if the preceding words increase, decrease, or negate/nullify the valence.

		Args:
			word (str): Preceding word to check for boost
			valence (float): Valence of current word

		Returns:
			scalar (float): Scalar to adjust valence

		"""
		scalar = 0.0
		word_lower = word.lower()
		if word_lower in BOOSTER_DICT:
			scalar = BOOSTER_DICT[word_lower]
			if valence < 0:
				scalar *= -1
			# Check if booster/dampener word is in ALLCAPS (while others aren't)
			if word.isupper() and self.upper_diff:
				scalar += UPPER_INCR if valence > 0 else -1 * UPPER_INCR
		return scalar

	def sentiment_valence(self, item: str, item_lowercase: str, i: int) -> float:
		"""Get valence of current item.

		Args:
			item (str): Token to calculate valence of
			item_lowercase (str): Lowercase token
			i (int): Token index

		Returns:
			valence (float): Valence of current token

		"""
		valence = 0
		if item_lowercase in lexicon_dict:
			valence = lexicon_dict[item_lowercase]

			# check for "no" as negation for an adjacent lexicon item vs as own stand-alone lexicon item
			if item_lowercase == "no" and i != self.n_tokens - 1 and self.tokens_lower[i +
			                                                                           1] in lexicon_dict:
				valence = 0.0  # Set valence to 0.0 and negate the next item
			if (i > 0 and
			    self.tokens_lower[i - 1] == "no") or (i > 1 and self.tokens_lower[i - 2] == "no") or (
			        i > 2 and self.tokens_lower[i - 3] == "no" and
			        self.tokens_lower[i - 1] in ["or", "nor"]):
				valence = lexicon_dict[item_lowercase] * NEGATOR_SCALAR

			# Check if sentiment laden word is in ALL CAPS (while others aren't)
			if item.isupper() and self.upper_diff:
				valence += UPPER_INCR if valence > 0 else -1 * UPPER_INCR

			for start_i in range(0, 3):
				# Dampen the scalar modifier of preceding words and emoticons (excluding the ones that
				# immediately preceed the item) based on their distance from the current item.
				if i > start_i and self.tokens_lower[i - (start_i + 1)] not in lexicon_dict:
					scalar = self.scalar_inc_dec(self.tokens[i - (start_i + 1)], valence)
					if start_i == 1 and scalar:
						scalar *= 0.95
					if start_i == 2 and scalar:
						scalar *= 0.9
					valence += scalar
					valence = self.negation_check(valence, start_i, i)
					if start_i == 2:
						valence = self.special_idioms_check(valence, i)

			# Check for negation case using "least"
			if i > 2 and " ".join(self.tokens_lower[i - 2:i]) not in ["at least", "very least"]:
				valence *= NEGATOR_SCALAR
		return valence

	def but_check(self, sentiments: List[float]) -> List[float]:
		"""Adjust sentiments upon finding the word "but" in text.

		Args:
			sentiments (list): List of pre-calculated sentiments

		Returns:
			sentiments (list): List of but-adjusted sentiments

		"""
		# check for modification in sentiment due to contrastive conjunction "but"
		if "but" in self.tokens_lower:
			bi = self.tokens_lower.index("but")
			for sentiment in sentiments:
				si = sentiments.index(sentiment)
				if si < bi:
					sentiments[si] = sentiment / 2
				elif si > bi:
					sentiments[si] = sentiment * 1.5
		return sentiments

	def special_idioms_check(self, valence: float, i: int) -> float:
		"""Check if word is part of a special idiom.

		Args:
			valence (float): Valence of current word
			i (int): Indx of current word

		Returns:
			valence (float): Special case valence

		"""
		onezero = " ".join(self.tokens_lower[i - 1:i])
		twoonezero = " ".join(self.tokens_lower[i - 2:i])
		twoone = " ".join(self.tokens_lower[i - 2:i - 1])
		threetwoone = " ".join(self.tokens_lower[i - 3:i - 1])
		threetwo = " ".join(self.tokens_lower[i - 3:i - 2])
		for seq in [onezero, twoonezero, twoone, threetwoone, threetwo]:
			if seq in SPECIAL_CASES:
				valence = SPECIAL_CASES[seq]
				break

		if i < self.n_tokens - 1:
			valence = SPECIAL_CASES.get(" ".join(self.tokens_lower[i:i + 1]), valence)
		if i < self.n_tokens - 2:
			valence = SPECIAL_CASES.get(" ".join(self.tokens_lower[i:i + 2]), valence)

		# Check for booster/dampener bi-grams such as "sort of" or "kind of"
		n_grams = [threetwoone, threetwo, twoone]
		for n_gram in n_grams:
			valence += BOOSTER_DICT.get(n_gram, 0)
		return valence

	@staticmethod
	def negated(token_list: List[str]) -> bool:
		"""Determine if input contains negation words.

		Args:
			token_list (List[str]): List of tokens

		Returns:
			bool: True if negator word in token list, otherwise False

		"""
		for word in map(str.lower, token_list):
			if word in NEGATORS or "n't" in word:
				return True
		return False

	def negation_check(self, valence: float, start_i: int, i: int) -> float:
		"""Check if negator word/phrase precedes current token.

		Args:
			valence (float): Current word valence
			start_i (int): Number of preceding tokens to check through
			i (int): Current token index

		Returns:
			valence (float): Corrected current word valence

		"""
		two_before = [self.tokens_lower[i - start_i - 1]]
		if start_i == 0 and self.negated(two_before):
			valence *= NEGATOR_SCALAR
		if start_i == 1:
			if " ".join(self.tokens_lower[i - 1:i]) in ["never so", "never this"]:
				valence *= 1.25
			elif " ".join(self.tokens_lower[i - 2:i]) != "without doubt" and self.negated(two_before):
				valence *= NEGATOR_SCALAR
		if start_i == 2:
			if self.tokens_lower[i - 3] == "never" and set(self.tokens_lower[i - 2:i]) & {"so", "this"}:
				valence *= 1.25
			elif " ".join(self.tokens_lower[i - 3:i - 1]) != "without doubt" and self.negated(two_before):
				valence *= NEGATOR_SCALAR
		return valence

	def punctuation_emphasis(self) -> float:
		"""Get punctation emphasis amplifier for current text."""
		# Check for added emphasis resulting from exclamation points (up to 4 of them)
		eq_amplifier = min(self.text.count("!"), 4) * 0.292
		# Check for added emphasis resulting from question marks
		qm_count = self.text.count("?")
		qm_amplifier = 0.96 if qm_count > 3 else qm_count * 0.18
		return eq_amplifier + qm_amplifier

	@staticmethod
	def sift_sentiment_scores(sentiments: List[float]) -> (float, float, float):
		"""Separate positive, negative and neutral sentiment score.

		Args:
			sentiments (List[float]): List of sentiment scores

		Returns:
			pos_sum (float): Calculated sum of positive sentiments
			neg_sum (float): Calculated sum of negative sentiments
			neu_sum (float): Calculated sum of neutral sentiments

		"""
		# want separate positive versus negative sentiment scores
		pos_sum = 0.0
		neg_sum = 0.0
		neu_count = 0
		for sentiment_score in sentiments:
			pos_sum += sentiment_score + 1 if sentiment_score > 0 else 0
			neg_sum += sentiment_score - 1 if sentiment_score < 0 else 0
			neu_count += 1 if sentiment_score == 0 else 0
		return pos_sum, neg_sum, neu_count

	def score_valence(self, sentiments: List[float]) -> dict:
		"""Get final sentiment score from list of sentiments.

		Args:
			sentiments (List[float]): List of sentiments to score

		Returns:
			dict: Corrected negative, neutral, positive and compound sentiment scores

		"""
		compound = 0.0
		pos = 0.0
		neg = 0.0
		neu = 0.0

		if sentiments:
			sum_s = sum(sentiments)
			# Compute and add emphasis from punctuation in text
			punct_emph_amplifier = self.punctuation_emphasis()
			sum_s += punct_emph_amplifier if sum_s > 0 else -1 * punct_emph_amplifier
			# discriminate between positive, negative and neutral sentiment scores
			pos_sum, neg_sum, neu_count = self.sift_sentiment_scores(sentiments)
			pos_sum += punct_emph_amplifier if pos_sum > np.abs(neg_sum) else -1 * punct_emph_amplifier
			total = pos_sum + np.abs(neg_sum) + neu_count
			neg = np.abs(neg_sum / total)
			neu = np.abs(neu_count / total)
			pos = np.abs(pos_sum / total)
			compound = np.clip(sum_s / np.sqrt((sum_s**2) + 15), -1, 1)

		return {
		    "neg": round(neg, 3),
		    "neu": round(neu, 3),
		    "pos": round(pos, 3),
		    "compound": round(compound, 4)
		}
