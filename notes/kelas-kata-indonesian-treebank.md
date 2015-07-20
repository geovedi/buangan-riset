# Indonesian Treebank

Sebagian besar informasi di bawah ini disalin dari proyek MorphInd oleh [Tina](http://septinalarasati.com/work/morphind/).

## Morphological Tagset

|   UD     |  ITB   | First position                  | Second position          | Third position              |
| -------- | ------ | ------------------------------- | ------------------------ | --------------------------- |
| `PROPN`  | `E--`  | `E` (Proper Noun)               |                          |                             |
| `NOUN`   | `NPF`  | `N` (Noun)                      | `P` (Plural)             | `F` (Feminine)              |
| `NOUN`   | `NPM`  | `N` (Noun)                      | `P` (Plural)             | `M` (Masculine)             |
| `NOUN`   | `NPD`  | `N` (Noun)                      | `P` (Plural)             | `D` (Non-Specified)         |
| `NOUN`   | `NSF`  | `N` (Noun)                      | `S` (Singular)           | `F` (Feminine)              |
| `NOUN`   | `NSM`  | `N` (Noun)                      | `S` (Singular)           | `M` (Masculine)             |
| `NOUN`   | `NSD`  | `N` (Noun)                      | `S` (Singular)           | `D` (Non-Specified)         |
| `PRON`   | `PP1`  | `P` (Personal Pronoun)          | `P` (Plural)             | `1` (First Person)          |
| `PRON`   | `PP2`  | `P` (Personal Pronoun)          | `P` (Plural)             | `2` (Second Person)         |
| `PRON`   | `PP3`  | `P` (Personal Pronoun)          | `P` (Plural)             | `3` (Third Person)          |
| `PRON`   | `PS1`  | `P` (Personal Pronoun)          | `S` (Singular)           | `1` (First Person)          |
| `PRON`   | `PS2`  | `P` (Personal Pronoun)          | `S` (Singular)           | `2` (Second Person)         |
| `PRON`   | `PS3`  | `P` (Personal Pronoun)          | `S` (Singular)           | `3` (Third Person)          |
| `VERB`   | `VPA`  | `V` (Verb)                      | `P` (Plural)             | `A` (Active Voice)          |
| `VERB`   | `VPP`  | `V` (Verb)                      | `P` (Plural)             | `P` (Passive Voice)         |
| `VERB`   | `VSA`  | `V` (Verb)                      | `S` (Singular)           | `A` (Active Voice)          |
| `VERB`   | `VSP`  | `V` (Verb)                      | `S` (Singular)           | `P` (Passive Voice)         |
| `NUM`    | `CC-`  | `C` (Numeral)                   | `C` (Cardinal Numeral)   |                             |
| `NUM`    | `CO-`  | `C` (Numeral)                   | `O` (Ordinal Numeral)    |                             |
| `NUM`    | `CD-`  | `C` (Numeral)                   | `D` (Collective Numeral) |                             |
| `ADJ`    | `APP`  | `A` (Adjective)                 | `P` (Plural)             | `P` (Positive)              |
| `ADJ`    | `APS`  | `A` (Adjective)                 | `P` (Plural)             | `S` (Superlative)           |
| `ADJ`    | `ASP`  | `A` (Adjective)                 | `S` (Singular)           | `P` (Positive)              |
| `ADJ`    | `ASS`  | `A` (Adjective)                 | `S` (Singular)           | `S` (Superlative)           |
| `CONJ`   | `H--`  | `H` (Coordinating Conjunction)  |                          |                             |
| `SCONJ`  | `S--`  | `S` (Subordinating Conjunction) |                          |                             |
| `X`      | `F--`  | `F` (Foreign Word)              |                          |                             |
| `ADP`    | `R--`  | `R` (Preposition)               |                          |                             |
| `AUX`    | `M--`  | `M` (Modal)                     |                          |                             |
| `DET`    | `B--`  | `B` (Determiner)                |                          |                             |
| `ADV`    | `D--`  | `D` (Adverb)                    |                          |                             |
| `PART`   | `T--`  | `T` (Particle)                  |                          |                             |
| `PART`   | `G--`  | `G` (Negation)                  |                          |                             |
| `INTJ`   | `I--`  | `I` (Interjection)              |                          |                             |
| `VERB`   | `O--`  | `O` (Copula)                    |                          |                             |
| `PRON`   | `WP-`  | `W` (Question)                  | `P` (Pronoun)            |                             |
| `ADV`    | `WD-`  | `W` (Question)                  | `D` (Adverb)             |                             |
| `DET`    | `WB-`  | `W` (Question)                  | `B` (Determiner)         |                             |
| `X`      | `X--`  | `X` (Unknown)                   |                          |                             |
| `PUNCT`  | `Z--`  | `Z` (Punctuation)               |                          |                             |

*) ~~untuk `W--` sebagai _interrogative pronouns_ (_who_; _siapa_, _siapakah_) menjadi `PRON`, `W--` sebagai _interrogative adverbs_ (_where_, _when_, _how_, _why_; _di mana_, _kapan_, _bilamana_, _bagaimana_, _mengapa_)  menjadi `ADV`, `W--` sebagai _interrogative determiners_ (_which_; _yang mana_) menjadi `DET`~~

**) ~~kelas `PROPN` masih belum ditentukan. oleh MorphInd, kelas yang digunakan adalah `X--` dan `F--`~~

## Lemma Tagset

|  .  | Tagset                     |
| --- | -------------------------- |
| `n` | Noun                       |
| `p` | Personal Pronoun           |
| `v` | Verb                       |
| `c` | Numeral                    |
| `q` | Adjective                  |
| `h` | Coordinating Conjunction   |
| `s` | Subordinating Conjunction  |
| `f` | Foreign Word               |
| `r` | Preposition                |
| `m` | Modal                      |
| `b` | Determiner                 |
| `d` | Adverb                     |
| `t` | Particle                   |
| `g` | Negation                   |
| `i` | Interjection               |
| `o` | Copula                     |
| `w` | Question                   |
| `x` | Unknown                    |
| `z` | Punctuation                |

